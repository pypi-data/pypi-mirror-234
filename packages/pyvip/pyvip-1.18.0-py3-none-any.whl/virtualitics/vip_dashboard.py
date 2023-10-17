from virtualitics import utils
from virtualitics import exceptions
from virtualitics import api

class VipDashboard:
    """
    The Dashboard class contains the basic metadata for addressing a Virtualitics Explore dashboard by ID/Name.
    """

    def __init__(self, name=None, guid=None):
        """
        Constructor for a VipDashboard instance. See parameter details.

        :param name: :class:`str` specifies a name provided by the user.
        :param guid: :class:`str` specifies a unique identifier provided by Virtualitics Explore.
        """
        self.name = name
        self.guid = guid

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
                                                    "must be a 'str' specifying the desired name of the dashboard.")

    @name.deleter
    def name(self):
        self.name = None

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, val):
        if val is None:
            self._guid = None
            return
        if isinstance(val, str):
            self._guid = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "guid",
                                                    "must be a 'str' specified the specified guid of the dashboard.")

    @guid.deleter
    def guid(self):
        self.guid = None

class VipDashboardTile:
    """
    The Dashboard Tile class contains the information used to define and create a dashboard tile in Virtualitics Explore.
    """

    def __init__(self, name=None, guid=None, dashboard=None, tile_type=None):
        """
        Constructor for a VipDashboardTile instance. See parameter details.
        
        :param name: :class:`str` specifies a name provided by the user.
        :param guid: :class:`str` specifies a unique identifier provided by Virtualitics Explore.
        :param dashboard: :class:`VipDashboard` specifies the VipDashboard instance that owns the tile.
        :param tile_type: :class:`str` specifies the tile type (i.e., Text, Histogram, Pichart, History, etc.)
        """
        self.name = name
        self.guid = guid
        self.dashboard = dashboard
        self.tile_type = tile_type

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
                                                    "must be a 'str' specified the desired name of the dashboard tile.")

    @name.deleter
    def name(self):
        self.name = None

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, val):
        if val is None:
            self._guid = None
            return
        if isinstance(val, str):
            self._guid = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "guid",
                                                    "must be a 'str' specified the specified guid of the dashboard tile.")

    @guid.deleter
    def guid(self):
        self.guid = None

    
    @property
    def tile_type(self):
        return self._tile_type

    @tile_type.setter
    def tile_type(self, val):
        if val is None:
            self._tile_type = None
            return
        if isinstance(val, str):
            self._tile_type = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "tile_type",
                                                    "must be a 'str' specified the tile_type of the dashboard tile.")

    @tile_type.deleter
    def tile_type(self):
        self.tile_type = None

    @property
    def dashboard(self):
        return self._dashboard

    @dashboard.setter
    def dashboard(self, val):
        if val is None:
            self._dashboard = None
            return
        if isinstance(val, VipDashboard):
            self._dashboard = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "dashboard",
                                                    "must be a 'VipDashboard' specified the dashboard owning the dashboard tile.")

    @dashboard.deleter
    def dashboard(self):
        self.dashboard = None