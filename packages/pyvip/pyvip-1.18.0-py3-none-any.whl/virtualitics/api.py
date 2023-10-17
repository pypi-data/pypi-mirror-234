import time
import json
import pandas as pd
import numpy as np
import os
import math
import asyncio
import websocket
import concurrent.futures
import queue
import networkx as nx
from websocket import WebSocketConnectionClosedException
from uuid import getnode as get_mac
from virtualitics import exceptions, utils, vip_plot, vip_dashboard, vip_annotation
from virtualitics import task_response_handlers as handlers
from virtualitics import encryption as enc
import virtualitics

LOG_HELP_LEVEL = 1
LOG_DEBUG_LEVEL = 2
REQUEST_RETRY_LIMIT = 10


# noinspection PyDictCreation
class VIP:
    """
    Virtualitics API handler for Python.

    The class will cache information about the Virtualitics Explore session and establish the Virtualitics Explore connection

    :param auth_token: User to pass Authentication Token; default: `None` will check environment variables for
        token under "VIP_AUTH_TOKEN"
    :param api_session_id: Used to connect to a specific instance of Explore Web, and obtained from the Settings Panel within the user's Explore Web instance. Do not use when connecting to Explore Desktop.
    :param port: The port Virtualitics Explore is serving. default: 12345. Integer in [0, 65535]
    :param encryption_key: Optional encryption key; default: None
    :param host: default is localhost connection. Only change this if you intend on connecting to a remote Virtualitics Explore
        instance. This is an advanced functionality.
    :param log_level: :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from Virtualitics Explore. The
        resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
        [8, 8].
    :raises AuthenticationException: if the auth token is not provided and cannot be found in the expected
        locations.
    """

    def __init__(
        self,
        auth_token=None,
        api_session_id=None,
        port=12345,
        encryption_key=None,
        host="ws://localhost",
        log_level=0,
        figsize=(8, 8),
        vpf_request_queue=None,
        vpf_response_queue=None,
    ):
        # Validate argument types of port and log_level
        if not isinstance(port, int) or port < 0 or port > 65535:
            utils.raise_invalid_argument_exception(str(type(port)), "port", "int in [0, 65535]")
        if not isinstance(log_level, int):
            utils.raise_invalid_argument_exception(
                str(type(log_level)), "log_level", [LOG_HELP_LEVEL, LOG_DEBUG_LEVEL, "other integer"]
            )

        if auth_token is None:
            if "VIP_AUTH_TOKEN" in os.environ:
                self.auth_token = os.environ["VIP_AUTH_TOKEN"]
            else:
                raise (
                    exceptions.AuthenticationException(
                        "You must provide an Authentication Token as a parameter or "
                        + "save it as an environment variable. See documentation."
                    )
                )
        else:
            if not isinstance(auth_token, str):
                raise exceptions.InvalidInputTypeException("auth_token parameter is either None or a string.")

            self.auth_token = auth_token
        if encryption_key is None:
            if "VIP_ENCRYPTION_KEY" in os.environ:
                self.cipher = enc.VIPCipher(os.environ["VIP_ENCRYPTION_KEY"])
            else:
                self.cipher = None
            # it is not required for the user to encrypt their data.
        else:
            if not isinstance(encryption_key, str):
                raise exceptions.InvalidInputTypeException("encryption_key parameter is either None or a string.")
            self.cipher = enc.VIPCipher(encryption_key)

        # WebSocket Connection variables
        self.host = host
        self.port = port
        self.url = self.host + ":" + str(self.port)
        self.max_request_bytes = 1160000000000  # TODO: Adjust for 1.5.0
        self.is_vpf_connection = (vpf_request_queue != None) and (vpf_response_queue != None)

        if self.is_vpf_connection:
            print("Using Virtualitics Fusion/Predict Request & Response Buffers.", flush=True)
            self.req_buffer = vpf_request_queue
            self.res_buffer = vpf_response_queue
        else:
            self.ws = websocket.WebSocket()

        self.api_session_id = api_session_id
        self.connection_url = self.url + "/api"
        self.connection_url += "?auth_token=" + self.auth_token
        if self.api_session_id is not None:
            self.connection_url += "&api_session_id=" + self.api_session_id
        self.debug = None
        self.log_level = log_level
        self.dataset_num = 1
        self._local_history = []
        self.figsize = figsize

        # Copied Network functionality
        self.delete_network = self.delete_dataset
        self.switch_network = self.switch_dataset

        if self.is_vpf_connection != True:
            print("Setting up WebSocket connection to: " + self.connection_url)
            try:
                self.ws.connect(self.connection_url)
                print("Connection Successful! Initializing session.")
            except Exception as e:
                print("Connection Failed: " + e.__str__())

        self._api_request()

    def _reconnect(self):
        self.ws.connect(self.connection_url)

    def _send_request(self, payload, pagenum=None):
        """
        All API commands will make use of this function to do the final preparations and sending of the request.
        All requests are made as ASYNC POST requests

        :param payload: JSON structure that will be prepped for sending.
        """
        attempts_remaining = REQUEST_RETRY_LIMIT
        while attempts_remaining > 0:
            try:
                if self.cipher is not None:
                    payload = self.cipher.encrypt(payload)
                try:
                    if self.is_vpf_connection != True:
                        self.ws.send_binary(payload)
                        raw_response = self.ws.recv()
                    else:
                        self.req_buffer.put(payload)
                        while self.res_buffer.qsize() < 1:
                            time.sleep(0.01)

                        raw_response = self.res_buffer.get()

                    if self.cipher is not None:
                        raw_response = self.cipher.decrypt(raw_response)
                except ConnectionAbortedError:
                    if self.is_vpf_connection != True:
                        self._reconnect()
                        self.ws.send_binary(payload)
                        raw_response = self.ws.recv()
                    else:
                        self.req_buffer.put(payload)
                        while self.res_buffer.qsize() < 1:
                            time.sleep(0.01)

                        raw_response = self.res_buffer.get()

                    if self.cipher is not None:
                        raw_response = self.cipher.decrypt(raw_response)
                except WebSocketConnectionClosedException as e:
                    print(
                        "There was an issue establishing the WebSocket connection. Here are some things to check: Virtualitics Explore "
                        "must be opened and logged in. If you are trying to connect to Explore Desktop, you must explicitly launch the API WebSocket server from the "
                        "settings panel unless you have previously selected 'Launch at Login'. Make sure you have "
                        "specified the correct host address and port number for Virtualitics Explore. If you are still having issues "
                        "connecting to Virtualitics Explore, please discuss with your IT team and email 'support@virtualitics.com'. "
                    )
                    if self.log_level >= LOG_DEBUG_LEVEL:
                        print("Connection Failed: " + e.__str__())
                    return
                except Exception as e:
                    print("There was an exception processing the api request or response.")
                    if self.log_level >= LOG_DEBUG_LEVEL:
                        print("Exception: " + e.__str__())
                    return

                # Partition raw response
                if isinstance(raw_response, str):
                    raise exceptions.ResponseFormatException(
                        "There was an issue in parsing the response from the software. "
                        "Please try executing the API call again."
                    )
                self.debug = raw_response
                response_size = int(int.from_bytes(raw_response[:4], byteorder="little", signed=True))
                response = utils.decompress(raw_response[4 : 4 + response_size])
                response_payload = raw_response[4 + response_size :]
                cur_result, task_response = handlers.generic_callback(
                    response, response_payload, self.log_level, self.figsize
                )
                if cur_result is None:
                    return
                # check this first if we need to append to history.
                if (
                    cur_result.plot is not None
                    and "SaveToLocalHistory" in task_response
                    and task_response["SaveToLocalHistory"]
                ):
                    self._local_history.append(cur_result.plot)
                # then check if we want to return data - this takes priority.
                if cur_result.data is not None:
                    return cur_result.data
                # if no data is returned, but we had a plot, return it.
                if (
                    cur_result.plot is not None
                    and "ReturnPlotMapping" in task_response
                    and task_response["ReturnPlotMapping"]
                ):
                    return cur_result.plot
                else:
                    return
            except exceptions.VipTaskUnknownExecutionException:
                if self.log_level == 2:
                    print("Request attempts remaining: {}".format(attempts_remaining))
                attempts_remaining -= 1
                time.sleep(1.5)
            except exceptions.ResponseFormatException:
                if self.log_level == 2:
                    print("Request attempts remaining: {}".format(attempts_remaining))
                attempts_remaining -= 1
                time.sleep(1.5)
            except Exception as e:
                raise e
        raise exceptions.VipTaskRetryLimitExceededException(
            "Failed to execute task and receive response from "
            "Virtualitics Explore API server successfully after several attempts. "
            "Please review documentation and contact "
            "support@virtualitics.com. "
        )

    def _api_request(self, params=None, data=None):
        """
        API Request formatter; hands off to _send_request
        :param params: defaults to None. parameters encoding Virtualitics Explore tasks
        :param data: defaults to None. data to be sent over to complete Virtualitics Explore tasks
        :return: may return a :class:`virtualitics.VipResult` or None
        """
        # TODO: Rewrite this method

        api_request = {}
        total_payload_size = 0
        api_request["AuthToken"] = self.auth_token
        api_request["ApiVersion"] = virtualitics.__version__
        api_request["ExpectedVIPVersion"] = virtualitics.__latest_compatible_vip_version__
        mac_address = ":".join(("%012X" % get_mac())[i: i + 2] for i in range(0, 12, 2))
        api_request["MacAddress"] = mac_address
        if params is not None:
            api_request["RequestTasks"] = params
        else:
            api_request["RequestTasks"] = []

        # Encode and compress api_request
        request = json.dumps(api_request)
        request_bytes = utils.compress(request.encode("unicode_escape"))

        if self.log_level >= LOG_DEBUG_LEVEL:
            print(request)

        # The max payload size has to account for the request and the
        # pre-request info. The use of magic number (12)
        max_page_size = self.max_request_bytes - len(request_bytes) - 12
        total_pages = 1
        if total_payload_size > max_page_size:
            # minimum 1 page
            total_pages = math.ceil(total_payload_size / float(max_page_size))

        for i in range(total_pages):
            request_info = np.array([len(request_bytes), i, total_pages - 1])
            info_bytes = request_info.astype(np.int32).tobytes()
            cur_payload = info_bytes + request_bytes
            # get the bytearray that we will send in this request based on page num
            if data is None:
                data = bytearray()
            if total_pages == 1:
                cur_payload += data
            else:
                start_idx = i * max_page_size
                end_idx = start_idx + max_page_size
                if end_idx >= len(data):
                    cur_payload += data[start_idx:]
                else:
                    cur_payload += data[start_idx:end_idx]
            return self._send_request(cur_payload, i)

    @property
    def local_history(self):
        """
        This is a list of :class:`VipPlot` instances that were generated by plotting request methods (e.g.
        :func:`VIP.show()`, :func:`VIP.hist()`, etc.) or AI routine methods (e.g. :func:`VIP.smart_mapping()`,
        :func:`VIP.pca()`, etc.). To control whether a :class:`VipPlot` object will be added to 'local_history',
        specify the 'save_to_local_history' parameter in your plotting/AI routine requests. The 'local_history'
        list is different from the :func:`VIP.history()` method, which allows the user to access :class:`VipPlot`
        objects saved to the Virtualitics Explore History panel.

        :return: :class:`[VipPlot]`
        """
        return self._local_history

    @property
    def log_level(self):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.

        :return: :class:`int`
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.

        :return: :class:`int`
        """
        if not isinstance(value, int):
            utils.raise_invalid_argument_exception(
                str(type(value)), "log_level", "must be an `int` between 0 and 2. See Documentation. "
            )

        if not (0 <= value <= 2):
            utils.raise_invalid_argument_exception(
                str(type(value)), "log_level", "must be an `int` between 0 and 2. See Documentation. "
            )

        self._log_level = value

    @property
    def figsize(self):
        """
        This is used as the setting for the matplotlib figure size when displaying the image of plots generated by
        Virtualitics Explore. The default value is (8, 8)

        :return: :class:`(int, int)`
        """
        return self._figsize

    @figsize.setter
    def figsize(self, value):
        """
        This is used as the setting for the matplotlib figure size when displaying the image of plots generated by
        Virtualitics Explore. The default value is (8, 8). Must be set to a :class:`(int, int)`.

        :param value: :class:`(int, int)`
        :return: :class:`None`
        """
        if not hasattr(value, "__iter__"):
            utils.raise_invalid_argument_exception(
                str(type(value)),
                "figsize",
                "must be a `(int, int)` with length " "of 2. The integers must be positive. ",
            )
        if not len(value) == 2:
            utils.raise_invalid_argument_exception(
                str(type(value)),
                "figsize",
                "must be a `(int, int)` with length " "of 2. The integers must be positive. ",
            )
        if not isinstance(value[0], int) or value[0] < 1:
            utils.raise_invalid_argument_exception(
                str(type(value)),
                "figsize",
                "must be a `(int, int)` with length " "of 2. The integers must be positive. ",
            )
        if not isinstance(value[1], int) or value[1] < 1:
            utils.raise_invalid_argument_exception(
                str(type(value)),
                "figsize",
                "must be a `(int, int)` with length " "of 2. The integers must be positive. ",
            )

        self._figsize = value

    def load_project(self, path, send_project_xml=False):
        """
        Loads Virtualitics Explore project file (.vip) into software from a path local to the machine running Virtualitics Explore. Note that any project
        currently open will be discarded. To save the project first, please use VIP.save_project().

        :param path: :class:`str`
        :param send_project_xml: :class:`bool`
        :return: :class:`None`
        """

        if not isinstance(path, str):
            utils.raise_invalid_argument_exception(str(type(path)), "path", "must be a string. ")

        # Following behavior in save_project(), append vip extension if it does not exist
        if path[-4:] != ".vip":
            path += ".vip"

        xmlData = None
        xmlCompressedData = None

        params = {"TaskType": "LoadProject", "Path": path}

        if send_project_xml is True:
            with open(path, "r", encoding="utf-8") as file:
                xmlData = file.read()

            xmlCompressedData = utils.compress(xmlData.replace("\ufeff", "").replace("\u200B", "").encode("utf-8"))

        self._api_request(params=[params], data=xmlCompressedData)

    def load_workflow(self, path=None, workflow_json=None, workflow_name=None):
        """
        Loads Virtualitics Explore workflow file into software from a path local to the machine running Virtualitics Explore. Note that any workflow
        currently open will be discarded. To save the workflow first, please use VIP.save_workflow().

        :param path: :class:`str` desired path of the workflow file (must be local to machine running Virtualitics Explore instance).
        :param workflow_json: object that contains the workflow data.
        :param workflow_name: optionally pass in a name for this workflow to show in Virtualitics Explore.
        :return: :class:`None`
        """

        useOnlyPath = False

        if path is not None and workflow_json is not None:
            useOnlyPath = True
            print("path or wofkflow_json should be used, not both. Using path...")

        if path is not None:
            useOnlyPath = True
            if not isinstance(path, str):
                utils.raise_invalid_argument_exception(str(type(path)), "path", "must be a string. ")

            # Following behavior in save_project(), append vip extension if it does not exist
            if path[-5:] != ".json":
                path += ".json"

        if workflow_name is not None:
            if not isinstance(workflow_name, str):
                utils.raise_invalid_argument_exception(str(type(workflow_name)), "workflow_name", "must be a string. ")

        if useOnlyPath:
            params = {
                "TaskType": "LoadWorkflow",
                "Path": path,
                "WorkflowName": workflow_name,
            }  # Don't pass over the JSON data (Optimization)
        else:
            params = {
                "TaskType": "LoadWorkflow",
                "Path": path,
                "WorkflowJSON": workflow_json,
                "WorkflowName": workflow_name,
            }

        self._api_request(params=[params], data=None)

    def get_workflow(self):
        """
        Returns the workflow for the active dataset in Virtualitics Explore.

        :return: :class:`JSON`
        """
        params = {"TaskType": "GetWorkflow"}
        return self._api_request(params=[params], data=None)

    def load_data(self, data, dataset_name=None):
        """
        Loads :class:`pandas.DataFrame` into Virtualitics Explore. Uses column dtype to determine column type in Virtualitics Explore.

        :param data: :class:`pandas.DataFrame` object that contains the users data.
        :param dataset_name: optionally pass in a name for this dataset to show in Virtualitics Explore
        :return: :class:`None`
        """
        if dataset_name is not None and not isinstance(dataset_name, str):
            raise exceptions.InvalidInputTypeException("dataset_name should be a string!")
        if not isinstance(data, pd.DataFrame):
            raise exceptions.InvalidInputTypeException("data should be a pd.DataFrame!")

        if len(set(data.columns)) != len(data.columns):
            raise exceptions.InvalidInputTypeException("Column names in the dataframe must be unique")

        params = {"TaskType": "DataSet"}
        params["ColumnInfo"] = []
        column_bytes = []
        payload_idx = 0

        # Serialize columns
        for col in list(data.columns):
            serial_col = utils.serialize_column(data[col].values)
            col_info = {
                "ColumnName": str(col).strip(),
                "ColumnType": serial_col[0],
                "BytesSize": serial_col[2],
                "BytesStartIndex": payload_idx,
            }
            params["ColumnInfo"].append(col_info)
            column_bytes.append(serial_col[1])
            payload_idx += serial_col[2]

        if dataset_name is None or dataset_name == "":
            dataset_name = "user_dataset_{i}".format(i=self.dataset_num)
        params["DataSetName"] = dataset_name
        data_bytes = b"".join(column_bytes)

        output = self._api_request(params=[params], data=data_bytes)

        # Now that data has been successfully loaded into Virtualitics Explore
        # Keep track of current columns and their data types
        self.dataset_num += 1
        return output

    def delete_dataset(self, name=None):
        """
        Deletes a dataset or network from Virtualitics Explore. This is particularly useful when you have a lot of data loaded into Virtualitics Explore
        and there is a performance slow down. If 'dataset_name' is passed, Virtualitics Explore will delete the dataset or network with
        the corresponding name. If 'dataset_name' is left as `None`, the currently loaded dataset or network will be
        deleted from Virtualitics Explore if there is a dataset loaded.

        :param name: :class:`str` specifying the name of the dataset or network to delete from Virtualitics Explore. Defaults to
            :class:`None`
        :return: :class:`None`
        """
        params = {"TaskType": "DeleteDataSet"}
        if name is None:
            params["CurrentDataSet"] = True
        else:
            if not isinstance(name, str):
                utils.raise_invalid_argument_exception(
                    str(type(name)),
                    "name",
                    "must be a 'str' specifying name of a dataset loaded into Virtualitics Explore",
                )
            params["CurrentDataSet"] = False
            params["DataSetName"] = name

        self._api_request(params=[params], data=None)

    def switch_dataset(self, name: str):
        """
        Switches Dataset context in Virtualitics Explore.

        :param name: :class:`str` for the name of the dataset or network to bring into context.
        :return: :class:`None`
        """
        params = {"TaskType": "SwitchDataset"}
        params["DataSetName"] = name

        self._api_request(params=[params], data=None)

    def load_object(
        self,
        path=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        imgPath=None,
        position=None,
        orientation=None,
    ):
        """
        Load an OBJ file into Virtualitics Explore.

        :param path: :class:`str` Desired path of the OBJ file (must be local to machine running Virtualitics Explore instance).
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        """
        params = {"TaskType": "LoadOBJ"}

        if not isinstance(path, str) or path is None:
            utils.raise_invalid_argument_exception(type(path), "path", "Should be a `str`.")

        params["OBJPath"] = path
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            imgPath,
            [params],
            ignore_no_plot=True,
            position=position,
            orientation=orientation,
        )

        output = self._api_request(params=params, data=None)
        return output

    def toggle_object_mode(self):
        """
        Toggles the current mode (object or plot) if possible.
        """
        params = {"TaskType": "ToggleOBJMode"}
        self._api_request(params=[params], data=None)

    def toggle_obj_mode(self):
        """
        Shortcut method for `toggle_object_mode`.
        """
        self.toggle_object_mode()

    def set_object_mode(self, mode: str):
        """
        Sets the current mode (object or plot) if possible.

        :param mode: :class:`str` Desired mode, `object` or `plot`.
        """
        params = {"TaskType": "ToggleOBJMode"}

        if not isinstance(mode, str) or mode is None:
            utils.raise_invalid_argument_exception(
                str(type(mode)), "mode", "`mode` must be specified as either `object` or `plot`."
            )

        mode = mode.lower()
        if mode != "object" and mode != "plot":
            utils.raise_invalid_argument_exception(
                str(type(mode)), "mode", "`mode` must be specified as either `object` or `plot`."
            )

        params["Mode"] = mode

        self._api_request(params=[params], data=None)

    def set_obj_mode(self, mode: str):
        """
        Shortcut method for `set_object_mode`.
        """
        self.set_object_mode(mode)

    def switch_object(self, id: str):
        """
        Switches the current Object context in Virtualitics Explore.

        :param id: :class:`str` id of the object (as provided by Virtualitics Explore).
        :return: :class:`None`
        """

        params = {"TaskType": "SwitchOBJ"}

        if not isinstance(id, str):
            utils.raise_invalid_argument_exception(str(type(id)), "id", "must be a `str`.")

        params["ObjectID"] = id

        self._api_request(params=[params], data=None)

    def switch_obj(self, id: str):
        """
        Shortcut for switch_object method.
        """

        self.switch_object(id=id)

    def delete_object(self, id=None):
        """
        Delete an object in Virtualitics Explore, given an id. If no id is passed, Virtualitics Explore will delete the current object.
        """
        params = {"TaskType": "DeleteOBJ"}
        if id is None:
            params["DeleteCurrentObject"] = True
        else:
            if not isinstance(id, str):
                utils.rais_invalid_argument_exception(
                    str(type(id)),
                    "id",
                    "must be a `str` specifying the id of an object loaded into Virtualitics Explore.",
                )
            params["DeleteCurrentObject"] = False
            params["ObjectID"] = id

        self._api_request(params=[params], data=None)

    def delete_obj(self, id=None):
        """
        Shortcut for `delete_object` method.
        """
        self.delete_object(id=id)

    def delete_all_objects(self):
        """
        Deletes all objects loaded into Virtualitics Explore.
        """
        params = {"TaskType": "DeleteOBJ"}
        params["DeleteAll"] = True

        self._api_request(params=[params], data=None)

    def delete_all_objs(self):
        """
        Shortcut for `delete_all_objects` method.
        """

        self.delete_all_objects()

    def save_project(self, filename: str, overwrite=False):
        """
        Saves Virtualitics Explore project to the specified filepath.

        :param filename: absolute path to the desired save location.
        :param overwrite: :class:`bool` that controls whether to write over a file that may exist at the specified path.
        :return: :class:`None`
        """
        try:
            path = filename
            if path[-4:] != ".vip":
                path += ".vip"
            params = {"TaskType": "SaveProject"}
            params["Path"] = path
        except Exception:
            raise exceptions.InvalidSavePathException("This is not a valid path.")

        if not isinstance(overwrite, bool):
            utils.raise_invalid_argument_exception(str(type(overwrite)), "overwrite", "must be a `bool`.")

        params["Overwrite"] = overwrite

        self._api_request(params=[params], data=None)

    def save_workflow(self, filename: str, overwrite=False):
        """
        Saves Virtualitics Explore workflow to the specified filepath.

        :param filename: absolute path to the desired save location.
        :param overwrite: :class:`bool` that controls whether to write over a file that may exist at the specified path.
        :return: :class:`None`
        """
        try:
            path = filename
            if path[-5:] != ".json":
                path += ".json"
            params = {"TaskType": "SaveWorkflow"}
            params["Path"] = path
        except Exception:
            raise exceptions.InvalidSavePathException("This is not a valid path.")

        if not isinstance(overwrite, bool):
            utils.raise_invalid_argument_exception(str(type(overwrite)), "overwrite", "must be a `bool`.")

        params["Overwrite"] = overwrite

        self._api_request(params=[params], data=None)

    def convert_column(self, column, column_type: str):
        """
        Converts column to the specified type.

        :param column: expects column name (:class:`str`) or a :class:`pandas.Series`
        :param column_type: {"Continuous", "Categorical"}
        :return: :class:`None`
        """
        col_name = utils.get_name(column)
        column_type = utils.case_insensitive_match(utils.COLUMN_TYPE_CHOICES, column_type, "column_type")

        params = {"TaskType": "ConvertColumn"}
        params["ColumnName"] = col_name
        params["ColumnType"] = column_type

        self._api_request(params=[params], data=None)

    def add_column(self, data, name=None):
        """
        Add a pandas series to the currently loaded dataset in Virtualitics Explore. Uses column dtype to determine column type in Virtualitics Explore.

        :param data: :class:`pandas.core.Series` object that contains a column of the user's data.
        :param name: if not :class:`None`, sets this as the name of the series when it is added.
        :return: :class:`None`
        """
        if not isinstance(data, pd.Series):
            raise exceptions.InvalidInputTypeException("data should be a pd.Series!")

        if name is not None:
            data.rename(name, inplace=True)

        self._add_data([data], "Column", replot=False)

    def add_rows(
        self,
        data,
        replot=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        show_legend=True,
    ):
        """
        Append a pandas data frame of rows to the currently loaded dataset in Virtualitics Explore.

        :param data: :class:`pandas.core.frame.DataFrame` object that contains rows of the user's data.
        :param replot: :class:`bool` Whether to replot the current mapping after the rows have been added.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        if not isinstance(data, pd.DataFrame):
            raise exceptions.InvalidInputTypeException("data should be a pd.DataFrame")

        if len(set(data.columns)) != len(data.columns):
            raise exceptions.InvalidInputTypeException("Column names in the dataframe must be unique")

        self._add_data(
            [data[c] for c in data.columns],
            "AddRows",
            replot=replot,
            export=export,
            background=background,
            imsize=imsize,
            autocrop=autocrop,
            path=path,
            save_to_local_history=save_to_local_history,
            show_legend=show_legend,
        )

    def _add_data(
        self,
        data,
        task_type,
        replot=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Add a pandas data frame to the currently loaded dataset in Virtualitics Explore. If the number of columns is one, adds the
        data as a new column. Else, appends the data as new rows.

        :param data: :class:`pandas.core.frame.DataFrame` or `pandas.core.Series` object that contains the user's data.
        :param task_type: the type of add_data operation in ['AddRows', `Column`]
        :param replot: Whether to replot the current mapping after the data has been added.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": task_type}
        params["ColumnInfo"] = []
        data_bytes = []
        payload_idx = 0

        for col in data:
            serial_col = utils.serialize_column(col.values)
            col_info = {
                "ColumnName": str(col.name).strip(),
                "ColumnType": serial_col[0],
                "BytesSize": serial_col[2],
                "BytesStartIndex": payload_idx,
            }
            params["ColumnInfo"].append(col_info)
            data_bytes.append(serial_col[1])
            payload_idx += serial_col[2]

        data_bytes = b"".join(data_bytes)

        params = [params]
        if replot is True:
            refresh_params = {"TaskType": "RefreshPlot"}
            params.append(refresh_params)
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )
            params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=data_bytes)

    def load_network(
        self,
        network,
        network_name=None,
        edge_weight_format="similarity",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Loads a network dataset into Virtualitics Explore. Datasets can be loaded as :class:`networkx.Graph` objects, Virtualitics Explore's JSON format
        as a string to a file or Python dictionary, or :class:`pandas.DataFrame` (for edgelists) objects. The
        Virtualitics Explore API does not support Adjacency Matrix format. Virtualitics Explore automatically computes structure (community
        detection and Force Directed Layout - ForceAtlas3D) upon load of the network dataset.

        :param network: Can be a :class:`networkx.Graph` object, :class:`pandas.DataFrame` containing an edgelist,
            :class:`str` of path to JSON file, or :class:`dict` representing the JSON as a dictionary.
        :param network_name: :class:`str` containing the desired name of the network dataset.
        :param edge_weight_format: :class:`str` containing edge weight format for this data (given that the data is
            weighted). "Similarity" should be used when larger edge weights indicate a closer/tighter relationship
            between the adjacent nodes. "Distance" should be used when larger edge weight represent a looser/weaker
            relationship between the adjacent nodes.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        # TODO: add an impute method

        if network_name is not None and not isinstance(network_name, str):
            raise exceptions.InvalidInputTypeException("network_name should be a string!")
        if network_name is None or network_name == "":
            network_name = "user_dataset_{i}".format(i=self.dataset_num)
        edge_weight_format = utils.case_insensitive_match(
            utils.EDGE_WEIGHT_FORMAT, edge_weight_format, "edge_weight_format"
        )

        if (
            edge_transparency is not None
            and (isinstance(edge_transparency, float) or isinstance(edge_transparency, int)) == False
        ):
            raise exceptions.InvalidInputTypeException("edge_transparency should be a float.")

        if isinstance(network, (dict, str)):
            # This allows us to validate the format of the json
            network = self.convert_json_to_networkx(network)

        if isinstance(network, nx.Graph):
            return self._load_network_from_networkx(
                network,
                network_name=network_name,
                edge_weight_format=edge_weight_format,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                edge_transparency=edge_transparency,
                show_legend=show_legend,
            )

        if isinstance(network, pd.DataFrame):
            return self._load_network_from_edgelist(
                network,
                network_name=network_name,
                edge_weight_format=edge_weight_format,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                position=None,
                orientation=None,
                edge_transparency=edge_transparency,
                show_legend=show_legend,
            )

        raise exceptions.InvalidInputTypeException(
            "Network input must be an instance of a NetworkX.Graph format, "
            "Python dictionary, string, or an edgelist (as a pandas DataFrame). "
            "See documentation. "
        )

    @staticmethod
    def convert_json_to_networkx(network):
        """
        Converts a network represented in Virtualitics Explore's JSON format into a NetworkX object.

        :param network: :class:`str` of path to JSON file or :class:`dict` representing the JSON as a dictionary.
        :return: :class:`networkx.Graph` object.
        """

        if isinstance(network, str):
            with open(network, "r") as f:
                network = json.load(f)
        elif not isinstance(network, dict):
            raise exceptions.InvalidInputTypeException(
                "Network input must be either a path to a JSON file or a " "Python dictionary"
            )
        try:
            graph = nx.empty_graph()
            net_keys = {str(k).lower(): k for k in network.keys()}
            nodes_key = net_keys["nodes"]
            edges_key = net_keys["edges"]

            # fallback to 'name' if 'node id' can't be found.
            try:
                node_name_key = [k for k in network[nodes_key][0].keys() if str(k).lower() == "node id"][0]
            except:
                node_name_key = [k for k in network[nodes_key][0].keys() if str(k).lower() == "name"][0]

            for node in network[nodes_key]:
                node_copy = node.copy()
                name = node_copy[node_name_key]
                del node_copy[node_name_key]
                graph.add_node(name, **node_copy)
            edge_keys = {str(k).lower(): k for k in network[edges_key][0].keys()}
            edge_src_key = edge_keys["source"]
            edge_tgt_key = edge_keys["target"]
            edge_weight_key = edge_keys.get("weight")
            for edge in network[edges_key]:
                if edge_weight_key in edge:
                    weight = edge[edge_weight_key]
                    if graph.has_edge(edge[edge_tgt_key], edge[edge_src_key]):
                        weight += graph.get_edge_data(edge[edge_tgt_key], edge[edge_src_key])[edge_weight_key]
                    graph.add_edge(edge[edge_src_key], edge[edge_tgt_key], weight=weight)
                else:
                    graph.add_edge(edge[edge_src_key], edge[edge_tgt_key])
        except Exception:
            raise exceptions.InvalidInputTypeException(
                "Network input does not match Virtualitics Explore's JSON format. Please see " "documentation. "
            )

        return graph

    @staticmethod
    def convert_networkx_to_json(network, path=None):
        """
        Converts a network represented as a NetworkX object into Virtualitics Explore's JSON format.

        :param network: :class:`networkx.Graph` an undirected NetworkX graph
        :param path: :class:`str` of path to write JSON to or :class:`None` to omit writing to file. Defaults is None.
        :return: :class:`dict` representing the JSON as a dictionary.
        """
        # TODO: add an impute method. default this to param to False. only _load_network_from_networkx sets it to True

        if type(network) is nx.Graph:
            nodes = []
            # iterate through node data (including attributes) and save to node list
            for n, n_data in network.nodes(data=True):
                node = {"Node ID": str(n)}
                for k, v in n_data.items():
                    if k != "Node ID":
                        if isinstance(v, (bool, float, int, str)) or None:
                            node[str(k)] = v

                nodes.append(node)
            if len(nodes) == 0:
                raise exceptions.InvalidInputTypeException("Network input must have at least one valid node.")

            edges = []
            # iterate through edge data and save to edgelist
            for es, et, e_data in network.edges(data=True):
                es, et = str(es), str(et)
                e_weight = e_data.get("weight")
                if e_weight is not None:
                    if (type(e_weight) is int or type(e_weight) is float) and e_weight > 0:
                        edges.append({"Source": es, "Target": et, "Weight": e_weight})
                    else:
                        raise exceptions.InvalidInputTypeException(
                            "Network input must have edge weights that are "
                            "strictly positive numbers (float or int > 0), "
                            "None, or empty"
                        )
                else:
                    edges.append({"Source": es, "Target": et})
            if len(edges) == 0:
                raise exceptions.InvalidInputTypeException("Network input must have at least one valid edge.")

            json_dict = {"Nodes": nodes, "Edges": edges}

            if path is not None:
                if isinstance(path, str):
                    try:
                        with open(path, "w") as f:
                            json.dump(json_dict, f)
                    except Exception as e:
                        raise exceptions.InvalidInputTypeException("Could not write to Path: " + str(e))
                else:
                    raise exceptions.InvalidInputTypeException("Path input, if not None, must be a string.")

        else:
            raise exceptions.InvalidInputTypeException(
                "Network input must be an instance of a "
                "NetworkX.Graph (simple, undirected NetworkX "
                "graph) format. See documentation. "
            )

        return json_dict

    def _load_network_from_networkx(
        self,
        network,
        network_name=None,
        edge_weight_format="Similarity",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        json_dict = self.convert_networkx_to_json(network, path=None)
        data_bytes = utils.compress(json.dumps(json_dict).encode("unicode_escape"))

        params = {
            "TaskType": "Network",
            "NetworkDataFormat": "JSON",
            "NetworkName": network_name,
            "EdgeWeightFormat": edge_weight_format,
            "ImputeMethod": "DISCARD",
            "ByteStartIndex": 0,
            "BytesSize": len(data_bytes),
        }

        if edge_transparency is not None:
            params["EdgeTransparency"] = edge_transparency

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            [params],
            ignore_no_plot=True,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        output = self._api_request(params=params, data=data_bytes)

        # Now that data has been successfully loaded into Virtualitics Explore
        # Keep track of current columns and their data types
        self.dataset_num += 1

        return output

    def _load_network_from_edgelist(
        self,
        edgelist,
        network_name=None,
        edge_weight_format="Similarity",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        # TODO: add an impute method

        if isinstance(edgelist, pd.DataFrame):
            if edgelist.shape[0] == 0:
                raise exceptions.InvalidInputTypeException("Network input must have at least one valid edge.")

            params = {"TaskType": "Network", "NetworkDataFormat": "EdgeList", "ImputeMethod": "DISCARD"}
            params["EdgeWeightFormat"] = edge_weight_format
            params["ColumnInfo"] = []
            params["NetworkName"] = network_name
            column_bytes = []
            payload_idx = 0

            if edge_transparency is not None:
                params["EdgeTransparency"] = edge_transparency

            # First and second column must be as strings
            column_names = list(edgelist.columns)

            if len(column_names) not in [2, 3]:
                raise exceptions.InvalidInputTypeException(
                    "Network input in the edgelist format must have either 2 or "
                    "3 columns only. The first 2 columns represent the source "
                    "and target of each edge. The optional third column must be "
                    "numerical positive values and represents the weight of the "
                    "edge described in the row. "
                )

            for column_counter in range(2):
                col_name = column_names[column_counter]
                col_values = edgelist[col_name].astype(str).values

                serial_col = utils.serialize_column(col_values)
                srctgt = ["source", "target"][column_counter]
                col_info = {
                    "ColumnName": srctgt,
                    "ColumnType": serial_col[0],
                    "BytesSize": serial_col[2],
                    "BytesStartIndex": payload_idx,
                }
                params["ColumnInfo"].append(col_info)
                column_bytes.append(serial_col[1])
                payload_idx += serial_col[2]

            # Third column must be numerical
            if len(column_names) == 3:
                weight = column_names[2]
                if not np.issubdtype(edgelist[weight].values.dtype, np.number) or (edgelist[weight] <= 0).any():
                    raise exceptions.InvalidInputTypeException(
                        "The third column in an edgelist represents edge "
                        "weights and must have numeric values above zero. "
                    )
                else:
                    serial_col = utils.serialize_column(edgelist[weight].values)
                    col_info = {
                        "ColumnName": "weight",
                        "ColumnType": serial_col[0],
                        "BytesSize": serial_col[2],
                        "BytesStartIndex": payload_idx,
                    }
                    params["ColumnInfo"].append(col_info)
                    column_bytes.append(serial_col[1])
                    payload_idx += serial_col[2]

            data_bytes = b"".join(column_bytes)

            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                [params],
                ignore_no_plot=True,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )
            params = self._add_plot_mapping_to_params(params, save_to_local_history)
            output = self._api_request(params=params, data=data_bytes)

            # Now that data has been successfully loaded into Virtualitics Explore
            # Keep track of current columns and their data types
            self.dataset_num += 1
            return output

    def get_network(self, as_edgelist=False):
        """
        This function fetches the network data for the currently loaded dataset. The data can be returned as an
        edgelist (:class:`pandas.DataFrame`) or as a :class:`networkx.Graph` object. When the data is returned as a
        :class:`networkx.Graph` object, it will also encode the additional columns of data that were recorded for
        each node in the network. By default, the function returns the data as a :class:`networkx.Graph` object.

        :param as_edgelist: :class:`bool` determining whether to return the data as a :class:`pandas.DataFrame`.
        :return: :class:`networkx.Graph` object by default. If the `as_edgelist` is set to True, then this method
            returns a :class:`pandas.DataFrame` containing the weighted edgelist.
        """
        if not isinstance(as_edgelist, bool):
            raise exceptions.InvalidInputTypeException("'as_edgelist' must be a `bool`")
        else:
            if as_edgelist:
                params = {"TaskType": "GetNetwork", "NetworkDataFormat": "Edgelist"}
                data_bytes = b""
                return self._api_request(params=[params], data=data_bytes)
            else:
                params = {"TaskType": "GetNetwork", "NetworkDataFormat": "JSON"}
                data_bytes = b""
                return self._api_request(params=[params], data=data_bytes)

    def get_plot(self, save_to_local_history=False):
        """
        Fetch the VipPlot information for the current plot.
        :param save_to_local_history: :class:`bool` Optionally, save the VipPlot local history.
        :return: :class:`VipPlot`
        """
        params = []
        params = self._add_plot_mapping_to_params(params, save_to_local_history, True)
        return self._api_request(params=params, data=None)

    def filter(
        self,
        feature_name,
        min=None,
        max=None,
        include=None,
        exclude=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        :param feature_name: Name of feature to add filter to
        :param min: If feature is continuous, set the lower bound of the filter to "min"
        :param max: If feature is continuous, set the upper bound of the filter to "max"
        :param include: If feature is categorical, set these categories to be visible
        :param exclude: If feature is categorical, set these categories to be invisible
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for filtering. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        params = {"TaskType": "Filter", "Action": "Add", "FeatureName": feature_name}
        if min is not None or max is not None:
            if include or exclude:
                raise exceptions.InvalidInputTypeException(
                    "A filter can be applied only when the continuous min/max "
                    "or categorical include/exclude arguments are set but not "
                    "both"
                )
            if min is not None:
                params["Min"] = min
            if max is not None:
                params["Max"] = max
            params["Type"] = "Continuous"
        elif include or exclude:
            if include:
                if type(include) is not list:
                    include = [str(include)]
                params["Include"] = utils.get_features(include)
            if exclude:
                if type(exclude) is not list:
                    exclude = [str(exclude)]
                params["Exclude"] = utils.get_features(exclude)
            params["Type"] = "Categorical"
        else:
            raise exceptions.InvalidInputTypeException(
                "To apply a filter to %s, either min/max or include/" "exclude arguments must be set" % feature_name
            )

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            [params],
            ignore_no_plot=True,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def remove_filter(
        self,
        feature_name,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        :param feature_name: Name of feature to remove any filter on if it exists
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "Filter", "Action": "Remove", "FeatureName": feature_name}
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            [params],
            ignore_no_plot=True,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def remove_all_filters(
        self,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "Filter", "Action": "RemoveAll"}
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            [params],
            ignore_no_plot=True,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def get_column(self, feature_name):
        """
        Gets the column named <feature_name> from the currently loaded dataset

        :param feature_name: Name of column to get
        :return: :class:`pandas.core.Series`
        """
        params = {"TaskType": "ColumnSync", "Action": "GetColumn", "FeatureName": feature_name}
        return self._api_request(params=[params], data=None)

    def get_column_stats(self, feature_name):
        """
        Gets the basic information and stats for a column named <feature_name> from the currently loaded dataset.

        :param feature_name: Name of the column to get stats for.
        :return: :class:`dict` Dictionary of column information & stats.
        """
        params = {"TaskType": "ColumnStats"}
        if isinstance(feature_name, str) and feature_name is not None:
            params["FeatureName"] = feature_name
        else:
            utils.raise_invalid_argument_exception(
                str(type(feature_name)), "feature_name", "must be of type `str` and not None."
            )

        return self._api_request(params=[params], data=None)

    def get_dataset(self, name=None, visible_points_only=False):
        """
        Gets the entire loaded dataset from the software in its current state

        :param name: If specified, get the dataset named <name>. Else, gets the currently loaded dataset.
        :param visible_points_only: :class:`bool` Whether to return visible points only or not.
            Default value is `False`.
        :return: :class:`pandas.DataFrame`
        """

        params = {"TaskType": "ColumnSync", "Action": "GetDataset"}

        if name:
            params["Name"] = name

        # [EXPD-24]
        if visible_points_only:
            params["VisiblePointsOnly"] = visible_points_only

        return self._api_request(params=[params], data=None)

    def pull_new_columns(self):
        """
        Gets new columns that were added to the currently loaded dataset since the last invocation of this method.
        This does not include columns from the initial loading of a dataset (call get_dataset() to access these) or
        columns created from via ML routines, such as clustering and PCA, that have not been added to the feature list.

        :return: :class:`pandas.DataFrame`
        """
        params = {"TaskType": "ColumnSync", "Action": "PullNewColumns"}
        return self._api_request(params=[params], data=None)

    def get_screen(
        self,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Exports a snapshot of the visible mapping in Virtualitics Explore and fetches a Plot object. If save_to_local_history is set to
        `True`, the VipPlot instance will be appended to the `local_history`
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        params = []
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )

        # This avoid returning an error message to the user about not being able to return the plot when attempting to get a screenshot for an OBJ.
        if (
            save_to_local_history is not None
            and isinstance(save_to_local_history, bool)
            and save_to_local_history == True
        ):
            params = self._add_plot_mapping_to_params(params, save_to_local_history, return_plot_mapping=False)

        return self._api_request(params=params, data=None)

    def history(
        self,
        index=None,
        name=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Allows users to re-plot mappings in Virtualitics Explore's history entries for the current dataset. The user must specify a
        desired index (negative indexing is allowed) or pass the name of the desired plot. If there are multiple
        history entries with the requested name, the last entry with the requested name will be plotted. Users
        have the ability to rename a plot through the software. The user should not specify an index and a name in
        the same function call.

        :param index: :class:`int` index to be used on the list of previously created plots through Virtualitics Explore. Default
            value is None. For the past 1...N plots, access via index=[-1 (latest), -N] or index=[0, N - 1 (latest)].
        :param name: :class:`str` plot name checked against the list of previously created plots through Virtualitics Explore. Default
            value is None
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho".
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "History"}
        if index is not None and name is not None:
            raise exceptions.InvalidUsageException(
                "Specifying an `index` and `name` for desired history entry " "simultaneously is not allowed. "
            )
        else:
            if index is not None and isinstance(index, int):
                params["Index"] = index
            elif name is not None and isinstance(name, str):
                params["Name"] = name
        params = [params]
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def refresh_plot(
        self,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Requests Virtualitics Explore to refresh the current plot. This is the equivalent of pressing the Plot button again. It may be helpful to use this to refresh the
        visualizations after manipulating or adding data to the active dataset.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        """
        params = {"TaskType": "RefreshPlot"}
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            [params],
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )

        self._api_request(params=params, data=None)

    def plot(
        self,
        plot_type="scatter",
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        color_normalization=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        trend_lines=None,
        scatter_plot_point_mode=None,
        line_plot_point_mode=None,
        viewby=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Requests Virtualitics Explore to make the specified plot. Expects column name or :class:`pandas.Series` dimension parameters.
        Plot type is expected to be string.

        :param plot_type: {"scatter", "hist", "line", "maps3d", "maps2d", "ellipsoid", "surface", "convex_hull"};
            default is "scatter"
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param x_range_min: Minimum visible value for the X dimension.
        :param x_range_max: Maximum visible value for the X dimension.
        :param x_limit_min: Minimum value displayed for the X dimension on the axis/grid box.
        :param x_limit_max: Maximum value displayed for the X dimension on the axis/grid box.
        :param x_limit_link: Whether limit is locked to range.
        :param y_range_min: Minimum visible value for the Y dimension.
        :param y_range_max: Maximum visible value for the Y dimension.
        :param y_limit_min: Minimum value displayed for the Y dimension on the axis/grid box.
        :param y_limit_max: Maximum value displayed for the Y dimension on the axis/grid box.
        :param y_limit_link: Whether limit is locked to range.
        :param z_range_min: Minimum visible value for the Z dimension.
        :param z_range_max: Maximum visible value for the Z dimension.
        :param z_limit_min: Minimum value displayed for the Z dimension on the axis/grid box.
        :param z_limit_max: Maximum value displayed for the Z dimension on the axis/grid box.
        :param z_limit_link: Whether limit is locked to range.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param trend_lines: :class:`str` specifying whether to build trend lines for the plot, and how they should be broken down.
            Options: None, Color, GroupBy, All.
            Note: Trend lines are only available for scatter plot and line plot types.
        :param scatter_plot_point_mode: :class:`str` specifies whether to show or hide points in a scatter plot visualization. (Only valid for plot_type = 'scatter_plot')
        :param line_plot_point_mode: :class:`str` specifies whether to show or hide points and lines in a line plot visualization. (Only valid for plot_type = 'line_plot')
        :param viewby: :class:`str` specifies which viewby mode ("color" or "groupby") to use in a line plot visualization. (Only valid for plot_type = 'line_plot')
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        plot_type = utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, plot_type, "plot_type")
        if plot_type == "SCATTER_PLOT":
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.scatter(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                trend_lines=trend_lines,
                scatter_plot_point_mode=scatter_plot_point_mode,
                edge_transparency=edge_transparency,
                show_legend=show_legend,
            )
        elif plot_type == "LINE_PLOT":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )

            return self.line(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                trend_lines=trend_lines,
                line_plot_point_mode=line_plot_point_mode,
                viewby=viewby,
                show_legend=show_legend,
            )
        elif plot_type == "VIOLIN_PLOT":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.violin(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "CONVEX_HULL":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.convex_hull(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "CONFIDENCE_ELLIPSOID":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.ellipsoid(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "HISTOGRAM":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.hist(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "MAPS2D":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.maps2d(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                groupby=groupby,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_scale=z_scale,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                export="front",
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "MAPS3D":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.maps3d(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                groupby=groupby,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_scale=z_scale,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )
        elif plot_type == "SURFACE":
            if scatter_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'scatter_plot_point_mode' is only applicable when plot_type='scatter_plot'"
                )
            if line_plot_point_mode is not None:
                raise exceptions.InvalidUsageException(
                    "'line_plot_point_mode' is only applicable when plot_type='line_plot'"
                )

            return self.surface(
                x=x,
                y=y,
                z=z,
                color=color,
                size=size,
                shape=shape,
                transparency=transparency,
                halo=halo,
                halo_highlight=halo_highlight,
                pulsation=pulsation,
                pulsation_highlight=pulsation_highlight,
                playback=playback,
                playback_highlight=playback_highlight,
                arrow=arrow,
                groupby=groupby,
                x_scale=x_scale,
                y_scale=y_scale,
                z_scale=z_scale,
                x_range_min=x_range_min,
                x_range_max=x_range_max,
                x_limit_min=x_limit_min,
                x_limit_max=x_limit_max,
                x_limit_link=x_limit_link,
                y_range_min=y_range_min,
                y_range_max=y_range_max,
                y_limit_min=y_limit_min,
                y_limit_max=y_limit_max,
                y_limit_link=y_limit_link,
                z_range_min=z_range_min,
                z_range_max=z_range_max,
                z_limit_min=z_limit_min,
                z_limit_max=z_limit_max,
                z_limit_link=z_limit_link,
                size_scale=size_scale,
                transparency_scale=transparency_scale,
                halo_scale=halo_scale,
                arrow_scale=arrow_scale,
                color_type=color_type,
                color_palette_id=color_palette_id,
                color_normalization=color_normalization,
                x_normalization=x_normalization,
                y_normalization=y_normalization,
                z_normalization=z_normalization,
                size_normalization=size_normalization,
                transparency_normalization=transparency_normalization,
                arrow_normalization=arrow_normalization,
                export=export,
                background=background,
                imsize=imsize,
                autocrop=autocrop,
                path=path,
                save_to_local_history=save_to_local_history,
                color_bins=color_bins,
                color_bin_dist=color_bin_dist,
                color_inverted=color_inverted,
                name=name,
                show_legend=show_legend,
            )

    def scatter(
        self,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        color_normalization=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        color_inverted=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        name=None,
        trend_lines=None,
        scatter_plot_point_mode=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates scatter plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param trend_lines: :class:`str` specifies whether to build trend lines for the plot, and how they should be broken down.
            Options: None, Color, GroupBy, All.
            Note: Trend lines are only available for scatter plot and line plot types.
        :param scatter_plot_point_mode: :class:`str` specifies whether to show or hide points in a scatter plot.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="SCATTER",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            color_normalization=color_normalization,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            color_inverted=color_inverted,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            name=name,
            trend_lines=trend_lines,
            scatter_plot_point_mode=scatter_plot_point_mode,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def hist(
        self,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=False,
        volume_by=None,
        x_bins=None,
        y_bins=None,
        z_bins=None,
        name=None,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Generates Histogram in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param groupby: Group By dimension. Works with categorical columns.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param volume_by: setting for metric used for height of histogram bins; {"count", "avg", "sum", "uniform"}
        :param x_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'x' dimension
        :param y_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'y' dimension
        :param z_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'z' dimension
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="HISTOGRAM",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            arrow=arrow,
            playback=playback,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            size_scale=size_scale,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            hist_volume_by=volume_by,
            x_bins=x_bins,
            y_bins=y_bins,
            z_bins=z_bins,
            name=name,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def line(
        self,
        x=None,
        y=None,
        z=None,
        show_points=True,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        color_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        viewby=None,
        color_inverted=None,
        name=None,
        trend_lines=None,
        line_plot_point_mode=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates line plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param show_points: Setting for how to view the points. Valid options are {True, False, "show",
            "hide"}
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param color_normalization: Normalization setting for Color. This can only be set if the feature mapped to
            this dimension is numerical and continuous, the color_type is set to "gradient" and the view-by mode is set to "groupby". The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param viewby: :class:`str` Specify the line plot series grouping dimension. Options are {"color", "groupby"}.
            The default option is "color"
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param trend_lines: :class:`str` specifying whether to build trend lines for the plot, and how they should be broken down.
            Options: None, Color, GroupBy, All.
            Note: Trend lines are only available for scatter plot and line plot types.
        :param line_plot_point_mode: :class:`str` specifies whether to show or hide points and lines in the line plot visualization.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="LINE_PLOT",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            color_normalization=color_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            color_inverted=color_inverted,
            arrow_normalization=arrow_normalization,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            name=name,
            show_points=show_points,
            viewby=viewby,
            trend_lines=trend_lines,
            line_plot_point_mode=line_plot_point_mode,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def maps3d(
        self,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        groupby=None,
        arrow=None,
        z_scale=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        z_normalization=None,
        color_normalization=None,
        x_range_min=None,
        x_range_max=None,
        y_range_min=None,
        y_range_max=None,
        z_range_min=None,
        z_range_max=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        lat_long_lines=True,
        country_lines=None,
        country_labels=None,
        globe_style="natural",
        heatmap_enabled=False,
        heatmap_intensity=None,
        heatmap_radius=None,
        heatmap_radius_unit=None,
        heatmap_feature=False,
        return_data=False,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates 3D Map plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param groupby: Group By dimension. Works with categorical columns.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param lat_long_lines: :class:`bool` visibility setting for Latitude/Longitude lines.
        :param country_lines: :class:`bool` visibility setting for country border lines.
        :param country_labels: :class:`bool` visibility setting for country labels.
        :param globe_style: {"natural", "dark", "black ocean", "blue ocean", "gray ocean", "water color",
            "topographic", "moon", "night"}
        :param heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
        :param heatmap_intensity: :class:`float` to determine the intensity of the heatmap. heatmap_enabled must be True
            for this parameter to be used.
        :param heatmap_radius: :class:`float` determining the radius of sensitivity for heatmap functionality.
            heatmap_enabled must be True for this parameter to be used.
        :param heatmap_radius_unit: determines the units of the heatmap_radius. Must be a :class:`str` and one of
            {"Kilometers", "Miles", "NauticalMiles"}. heatmap_enabled must be True for this parameter to be used.
        :param heatmap_feature: :class:`bool` to determine whether to compute a heatmap feature (computes density of
            points).
        :param return_data: :class:`bool` to determine whether to send back the computed heatmap feature.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None` or :class:`pd.DataFrame` if return_data is True for heatmap_feature
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="MAPS3D",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            groupby=groupby,
            arrow=arrow,
            z_scale=z_scale,
            size_scale=size_scale,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_normalization=z_normalization,
            color_normalization=color_normalization,
            size_normalization=size_normalization,
            arrow_normalization=arrow_normalization,
            transparency_normalization=transparency_normalization,
            lat_long_lines=lat_long_lines,
            country_lines=country_lines,
            country_labels=country_labels,
            globe_style=globe_style,
            heatmap_enabled=heatmap_enabled,
            heatmap_intensity=heatmap_intensity,
            heatmap_radius=heatmap_radius,
            heatmap_radius_unit=heatmap_radius_unit,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            name=name,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        if heatmap_enabled:
            params = self._add_heatmap_feature_to_params(params, heatmap_feature, return_data)
        elif heatmap_feature:
            utils.raise_invalid_argument_exception(
                str(type(heatmap_feature)),
                "heatmap_feature",
                "'heatmap_feature' is only applicable when 'heatmap_enabled' has " "been set to `True`. ",
            )

        return self._api_request(params=params, data=None)

    def maps2d(
        self,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        z_scale=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        z_normalization=None,
        color_normalization=None,
        x_range_min=None,
        x_range_max=None,
        y_range_min=None,
        y_range_max=None,
        z_range_min=None,
        z_range_max=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="front",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        map_provider="ArcGIS",
        map_style="Topographic",
        heatmap_enabled=False,
        heatmap_intensity=None,
        heatmap_radius=None,
        heatmap_radius_unit=None,
        heatmap_feature=False,
        return_data=False,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates 2D Map plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param groupby: Group By dimension. Works with categorical columns.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param map_provider: {"ArcGIS", "Stamen", "OpenStreetMap"}
        :param map_style: depends on the map_provider. See documentation for options.
        :param heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
        :param heatmap_intensity: :class:`float` to determine the intensity of the heatmap. heatmap_enabled must be True
            for this parameter to be used.
        :param heatmap_radius: :class:`float` determining the radius of sensitivity for heatmap functionality.
            heatmap_enabled must be True for this parameter to be used.
        :param heatmap_radius_unit: determines the units of the heatmap_radius. Must be a :class:`str` and one of
            {"Kilometers", "Miles", "NauticalMiles"}. heatmap_enabled must be True for this parameter to be used.
        :param heatmap_feature: :class:`bool` to determine whether to compute a heatmap feature (computes density of
            points).
        :param return_data: :class:`bool` to determine whether to send back the computed heatmap feature.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None` or :class:`pd.DataFrame` if return_data is True for heatmap_feature

        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="MAPS2D",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            groupby=groupby,
            arrow=arrow,
            z_scale=z_scale,
            size_scale=size_scale,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_normalization=z_normalization,
            color_normalization=color_normalization,
            size_normalization=size_normalization,
            arrow_normalization=arrow_normalization,
            transparency_normalization=transparency_normalization,
            heatmap_enabled=heatmap_enabled,
            heatmap_intensity=heatmap_intensity,
            heatmap_radius=heatmap_radius,
            heatmap_radius_unit=heatmap_radius_unit,
            map_provider=map_provider,
            color_inverted=color_inverted,
            map_style=map_style,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            name=name,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export, background, imsize, autocrop, path, params, ignore_no_plot=False, show_legend=show_legend
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        if heatmap_enabled:
            params = self._add_heatmap_feature_to_params(params, heatmap_feature, return_data)
        elif heatmap_feature:
            utils.raise_invalid_argument_exception(
                str(type(heatmap_feature)),
                "heatmap_feature",
                "'heatmap_feature' is only applicable when 'heatmap_enabled' has " "been set to `True`. ",
            )

        return self._api_request(params=params, data=None)

    def ellipsoid(
        self,
        confidence=95.0,
        show_points=True,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates Ellipsoid plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param confidence: :class:`float` confidence probability that must be in {99.5, 99.0, 97.5, 95.0, 90.0, 80.0,
            75.0, 70.0, 50.0, 30.0, 25.0, 20.0, 10.0, 5.0, 2.5, 1.0, 0.5}
        :param show_points: Setting for how to view the confidence ellipsoids. Valid options are {True, False, "show",
            "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`

        """
        # Pass dimension info
        plot = vip_plot.VipPlot(
            plot_type="CONFIDENCE_ELLIPSOID",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            confidence=confidence,
            show_points=show_points,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            name=name,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def convex_hull(
        self,
        show_points=True,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates Convex Hull plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param show_points: Setting for how to view the convex hull. Valid options are {True, False, "show", "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between 5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(
            plot_type="CONVEX_HULL",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            show_points=show_points,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            name=name,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def violin(
        self,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        color_normalization=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        position=None,
        orientation=None,
        edge_transparency=None,
        show_legend=True,
    ):
        """
        Generates violin plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between 5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(
            plot_type="VIOLIN_PLOT",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            color_normalization=color_normalization,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            name=name,
            edge_transparency=edge_transparency,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def surface(
        self,
        show_points=False,
        x=None,
        y=None,
        z=None,
        color=None,
        size=None,
        shape=None,
        transparency=None,
        halo=None,
        halo_highlight=None,
        pulsation=None,
        pulsation_highlight=None,
        playback=None,
        playback_highlight=None,
        arrow=None,
        groupby=None,
        x_scale=None,
        y_scale=None,
        z_scale=None,
        x_range_min=None,
        x_range_max=None,
        x_limit_min=None,
        x_limit_max=None,
        x_limit_link=None,
        y_range_min=None,
        y_range_max=None,
        y_limit_min=None,
        y_limit_max=None,
        y_limit_link=None,
        z_range_min=None,
        z_range_max=None,
        z_limit_min=None,
        z_limit_max=None,
        z_limit_link=None,
        size_scale=None,
        transparency_scale=None,
        halo_scale=None,
        arrow_scale=None,
        color_type=None,
        color_palette_id=None,
        color_normalization=None,
        x_normalization=None,
        y_normalization=None,
        z_normalization=None,
        size_normalization=None,
        transparency_normalization=None,
        arrow_normalization=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        color_bins=None,
        color_bin_dist=None,
        color_inverted=None,
        name=None,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Generates Surface plot in Virtualitics Explore. Expects column name or pandas data series dimension parameters.

        :param show_points: Setting for how to view the surface. Valid options are {True, False, "show", "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
        :param color_inverted: :class:`bool` controlling the order of colors for all color types.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in Virtualitics Explore.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(
            plot_type="SURFACE",
            x=x,
            y=y,
            z=z,
            color=color,
            size=size,
            shape=shape,
            transparency=transparency,
            halo=halo,
            halo_highlight=halo_highlight,
            pulsation=pulsation,
            pulsation_highlight=pulsation_highlight,
            playback=playback,
            playback_highlight=playback_highlight,
            arrow=arrow,
            groupby=groupby,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            size_scale=size_scale,
            x_range_min=x_range_min,
            x_range_max=x_range_max,
            x_limit_min=x_limit_min,
            x_limit_max=x_limit_max,
            x_limit_link=x_limit_link,
            y_range_min=y_range_min,
            y_range_max=y_range_max,
            y_limit_min=y_limit_min,
            y_limit_max=y_limit_max,
            y_limit_link=y_limit_link,
            z_range_min=z_range_min,
            z_range_max=z_range_max,
            z_limit_min=z_limit_min,
            z_limit_max=z_limit_max,
            z_limit_link=z_limit_link,
            transparency_scale=transparency_scale,
            halo_scale=halo_scale,
            arrow_scale=arrow_scale,
            color_type=color_type,
            color_palette_id=color_palette_id,
            color_normalization=color_normalization,
            x_normalization=x_normalization,
            y_normalization=y_normalization,
            z_normalization=z_normalization,
            size_normalization=size_normalization,
            transparency_normalization=transparency_normalization,
            arrow_normalization=arrow_normalization,
            show_points=show_points,
            color_bins=color_bins,
            color_bin_dist=color_bin_dist,
            color_inverted=color_inverted,
            name=name,
        )
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def show(
        self,
        plot: vip_plot.VipPlot,
        display=True,
        save_to_local_history=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Recreates a plot in Virtualitics Explore from a VipPlot instance.

        :param plot: VipPlot instance that contains all important details to send to Virtualitics Explore
        :param display: :class:`bool` flag for whether to show this plot to the user
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param export: Specify whether to export a capture of the plot. defaults to "ortho". If the plot type is
            "MAPS2D", the export setting will be set to "front" regardless of requested parameter, unless the user
            passes `None`/`False`.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        if not isinstance(plot, vip_plot.VipPlot):
            utils.raise_invalid_argument_exception(str(type(plot)), "plot", "must be a VipPlot object instance. ")
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        if display:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )
            params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def smart_mapping(
        self,
        target,
        features=None,
        exclude=None,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        return_results_df=False,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs smart mapping in Virtualitics Explore.

        :param target: Target column that the user wants to find insights about; this feature will be dropped
            automatically from Smart Mapping input regardless of what is listed in the `features` and `exclude`
            parameters.
        :param features: List of column names that user wants to analyze in comparison to target
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_results_df: :class:`bool` for whether to return the feature ranking and correlation groups
            :class:`pd.DataFrame`. The default is `False`; in which case the head of the feature ranking
            :class:`pd.DataFrame` is displayed.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for smart mapping. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: if 'return_results_df' is `True`, this returns the feature importance and correlation groups of
            the input features as a :class:`pd.DataFrame`.
        """
        if not isinstance(return_results_df, bool):
            raise exceptions.InvalidInputTypeException("return_data parameter should be a boolean (True or False.")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        target = utils.get_name(target)

        params = {"TaskType": "SmartMapping"}
        params["Target"] = target

        # Special logic for smart mapping
        # Always return the ranking information from Virtualitics Explore ExploreP; however, only display the head of df if the user does not
        # want to return the df to function caller. This is to ensure that pyVIP user always has access to full smart
        # mapping results.
        params["ReturnData"] = True
        params["Disp"] = not return_results_df

        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        params = [params]

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def apply_suggested_mapping(
        self,
        result_index,
        mapping_index,
        method="smart_mapping",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Applies a suggested mapping from a given smart mapping or pca result.

        :param result_index: :class:`int`; The desired Smart Mapping or PCA Result index (use -1 for currently selected result).
        :param mapping_index: :class:`int`; The desired Suggested Mapping index (warning will be returned if no mapping exists for the provided index).
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param export: Specify whether to export a capture of the plot. defaults to "ortho". If the plot type is
            "MAPS2D", the export setting will be set to "front" regardless of requested parameter, unless the user
            passes `None`/`False`.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        """

        if not isinstance(result_index, int):
            raise exceptions.InvalidInputTypeException("result_index parameter should be an integer.")

        if not isinstance(mapping_index, int):
            raise exceptions.InvalidInputTypeException("mapping_index parameter should be an integer.")

        if method.lower() == "smart_mapping":
            params = {"TaskType": "SmartMappingSuggestedMapping"}
        elif method.lower() == "pca":
            params = {"TaskType": "PcaSuggestedMapping"}
        else:
            utils.raise_invalid_argument_exception(str(type(method)), "method", "must be `smart_mapping` or `pca`. ")
        params["ResultIndex"] = result_index
        params["MappingIndex"] = mapping_index

        params = [params]

        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def ad(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        plus_minus="both",
        stdev=0.5,
        and_or="and",
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
    ):
        """
        Alias to anomaly_detection
        """
        return self.anomaly_detection(
            features,
            exclude,
            return_anomalies_df,
            plus_minus,
            stdev,
            and_or,
            apply,
            export,
            background,
            imsize,
            autocrop,
            path,
            save_to_local_history,
            keep_missing_value_columns,
        )

    def anomaly_detection(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        plus_minus="both",
        stdev=0.5,
        and_or="and",
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs anomaly detection in Virtualitics Explore

        :param features: List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param plus_minus: Include outliers that are above, below, or above and below the desired standard deviation
            mark. Defaults to both. Can be "both", "plus", or "minus"
        :param stdev: User defined standard deviation on which to classify outliers.
        :param and_or: "and" identifies data points that are outliers in all input features. "or" identifies data
            points that are outliers in any of the input features.
        :param apply: [Deprecated] :class:`bool` for whether to apply the result to the halo dimension.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for anomaly detection. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`

        """
        plus_minus = int(utils.case_insensitive_match(utils.POS_NEG_CHOICES, plus_minus, "plus_minus"))
        and_or = utils.case_insensitive_match(utils.AND_OR_CHOICES, and_or, "and_or")
        if not isinstance(return_anomalies_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_anomalies_df parameter should be a boolean " "(True or False)."
            )
        try:
            stdev = utils.case_insensitive_match(utils.STDEV_CHOICES, stdev, "stdev")
        except exceptions.InvalidInputTypeException:
            raise exceptions.InvalidInputTypeException(
                "Invalid standard deviation (we only support a " "range of 0.5 to 5 in 0.5 intervals): " + str(stdev)
            )
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        params = {"TaskType": "AnomalyDetection"}
        params["PositiveNegative"] = plus_minus
        params["StdDev"] = stdev
        params["AndOr"] = and_or

        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["ReturnData"] = return_anomalies_df

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        # if isinstance(apply, bool):
        #     if apply:
        #         params["Apply"] = apply
        #         params = [params]
        #         params = self._add_export_to_params(export, background, imsize, path, params)
        #         params = self._add_plot_mapping_to_params(params, save_to_local_history)
        #     else:
        #         params = [params]
        # else:
        #     utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        params = [params]

        if export is not None and export is not False:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )

        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def threshold_ad(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        threshold=1,
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Alias to pca_anomaly_detection

        :param features:  List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param threshold: Percent threshold on which to classify outliers. Takes values from 0 to 100 exclusive.
            Defaults to a threshold of 1.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the anomaly detection result to the halo dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca based anomaly detection. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        return self.pca_anomaly_detection(
            features,
            exclude,
            return_anomalies_df,
            threshold,
            apply,
            export,
            background,
            imsize,
            autocrop,
            path,
            save_to_local_history,
            keep_missing_value_columns,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )

    def threshold_anomaly_detection(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        threshold=1,
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Alias to pca_anomaly_detection

        :param features:  List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param threshold: Percent threshold on which to classify outliers. Takes values from 0 to 100 exclusive.
            Defaults to a threshold of 1.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the anomaly detection result to the halo dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca based anomaly detection. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        return self.pca_anomaly_detection(
            features,
            exclude,
            return_anomalies_df,
            threshold,
            apply,
            export,
            background,
            imsize,
            autocrop,
            path,
            save_to_local_history,
            keep_missing_value_columns,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )

    def pca_ad(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        threshold=1,
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Alias to pca_anomaly_detection

        :param features:  List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param threshold: Percent threshold on which to classify outliers. Takes values from 0 to 100 exclusive.
            Defaults to a threshold of 1.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the anomaly detection result to the halo dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca based anomaly detection. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        return self.pca_anomaly_detection(
            features,
            exclude,
            return_anomalies_df,
            threshold,
            apply,
            export,
            background,
            imsize,
            autocrop,
            path,
            save_to_local_history,
            keep_missing_value_columns,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )

    def pca_anomaly_detection(
        self,
        features=None,
        exclude=None,
        return_anomalies_df=True,
        threshold=1,
        apply=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        PCA based Anomaly Detection.

        :param features:  List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param threshold: Percent threshold on which to classify outliers. Takes values from 0 to 100 exclusive.
            Defaults to a threshold of 1.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the anomaly detection result to the halo dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca based anomaly detection. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        if not isinstance(threshold, int) and not isinstance(threshold, float):
            raise exceptions.InvalidInputTypeException("Threshold must be a number (int or float) between 0 and 100.")
        if (threshold <= 0) or (threshold >= 100):
            raise exceptions.InvalidInputTypeException(
                "Threshold value, " + str(threshold) + ", is not within the " "accepted range of 0 to " "100 exclusive."
            )
        if not isinstance(return_anomalies_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_anomalies_df parameter should be a boolean " "(True or False)."
            )
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        params = {"TaskType": "PcaAnomalyDetection"}
        params["Threshold"] = threshold
        params["ReturnData"] = return_anomalies_df

        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        # if isinstance(apply, bool):
        #     if apply:
        #         params["Apply"] = apply
        #         params = [params]
        #         params = self._add_export_to_params(export, background, imsize, autocrop, path, params)
        #         params = self._add_plot_mapping_to_params(params, save_to_local_history)
        #     else:
        #         params = [params]
        # else:
        #     utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")

        params = [params]

        if export is not None and export is not False:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )

        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def pca(
        self,
        num_components,
        features=None,
        exclude=None,
        apply=True,
        return_components_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs Principal Component Analysis (PCA) in Virtualitics Explore

        :param num_components: :class:`int` for the number of principle components to compute from the input data.
            The number of components must be within [1, 10] and cannot be greater than the number of features to run on.
        :param features: List of column names that user wants to analyze
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_components_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the first 3 computed components to the spatial
            dimensions. Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: if return_data is True, this returns a :class:`pandas.DataFrame` containing the user specified number
            of principal components. Otherwise, this returns None.
        """
        # Check num_components is a positive integer and that user inputs are formatted correctly
        if not isinstance(return_components_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_components_df parameter should be a boolean " "(True or False)."
            )
        if (num_components is not None) and not isinstance(num_components, int):
            raise exceptions.InvalidInputTypeException("num_components parameter should be a positive integer.")
        if (num_components is not None) and not (1 <= num_components <= 10):
            raise exceptions.InvalidInputTypeException(
                "num_components parameter should be a positive integer " "between 1 and 10."
            )
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        params = {"TaskType": "Pca"}

        params["ReturnData"] = return_components_df
        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)
        if num_components is not None:
            params["NumComponents"] = num_components

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        # if isinstance(apply, bool):
        #     if apply:
        #         params["Apply"] = apply
        #         params = [params]
        #         params = self._add_export_to_params(export, background, imsize, autocrop, path, params)
        #         params = self._add_plot_mapping_to_params(params, save_to_local_history)
        #     else:
        #         params = [params]
        # else:
        #     utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")

        params = [params]

        if export is not None and export is not False:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )

        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def clustering(
        self,
        num_clusters=None,
        features=None,
        exclude=None,
        keep_missing_value_columns=True,
        apply=True,
        return_clusters_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs K-means clustering in Virtualitics Explore

        :param num_clusters: :class:`int` between 1 and 16, specifying the number of clusters to compute. Default is
            `None` and enables 'auto'-mode where the number of clusters to compute is algorithmically determined based
            on stability.
        :param features: List of column names that user wants to analyze
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_clusters_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: [Deprecated] :class:`bool` determining whether to apply the clustering result to the color dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for clustering. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the clustering. If return_data is false, this
            returns None.
        """
        # Check num_clusters is a positive integer and that user inputs are formatted correctly
        if not isinstance(return_clusters_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_clusters_df parameter should be a boolean " "(True or False)."
            )
        if (num_clusters is not None) and (not isinstance(num_clusters, int) or num_clusters < 1 or num_clusters > 16):
            raise exceptions.InvalidInputTypeException("num_clusters parameter must be an 'int' between 1 and 16. ")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )

        params = {"TaskType": "Clustering"}
        if num_clusters is not None:
            params["NumClusters"] = num_clusters
        params["ReturnData"] = return_clusters_df
        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        # if isinstance(apply, bool):
        #     if apply:
        #         params["Apply"] = apply
        #         params = [params]
        #         params = self._add_export_to_params(export, background, imsize, autocrop, path, params)
        #         params = self._add_plot_mapping_to_params(params, save_to_local_history)
        #     else:
        #         params = [params]
        # else:
        #     utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")

        params = [params]

        if export is not None and export is not False:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )

        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def search(
        self,
        search_term=None,
        features=None,
        exclude=None,
        exact_match=False,
        return_search_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        keep_missing_value_columns=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs Search tool in Virtualitics Explore.

        :param search_term: :class:`str` string to search for in the current dataset.
        :param features: List of column names that user wants to include in the search area
        :param exclude: List of column names to exclude in the search area; this overrides any features listed in the
            `features` parameter.
        :param return_search_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for Search. Default is `True`.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the search. If return_data is false, this
            returns None.
        """
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(
                str(type(keep_missing_value_columns)), "keep_missing_value_columns", "must be a `bool`. "
            )
        # Check num_clusters is a positive integer and that user inputs are formatted correctly
        if not isinstance(return_search_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_search_df parameter should be a boolean " "(True or False)."
            )
        if (search_term is not None) and (not isinstance(search_term, str)):
            raise exceptions.InvalidInputTypeException("search_term parameter must be a 'str'")
        if (exact_match is not None) and (not isinstance(exact_match, bool)):
            raise exceptions.InvalidInputTypeException("exact_match parameter must be a boolean.")

        params = {"TaskType": "Search"}
        if search_term is not None:
            params["SearchTarget"] = search_term
        params["ReturnData"] = return_search_df
        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)
        if exact_match is not None:
            params["IsExactSearch"] = exact_match

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        params = [params]

        if export is not None and export is not False:
            params = self._add_export_to_params(
                export,
                background,
                imsize,
                autocrop,
                path,
                params,
                ignore_no_plot=False,
                position=position,
                orientation=orientation,
                show_legend=show_legend,
            )

        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def network_extractor(
        self,
        node_column,
        associative_columns,
        pivot_type="mean",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        bypass_warning=False,
        extraction_type="Categorical",
        standard_scale=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Network extractor is a beta functionality (please submit feedback to "support@virtualitics.com"). With this
        method, you can extract network structures from non-network data. You must specify a column containing
        entities you would like to use as nodes as the 'node_column.' Furthermore, you must specify a list containing
        at least one column of values that will be used to find associations between the selected nodes. There can
        be multiple rows of data about any given node. This tool is especially useful for analyzing categorical
        columns of data.

        :param node_column: :class:`pandas.Series` containing values which will be treated as nodes in a network.
        :param associative_columns: [:class:`pandas.Series`] containing list of columns that will be used to find
            associations between the nodes.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param bypass_warning: :class:`bool`; whether to bypass warning from Network Extractor tool that warns the user
            that the variety and size of the data will require large computational resources and memory. Use with care.
        :param extraction_type: :class:`str`; whether the extraction should be based on Categorical or Numerical associative features.
        :param standard_scale: :class:`bool`; whether to scale numerical values with respect to column mean and standard-deviation.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`None`
        """
        node_column = utils.get_name(node_column)
        associative_columns = utils.get_features(associative_columns)
        pivot_type = utils.case_insensitive_match(utils.PIVOT_TYPES, pivot_type, "pivot_type")
        if len(associative_columns) < 1:
            raise exceptions.InvalidUsageException(
                "`associative_columns` must be a list of column names. Please " "see documentation. "
            )
        if not isinstance(bypass_warning, bool):
            utils.raise_invalid_argument_exception(
                str(type(bypass_warning)), "bypass_warning", "must be a boolean value (True or False). "
            )

        params = {"TaskType": "NetworkExtractor"}
        params["NodeColumnName"] = node_column
        params["AssociativeColumnNames"] = associative_columns
        params["PivotType"] = pivot_type
        params["Bypass_Warning"] = bypass_warning
        if extraction_type not in ["Numerical", "Categorical"]:
            raise exceptions.InvalidUsageException(
                "`extraction_type` must be Numerical or Categorical. Please see documentation"
            )
        params["ExtractionType"] = extraction_type
        params["StandardScale"] = standard_scale
        params = [params]
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
            show_legend=show_legend,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def pagerank(
        self,
        damping_factor=0.85,
        apply=True,
        use_color_normalization=True,
        return_pagerank_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs PageRank algorithm on the visible network that is currently loaded in Virtualitics Explore.

        :param damping_factor: :class:`float` between 0 and 1 representing the damping factor for the PageRank
            algorithm. Defaults to 0.85 which is widely considered a good value. Users are recommended not to change
            this unless they are familiar with the PageRank algorithm.
        :param return_pagerank_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the pagerank result to the color dimension.
            Default is True. When True, color_type is automatically changed to gradient.
        :param use_color_normalization: :class:`bool` determining whether to use softmax color normalization when the
            pagerank result has been applied to color. Default is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the pagerank. If return_pagerank_df is false, this
            returns None.
        """
        # validate input parameters
        if not isinstance(damping_factor, float) or (damping_factor > 1.0) or (damping_factor < 0.0):
            utils.raise_invalid_argument_exception(
                str(type(damping_factor)), "damping_factor", "must be a `float` beteween 0.0 and 1.0"
            )
        if not isinstance(return_pagerank_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_pagerank_df parameter should be a boolean " "(True or False)."
            )

        params = {"TaskType": "PageRank"}
        params["DampingFactor"] = damping_factor
        params["ReturnData"] = return_pagerank_df

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                if isinstance(use_color_normalization, bool):
                    params["UseColorNormalization"] = use_color_normalization
                else:
                    utils.raise_invalid_argument_exception(
                        str(type(use_color_normalization)),
                        "use_color_normalization",
                        "must be a boolean (True or False)",
                    )
                params = [params]
                params = self._add_export_to_params(
                    export,
                    background,
                    imsize,
                    autocrop,
                    path,
                    params,
                    ignore_no_plot=False,
                    position=position,
                    orientation=orientation,
                    show_legend=show_legend,
                )
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def graph_distance(
        self,
        apply=True,
        use_color_normalization=True,
        return_centralities_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs the graph distance algorithms on the visible network that is currently loaded in Virtualitics Explore. The graph distance
        algorithms include betweenness centrality, closeness centrality, and eccentricity.

        :param return_centralities_df: :class:`bool` determining whether to return a :class:`pandas.DataFrame`
            containing the centralities to the caller. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the betweeenness centrality result to the color
            dimension. Default is True. When True, color_type is automatically changed to gradient.
        :param use_color_normalization: :class:`bool` determining whether to use softmax color normalization when the
            betweenness centrality result has been applied to color. Default is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the graph distance algorithms. If
            return_centralities_df is False, this returns `None`.
        """
        # validate input parameters
        if not isinstance(return_centralities_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_centralities_df parameter should be a boolean " "(True or False)."
            )
        params = {"TaskType": "GraphDistance"}
        params["ReturnData"] = return_centralities_df

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                if isinstance(use_color_normalization, bool):
                    params["UseColorNormalization"] = use_color_normalization
                else:
                    utils.raise_invalid_argument_exception(
                        str(type(use_color_normalization)),
                        "use_color_normalization",
                        "must be a boolean (True or False)",
                    )
                params = [params]
                params = self._add_export_to_params(
                    export,
                    background,
                    imsize,
                    autocrop,
                    path,
                    params,
                    ignore_no_plot=False,
                    position=position,
                    orientation=orientation,
                    show_legend=show_legend,
                )
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def network_structure(
        self,
        apply=True,
        return_structure_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs the network structure algorithms on the visible network that is currently loaded in Virtualitics Explore. Network structure
        algorithms include community detection and ForceAtlas3D. The results will also included degree and
        weighted degree results.

        :param return_structure_df: :class:`bool` determining whether to return a :class:`pandas.DataFrame`
            containing the structure results to the caller. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to map the network structure. Default is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the network structure. If
            return_structure_df is False, this returns `None`.
        """
        # validate input parameters
        if not isinstance(return_structure_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_centralities_df parameter should be a boolean " "(True or False)."
            )
        params = {"TaskType": "Structure"}
        params["ReturnData"] = return_structure_df

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                params = [params]
                params = self._add_export_to_params(
                    export,
                    background,
                    imsize,
                    autocrop,
                    path,
                    params,
                    ignore_no_plot=False,
                    position=position,
                    orientation=orientation,
                    show_legend=show_legend,
                )
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def clustering_coefficient(
        self,
        apply=True,
        use_color_normalization=True,
        return_clustering_coefficient_df=True,
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Runs the clustering coefficient algorithm on the visible network that is currently loaded in Virtualitics Explore.

        :param return_clustering_coefficient_df: :class:`bool` determining whether to return a :class:`pandas.DataFrame`
            containing the clustering coefficient results to the caller. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the clustering coefficient result to the color
            dimension. Default is True. When True, color_type is automatically changed to gradient.
        :param use_color_normalization: :class:`bool` determining whether to use softmax color normalization when the
            clustering coefficient result has been applied to color. Default is True.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: :class:`pandas.DataFrame` containing the results of the clustering coefficient. If
            return_clustering_coefficient_df is False, this returns `None`.
        """
        # validate input parameters
        if not isinstance(return_clustering_coefficient_df, bool):
            raise exceptions.InvalidInputTypeException(
                "return_clustering_coefficient_df parameter should be a boolean " "(True or False)."
            )

        params = {"TaskType": "ClusteringCoefficient"}
        params["ReturnData"] = return_clustering_coefficient_df

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                if isinstance(use_color_normalization, bool):
                    params["UseColorNormalization"] = use_color_normalization
                else:
                    utils.raise_invalid_argument_exception(
                        str(type(use_color_normalization)),
                        "use_color_normalization",
                        "must be a boolean (True or False)",
                    )
                params = [params]
                params = self._add_export_to_params(
                    export,
                    background,
                    imsize,
                    autocrop,
                    path,
                    params,
                    ignore_no_plot=False,
                    position=position,
                    orientation=orientation,
                    show_legend=show_legend,
                )
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def explainable_ai(self, function, targetColumn, associativeColumns):
        """
        Configures and runs the Explainable AI tool in Virtualitics Explore.

        :param function: The type of explainability function to run. Can be "IdentificationTree", "RelativeEdgeDensity", "KolmogorovSmirnov".
        :param targetColumn: :class:`pandas.Series` containing values which will be treated as the target categories for explainability.
        :param associativeColumns: [:class:`pandas.Series`] containing list of columns that will be used to as input alongside the target column.

        :return: :class:`None`
        """
        targetColumn = utils.get_name(targetColumn)
        associativeColumns = utils.get_features(associativeColumns)
        netx_function = utils.case_insensitive_match(utils.EXPLAINABLE_AI_FUNCTION, function, "function")
        if len(associativeColumns) < 1:
            raise exceptions.InvalidUsageException(
                "`associativeColumns` must be a list of column names. Please " "see documentation. "
            )

        params = {"TaskType": "ExplainableAI"}
        params["Target Feature"] = targetColumn
        params["Associative Features"] = associativeColumns
        params["ExplainableAIFunction"] = netx_function
        params = [params]
        return self._api_request(params=params, data=None)

    def normalize(
        self,
        norm_type="Softmax",
        export="ortho",
        background="light",
        imsize=(2048, 2048),
        autocrop=True,
        path=None,
        save_to_local_history=True,
        position=None,
        orientation=None,
    ):
        """
        Normalizes the axis for spatial dimensions in Virtualitics Explore if applicable.

        :param norm_type: The type of normalization to apply to the data. Can be "softmax", "log10", or "ihst"
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :return: :class:`None`
        """
        params = []
        params = self._add_normalize_task_to_params(params, norm_type)
        params = self._add_export_to_params(
            export,
            background,
            imsize,
            autocrop,
            path,
            params,
            ignore_no_plot=False,
            position=position,
            orientation=orientation,
        )
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def stats(self, feature=None):
        """
        Alias for statistics
        """
        return self.statistics(feature)

    def statistics(self, feature=None):
        """
        Runs statistics in Virtualitics Explore

        :return: :class:`None`
        """
        params = {"TaskType": "Statistics"}

        if feature is not None:
            feature = utils.get_name(feature)
            params["Feature"] = feature

        return self._api_request(params=[params], data=None)

    def insights(self, insight_type="default"):
        """
        Runs insights in Virtualitics Explore. Returns a pandas data frame containing the requested insights.
        :param insight_type: The type of insights to retrieve. "default", "standard", or "network". Default will automatically choose based on the current dataset type of plot type.

        :return: :class:`pandas.DataFrame`
        """
        params = {"TaskType": "Insights"}
        if not isinstance(insight_type, str):
            raise exceptions.InvalidInputTypeException("Invalid insight_type provided. Value should be a `str`.")

        params["InsightType"] = insight_type

        return self._api_request(params=[params], data=None)

    def set_gridbox_tickmarks_view(self, gridbox=None, tickmarks=None):
        """
        Sets the visibility of the gridbox and tickmarks. Expects one or both of gridbox and tickmarks to be not None.

        :param gridbox: :class:`bool` controlling visibility of gridbox. True sets to "show", False sets to "hide"
        :param tickmarks: :class:`bool` controlling visibility of tickmarks. True sets to "show", False sets to "hide'
        :return: :class:`None`
        """
        if gridbox is None and tickmarks is None:
            raise exceptions.InvalidInputTypeException("Please specify at least one of gridbox or tickmarks arguments.")
        params = {"TaskType": "GridboxAndTickmarks"}
        gridbox = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, str(gridbox), "gridbox")
        tickmarks = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, str(tickmarks), "tickmarks")

        if gridbox is not None:
            params["Gridbox"] = gridbox
        if tickmarks is not None:
            params["Tickmarks"] = tickmarks

        return self._api_request(params=[params], data=None)

    def shape_options(self, render_mode):
        """
        Updates optimization mode of software by setting the shape options render mode.

        :param render_mode: :class:`str` to set the shape options (formerly point render) mode. Can be {"Shapes",
            "Default", "2D", "Points", "Point Cloud", or "PointCloud"}. The "Default" case yields 2D billboard
            rendering of the data points.
        :return: :class:`None`
        """
        render_mode = utils.case_insensitive_match(utils.POINT_RENDER_MODES, render_mode, "render_mode")
        params = {"TaskType": "Optimization", "PointRenderMode": render_mode}
        return self._api_request(params=[params], data=None)

    # @utils.deprecated(version="1.2.1", new_name="VIP.shape_options()")
    # def set_point_render_mode(self, render_mode):
    #     """
    #     Updates optimization mode of software by setting the shape options (point render) mode.
    #
    #     :param render_mode: :class:`str` to set the shape options (point render) mode. Can be {"Shapes", "Default",
    #         "2D", "Points"}
    #     :return: :class:`None`
    #     """
    #     render_mode = utils.case_insensitive_match(utils.POINT_RENDER_MODES, render_mode, "render_mode")
    #     params = {"TaskType": "Optimization", "PointRenderMode": render_mode}
    #     return self._api_request(params=[params], data=None)

    # def point_interaction(self, render_mode):
    #     """
    #     Sets the point interaction mode.
    #
    #     :param render_mode: :class:`bool`. User can interact with point if and only if render_mode is True
    #     :return: :class:`None`
    #     """
    #
    #     if not isinstance(render_mode, bool):
    #         utils.raise_invalid_argument_exception(str(type(render_mode)), "render_mode", "must be a boolean. ")
    #
    #     params = {"TaskType": "Optimization", "PointInteraction": render_mode}
    #     return self._api_request(params=[params], data=None)

    # def optimization(self, optimized):
    #     """
    #     Sets the optimization mode.
    #
    #     :param optimized: If true, sets shape options to Points mode and disables point interaction. Else, sets shape
    #         options to Shapes mode and enables point interaction.
    #     :return: :class:`None`
    #     """
    #     if not isinstance(optimized, bool):
    #         utils.raise_invalid_argument_exception(str(type(optimized)), "optimized", "must be a boolean. ")
    #
    #     params = {"TaskType": "Optimization"}
    #
    #     if optimized:
    #         params["PointRenderMode"] = "Points"
    #         params["PointInteraction"] = False
    #     else:
    #         params["PointRenderMode"] = "Shapes"
    #         params["PointInteraction"] = True
    #
    #     return self._api_request(params=[params], data=None)

    def set_camera_angle(self, angle):
        """
        Sets the camera angle in Virtualitics Explore (does not effect `export` camera angle).

        :param angle: :class:`str` controlling camera angle in Virtualitics Explore. {"Default", "Top", "Front", "Side"}
        :return: :class:`None`
        """
        angle = utils.case_insensitive_match(utils.CAMERA_ANGLE, angle, "angle")
        params = {"TaskType": "CameraAngle", "CameraAngle": angle}
        return self._api_request(params=[params], data=None)

    def get_visible_points(self):
        """
        Returns indices of points visible in Virtualitics Explore in a pandas DataFrame.

        :return: :class:`pandas.DataFrame` with one column containing an indicator of whether
            each point is currently visible in Virtualitics Explore.
        """
        params = {"TaskType": "VisiblePoints"}
        return self._api_request(params=[params], data=None)

    @staticmethod
    def _add_export_to_params(
        export,
        background,
        imsize,
        autocrop,
        path,
        params,
        ignore_no_plot=False,
        position=None,
        orientation=None,
        show_legend=True,
    ):
        """
        Helper function to attach an export task to the current request.

        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :param imsize: Tuple or list of two integers
        :param autocrop: Specify whether to automatically crop the plot capture to remove whitespace
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param params: The current API request
        :param ignore_no_plot: Whether the software should ignore the export task and not raise an exception if
        nothing has been mapped to the plot as yet.
        :param position: { pos_x: float, pos_y: float, pos_z: float } horizontal, vertical and depth values for plot position in meters.
        :param orientation: { rot_x: float, rot_y: float, rot_z: float } pitch, yaw, roll values for plot orientation in degrees.
        :param show_legend: :class:`bool`; whether to show the legend in the plot capture. Default value is True.
        :return: params
        """
        if export in [None, False]:
            return params

        # Check to make sure user params formatted correctly
        if export:
            export = utils.case_insensitive_match(utils.EXPORT_VIEWS, export, "export")

        if path is not None and not isinstance(path, str):
            utils.raise_invalid_argument_exception(
                str(type(path)), "path", "Should be 'str' type encoding path to save" " the exported image. "
            )
        if not (isinstance(imsize, tuple) or isinstance(imsize, list)):
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        if not len(imsize) == 2:
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        if not isinstance(imsize[0], int) or not isinstance(imsize[1], int):
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        hasPosX = False
        hasPosY = False
        hasPosZ = False

        if position is not None:
            if not isinstance(position, dict):
                utils.raise_invalid_argument_exception(
                    str(type(dict)), "position", "{ pos_x: float, pos_y: float, pos_z: float }"
                )

            hasPosX = "pos_x" in position
            hasPosY = "pos_y" in position
            hasPosZ = "pos_z" in position

            if (hasPosX) and (type(position["pos_x"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(position["pos_x"])), "pos_x", "float")

            if (hasPosY) and (type(position["pos_y"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(position["pos_y"])), "pos_y", "float")

            if (hasPosZ) and (type(position["pos_z"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(position["pos_z"])), "pos_z", "float")

        hasRotX = False
        hasRotY = False
        hasRotZ = False

        if orientation is not None:
            if not isinstance(orientation, dict):
                utils.raise_invalid_argument_exception(
                    str(type(dict)), "orientation", "{ rot_x: float, rot_y: float, rot_z: float }"
                )

            hasRotX = "rot_x" in orientation
            hasRotY = "rot_y" in orientation
            hasRotZ = "rot_z" in orientation

            if (hasRotX) and (type(orientation["rot_x"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(orientation["rot_x"])), "rot_x", "float")

            if (hasRotY) and (type(orientation["rot_y"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(orientation["rot_y"])), "rot_y", "float")

            if (hasRotZ) and (type(orientation["rot_z"]) == int or float) == False:
                utils.raise_invalid_argument_exception(str(type(orientation["rot_z"])), "rot_z", "float")

        # attach the new export task
        if (export is not None) or (export is not False):
            export_params = {"TaskType": "Export"}
            export_params["View"] = export
            export_params["Width"] = imsize[0]
            export_params["Height"] = imsize[1]
            export_params["IgnoreNoPlot"] = ignore_no_plot
            export_params["Background"] = background
            export_params["Autocrop"] = autocrop

            if isinstance(show_legend, bool):
                export_params["ShowLegend"] = show_legend
            else:
                raise exceptions.InvalidInputTypeException("show_legend parameter should be of bool type.")

            if hasPosX:
                export_params["PosX"] = position["pos_x"]

            if hasPosY:
                export_params["PosY"] = position["pos_y"]

            if hasPosZ:
                export_params["PosZ"] = position["pos_z"]

            if hasRotX:
                export_params["RotX"] = orientation["rot_x"]

            if hasRotY:
                export_params["RotY"] = orientation["rot_y"]

            if hasRotZ:
                export_params["RotZ"] = orientation["rot_z"]

            if path is not None:
                export_params["Path"] = path

            params.append(export_params)
        return params

    @staticmethod
    def _add_plot_mapping_to_params(params, save_to_local_history, return_plot_mapping=False):
        """
        Constructs the task to get the current plot mapping info

        :param params: The current API request
        :return: params
        """
        plot_mapping_task = {"TaskType": "PlotMappingExport"}

        if (
            save_to_local_history is not None
            and isinstance(save_to_local_history, bool)
            and save_to_local_history == True
        ):
            plot_mapping_task["SaveToLocalHistory"] = save_to_local_history

        if return_plot_mapping is not None and isinstance(return_plot_mapping, bool) and return_plot_mapping == True:
            plot_mapping_task["ReturnPlotMapping"] = return_plot_mapping

        params.append(plot_mapping_task)
        return params

    @staticmethod
    def _add_heatmap_feature_to_params(params, heatmap_feature, return_data):
        if not isinstance(heatmap_feature, bool):
            utils.raise_invalid_argument_exception(str(type(heatmap_feature)), "heatmap_feature", "must be a `bool`.")
        if not isinstance(return_data, bool):
            utils.raise_invalid_argument_exception(str(type(return_data)), "return_data", "must be a `bool`")

        if heatmap_feature:
            heatmap_task = {"TaskType": "HeatmapFeature"}
            heatmap_task["ReturnData"] = return_data
            params.append(heatmap_task)
        return params

    @staticmethod
    def _add_normalize_task_to_params(params, norm_type):
        """
        Constructs the task to apply normalize to the spatial dimensions (with option to apply to size).

        :param params: the current API request's task params list
        :param norm_type: the normalization option to use.
        :return: params
        """
        norm_param = {"TaskType": "Normalize"}
        norm_param["NormType"] = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, norm_type, "norm_type")
        params.append(norm_param)
        return params

    def _update_invalid_export_view(self, plot, requested_view):
        """
        This checks if the requested view is invalid and substitutes it if necessary.

        :param plot: :class:`VipPlot` instance.
        :param requested_view: :class:`str` specifying the requested view.
        :return: :class:`None`
        """
        if requested_view in [None, False]:
            return requested_view
        if not isinstance(requested_view, str):
            utils.raise_invalid_argument_exception(
                type(requested_view),
                "export",
                "Should be None/False or 'ortho', " "'front', 'side' or 'right', 'top', " "or 'perspective'",
            )
        if requested_view.lower() in ["none", "false"]:
            return None

        best_view = plot.get_best_export_view()
        if best_view is not None and best_view != requested_view:
            print(
                "The 'export' view is being reset to '{}' view since this is the only valid view for "
                "this plot. ".format(best_view)
            )
            requested_view = best_view

        return requested_view

    ############# Dashboard API #############

    def create_custom_dashboard(self, name=None):
        """
        Create a new VipDashboard instance in Virtualitics Explore.

        :param name: :class:`str` user-specified name for the VipDashboard instance.
        :return: :class:`VipDashboard`
        """

        if not isinstance(name, str) and name is not None:
            raise exceptions.InvalidInputTypeException("name should be a `str` or `None`")

        params = {"TaskType": "CreateCustomDashboard"}
        params["VipDashboardName"] = name

        output = self._api_request(params=[params], data=None)
        return output

    def clear_custom_dashboard(self, guid=None):
        """
        Clears all VipDashboardTiles from a VipDashboard instance in Virtualitics Explore.

        :param guid: :class:`str` The GUID of the dashboard to clear.
        :return: :class:`None`
        """

        if not isinstance(guid, str):
            raise exceptions.InvalidInputTypeException("guid should be a `str`")

        params = {"TaskType": "ClearCustomDashboard"}
        params["VipDashboardGUID"] = guid

        output = self._api_request(params=[params], data=None)
        return output

    def set_current_dashboard(self, guid=None):
        """
        Sets the current VipDashboard in the dashboard window in Virtualitics Explore, based on the specified GUID.

        :param guid: :class:`str` The GUID of the dashboard to activate.
        :return: :class:`None`
        """

        if not isinstance(guid, str):
            raise exceptions.InvalidInputTypeException("guid should be a `str`")

        params = {"TaskType": "SetCurrentDashboard"}
        params["VipDashboardGUID"] = guid

        output = self._api_request(params=[params], data=None)
        return output

    def destroy_custom_dashboard(self, guid=None):
        """
        Destroys a VipDashboard instance in Virtualitics Explore.

        :param guid: :class:`str` The GUID of the dashboard to destroy.
        :return: :class:`None`
        """

        if not isinstance(guid, str):
            raise exceptions.InvalidInputTypeException("guid should be a `str`")

        params = {"TaskType": "DestroyCustomDashboard"}
        params["VipDashboardGUID"] = guid

        output = self._api_request(params=[params], data=None)
        return output

    def add_dashboard_tile(
        self,
        name: str,
        dashboard: vip_dashboard.VipDashboard,
        tile_type: str,
        header_text=None,
        width=None,
        height=None,  # general arguments
        body_text=None,  # Text Tile arguments
        mapping_id=None,
        plot=None,  # snapshot tile arguments
        # Histogram/Piechart args
        dataset_name=None,
        column_name=None,
        column_bins=8,
        # Histogram args
        breakdown_column_name=None,
        breakdown_index=-1,
        breakdown_bins=4,
        breakdown_bin_dist="equal",  # When breakdown column is numerical
    ):
        """
        Create a new VipDashboardTile instance in Virtualitics Explore and assign it to a dashboard.

        :param name: :class:`str` Desired name of the dashboard (may be displayed in Virtualitics Explore).
        :param dashboard: :class:`vip_dashboard.VipDashboard` object on which to add a tile.
        :param tile_type: :class:`str` Desired tile type (i.e., text, histogram, piechart, snapshot)
        :param header_text: :class:`str` Text to be displayed in the header bar of the tile in Virtualitics Explore.
        :param body_text: :class:`str` Text to be displayed in the body of the tile in Virtualitics Explore (for `text` tile_type only).
        :param width: :class:`int` or `float` Desired tile width in pixels (may be clamped by Virtualitics Explore, [370,1110]).
        :param height: :class:`int` or `float` Desired tile height in pixels (may be clamped by Virtualitics Explore [290,870]).
        :param mapping_id: :class:`int` Mapping index used to produce a snapshot tile. (optional - for `snapshot` tile_type only.)
        :param plot: :class:`VipPlot` object used to generate a new mapping to use when producing a snapshot tile. (optional - for `snapshot` tile_type only)
        :param dataset_name: :class:`str` Name of the dataset in Virtualitics Explore that holds the data needed for the tile (optional - for `histogram` and `piechart` tile_type only)
        :param column_name: :class:`str` Name of the column used to the tile (optional - for `histogram` and `piechart` tile_type only)
        :param column_bins: :class:`int` Number of bins to display for a numerical histogram or piechart (optional - for `histogram` and `piechart` tile_type only, default value is 8 for histogram, 4 for piechart)
        :param breakdown_column_name: :class:`str` Name of breakdown column used to divide histogram bins further into groups (optional - for `histogram` tile_type only)
        :param breakdown_index: :class:`int` Preferred breakdown category, by index. Default value of -1 will display an aggregate of all categories in the breakdown. (optional - for `histogram` tile_type only)
        :param breakdown_bins: :class:`int` Number of bins to divide the breakdown column. (optional - for `histogram` tile_type only.) Default value: 4.
        :param breakdown_bin_dist: :class:`str` Preferred breakdown bin distribution for numerical breakdown columns. `equal` or `range`. (optional - for `histogram` tile_type only)
        :return: :class:`VipDashboardTile`
        """

        params = {"TaskType": "AddDashboardTile"}
        params["VipDashboardTileName"] = name
        params["VipDashboardTileType"] = tile_type
        params["VipDashboardGUID"] = dashboard.guid
        params["HeaderText"] = header_text

        if not isinstance(width, float) and not isinstance(width, int) and width is not None:
            utils.raise_invalid_argument_exception(type(width), "width", "Should be a `int`, a `float`, or None.")

        if not isinstance(height, float) and not isinstance(height, int) and height is not None:
            utils.raise_invalid_argument_exception(type(height), "height", "Should be a `int`, a `float`, or None.")

        if width is not None:
            params["Width"] = width

        if height is not None:
            params["Height"] = height

        if tile_type.lower() == "text":
            params["BodyText"] = body_text

        elif tile_type.lower() == "histogram":
            params["ColumnName"] = column_name
            params["ColumnBins"] = column_bins
            params["BreakdownColumnName"] = breakdown_column_name
            params["BreakdownIndex"] = breakdown_index
            params["BreakdownBins"] = breakdown_bins
            params["BreakdownBinDist"] = breakdown_bin_dist
            params["DatasetName"] = dataset_name

            if not isinstance(column_name, str):
                utils.raise_invalid_argument_exception(
                    type(column_name), "column_name", "Should be a `str` and not None."
                )

            if not isinstance(column_bins, int) or column_bins > 16 or column_bins < 1:
                utils.raise_invalid_argument_exception(
                    type(column_bins), "column_bins", "Should be a `int` between 1 and 16."
                )

            if not isinstance(breakdown_bins, int) or breakdown_bins > 16 or breakdown_bins < 1:
                utils.raise_invalid_argument_exception(
                    type(breakdown_bins), "breakdown_bins", "Should be a `int` between 1 and 16."
                )

            if not isinstance(breakdown_bin_dist, str) or (
                breakdown_bin_dist != "equal" and breakdown_bin_dist != "range"
            ):
                utils.raise_invalid_argument_exception(
                    type(breakdown_bin_dist), "breakdown_bin_dist", "Should be a `str` and either `equal` or `range`."
                )

            if not isinstance(breakdown_column_name, str) and breakdown_column_name is not None:
                utils.raise_invalid_argument_exception(
                    type(breakdown_column_name), "breakdown_column_name", "Should be a `str` or None."
                )

            if not isinstance(breakdown_index, int):
                utils.raise_invalid_argument_exception(type(breakdown_index), "breakdown_index", "Should be a `int`.")

            if not isinstance(dataset_name, str):
                utils.raise_invalid_argument_exception(
                    type(dataset_name), "dataset_name", "Should be a `str` and not None."
                )

        elif tile_type.lower() == "piechart":
            params["ColumnName"] = column_name
            params["DatasetName"] = dataset_name
            params["ColumnBins"] = column_bins
            # params["BreakdownBins"] = breakdown_bins
            # params["BreakdownBinDist"] = breakdown_bin_dist

            if not isinstance(column_name, str):
                utils.raise_invalid_argument_exception(
                    type(column_name), "column_name", "Should be a `str` and not None."
                )

            if not isinstance(column_bins, int) or column_bins > 16 or column_bins < 1:
                utils.raise_invalid_argument_exception(
                    type(column_bins), "column_bins", "Should be a `int` between 1 and 16."
                )

            # if not isinstance(breakdown_bins, int) or breakdown_bins > 16 or breakdown_bins < 1:
            #    utils.raise_invalid_argument_exception(type(breakdown_bins), "breakdown_bins", "Should be a `int` between 1 and 16.")

            # if not isinstance(breakdown_bin_dist, str) or (breakdown_bin_dist != "equal" and breakdown_bin_dist != "range"):
            #    utils.raise_invalid_argument_exception(type(breakdown_bin_dist), "breakdown_bin_dist", "Should be a `str` and either `equal` or `range`.")

            if not isinstance(dataset_name, str):
                utils.raise_invalid_argument_exception(
                    type(dataset_name), "dataset_name", "Should be a `str` and not None."
                )

        elif tile_type.lower() == "snapshot":
            if not isinstance(dataset_name, str):
                utils.raise_invalid_argument_exception(
                    type(dataset_name), "dataset_name", "Should be a `str` and not None."
                )

            params["DatasetName"] = dataset_name
            if mapping_id is not None:
                if not isinstance(mapping_id, int):
                    utils.raise_invalid_argument_exception(
                        type(mapping_id), "mapping_id", "Should be a `int` or `None`."
                    )

                params["MappingID"] = mapping_id
                if plot is not None:
                    utils.raise_invalid_argument_exception(
                        type(plot), "plot", "Should be `None` if mapping_id is provided."
                    )

            if plot is not None:
                if not isinstance(plot, vip_plot.VipPlot):
                    utils.raise_invalid_argument_exception(type(plot), "plot", "Should be a `VipPlot`.")

                params = [plot.get_params(), params]
                # params = self._add_plot_mapping_to_params(params, False)
                output = self._api_request(params=params, data=None)
                return output

        output = self._api_request(params=[params], data=None)
        return output

    def add_text_dashboard_tile(
        self,
        name: str,
        dashboard: vip_dashboard.VipDashboard,
        header_text=None,
        body_text=None,
        width=None,
        height=None,
    ):
        """
        Helper method for generating a text dashboard tile.

        :param name: :class:`str` Desired name of the dashboard (may be displayed in Virtualitics Explore).
        :param dashboard: :class:`vip_dashboard.VipDashboard` object on which to add a tile.
        :param header_text: :class:`str` Text to be displayed in the header bar of the tile in Virtualitics Explore.
        :param body_text: :class:`str` Text to be displayed in the body of the tile in Virtualitics Explore (for `text` tile_type only).
        :param width: :class:`int` or `float` Desired tile width in pixels (may be clamped by Virtualitics Explore, [370,1110]).
        :param height: :class:`int` or `float` Desired tile height in pixels (may be clamped by Virtualitics Explore [290,870]).
        :return: :class:`VipDashboardTile`
        """

        return self.add_dashboard_tile(
            name=name,
            dashboard=dashboard,
            tile_type="text",
            header_text=header_text,
            body_text=body_text,
            width=width,
            height=height,
        )

    def add_histogram_dashboard_tile(
        self,
        name: str,
        dashboard: vip_dashboard.VipDashboard,
        header_text=None,
        width=None,
        height=None,
        dataset_name=None,
        column_name=None,
        column_bins=8,
        breakdown_column_name=None,
        breakdown_index=-1,
        breakdown_bins=4,
        breakdown_bin_dist="equal",
    ):
        """
        Helper method for generating a histogram dashboard tile.

        :param name: :class:`str` Desired name of the dashboard (may be displayed in Virtualitics Explore).
        :param dashboard: :class:`vip_dashboard.VipDashboard` object on which to add a tile.
        :param header_text: :class:`str` Text to be displayed in the header bar of the tile in Virtualitics Explore.
        :param width: :class:`int` or `float` Desired tile width in pixels (may be clamped by Virtualitics Explore, [370,1110]).
        :param height: :class:`int` or `float` Desired tile height in pixels (may be clamped by Virtualitics Explore [290,870]).
        :param dataset_name: :class:`str` Name of the dataset in Virtualitics Explore that holds the data needed for the tile (required for `histogram`, `piechart`, and `snapshot` tile_type only)
        :param column_name: :class:`str` Name of the column used to the tile (optional - for `histogram` and `piechart` tile_type only)
        :param column_bins: :class:`int` Number of bins to display for a numerical histogram or piechart (optional - for `histogram` and `piechart` tile_type only, default value is 8 for histogram, 4 for piechart)
        :param breakdown_column_name: :class:`str` Name of breakdown column used to divide histogram bins further into groups (optional - for `histogram` tile_type only)
        :param breakdown_index: :class:`int` Preferred breakdown category, by index. Default value of -1 will display an aggregate of all categories in the breakdown. (optional - for `histogram` tile_type only)
        :param breakdown_bins: :class:`int` Number of bins to divide the breakdown column. (optional - for `histogram` tile_type only.) Default value: 4.
        :param breakdown_bin_dist: :class:`str` Preferred breakdown bin distribution for numerical breakdown columns. `equal` or `range`. (optional - for `histogram` tile_type only)
        :return: :class:`VipDashboardTile`
        """

        return self.add_dashboard_tile(
            name=name,
            dashboard=dashboard,
            tile_type="histogram",
            header_text=header_text,
            width=width,
            height=height,
            dataset_name=dataset_name,
            column_name=column_name,
            column_bins=column_bins,
            breakdown_column_name=breakdown_column_name,
            breakdown_index=breakdown_index,
            breakdown_bins=breakdown_bins,
            breakdown_bin_dist=breakdown_bin_dist,
        )

    def add_piechart_dashboard_tile(
        self,
        name: str,
        dashboard: vip_dashboard.VipDashboard,
        header_text=None,
        width=None,
        height=None,
        dataset_name=None,
        column_name=None,
        column_bins=8,
    ):
        """
        Helper method for generating a piechart dashboard tile.

        :param name: :class:`str` Desired name of the dashboard (may be displayed in Virtualitics Explore).
        :param dashboard: :class:`vip_dashboard.VipDashboard` object on which to add a tile.
        :param header_text: :class:`str` Text to be displayed in the header bar of the tile in Virtualitics Explore.
        :param width: :class:`int` or `float` Desired tile width in pixels (may be clamped by Virtualitics Explore, [370,1110]).
        :param height: :class:`int` or `float` Desired tile height in pixels (may be clamped by Virtualitics Explore [290,870]).
        :param dataset_name: :class:`str` Name of the dataset in Virtualitics Explore that holds the data needed for the tile (required for `histogram`, `piechart`, and `snapshot` tile_type only)
        :param column_name: :class:`str` Name of the column used to the tile (optional - for `histogram` and `piechart` tile_type only)
        :param column_bins: :class:`int` Number of bins to display for a numerical histogram or piechart (optional - for `histogram` and `piechart` tile_type only, default value is 8 for histogram, 4 for piechart)
        :return: :class:`VipDashboardTile`
        """

        return self.add_dashboard_tile(
            name=name,
            dashboard=dashboard,
            tile_type="piechart",
            header_text=header_text,
            width=width,
            height=height,
            dataset_name=dataset_name,
            column_name=column_name,
            column_bins=column_bins,
        )

    def add_snapshot_dashboard_tile(
        self,
        name: str,
        dashboard: vip_dashboard.VipDashboard,
        header_text=None,
        width=None,
        height=None,
        dataset_name=None,
        mapping_id=None,
        plot=None,
    ):
        """
        Helper method for generating a snapshot dashboard tile.

        :param name: :class:`str` Desired name of the dashboard (may be displayed in Virtualitics Explore).
        :param dashboard: :class:`vip_dashboard.VipDashboard` object on which to add a tile.
        :param header_text: :class:`str` Text to be displayed in the header bar of the tile in Virtualitics Explore.
        :param width: :class:`int` or `float` Desired tile width in pixels (may be clamped by Virtualitics Explore, [370,1110]).
        :param height: :class:`int` or `float` Desired tile height in pixels (may be clamped by Virtualitics Explore [290,870]).
        :param dataset_name: :class:`str` Name of the dataset in Virtualitics Explore that holds the data needed for the tile (required for `histogram`, `piechart`, and `snapshot` tile_type only)
        :param mapping_id: :class:`int` Mapping index used to produce a snapshot tile. (for `snapshot` tile_type only.)
        :param plot: :class:`VipPlot` object used to generate a new mapping to use when producing a snapshot tile. (for `snapshot` tile_type only)
        :return: :class:`VipDashboardTile`
        """

        return self.add_dashboard_tile(
            name=name,
            dashboard=dashboard,
            tile_type="snapshot",
            header_text=header_text,
            width=width,
            height=height,
            dataset_name=dataset_name,
            mapping_id=mapping_id,
            plot=plot,
        )

    def remove_dashboard_tiles(self, dashboard: vip_dashboard.VipDashboard, guids=None):
        """
        Remove a list of dashboards by GUID from a specified VipDashboard.

        :param dashboard: :class:`VipDashboard` Dashboard from which to remove tiles.
        :param guids: :class:`str[]` Array of tile guids to remove from the dashboard.
        :return: :class:`None`
        """

        params = {"TaskType": "RemoveDashboardTiles"}
        params["VipDashboardGUID"] = dashboard.guid
        params["VipDashboardTileGUIDs"] = guids

        output = self._api_request(params=[params], data=None)
        return output

    ############# Annotations API #############

    def create_annotation(
        self,
        # generic arguments
        a_type: vip_annotation.AnnotationType,
        name=None,
        comment=None,
        userID=None,
        isCollapsed=False,
        windowColor=None,
        textColor=None,
        pipPosition=None,
        screenPositionX=None,
        screenPositionY=None,
        screenOffsetX=None,
        screenOffsetY=None,  # worldOffset=None,
        width=None,
        height=None,
        # dataset, mapping, and point annotation arguments
        datasetName=None,
        mappingID=None,
        rowIndex=None,
        # object annotation arguments
        objectName=None,
        objectID=None,
        isAttached=False,
        objectAnchorX=None,
        objectAnchorY=None,
        objectAnchorZ=None,
    ):
        """
        Base method to create an annotation of any type.

        :param a_type: :class:`AnnotationType` specifies the type of annotation.
        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation.
        :param userID: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param datasetName: :class:`str` The name of the dataset the annotation belongs to (if a DATASET, MAPPING, or POINT annotation).
        :param mappingID: :class:`int` The index of the mapping the annotation belongs to (if a MAPPING ANNOTATION).
        :param objectName: :class:`str` The name of the object the annotation belongs to (if an OBJECT annotation). This can be used in place of `objectID`.
        :param objectID: :class:`str` The id of the object the annotation belongs to (if an OBJECT annotation). This can be used in place of `objectName`.
        :param rowIndex: :class:`int` The rowIndex of the data point the annotation belongs to (if a POINT annotation).
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` or `str` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenPositionX: :class:`float` The screen-space X position of the annotation, normalized from 0 (left) to 1 (right). This setting is only used for DATASET, MAPPING, and Detached OBJECT annotations.
        :param screenPositionY: :class:`float` The screen-space Y position of the annotation, normalized from 0 (bottom) to 1 (top). This setting is only used for DATASET, MAPPING, and Detached OBJECT annotations.
        :param screenOffsetX: :class:`float` The screen-space X offset of the annotation, normalized from -1 (full screen width to the left) to 1 (full screen width to the right). This setting is only used for POINT annotations and Attached OBJECT annotations.
        :param screenOffsetY: :class:`float` The screen-space Y offset of the annotation, normalized from -1 (full screen height below) to 1 (full screen height above). This setting is only used for POINT annotations and Attached OBJECT annotations.
        :param objectAnchorX: :class:`float` The object-space X position of the object annotation attach point, or anchor.
        :param objectAnchorY: :class:`float` The object-space Y position of the object annotation attach point, or anchor.
        :param objectAnchorZ: :class:`float` The object-space Z position of the object annotation attach point, or anchor.
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isAttached: :class:`bool` The attached/detached state of an annotation (if an OBJECT annotation).
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.
        :return: :class:`VipAnnotation`
        """

        params = {"TaskType": "CreateAnnotation"}

        if not isinstance(a_type, vip_annotation.AnnotationType) or a_type is None:
            utils.raise_invalid_argument_exception(type(a_type), "a_type", "Should be a `AnnotationType` and not None.")

        params["AnnotationType"] = a_type.name

        if not isinstance(name, str) and name is not None:
            utils.raise_invalid_argument_exception(type(name), "name", "Should be a `str` or None.")

        params["AnnotationName"] = name

        if not isinstance(comment, str) and comment is not None:
            utils.raise_invalid_argument_exception(type(comment), "comment", "Should be a `str` or None.")

        params["AnnotationComment"] = comment

        if not isinstance(userID, str) and userID is not None:
            utils.raise_invalid_argument_exception(type(userID), "userID", "Should be a `str` or None.")

        params["AnnotationUserID"] = userID

        if not isinstance(isCollapsed, bool):
            utils.raise_invalid_argument_exception(type(isCollapsed), "isCollapsed", "Should be a `bool`.")

        params["AnnotationIsCollapsed"] = isCollapsed

        if not isinstance(windowColor, str) and windowColor is not None:
            utils.raise_invalid_argument_exception(type(windowColor), "windowColor", "Should be a `str` and not None.")

        params["AnnotationWindowColor"] = windowColor

        if not isinstance(textColor, str) and textColor is not None:
            utils.raise_invalid_argument_exception(type(textColor), "textColor", "Should be a `str` and not None.")

        params["AnnotationTextColor"] = textColor

        if (
            not isinstance(pipPosition, vip_annotation.AnnotationPipPosition)
            and not isinstance(pipPosition, str)
            and pipPosition is not None
        ):
            utils.raise_invalid_argument_exception(
                type(pipPosition), "pipPosition", "Should be a `AnnotationPipPosition` or a `str` and not None."
            )

        if pipPosition is vip_annotation.AnnotationPipPosition.LEFT or pipPosition is None:
            pipPosition = "left"
        elif pipPosition is vip_annotation.AnnotationPipPosition.RIGHT:
            pipPosition = "right"

        if pipPosition is not None:
            pipPosition = pipPosition.lower()
            if pipPosition != "left" and pipPosition != "right":
                utils.raise_invalid_argument_exception(
                    str(type(pipPosition)),
                    "pipPosition",
                    "Should be a valid `AnnotationPipPosition` or 'left' or 'right'.",
                )

        params["AnnotationPipPosition"] = pipPosition

        if (
            not isinstance(screenPositionX, float)
            and not isinstance(screenPositionX, int)
            and screenPositionX is not None
        ):
            utils.raise_invalid_argument_exception(
                type(screenPositionX), "screenPositionX", "Should be a `float` or `int` and not None."
            )

        if screenPositionX is None:
            screenPositionX = 0.5

        params["AnnotationScreenPositionX"] = screenPositionX

        if (
            not isinstance(screenPositionY, float)
            and not isinstance(screenPositionY, int)
            and screenPositionY is not None
        ):
            utils.raise_invalid_argument_exception(
                type(screenPositionY), "screenPositionY", "Should be a `float` or `int` and not None."
            )

        if screenPositionY is None:
            screenPositionY = 0.5

        params["AnnotationScreenPositionY"] = screenPositionY

        # screenoffset for point annotations and attached object annotations.
        if not isinstance(screenOffsetX, float) and not isinstance(screenOffsetX, int) and screenOffsetX is not None:
            utils.raise_invalid_argument_exception(
                type(screenOffsetX), "screenOffsetX", "Should be a `float` or `int` and not None."
            )

        if screenOffsetX is None:
            screenOffsetX = 0.0

        params["AnnotationScreenOffsetX"] = screenOffsetX

        if not isinstance(screenOffsetY, float) and not isinstance(screenOffsetY, int) and screenOffsetY is not None:
            utils.raise_invalid_argument_exception(
                type(screenOffsetY), "screenOffsetY", "Should be a `float` or `int` and not None."
            )

        if screenOffsetY is None:
            screenOffsetY = 0.0

        params["AnnotationScreenOffsetY"] = screenOffsetY

        # if not isinstance(a_type, vip_annotation.VipAnnotation) or a_type is None:
        #    utils.raise_invalid_argument_exception(type(a_type), "a_type", "Should be a `VipAnnotation` and not None.")

        # params["AnnotationWorldOffset"] = worldOffset

        if width is not None:
            if not isinstance(width, float) and not isinstance(width, int):
                utils.raise_invalid_argument_exception(type(width), "width", "Should be a `float` or `int`.")
            params["AnnotationWidth"] = width

        if height is not None:
            if not isinstance(height, float) and not isinstance(height, int):
                utils.raise_invalid_argument_exception(type(height), "height", "Should be a `float` or `int`.")
            params["AnnotationHeight"] = height

        if a_type is vip_annotation.AnnotationType.DATASET:
            if datasetName is not None:
                if not isinstance(datasetName, str):
                    utils.raise_invalid_argument_exception(type(datasetName), "datasetName", "Should be a `str`.")

                params["AnnotationDatasetName"] = datasetName

        elif a_type is vip_annotation.AnnotationType.MAPPING:
            if datasetName is not None:
                if not isinstance(datasetName, str):
                    utils.raise_invalid_argument_exception(type(datasetName), "datasetName", "Should be a `str`.")

                params["AnnotationDatasetName"] = datasetName

            if mappingID is not None:
                if not isinstance(mappingID, int):
                    utils.raise_invalid_argument_exception(type(mappingID), "mappingID", "Should be a `int`.")

                params["AnnotationMapping"] = mappingID

        elif a_type is vip_annotation.AnnotationType.POINT:
            if datasetName is not None:
                if not isinstance(datasetName, str):
                    utils.raise_invalid_argument_exception(type(datasetName), "datasetName", "Should be a `str`.")

                params["AnnotationDatasetName"] = datasetName

            if rowIndex is not None:
                if not isinstance(rowIndex, int):
                    utils.raise_invalid_argument_exception(type(rowIndex), "rowIndex", "Should be a `int`.")

                params["AnnotationRowIndex"] = rowIndex

        elif a_type is vip_annotation.AnnotationType.OBJECT:
            if objectName is not None:
                if not isinstance(objectName, str):
                    utils.raise_invalid_argument_exception(type(objectName), "objectName", "Should be a `str`.")

                params["AnnotationObjectName"] = objectName

            if objectID is not None:
                if not isinstance(objectID, str):
                    utils.raise_invalid_argument_exception(type(objectID), "objectID", "Should be a `str`.")

                params["AnnotationObjectID"] = objectID

            if isAttached is not None:
                if not isinstance(isAttached, bool):
                    utils.raise_invalid_argument_exception(type(isAttached), "isAttached", "Should be a `bool`.")

                params["AnnotationIsAttached"] = isAttached

            if objectAnchorX is not None:
                params["AnnotationObjectAnchorX"] = objectAnchorX

            if objectAnchorY is not None:
                params["AnnotationObjectAnchorY"] = objectAnchorY

            if objectAnchorZ is not None:
                params["AnnotationObjectAnchorZ"] = objectAnchorZ

        output = self._api_request(params=[params], data=None)
        return output

    def create_annotation_from_instance(self, annotation: vip_annotation.VipAnnotation):
        """
        Creates a Virtualitics Explore annotation from an instance of a VipAnnotation.
        :param annotation: :class:`VipAnnotation` Annotation instance holding all relevant information for the annotation.
        :return: :class:`VipAnnotation`
        """
        return self.create_annotation(
            a_type=annotation.a_type,
            name=annotation.name,
            comment=annotation.comment,
            userID=annotation.userID,
            isCollapsed=annotation.isCollapsed,
            windowColor=annotation.windowColor,
            textColor=annotation.textColor,
            pipPosition=annotation.pipPosition,
            screenPositionX=annotation.screenPositionX,
            screenPositionY=annotation.screenPositionY,
            screenOffsetX=annotation.screenOffsetX,
            screenOffsetY=annotation.screenOffsetY,
            # worldOffset=annotation.worldOffset,
            width=annotation.width,
            height=annotation.height,
        )

    def create_dataset_annotation(
        self,
        name=None,
        comment=None,
        userID=None,
        isCollapsed=False,
        windowColor=None,
        textColor=None,
        pipPosition=None,
        screenPositionX=None,
        screenPositionY=None,
        # worldOffset=None,
        width=None,
        height=None,
        datasetName=None,
    ):
        """
        Helper method to create a dataset annotation.

        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation.
        :param userID: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param datasetName: :class:`str` The name of the dataset to which the annotation belongs.
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` or `str` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenPositionX: :class:`float` The screen-space X position of the annotation, normalized from 0 (left) to 1 (right).
        :param screenPositionY: :class:`float` The screen-space Y position of the annotation, normalized from 0 (bottom) to 1 (top).
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.
        :return: :class:`VipAnnotation`
        """
        return self.create_annotation(
            a_type=vip_annotation.AnnotationType.DATASET,
            name=name,
            comment=comment,
            userID=userID,
            isCollapsed=isCollapsed,
            windowColor=windowColor,
            textColor=textColor,
            pipPosition=pipPosition,
            screenPositionX=screenPositionX,
            screenPositionY=screenPositionY,
            # worldOffset=worldOffset,
            width=width,
            height=height,
            datasetName=datasetName,
        )

    def create_mapping_annotation(
        self,
        name=None,
        comment=None,
        userID=None,
        isCollapsed=False,
        windowColor=None,
        textColor=None,
        pipPosition=None,
        screenPositionX=None,
        screenPositionY=None,
        # worldOffset=None,
        width=None,
        height=None,
        datasetName=None,
        mappingID=None,
    ):
        """
        Helper method to create a mapping annotation.

        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation.
        :param userID: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param datasetName: :class:`str` The name of the dataset to which the annotation belongs.
        :param mappingID: :class:`int` The index of the mapping to which the annotation belongs.
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` or `str` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenPositionX: :class:`float` The screen-space X position of the annotation, normalized from 0 (left) to 1 (right).
        :param screenPositionY: :class:`float` The screen-space Y position of the annotation, normalized from 0 (bottom) to 1 (top).
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.

        :return: :class:`VipAnnotation`
        """
        return self.create_annotation(
            a_type=vip_annotation.AnnotationType.MAPPING,
            name=name,
            comment=comment,
            userID=userID,
            isCollapsed=isCollapsed,
            windowColor=windowColor,
            textColor=textColor,
            pipPosition=pipPosition,
            screenPositionX=screenPositionX,
            screenPositionY=screenPositionY,
            # worldOffset=worldOffset,
            width=width,
            height=height,
            datasetName=datasetName,
            mappingID=mappingID,
        )

    def create_point_annotation(
        self,
        name=None,
        comment=None,
        userID=None,
        isCollapsed=False,
        windowColor=None,
        textColor=None,
        pipPosition=None,
        screenOffsetX=None,
        screenOffsetY=None,
        # worldOffset=None,
        width=None,
        height=None,
        datasetName=None,
        rowIndex=None,
    ):
        """
        Helper method to create a point annotation. Only one point annotation per row index is allowed.
        Any attempts to add an annotation to a row index that already contains one will result in an error being returned.

        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation.
        :param userID: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param datasetName: :class:`str` The name of the dataset to which the annotation belongs.
        :param rowIndex: :class:`int` The rowIndex of the data point to which the annotation belongs.
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` or `str` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenOffsetX: :class:`float` The screen-space X offset of the annotation from its attached point, normalized from -1 (full screen width to the left) to 1 (full screen width to the right).
        :param screenOffsetY: :class:`float` The screen-space Y offset of the annotation from its attached point, normalized from -1 (full screen height below) to 1 (full screen height above).
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.

        :return: :class:`VipAnnotation`
        """
        return self.create_annotation(
            a_type=vip_annotation.AnnotationType.POINT,
            name=name,
            comment=comment,
            userID=userID,
            isCollapsed=isCollapsed,
            windowColor=windowColor,
            textColor=textColor,
            pipPosition=pipPosition,
            screenOffsetX=screenOffsetX,
            screenOffsetY=screenOffsetY,
            # worldOffset=worldOffset,
            width=width,
            height=height,
            datasetName=datasetName,
            rowIndex=rowIndex,
        )

    def create_object_annotation(
        self,
        name=None,
        comment=None,
        userID=None,
        isCollapsed=False,
        windowColor=None,
        textColor=None,
        pipPosition=None,
        screenPositionX=None,
        screenPositionY=None,
        screenOffsetX=None,
        screenOffsetY=None,
        # worldOffset=None,
        width=None,
        height=None,
        objectID=None,
        isAttached=False,
        objectAnchorX=None,
        objectAnchorY=None,
        objectAnchorZ=None,
    ):
        """
        Helper method to create an object annotation.

        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation.
        :param userID: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param objectID: :class:`str` The id of the object the annotation belongs to (if an OBJECT annotation).
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` or `str` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenPositionX: :class:`float` The screen-space X position of the annotation, normalized from 0 (left) to 1 (right). This setting is only used if `isAttached` is False.
        :param screenPositionY: :class:`float` The screen-space Y position of the annotation, normalized from 0 (bottom) to 1 (top). This setting is only used if `isAttached` is False.
        :param screenOffsetX: :class:`float` The screen-space X offset of the annotation from its attached point, normalized from -1 (full screen width to the left) to 1 (full screen width to the right). This setting is only used if `isAttached` is True.
        :param screenOffsetY: :class:`float` The screen-space Y offset of the annotation from its attached point, normalized from -1 (full screen height below) to 1 (full screen height above). This setting is only used if `isAttached` is True.
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isAttached: :class:`bool` The attached/detached state of an annotation.
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.
        :param objectAnchorX: :class:`float` The object-space X position of the object annotation attach point, or anchor.
        :param objectAnchorY: :class:`float` The object-space Y position of the object annotation attach point, or anchor.
        :param objectAnchorZ: :class:`float` The object-space Z position of the object annotation attach point, or anchor.
        :return: :class:`VipAnnotation`
        """
        return self.create_annotation(
            a_type=vip_annotation.AnnotationType.OBJECT,
            name=name,
            comment=comment,
            userID=userID,
            isCollapsed=isCollapsed,
            windowColor=windowColor,
            textColor=textColor,
            pipPosition=pipPosition,
            screenPositionX=screenPositionX,
            screenPositionY=screenPositionY,
            screenOffsetX=screenOffsetX,
            screenOffsetY=screenOffsetY,
            # worldOffset=worldOffset,
            width=width,
            height=height,
            objectID=objectID,
            isAttached=isAttached,
            objectAnchorX=objectAnchorX,
            objectAnchorY=objectAnchorY,
            objectAnchorZ=objectAnchorZ,
        )

    def change_annotation_type(self, id: str, new_type: vip_annotation.AnnotationType):
        """
        Convert an annotation from one type to another.
        Only certain transformations are allowed (i.e. Point->Mapping, Point->Dataset, Mapping->Dataset, Dataset->Mapping)

        :param id: :class:`str` ID of the annotation to be changed.
        :param new_type: :class:`AnnotationType` New desired type for the annotation. (i.e. mapping, dataset)
        :return: :class:`VipAnnotation`
        """
        params = {"TaskType": "CreateAnnotation"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(str(type(id)), "id", "`id` must be specified as a `str`.")

        params["AnnotationID"] = id

        if not isinstance(new_type, vip_annotation.AnnotationType) or new_type is None:
            utils.raise_invalid_argument_exception(
                str(type(new_type)), "new_type", "`new_type` must be specified as a `AnnotationType`."
            )

        params["AnnotationNewType"] = new_type.name

        return self._api_request(params=[params], data=None)

    def link_annotation(
        self,
        id=None,
        linkedObjectID=None,
        linkedObjectName=None,
        linkedDatasetName=None,
        linkedMappingID=None,
        linkLatestMapping=False,
    ):
        """
        Link an annotation, by id, to a specificed object or dataset/mapping.

        :param id: :class:`str` ID of the annotation to link.
        :param linkedObjectName: :class:`str` Name of the object to link to (if linking to an object).
        :param linkedObjectID: :class:`str` ID of the object to link to (if object name not provided).
        :param linkedDatasetName: :class:`str` Name of the dataset to link to (if linking to a mapping).
        :param linkedMappingID: :class:`int` ID of the mapping to link to (if linking to a mapping).
        :param linkLatestMapping: :class:`bool` Whether to ignore the linkedMappingID and simply link to the latest mapping for the specified dataset.

        :return: :class:`None`
        """
        params = {"TaskType": "LinkAnnotation"}

        # check annotation id
        if not isinstance(id, str):
            utils.raise_invalid_argument_exception(type(id), "id must be a `str` and not None.")

        params["AnnotationID"] = id

        # specify linked object
        if linkedObjectName is not None:
            if not isinstance(linkedObjectName, str):
                utils.raise_invalid_argument_exception(type(linkedObjectName), "linkedObjectName", "Should be a `str`.")

            params["AnnotationLinkedObjectName"] = linkedObjectName

        if linkedObjectID is not None:
            if not isinstance(linkedObjectID, str):
                utils.raise_invalid_argument_exception(type(linkedObjectID), "linkedObjectID", "Should be a `str`.")

            params["AnnotationLinkedObjectID"] = linkedObjectID

        # specify linked dataset
        if linkedDatasetName is not None:
            if not isinstance(linkedDatasetName, str):
                utils.raise_invalid_argument_exception(
                    type(linkedDatasetName), "linkedDatasetName", "Should be a `str`."
                )

            params["AnnotationLinkedDatasetName"] = linkedDatasetName

            if not isinstance(linkedMappingID, int) or linkedMappingID is None:
                utils.raise_invalid_argument_exception(
                    type(linkedMappingID), "linkedMappingID", "Should be an `int` and not None."
                )

            params["AnnotationLinkedMappingID"] = linkedMappingID
        elif isinstance(linkedMappingID, int) and linkedMappingID is not None:
            utils.raise_invalid_argument_exception(
                type(linkedDatasetName), "linkedDatasetName", "Cannot be None when trying to link a mapping."
            )

        # specify linked mapping
        if linkLatestMapping is not None:
            if not isinstance(linkLatestMapping, bool):
                utils.raise_invalid_argument_exception(
                    type(linkLatestMapping), "linkLatestMapping", "Should be a `bool`"
                )

            params["AnnotationLinkLatestMapping"] = linkLatestMapping

        output = self._api_request(params=[params], data=None)
        return output

    def attach_object_annotation(self, id: str, objectAnchorX=None, objectAnchorY=None, objectAnchorZ=None):
        """
        Given an object annotation by id, attach to to its object at the specified anchor position.

        :return: :class:`None`
        """
        params = {"TaskType": "AttachAnnotation"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(
                str(type(id)), "id", "must be a `str` specifying an annotation by id, and not None."
            )
        params["AnnotationID"] = id
        params["Attach"] = True

        if objectAnchorX is not None:
            params["AnnotationObjectAnchorX"] = objectAnchorX

        if objectAnchorY is not None:
            params["AnnotationObjectAnchorY"] = objectAnchorY

        if objectAnchorZ is not None:
            params["AnnotationObjectAnchorZ"] = objectAnchorZ

        self._api_request(params=[params], data=None)

    def detach_object_annotation(self, id: str):
        """
        Given an object annotation by id, detach it from its object anchor position.

        :return: :class:`None`
        """
        params = {"TaskType": "AttachAnnotation"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(
                str(type(id)), "id", "must be a `str` specifying an annotation by id, and not None."
            )
        params["AnnotationID"] = id
        params["Attach"] = False

        self._api_request(params=[params], data=None)

    def set_annotation_color(self, id: str, windowColor=None, textColor=None):
        """
        Set the window and/or text color of an annotation.
        :param id: :class:`str` Annotation id provided by Virtualitics Explore.
        :param windowColor: :class:`str` The color of the header in the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the header text in the annotation, represented as an HTML color string (i.e. FF0000 for RED)

        :return: :class:`None`
        """
        params = {"TaskType": "SetAnnotationColor"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(
                str(type(id)), "id", "must be a `str` specifying an annotation by id, and not None."
            )
        params["AnnotationID"] = id

        if not isinstance(windowColor, str):
            utils.raise_invalid_argument_exception(
                str(type(windowColor)), "windowColor", "must be a `str` specifying the desired window color."
            )

        params["AnnotationWindowColor"] = windowColor

        if not isinstance(textColor, str):
            utils.raise_invalid_argument_exception(
                str(type(textColor)), "textColor", "must be a `str` specifying the desired text color."
            )

        params["AnnotationTextColor"] = textColor

        self._api_request(params=[params], data=None)

    def reset_annotation_color(self, id: str):
        """
        Resets the annotation color back to default.

        :return: :class:`None`
        """
        params = {"TaskType": "SetAnnotationColor"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(
                str(type(id)), "id", "must be a `str` specifying an annotation by id, and not None."
            )
        params["AnnotationID"] = id
        params["Reset"] = True

        self._api_request(params=[params], data=None)

    def set_annotation_position(self, id: str, posX: float, posY: float):
        """
        Set the screen position of an annotation.

        :param id:  :class:`str` id of the annotation to position.
        :param posX: :class:`float` Screen X position, normalized 0.0-1.0 (left to right). Values outside of this range will results in off-screen annotations.
        :param posY: :class:`float` Screen Y position, normalized 0.0-1.0 (bottom to top). Values outside of this range will results in off-screen annotations.
        :return: :class:`None`
        """
        params = {"TaskType": "SetAnnotationScreenPosition"}

        if not isinstance(id, str):
            utils.raise_invalid_argument_exception(str(type(id)), "id", "must be a `str`.")

        params["AnnotationID"] = id

        if not isinstance(posX, int) and not isinstance(posX, float):
            utils.raise_invalid_argument_exception(str(type(posX)), "posX", "must be an `int` or `float`.")

        params["ScreenPositionX"] = posX

        if not isinstance(posY, int) and not isinstance(posY, float):
            utils.raise_invalid_argument_exception(str(type(posY)), "posY", "must be an `int` or `float`.")

        params["ScreenPositionY"] = posY

        self._api_request(params=[params], data=None)

    def set_annotation_dimensions(self, id: str, width: float, height: float):
        """
        Set the dimensions for an annotation.

        :param id:  :class:`str` id of the annotation to position.
        :param width: :class:`float` width as a ratio of screen size.
        :param height: :class:`float` height as a ratio of screen size.
        :return: :class:`None`
        """
        params = {"TaskType": "SetAnnotationDimensions"}

        if not isinstance(id, str):
            utils.raise_invalid_argument_exception(str(type(id)), "id", "must be a `str`.")

        params["AnnotationID"] = id

        if not isinstance(width, int) and not isinstance(width, float):
            utils.raise_invalid_argument_exception(str(type(width)), "width", "must be an `int` or `float`.")

        params["Width"] = width

        if not isinstance(height, int) and not isinstance(height, float):
            utils.raise_invalid_argument_exception(str(type(height)), "height", "must be an `int` or `float`.")

        params["Height"] = height

        self._api_request(params=[params], data=None)

    def delete_annotation(self, id: str):
        """
        Delete an annotation based on a given id.

        :param id: :class:`str` ID for an annotation (provided) by Virtualitics Explore.
        :return: :class:`None`
        """
        params = {"TaskType": "DeleteAnnotation"}

        if not isinstance(id, str) or id is None:
            utils.raise_invalid_argument_exception(
                str(type(id)), "id", "must be a `str` specifying an annotation by id, and not None."
            )
        params["AnnotationID"] = id

        self._api_request(params=[params], data=None)

    def show_annotations(self):
        """
        Triggers the global toggle to show all Annotations in Virtualitics Explore.

        :return: :class:`None`
        """
        params = {"TaskType": "ShowAnnotations"}

        self._api_request(params=[params], data=None)

    def hide_annotations(self):
        """
        Triggers the global toggle to hide all Annotations in Virtualitics Explore.

        :return: :class:`None`
        """
        params = {"TaskType": "HideAnnotations"}

        self._api_request(params=[params], data=None)

    def get_all_annotations(self, a_type=None):
        """
        Get all annotations of a specific type in the current Virtualitics Explore project.

        :param a_type: :class:`vip_annotation.AnnotationType` The desired type of annotations to retrieve. If set to `None`, all annotations of all types will be retrieved.
        :return: :class:`[AnnotationType]`
        """
        params = {"TaskType": "GetAnnotations"}

        if not isinstance(a_type, vip_annotation.AnnotationType) and a_type is not None:
            utils.raise_invalid_argument_exception(
                str(type(a_type)), "a_type", "must be a `vip_Annotation.AnnotationType` or None."
            )

        if a_type is not None:
            params["AnnotationType"] = a_type.name

        return self._api_request(params=[params], data=None)

    def get_all_dataset_annotations(self, dataset_name=None):
        """
        Get all dataset annotations. (optional: limit to a particular dataset, by name)

        :param dataset_name: :class:`str` (optional) Dataset name of the desired data from which to retrieve annotations.
        :return: :class:`[AnnotationType]`
        """
        params = {"TaskType": "GetAnnotations"}
        params["AnnotationType"] = vip_annotation.AnnotationType.DATASET.name

        if not isinstance(dataset_name, str) and dataset_name is not None:
            utils.raise_invalid_argument_exception(str(type(dataset_name)), "dataset_name", "must be a `str` or None.")
        if dataset_name is not None:
            params["DatasetName"] = dataset_name

        return self._api_request(params=[params], data=None)

    def get_all_mapping_annotations(self, dataset_name=None):
        """
        Get all mapping annotations. (optional: limit to a particular dataset, by name)

        :param dataset_name: :class:`str` (optional) Dataset name of the desired data from which to retrieve annotations.
        :return: :class:`[AnnotationType]`
        """
        params = {"TaskType": "GetAnnotations"}
        params["AnnotationType"] = vip_annotation.AnnotationType.MAPPING.name

        if not isinstance(dataset_name, str) and dataset_name is not None:
            utils.raise_invalid_argument_exception(str(type(dataset_name)), "dataset_name", "must be a `str` or None.")
        if dataset_name is not None:
            params["DatasetName"] = dataset_name

        return self._api_request(params=[params], data=None)

    def get_all_point_annotations(self, dataset_name=None):
        """
        Get all point annotations. (optional: limit to a particular dataset, by name)

        :param dataset_name: :class:`str` (optional) Dataset name of the desired data from which to retrieve annotations.
        :return: :class:`[AnnotationType]`
        """
        params = {"TaskType": "GetAnnotations"}
        params["AnnotationType"] = vip_annotation.AnnotationType.POINT.name

        if not isinstance(dataset_name, str) and dataset_name is not None:
            utils.raise_invalid_argument_exception(str(type(dataset_name)), "dataset_name", "must be a `str` or None.")
        if dataset_name is not None:
            params["DatasetName"] = dataset_name

        return self._api_request(params=[params], data=None)

    def get_all_object_annotations(self, object_id=None):
        """
        Get all object annotations. (optional: limit to a particular object, by id)

        :param object_id: :class:`str` (optional) Object ID of the desired object from which to retrieve annotations.
        :return: :class:`[AnnotationType]`
        """
        params = {"TaskType": "GetAnnotations"}
        params["AnnotationType"] = vip_annotation.AnnotationType.OBJECT.name

        if not isinstance(object_id, str) and object_id is not None:
            utils.raise_invalid_argument_exception(str(type(object_id)), "object_id", "must be a `str` or None.")
        if object_id is not None:
            params["ObjectID"] = object_id

        return self._api_request(params=[params], data=None)

    def delete_all_annotations(self):
        """
        Deletes all Annotations (globally) in Virtualitics Explore.

        :return: :class:`None`
        """
        params = {"TaskType": "DeleteAllAnnotations"}

        self._api_request(params=[params], data=None)

    def collapse_all_annotations(self):
        """
        Triggers the global toggle to collapse all expanded Annotations in Virtualitics Explore.

        :return: :class:`None`
        """
        params = {"TaskType": "CollapseAllAnnotations"}

        self._api_request(params=[params], data=None)

    def expand_all_annotations(self):
        """
        Triggers the global toggle to expand all collapsed Annotations in VIP.

        :return: :class:`None`
        """
        params = {"TaskType": "ExpandAllAnnotations"}

        self._api_request(params=[params], data=None)

    def get_legend(self, color=True, shape=True, groupby=True, background="light"):
        """
        Returns the legend information from the active dataset in Virtualitics Explore.

        :param color: :class:`bool` Whether to return Color legend information.
        :param shape: :class:`bool` Whether to return Shape legend information.
        :param groupby: :class:`bool` Whether to return Group By legend information.
        :param background: Specify whether to export a plot capture with a light or dark theme, or the current color
            scheme configured in Virtualitics Explore. Options are {"light", "dark", "current"}. Light is used if the value is not specified.
        :return: :class:`None`
        """

        params = {"TaskType": "GetLegend", "GetColor": color, "GetShape": shape, "GetGroupBy": groupby, "Background": background}

        return self._api_request(params=[params], data=None)

    def get_orientation(self):
        """
        Returns the Plot or OBJ orientation and position in Virtualitics Explore.

        :return: :class:`None`
        """

        params = {"TaskType": "GetOrientation"}

        return self._api_request(params=[params], data=None)
