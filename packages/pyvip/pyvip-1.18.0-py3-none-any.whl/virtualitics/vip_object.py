from virtualitics import utils
from virtualitics import exceptions
from virtualitics import api

class VipObject:
    """
    Class to store metadata about a VipObject.
    """

    def __init__(self, name=None, id=None, path=None):
        """
        Constructor for a VipObject instance. See parameter details.

        :param name: :class:`str` specifies the name of the object.
        :param id: :class:`str` specifies the unique identifier provided by Virtualitics Explore.
        :param path: :class:`str` specifies the path from where the object was loaded.
        """

        self.name = name
        self.id = id
        self.path = path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if val is None:
            self._name = None
            return
        if isinstance(val, str):
            self._name = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "name",
                                                        "must be a `str` specifying the name of the VipObject.")

    @name.deleter
    def name(self):
        self.name = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        if val is None:
            self._id = None
            return
        if isinstance(val, str):
            self._id = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "id",
                                                        "must be a `str` specifying the id of the VipObject.")

    @id.deleter
    def id(self):
        self.id = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        if val is None:
            self._path = None
            return
        if isinstance(val, str):
            self._path = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "path",
                                                        "must be a `str` specifying the path of the VipObject.")

    @path.deleter
    def path(self):
        self.path = None