import networkx as nx
from virtualitics import exceptions, utils, vip_result, vip_plot, vip_dashboard, vip_annotation, vip_object
from virtualitics.legend_builder import LegendBuilder
import virtualitics
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import pandas as pd
import json
import tabulate
from IPython.display import display, HTML
import time

DEBUG_LEVEL = 2
PLOT_MARGIN_DEFAULT = 50


def generic_callback(response_bytes, payload, log_level, figsize):
    """
    General callback called upon API request response

    :param response_bytes: The header of the request received
    :param payload: Larger data
    :param log_level: logging level used in the callbacks
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from Virtualitics Explore. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: Default None or pd.DataFrame containing column(s) of results
    """
    results = []
    response = json.loads(response_bytes.decode())

    if log_level == DEBUG_LEVEL:
        print(response)

    if ("AuthStatus" not in response):  # [EXPW-1446]
        if ("Error" in response):
            raise exceptions.AuthenticationException(response["Error"])  # [EXPW-1446]
        else:
            raise exceptions.AuthenticationException("Virtualitics Explore failed to authenticate the session. AuthStatus could not be found.") # [EXPW-1446]

    if ("VersionStatus" not in response): # [EXPW-1446]
        if ("Error" in response):
            raise exceptions.AuthenticationException(response["Error"])  # [EXPW-1446]
        else:
            raise exceptions.AuthenticationException("Virtualitics Explore failed to authenticate the session. VersionStatus could not be found.") # [EXPW-1446]

    if (response["AuthStatus"] == "Success") and (response["VersionStatus"] == "Success"):
        if "SpecialResponse" in response:
            print(response["SpecialResponse"] + "\n")
            return None, None

        task_failures = []
        task_index = 1

        for task_response in response["TaskResponses"]:
            task_status = task_response.get("TaskStatus") or "Failed"
            if task_status != "Success":
                task_failures.append(task_response)
            else:
                # Handle outputs for specific task types
                output = _process_specific_task(task_response, payload, log_level, figsize)
                if output is not None:
                    results.append(output)

            task_index += 1

        if len(task_failures) > 0:
            failure = task_failures[0]
            task_type = failure.get('TaskType') or 'unknown'
            error = failure.get('Error') or '(unknown reason)'
            error = error.replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
            exception_message = "Task '%s' failed because '%s'" % (task_type, error)

            if (task_type == "unknown") and (error == "(unknown reason)"):
                raise exceptions.VipTaskUnknownExecutionException("The Virtualitics Explore task execution failed without providing a "
                                                                  "reason. Please try running the command again. ")
            # also print 'Note' attribute if it exists
            if "Note" in failure:
                note = failure["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
                exception_message += ". Note: '%s'" % note

            raise exceptions.VipTaskExecutionException(exception_message)

        if len(results) == 0:
            return None, None
        elif len(results) > 0:
            return vip_result.VipResult(results), response["TaskResponses"][-1] # along with the last result, return the last task response.
        else:
            raise (exceptions.MultipleObjectsToReturnException("There was more than one object to return to caller!"))
    else:
        # Priority given to authentication errors
        if response["AuthStatus"] != "Success":
            # Raise and exception with the bubbled up error message from Virtualitics Explore
            raise exceptions.AuthenticationException(response["Error"])
        if response["VersionStatus"] != "Success":
            if response["VersionStatusFailReason"] == "InvalidApiVersion":
                raise exceptions.VersionMismatchException(
                    "pyVIP version (" + virtualitics.__version__ + ") is not supported by the installed version " +
                    "of Virtualitics Explore (" + response["VIPVersion"] + "). Virtualitics Explore expecting pyVIP version (" +
                    response["ExpectedAPIVersion"] + ") or greater. Check 'Version' section in the documentation " +
                    "and update the appropriate tool.")
            elif response["VersionStatusFailReason"] == "InvalidVIPVersion":
                raise exceptions.VersionMismatchException(
                    "Virtualitics Explore version (" + response["VIPVersion"] + ") is not supported by the installed version of " +
                    "pyVIP (" + virtualitics.__version__ + "). pyVIP expecting Virtualitics Explore version (" +
                    virtualitics.__latest_compatible_vip_version__ + ") or greater. Check 'Version' section in the " +
                    "documentation and update the appropriate tool.")

def _process_specific_task(task_response, payload, log_level, figsize):
    """
    Processes the responses for specific task types. When adding a specific callback create the function and then add
    the task type and function name to the switcher dictionary

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :param log_level: logging level used in the callbacks
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from Virtualitics Explore. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: Output of any specific task processing
    """
    # Maps task types to callback functions
    task_type = task_response["TaskType"]

    #print("Processing Task: " + task_type)
    if task_type == "Export":
        return _export_callback(task_response, payload, figsize)
    elif task_type == "SmartMapping":
        return _smart_mapping_callback(task_response, payload)
    elif task_type == "AnomalyDetection" or task_type == "PcaAnomalyDetection":
        return _ad_callback(task_response, payload)
    elif task_type == "Pca":
        return _pca_callback(task_response, payload)
    elif task_type == "Clustering":
        return _clustering_callback(task_response, payload)
    elif task_type == "Search":
        return _search_callback(task_response, payload)
    elif task_type == "PlotMappingExport":
        return _plot_mapping_export_callback(task_response, payload, log_level)
    elif task_type == "VisiblePoints":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "HeatmapFeature":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "AddRows":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "Filter":
        return _filter_callback(task_response, payload)
    elif task_type == "ColumnSync":
        return _column_sync_callback(task_response, payload)
    elif task_type == "ColumnStats":
        return _column_stats_callback(task_response, payload)
    elif task_type == "ConvertColumn":
        return _convert_column_callback(task_response, payload)
    elif task_type == "GetNetwork":
        return _get_network_callback(task_response, payload)
    elif task_type == "PageRank":
        return _pagerank_callback(task_response, payload)
    elif task_type == "ClusteringCoefficient":
        return _clustering_coefficient_callback(task_response, payload)
    elif task_type == "GraphDistance":
        return _graph_distance_callback(task_response, payload)
    elif task_type == "Structure":
        return _structure_callback(task_response, payload)
    elif task_type == "Insights":
        return _insights_callback(task_response, payload)
    elif task_type == "DataSet":
        return _dataset_callback(task_response, payload)
    elif task_type == "Network":
        return _network_callback(task_response, payload)
    elif task_type == "LoadOBJ":
        return _obj_callback(task_response, payload)
    elif task_type == "CreateCustomDashboard":
        return _create_custom_dashboard_callback(task_response, payload)
    elif task_type == "ClearCustomDashboard":
        return _clear_custom_dashboard_callback(task_response, payload)
    elif task_type == "DestroyCustomDashboard":
        return _destroy_custom_dashboard_callback(task_response, payload)
    elif task_type == "AddDashboardTile":
        return _create_dashboard_tile_callback(task_response, payload)
    elif task_type == "RemoveDashboardTiles":
        return _remove_dashboard_tiles_callback(task_response, payload)
    elif task_type == "CreateAnnotation":
        return _create_annotation_callback(task_response, payload)
    elif task_type == "GetAnnotations":
        return _get_annotations_callback(task_response, payload)
    elif task_type == "ExplainableAI":
        return _explainable_ai_callback(task_response, payload)
    elif task_type == "GetWorkflow":
        return _get_workflow_callback(task_response, payload)
    elif task_type == "GetLegend":
        return _get_legend_callback(task_response, payload)
    elif task_type == "GetOrientation":
        return _get_orientation_callback(task_response, payload)

    notes_message = ""
    if "Note" in task_response:
        note = task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
        notes_message += "Note: '%s'" % note

    print(notes_message)

    return None


def _plot_mapping_export_callback(task_response, payload, log_level):
    """
    Callback handler for plot mapping export tasks

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array. unused here
    :param log_level: logging level used in the callbacks to set in returned vip plot
    :return: :class:`VipPlot` object instance
    """
    if ((not task_response["SaveToLocalHistory"] or not isinstance(task_response["SaveToLocalHistory"], bool) or task_response["SaveToLocalHistory"] == False) and
        (not task_response["ReturnPlotMapping"] or not isinstance(task_response["ReturnPlotMapping"], bool) or task_response["ReturnPlotMapping"] == False)):
        return None

    plot = vip_plot.VipPlot(data_set_name=task_response["DataSetName"], plot_type=task_response["PlotType"],
                            map_mode=task_response["MapMode"], name=task_response["PlotName"], log_level=log_level)

    # Dimensions
    if "DimensionInfo" in task_response.keys():
        # Virtualitics Explore 2021.2 and above packs dimension info in an array.
        for d in task_response["DimensionInfo"]:
            try:
                if d["Dimension"] == "X":
                    plot.x = d["Column"]
                if d["Dimension"] == "Y":
                    plot.y = d["Column"]
                if d["Dimension"] == "Z":
                    plot.z = d["Column"]
                if d["Dimension"] == "Color":
                    plot.color = d["Column"]
                if d["Dimension"] == "Shape":
                    plot.shape = d["Column"]
                if d["Dimension"] == "Size":
                    plot.size = d["Column"]
                if d["Dimension"] == "Transparency":
                    plot.transparency = d["Column"]
                if d["Dimension"] == "ShowBy":
                    plot.playback = d["Column"]
                if d["Dimension"] == "Playback":
                    plot.playback = d["Column"]
                if d["Dimension"] == "Arrow":
                    plot.arrow = d["Column"]
                if d["Dimension"] == "Halo":
                    plot.halo = d["Column"]
                if d["Dimension"] == "Pulsation":
                    plot.pulsation = d["Column"]
                if d["Dimension"] == "GroupBy":
                    plot.groupby = d["Column"]
            except:
                pass
    else:
        # This the here to support older versions of Virtualitics Explore (< 2021.2 (1.9.0))
        dimensionInfo = task_response
        if "X" in dimensionInfo.keys() and dimensionInfo["X"] is not None:
            try:
                plot.x = dimensionInfo["X"]
            except:
                pass
        if "Y" in dimensionInfo.keys() and dimensionInfo["Y"] is not None:
            try:
                plot.y = dimensionInfo["Y"]
            except:
                pass
        if "Z" in dimensionInfo.keys() and dimensionInfo["Z"] is not None:
            try:
                plot.z = dimensionInfo["Z"]
            except:
                pass
        if "Color" in dimensionInfo.keys() and dimensionInfo["Color"] is not None:
            try:
                plot.color = dimensionInfo["Color"]
            except:
                pass
        if "Size" in dimensionInfo.keys() and dimensionInfo["Size"] is not None:
            try:
                plot.size = dimensionInfo["Size"]
            except:
                pass
        if "Shape" in dimensionInfo.keys() and dimensionInfo["Shape"] is not None:
            try:
                plot.shape = dimensionInfo["Shape"]
            except:
                pass
        if "GroupBy" in dimensionInfo.keys() and dimensionInfo["GroupBy"] is not None:
            try:
                plot.groupby = dimensionInfo["GroupBy"]
            except:
                pass
        if "Playback" in dimensionInfo.keys() and dimensionInfo["Playback"] is not None:
            try:
                plot.playback = dimensionInfo["Playback"]
            except:
                pass
        if "ShowBy" in dimensionInfo.keys() and dimensionInfo["ShowBy"] is not None:
            try:
                plot.playback = dimensionInfo["ShowBy"]
            except:
                pass
        if "Transparency" in dimensionInfo.keys() and dimensionInfo["Transparency"] is not None:
            try:
                plot.transparency = dimensionInfo["Transparency"]
            except:
                pass
        if "Halo" in dimensionInfo.keys() and dimensionInfo["Halo"] is not None:
            try:
                plot.halo = dimensionInfo["Halo"]
            except:
                pass
        if "Pulsation" in dimensionInfo.keys() and dimensionInfo["Pulsation"] is not None:
            try:
                plot.pulsation = dimensionInfo["Pulsation"]
            except:
                pass
        if "Arrow" in dimensionInfo.keys() and dimensionInfo["Arrow"] is not None:
            try:
                plot.arrow = dimensionInfo["Arrow"]
            except:
                pass

    # Plot Settings
    if "PlotSettings" in task_response.keys():
        plotSettings = task_response["PlotSettings"]
    else:
        plotSettings = task_response

    if "XScale" in plotSettings.keys() and plotSettings["XScale"] is not None:
        try:
            plot.x_scale = float(plotSettings["XScale"])
        except:
            pass
    if "YScale" in plotSettings.keys() and plotSettings["YScale"] is not None:
        try:
            plot.y_scale = float(plotSettings["YScale"])
        except:
            pass
    if "ZScale" in plotSettings.keys() and plotSettings["ZScale"] is not None:
        try:
            plot.z_scale = float(plotSettings["ZScale"])
        except:
            pass
    if "SizeScale" in plotSettings.keys() and plotSettings["SizeScale"] is not None:
        try:
            plot.size_scale = float(plotSettings["SizeScale"])
        except:
            pass
    if "TransparencyScale" in plotSettings.keys() and plotSettings["TransparencyScale"] is not None:
        try:
            plot.transparency_scale = float(plotSettings["TransparencyScale"])
        except:
            pass
    if "HaloScale" in plotSettings.keys() and plotSettings["HaloScale"] is not None:
        try:
            plot.halo_scale = float(plotSettings["HaloScale"])
        except:
            pass
    if "ArrowScale" in plotSettings.keys() and plotSettings["ArrowScale"] is not None:
        try:
            plot.arrow_scale = float(plotSettings["ArrowScale"])
        except:
            pass
    if "ColorType" in plotSettings.keys() and plotSettings["ColorType"] is not None:
        try:
            plot.color_type = plotSettings["ColorType"]
        except:
            pass
    if "ColorPaletteID" in plotSettings.keys() and plotSettings["ColorPaletteID"] is not None:
        try:
            plot.color_palette_id = plotSettings["ColorPaletteID"]
        except:
            pass
    if "ColorBins" in plotSettings.keys() and plotSettings["ColorBins"] is not None:
        try:
            plot.color_bins = int(plotSettings["ColorBins"])
        except:
            pass
    if "ColorBinDist" in plotSettings.keys() and plotSettings["ColorBinDist"] is not None:
        try:
            plot.color_bin_dist = plotSettings["ColorBinDist"]
        except:
            pass
    if "ColorInverted" in plotSettings.keys() and plotSettings["ColorInverted"] is not None:
        try:
            plot.color_inverted = plotSettings["ColorInverted"]
        except:
            pass
    if "XNormalization" in plotSettings.keys() and plotSettings["XNormalization"] is not None:
        try:
            plot.x_normalization = plotSettings["XNormalization"]
        except:
            pass
    if "YNormalization" in plotSettings.keys() and plotSettings["YNormalization"] is not None:
        try:
            plot.y_normalization = plotSettings["YNormalization"]
        except:
            pass
    if "ZNormalization" in plotSettings.keys() and plotSettings["ZNormalization"] is not None:
        try:
            plot.z_normalization = plotSettings["ZNormalization"]
        except:
            pass
    if "ColorNormalization" in plotSettings.keys() and plotSettings["ColorNormalization"] is not None:
        try:
            plot.color_normalization = plotSettings["ColorNormalization"]
        except:
            pass
    if "SizeNormalization" in plotSettings.keys() and plotSettings["SizeNormalization"] is not None:
        try:
            plot.size_normalization = plotSettings["SizeNormalization"]
        except:
            pass
    if "TransparencyNormalization" in plotSettings.keys() and plotSettings["TransparencyNormalization"] is not None:
        try:
            plot.transparency_normalization = plotSettings["TransparencyNormalization"]
        except:
            pass
    if "ArrowNormalization" in plotSettings.keys() and plotSettings["ArrowNormalization"] is not None:
        try:
            plot.arrow_normalization = plotSettings["ArrowNormalization"]
        except:
            pass
    if "GlobeStyle" in plotSettings.keys() and plotSettings["GlobeStyle"] is not None:
        try:
            plot.globe_style = plotSettings["GlobeStyle"]
        except:
            pass
    if "LatLongLines" in plotSettings.keys() and plotSettings["LatLongLines"] is not None:
        try:
            plot.lat_long_lines = plotSettings["LatLongLines"]
        except:
            pass
    if "CountryLines" in plotSettings.keys() and plotSettings["CountryLines"] is not None:
        try:
            plot.country_lines = plotSettings["CountryLines"]
        except:
            pass
    if "CountryLabels" in plotSettings.keys() and plotSettings["CountryLabels"] is not None:
        try:
            plot.country_labels = plotSettings["CountryLabels"]
        except:
            pass
    if "MapProvider" in plotSettings.keys() and plotSettings["MapProvider"] is not None:
        try:
            plot.map_provider = plotSettings["MapProvider"]
        except:
            pass
    if "MapStyle" in plotSettings.keys() and plotSettings["MapStyle"] is not None:
        try:
            plot.map_style = plotSettings["MapStyle"]
        except:
            pass
    if "HeatmapEnabled" in plotSettings.keys() and plotSettings["HeatmapEnabled"] is not None:
        try:
            plot.heatmap_enabled = plotSettings["HeatmapEnabled"]
        except:
            pass
    if "HeatmapIntensity" in plotSettings.keys() and plotSettings["HeatmapIntensity"] is not None:
        try:
            plot.heatmap_intesity = float(plotSettings["HeatmapIntensity"])
        except:
            pass
    if "HeatmapRadius" in plotSettings.keys() and plotSettings["HeatmapRadius"] is not None:
        try:
            plot.heatmap_radius = float(plotSettings["HeatmapRadius"])
        except:
            pass
    if "HeatmapRadiusUnit" in plotSettings.keys() and plotSettings["HeatmapRadiusUnit"] is not None:
        try:
            plot.heatmap_radius_unit = plotSettings["HeatmapRadiusUnit"]
        except:
            pass
    if "XBins" in plotSettings.keys() and plotSettings["XBins"] is not None:
        try:
            plot.x_bins = int(plotSettings["XBins"])
        except:
            pass
    if "YBins" in plotSettings.keys() and plotSettings["YBins"] is not None:
        try:
            plot.y_bins = int(plotSettings["YBins"])
        except:
            pass
    if "ZBins" in plotSettings.keys() and plotSettings["ZBins"] is not None:
        try:
            plot.z_bins = int(plotSettings["ZBins"])
        except:
            pass
    if "VolumeBy" in plotSettings.keys() and plotSettings["VolumeBy"] is not None:
        try:
            plot.hist_volume_by = plotSettings["VolumeBy"]
        except:
            pass
    if "SurfaceViewMode" in plotSettings.keys() and plotSettings["SurfaceViewMode"] is not None:
        try:
            plot.show_points = plotSettings["SurfaceViewMode"]
        except:
            pass
    if "ConfidenceLevel" in plotSettings.keys() and plotSettings["ConfidenceLevel"] is not None:
        try:
            plot.confidence = plotSettings["ConfidenceLevel"]
        except:
            pass
    if "TrendLines" in plotSettings.keys() and plotSettings["TrendLines"] is not None:
        try:
            plot.trend_lines = plotSettings["TrendLines"]
        except:
            pass
    if "LinePlotPointMode" in plotSettings.keys() and plotSettings["LinePlotPointMode"] is not None:
        try:
            plot.line_plot_point_mode = plotSettings["LinePlotPointMode"]
        except:
            pass
    if "ScatterPlotPointMode" in plotSettings.keys() and plotSettings["ScatterPlotPointMode"] is not None:
        try:
            plot.scatter_plot_point_mode = plotSettings["ScatterPlotPointMode"]
        except:
            pass
    if "XRangeMin" in plotSettings.keys() and plotSettings["XRangeMin"] is not None:
        try:
            plot.x_range_min = float(plotSettings["XRangeMin"])
        except:
            pass
    if "XRangeMax" in plotSettings.keys() and plotSettings["XRangeMax"] is not None:
        try:
            plot.x_range_max = float(plotSettings["XRangeMax"])
        except:
            pass
    if "XLimitMin" in plotSettings.keys() and plotSettings["XLimitMin"] is not None:
        try:
            plot.x_limit_min = float(plotSettings["XLimitMin"])
        except:
            pass
    if "XLimitMax" in plotSettings.keys() and plotSettings["XLimitMax"] is not None:
        try:
            plot.x_limit_max = float(plotSettings["XLimitMax"])
        except:
            pass
    if "XLimitLink" in plotSettings.keys() and plotSettings["XLimitLink"] is not None:
        try:
            plot.x_limit_link = bool(plotSettings["XLimitLink"].lower() == "true")
        except:
            pass
    if "YRangeMin" in plotSettings.keys() and plotSettings["YRangeMin"] is not None:
        try:
            plot.y_range_min = float(plotSettings["YRangeMin"])
        except:
            pass
    if "YRangeMax" in plotSettings.keys() and plotSettings["YRangeMax"] is not None:
        try:
            plot.y_range_max = float(plotSettings["YRangeMax"])
        except:
            pass
    if "YLimitMin" in plotSettings.keys() and plotSettings["YLimitMin"] is not None:
        try:
            plot.y_limit_min = float(plotSettings["YLimitMin"])
        except:
            pass
    if "YLimitMax" in plotSettings.keys() and plotSettings["YLimitMax"] is not None:
        try:
            plot.y_limit_max = float(plotSettings["YLimitMax"])
        except:
            pass
    if "YLimitLink" in plotSettings.keys() and plotSettings["YLimitLink"] is not None:
        try:
            plot.y_limit_link = bool(plotSettings["YLimitLink"].lower() == "true")
        except:
            pass
    if "ZRangeMin" in plotSettings.keys() and plotSettings["ZRangeMin"] is not None:
        try:
            plot.z_range_min = float(plotSettings["ZRangeMin"])
        except:
            pass
    if "ZRangeMax" in plotSettings.keys() and plotSettings["ZRangeMax"] is not None:
        try:
            plot.z_range_max = float(plotSettings["ZRangeMax"])
        except:
            pass
    if "ZLimitMin" in plotSettings.keys() and plotSettings["ZLimitMin"] is not None:
        try:
            plot.z_limit_min = float(plotSettings["ZLimitMin"])
        except:
            pass
    if "ZLimitMax" in plotSettings.keys() and plotSettings["ZLimitMax"] is not None:
        try:
            plot.z_limit_max = float(plotSettings["ZLimitMax"])
        except:
            pass
    if "ZLimitLink" in plotSettings.keys() and plotSettings["ZLimitLink"] is not None:
        try:
            plot.z_limit_link = bool(plotSettings["ZLimitLink"].lower() == "true")
        except:
            pass
    if "EdgeTransparency" in plotSettings.keys() and plotSettings["EdgeTransparency"] is not None:
        try:
            plot.edge_transparency = float(plotSettings["EdgeTransparency"])
        except:
            pass

    notes_message = ""
    if "Note" in task_response:
        note = task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
        notes_message += "Note: '%s'" % note

    print(notes_message)

    return plot


def _crop_plot(img):
    margin_top = int(img.height * (PLOT_MARGIN_DEFAULT / 2048))
    margin_side = int(img.width * (PLOT_MARGIN_DEFAULT / 2048))
    img_array = np.array(img)
    pixel_first = img_array[0,0]
    pix_match = np.all(img_array == pixel_first, axis=2)
    rows, cols = np.where(pix_match == False)

    #print("Rows: ", rows, "Cols: ", cols) #[DEBUG]

    # Not enough data or variation in pixel color to do an auto-crop. This happens when the plot is outside of camera view and all the pixels in the original image are the same color.
    # Can happen after adding support for custom plot transform values -> [EXPD-1993]
    if (rows is None or cols is None or len(rows) <= 0 or len(cols) <= 0):
        return img; # Return the original image to avoid any errors.

    min_row = max(np.min(rows) - margin_top, 0)
    max_row = min(np.max(rows) + margin_top, img_array.shape[0] - 1)
    min_col = max(np.min(cols) - margin_side, 0)
    max_col = min(np.max(cols) + margin_side, img_array.shape[1] - 1)
    crop = img_array[min_row: max_row,  min_col: max_col]
    return Image.fromarray(crop)


def _export_callback(task_response, payload, figsize):
    """
    Callback handler for export tasks.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from Virtualitics Explore. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: :class:`None`; displays the returned capture.
    """
    if "PayloadType" in task_response.keys():
        if task_response["PayloadType"] == "Image":
            start = task_response["BytesStartIndex"]
            size = task_response["BytesSize"]
            image_bytes = utils.decompress(utils.get_bytes(payload, start, size))
            image = Image.open(BytesIO(image_bytes))
            image = image.convert("RGB")
            if "Autocrop" in task_response and task_response["Autocrop"]:
                image = _crop_plot(image)
            matplotlib.rcParams["figure.figsize"] = figsize
            matplotlib.rcParams["figure.dpi"] = 250

            if "Legend" in task_response.keys() and image.height > 0 and image.width > 0:

                legend_dictionary = json.loads(task_response["Legend"])

                dark_theme = True if "Background" in legend_dictionary and legend_dictionary["Background"].lower() == "dark" else False

                if "Color" in legend_dictionary or "Shape" in legend_dictionary:
                    legend_builder = LegendBuilder(legend_dict=legend_dictionary, dark_theme=dark_theme)
                    legend_image = legend_builder.get_legend_image()

                    # Scale the legend image to match a quarter of the plot image height and preserve aspect ratio
                    scale_ratio = 4
                    if image.height > legend_image.height / scale_ratio:
                        legend_size = (
                            int(image.height / scale_ratio),
                            int(image.height / scale_ratio * legend_image.height / legend_image.width)
                        )

                        legend_image = legend_image.resize(legend_size, Image.LANCZOS)
                        full_image = Image.new(
                            'RGB',
                            (image.width + legend_image.width, image.height),
                            color=legend_builder.bg_color
                        )
                    else:
                        minimum_legend_height = 500
                        legend_size = (
                            minimum_legend_height,
                            int(minimum_legend_height * legend_image.height / legend_image.width)
                        )
                        legend_image = legend_image.resize(legend_size, Image.LANCZOS)
                        largest_image = image if image.height > legend_image.height else legend_image
                        full_image = Image.new(
                            'RGB',
                            (image.width + legend_image.width, largest_image.height),
                            color=legend_builder.bg_color
                        )

                    # Stitch together the image and legend_image arrays and fill in the legend_image with white space
                    full_image.paste(image, (0, 0))
                    full_image.paste(legend_image, (image.width, 50))

                    image = full_image

            plt.imshow(np.asarray(image))
            plt.axis("off")
            if "Path" in task_response.keys():
                image.save(task_response["Path"], quality=100)

    if "Note" in task_response:
        print("Note: '%s'\n" % task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip())

    return None


def _smart_mapping_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for SmartMapping

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array. not used for smart mapping
    :return: if the user opted to return_data, then returns the pd.DataFrame of the ranked features and correlation
    groups.
    """
    if "Note" in task_response:
        print("Note: '%s'\n" % task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip())
    if "ReturnData" in task_response.keys():
        if task_response["ReturnData"]:
            results = task_response["SmartMappingResults"]
            results = pd.DataFrame(results, columns=["SmartMapping Rank", "Feature", "Correlated Group"])
            results["Correlated Group"] = results["Correlated Group"].replace(-1, "None")
            if task_response["Disp"]:
                display(results[:min(5, len(results))])
                return None
            else:
                return results
        else:
            return None
    else:
        return None


def _convert_column_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for Filtering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _filter_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for Filtering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _column_sync_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for ColumnSync tasks

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _clustering_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for Clustering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _ad_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for anomaly detection.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    """
    return _ml_routine_callback(task_response, payload)


def _pca_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for pca detection.

    :param task_response: json object of the task response
    :param payload:  reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _search_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for search.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: if the user opted to return data, then returns the pd.DataFrame of the search result.
    """
    return _ml_routine_callback(task_response, payload)

def _pagerank_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for the pagerank callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _clustering_coefficient_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for the clustering coefficient callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _graph_distance_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for the graph distance callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _structure_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for the clustering coefficient callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)

def _column_stats_callback(task_response, payload):
    """
    Handles the Virtualitics Explore response for the Column Stats callback.
    """
    column_stats = { "FeatureName" : task_response["FeatureName"],
                     "DataType" : task_response["DataType"],
                     "SubType" : task_response["SubType"],
                     "Classification" : task_response["Classification"],
                     "RowCount" : task_response["RowCount"],
                     "UniqueValues" : task_response["UniqueValues"],
                     "MissingValues" : task_response["MissingValues"] }

    if "Mean" in task_response:
        column_stats["Mean"] = task_response["Mean"]
    if "StdDev" in task_response:
        column_stats["StdDev"] = task_response["StdDev"]
    if "Median" in task_response:
        column_stats["Median"] = task_response["Median"]
    if "Min" in task_response:
        column_stats["Min"] = task_response["Min"]
    if "Max" in task_response:
        column_stats["Max"] = task_response["Max"]
    if "Sum" in task_response:
        column_stats["Sum"] = task_response["Sum"]

    return column_stats

def _insights_callback(task_response, payload):
    network_insights_table = []
    standard_insights_table = []

    insight_type = "standard"
    insights_df = None

    if "InsightType" in task_response:
        insight_type = task_response["InsightType"]

    # for network insights
    if insight_type.lower() == "network":
        if "InsightsReport" in task_response:
            for insight in task_response["InsightsReport"]:
                network_insights_table.append([insight["Title"], insight["Story"]])
            # TODO: Aakash, I don't think this works. Is vip.insights() supposed to show anything? It doesn't
            display(HTML(tabulate.tabulate(network_insights_table, headers=["Topic", "Insight"], tablefmt='html')))
            insights_df = pd.DataFrame(network_insights_table)
    elif insight_type.lower() == "standard":
        # for standard insights
        if "NonNetworkInsights" in task_response:
            for insight in task_response["NonNetworkInsights"]:
                standard_insights_table.append([insight["Key Insight"]])

            display(HTML(tabulate.tabulate(standard_insights_table, headers=["Insight"], tablefmt='html')))
            insights_df = pd.DataFrame(standard_insights_table)

    notes_message = ""
    if "Note" in task_response:
        note = task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
        notes_message += "Note: '%s'" % note

    print(notes_message)

    return insights_df

def _explainable_ai_callback(task_response, payload):
    table = []
    if "ExplainableAIReport" in task_response:
        for insight in task_response["ExplainableAIReport"]:
            table.append([insight["Category"], insight["Description"]])
        display(HTML(tabulate.tabulate(table, headers=["Category", "Description"], tablefmt='html')))

    notes_message = ""
    if "Note" in task_response:
        note = task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
        notes_message += "Note: '%s'" % note

    print(notes_message)

    return pd.DataFrame(table)

def _dataset_callback(task_response, payload):
    if "DataSetName" in task_response:
        print("Data set loaded with name: '%s'" % task_response["DataSetName"])
        return task_response["DataSetName"]

    return None

def _network_callback(task_response, payload):
    if "DataSetName" in task_response:
        print("Network data set loaded with name: '%s'" % task_response["DataSetName"])
        return task_response["DataSetName"]

    return None

def _obj_callback(task_response, payload):
    if "ObjectName" in task_response and "ObjectID" in task_response:
        print("OBJ loaded with name: '%s' and id: '%s'" % (task_response["ObjectName"], task_response["ObjectID"]))

        return vip_object.VipObject(name=task_response["ObjectName"], id=task_response["ObjectID"], path=task_response["ObjectPath"])

def _ml_routine_callback(task_response, payload):
    """
    Generic handler for ML routines.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the :class:`pd.DataFrame` of results
    """
    if "Note" in task_response:
        print("Note: '%s'\n" % task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip())
    if "ReturnData" in task_response.keys():
        if task_response["ReturnData"]:
            start = task_response["BytesStartIndex"]
            size = task_response["BytesSize"]
            columns_bytes = utils.get_bytes(payload, start, size)
            columns = {}
            for col in task_response["ColumnInfo"]:
                col_bytes = utils.get_bytes(columns_bytes, col["BytesStartIndex"], col["BytesSize"])
                column = pd.Series(data=utils.deserialize_column(col["ColumnType"], col_bytes),
                                   name=col["ColumnName"])
                column.replace('', np.NaN, inplace=True)  # if value is empty string, convert to NaN
                if col["ColumnType"] == "date":
                    try:
                        column = pd.to_datetime(column)
                    except ValueError:
                        # keep as strings if the column can't be parsed into datetime format
                        pass
                columns[col["ColumnName"]] = column
            components = pd.DataFrame(data=columns)
            return components
        else:
            return None
    else:
        return None


def _get_network_callback(task_response, payload):
    if "NetworkDataFormat" in task_response.keys():
        start = task_response["BytesStartIndex"]
        size = task_response["BytesSize"]
        data_bytes = utils.get_bytes(payload, start, size)
        if task_response["NetworkDataFormat"] == "JSON":
            data = json.loads(utils.decompress(data_bytes).decode())
            g = nx.Graph()
            for node_data in data["Nodes"]:
                g.add_node(node_data["Node ID"], **node_data)
            for edge_data in data["Edges"]:
                g.add_edge(edge_data["Source"], edge_data["Target"], weight=edge_data["Weight"])
            return g
        elif task_response["NetworkDataFormat"] == "Edgelist":
            return _ml_routine_callback(task_response, payload)
    else:
        raise exceptions.VipTaskUnknownExecutionException("Failed to get network data from Virtualitics Explore. ")

def _create_custom_dashboard_callback(task_response, payload):
    # print(task_response)
    if "VipDashboardName" in task_response and "VipDashboardGUID" in task_response:
        name = task_response["VipDashboardName"]
        guid = task_response["VipDashboardGUID"]
        print("Dashboard created with name: '%s' and guid: '%s'" % (name, guid))
        return vip_dashboard.VipDashboard(name, guid)

def _clear_custom_dashboard_callback(task_response, payload):
    if "VipDashboardGUID" in task_response:
        guid = task_response["VipDashboardGUID"]
        print("Dashboard with guid: '%s' has been cleared." % guid)
        return None

def _destroy_custom_dashboard_callback(task_response, payload):
    if "VipDashboardGUID" in task_response:
        guid = task_response["VipDashboardGUID"]
        print("Dashboard with guid: '%s' has been destroyed." % guid)
        return None

def _create_dashboard_tile_callback(task_response, payload):
    if "VipDashboardTileName" in task_response:
        tile_name = task_response["VipDashboardTileName"]
    if "VipDashboardTileGUID" in task_response:
        tile_guid = task_response["VipDashboardTileGUID"]
    if "VipDashboardTileType" in task_response:
        tile_type = task_response["VipDashboardTileType"]

    print("Dashboard tile created with name: '%s' guid: '%s' tile_type: '%s'" % (tile_name, tile_guid, tile_type))

    #TODO: lookup the owning dashboard
    return vip_dashboard.VipDashboardTile(tile_name, tile_guid, None, tile_type)

def _remove_dashboard_tiles_callback(task_response, payload):
    if "VipDashboardTileGUIDs" in task_response:
        tile_guids = task_response["VipDashboardTileGUIDs"]
    if "VipDashboardGUID" in task_response:
        dashboard_guid = task_response["VipDashboardGUID"]

    print("Dashboard tiles with guids: '%s' have been removed from dashboard: '%s'." % (tile_guids, dashboard_guid))

    return None

def _create_annotation_callback(task_response, payload):
    a_type = _extract_annotation_info("AnnotationType", task_response)
    if a_type is not None:
        a_type = a_type.lower()
        if a_type == "dataset":
            a_type = vip_annotation.AnnotationType.DATASET
        elif a_type == "mapping":
            a_type = vip_annotation.AnnotationType.MAPPING
        elif a_type == "point":
            a_type = vip_annotation.AnnotationType.POINT
        elif a_type == "object":
            a_type = vip_annotation.AnnotationType.OBJECT

    pipPosition = _extract_annotation_info("PipPosition", task_response)
    if pipPosition is not None:
        pipPosition = pipPosition.lower()
        if pipPosition == "left":
            pipPosition = vip_annotation.AnnotationPipPosition.LEFT
        elif pipPosition == "right":
            pipPosition = vip_annotation.AnnotationPipPosition.RIGHT

    return vip_annotation.VipAnnotation(
                a_type=a_type,
                name=_extract_annotation_info("AnnotationName", task_response), 
                id=_extract_annotation_info("AnnotationID", task_response), 
                comment=_extract_annotation_info("AnnotationComment", task_response),
                userID=_extract_annotation_info("AnnotationUserID", task_response),
                datasetName=_extract_annotation_info("AnnotationDatasetName", task_response),
                mappingID=_extract_annotation_info("AnnotationMappingID", task_response),
                objectID=_extract_annotation_info("AnnotationObjectID", task_response),
                linkedObjectID=_extract_annotation_info("AnnotationLinkedObjectID", task_response), 
                linkedDatasetName=_extract_annotation_info("AnnotationLinkedDatasetName", task_response),
                linkedMappingID=_extract_annotation_info("AnnotationLinkedMappingID", task_response),
                windowColor=_extract_annotation_info("AnnotationWindowColor", task_response), 
                textColor=_extract_annotation_info("AnnotationTextColor", task_response),
                pipPosition=pipPosition,
                screenPositionX=_extract_annotation_info("AnnotationScreenPositionX", task_response), 
                screenPositionY=_extract_annotation_info("AnnotationScreenPositionY", task_response),
                screenOffsetX=_extract_annotation_info("AnnotationScreenOffsetX", task_response), 
                screenOffsetY=_extract_annotation_info("AnnotationScreenOffsetY", task_response),
                width=_extract_annotation_info("AnnotationWidth", task_response), 
                height=_extract_annotation_info("AnnotationHeight", task_response),
                rowIndex=_extract_annotation_info("AnnotationRowIndex", task_response),
                isAttached=_extract_annotation_info("AnnotationIsAttached", task_response),
                isCollapsed=_extract_annotation_info("AnnotationIsCollapsed", task_response)
            )

def _get_annotations_callback(task_response, payload):
    annotations = []
    if "AnnotationInfo" in task_response:
        for aInfo in task_response["AnnotationInfo"]:
            a_type = _extract_annotation_info("Type", aInfo)
            if a_type is not None:
                a_type = a_type.lower()
                if a_type == "dataset":
                    a_type = vip_annotation.AnnotationType.DATASET
                elif a_type == "mapping":
                    a_type = vip_annotation.AnnotationType.MAPPING
                elif a_type == "point":
                    a_type = vip_annotation.AnnotationType.POINT
                elif a_type == "object":
                    a_type = vip_annotation.AnnotationType.OBJECT

            pipPosition = _extract_annotation_info("PipPosition", aInfo)
            if pipPosition is not None:
                pipPosition = pipPosition.lower()
                if pipPosition == "left":
                    pipPosition = vip_annotation.AnnotationPipPosition.LEFT
                elif pipPosition == "right":
                    pipPosition = vip_annotation.AnnotationPipPosition.RIGHT

            a = vip_annotation.VipAnnotation(
                a_type=a_type,
                name=_extract_annotation_info("Name", aInfo), 
                id=_extract_annotation_info("ID", aInfo), 
                comment=_extract_annotation_info("Comment", aInfo),
                userID=_extract_annotation_info("UserID", aInfo),
                datasetName=_extract_annotation_info("DatasetName", aInfo),
                mappingID=_extract_annotation_info("MappingID", aInfo),
                objectID=_extract_annotation_info("ObjectID", aInfo),
                linkedObjectID=_extract_annotation_info("LinkedObjectID", aInfo), 
                linkedDatasetName=_extract_annotation_info("LinkedDatasetName", aInfo),
                linkedMappingID=_extract_annotation_info("LinkedMappingID", aInfo),
                windowColor=_extract_annotation_info("WindowColor", aInfo), 
                textColor=_extract_annotation_info("TextColor", aInfo),
                pipPosition=pipPosition,
                screenPositionX=_extract_annotation_info("ScreenPositionX", aInfo), 
                screenPositionY=_extract_annotation_info("ScreenPositionY", aInfo),
                screenOffsetX=_extract_annotation_info("ScreenOffsetX", aInfo), 
                screenOffsetY=_extract_annotation_info("ScreenOffsetY", aInfo),
                objectAnchorX=_extract_annotation_info("ObjectAnchorX", aInfo),
                objectAnchorY=_extract_annotation_info("ObjectAnchorY", aInfo),
                objectAnchorZ=_extract_annotation_info("ObjectAnchorZ", aInfo),
                width=_extract_annotation_info("Width", aInfo), 
                height=_extract_annotation_info("Height", aInfo),
                rowIndex=_extract_annotation_info("RowIndex", aInfo),
                isAttached=_extract_annotation_info("IsAttached", aInfo),
                isCollapsed=_extract_annotation_info("IsCollapsed", aInfo)
            )

            annotations.append(a)

    return annotations

def _extract_annotation_info(key, aInfo):
    if key in aInfo:
        return aInfo[key]

    return None

def _get_workflow_callback(task_response, payload):
    if "Workflow" in task_response:
        return json.loads(task_response["Workflow"]);

    return None


def _get_legend_callback(task_response, payload):
    if "Legend" in task_response.keys():
        legend_dict = json.loads(task_response["Legend"])

        if "Color" in legend_dict or "Shape" in legend_dict:
            isDarkTheme = "Background" in legend_dict and legend_dict["Background"].lower() == "dark"
            #print("Is Dark Theme: ", isDarkTheme)

            legend_builder = LegendBuilder(legend_dict, dark_theme=isDarkTheme)
            image = legend_builder.get_legend_image()
            image = image.resize(
                size=(
                    int(image.width/2),
                    int(image.height/2)
                )
            )
            matplotlib.rcParams["figure.dpi"] = 250
            plt.imshow(np.asarray(image))
            plt.axis("off")
            if "Path" in task_response.keys():
                image.save(task_response["Path"], quality=100)

        return legend_dict

    return None


def _get_orientation_callback(task_response, payload):
    if "Transforms" in task_response:
        return task_response["Transforms"]

    return None
