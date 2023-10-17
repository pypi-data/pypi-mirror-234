import gzip
from io import BytesIO
import numpy as np
import pandas as pd
from virtualitics import exceptions
import warnings

DATASET_TYPES = ["TABULAR", "NETWORK"]
PLOT_TYPES = ["SCATTER_PLOT", "LINE_PLOT", "VIOLIN_PLOT", "HISTOGRAM", "CONFIDENCE_ELLIPSOID", "CONVEX_HULL", "SURFACE",
              "MAPS2D", "MAPS3D"]
MAP_MODE_ALIASES = ["GLOBE", "FLAT"]
MAPS3D_ALIASES = ["globe", "maps3d", "map3d", "3dmap"]
MAPS2D_ALIASES = ["map", "2dmap", "flatmap", "map2d", "maps2d"]
HISTOGRAM_ALIASES = ["histogram", "hist", "swarm", "bar", "barchart"]
ELLIPSOID_ALIASES = ["ellipsoids", "ellipsoid", "confidence", "conf", "confidence_ellipsoid"]
CONVEX_HULL_ALIASES = ["convex_hull", "convex", "wrapper", "conv"]
VIOLIN_ALIASES = ['violin', 'density', "violin_plot"]
SURFACE_ALIASES = ["surface", "surf", "gradient"]
LINE_ALIASES = ["line", "timeseries", "line_plot"]
SCATTER_ALIASES = ["scatter", "scatter_plot", "none"]
PLOT_TYPE_ALIASES = {}
for name in SCATTER_ALIASES:
    PLOT_TYPE_ALIASES[name] = "SCATTER_PLOT"
for name in LINE_ALIASES:
    PLOT_TYPE_ALIASES[name] = "LINE_PLOT"
for name in VIOLIN_ALIASES:
    PLOT_TYPE_ALIASES[name] = "VIOLIN_PLOT"
for name in CONVEX_HULL_ALIASES:
    PLOT_TYPE_ALIASES[name] = "CONVEX_HULL"
for name in ELLIPSOID_ALIASES:
    PLOT_TYPE_ALIASES[name] = "CONFIDENCE_ELLIPSOID"
for name in HISTOGRAM_ALIASES:
    PLOT_TYPE_ALIASES[name] = "HISTOGRAM"
for name in MAPS2D_ALIASES:
    PLOT_TYPE_ALIASES[name] = "MAPS2D"
for name in MAPS3D_ALIASES:
    PLOT_TYPE_ALIASES[name] = "MAPS3D"
for name in SURFACE_ALIASES:
    PLOT_TYPE_ALIASES[name] = "SURFACE"

NORMALIZATION_OPTIONS = {"softmax": "Softmax", "log10": "Log10", "ihst": "IHST", None: "None", "none": "None",
                         "cdf": "CDF"}
COLOR_GRADIENT_OPTIONS = ["gradient", "Gradient", "grad", "COLOR_GRADIENT"]
COLOR_BIN_OPTIONS = ["Bins", "bins", "bin", "Bin", "COLOR_BIN"]
COLOR_PALETTE_OPTIONS = ["Palette", "palette", "pal", "COLOR_PALETTE"]
COLOR_OPTIONS = {}
for name in COLOR_BIN_OPTIONS:
    COLOR_OPTIONS[name] = "COLOR_BIN"
for name in COLOR_GRADIENT_OPTIONS:
    COLOR_OPTIONS[name] = "COLOR_GRADIENT"
for name in COLOR_PALETTE_OPTIONS:
    COLOR_OPTIONS[name] = "COLOR_PALETTE"
EDGE_WEIGHT_FORMAT = {"similarity": "Similarity", "distance": "Distance"}
EXPORT_VIEWS = {"ortho": "ortho", "front": "front", "right": "right", "top": "top", "perspective": "perspective",
                "side": "right"}
POS_NEG_CHOICES = {"both": 0, "positive": 1, "negative": 2, "plus": 1, "minus": 2, "+-": 0, "+": 1, "-": 2, 0: 0, 1: 1,
                   2: 2, "b": 0, "p": 1, "n": 2, "m": 2}
AND_OR_CHOICES = {"and": True, "or": False, "a": True, "o": False, True: True, False: False, 1: True, 0: False,
                  "true": True, "false": False}
STDEV_CHOICES = {0.5: 0.5, 1: 1, 1.5: 1.5, 2: 2, 2.5: 2.5, 3: 3, 3.5: 3.5, 4: 4, 4.5: 4.5, 5: 5}
COLUMN_TYPE_CHOICES = {"Continuous": "Continuous", "Categorical": "Categorical"}
CONFIDENCE_LEVELS = {99.5: "EChiSquare_0995", 99.0: "EChiSquare_0990", 97.5: "EChiSquare_0975", 95.0: "EChiSquare_0950",
                     90.0: "EChiSquare_0900", 80.0: "EChiSquare_0800", 75.0: "EChiSquare_0750", 70.0: "EChiSquare_0700",
                     50.0: "EChiSquare_0500", 30.0: "EChiSquare_0300", 25.0: "EChiSquare_0250", 20.0: "EChiSquare_0200",
                     10.0: "EChiSquare_0100", 5.0: "EChiSquare_0050", 2.5: "EChiSquare_0025", 1.0: "EChiSquare_0010",
                     .5: "EChiSquare_0005", "EChiSquare_0995": "EChiSquare_0995", "EChiSquare_0990": "EChiSquare_0990",
                     "EChiSquare_0975": "EChiSquare_0975", "EChiSquare_0950": "EChiSquare_0950",
                     "EChiSquare_0900": "EChiSquare_0900", "EChiSquare_0800": "EChiSquare_0800",
                     "EChiSquare_0750": "EChiSquare_0750", "EChiSquare_0700": "EChiSquare_0700",
                     "EChiSquare_0500": "EChiSquare_0500", "EChiSquare_0300": "EChiSquare_0300",
                     "EChiSquare_0250": "EChiSquare_0250", "EChiSquare_0200": "EChiSquare_0200",
                     "EChiSquare_0100": "EChiSquare_0100", "EChiSquare_0050": "EChiSquare_0050",
                     "EChiSquare_0025": "EChiSquare_0025", "EChiSquare_0010": "EChiSquare_0010",
                     "EChiSquare_0005": "EChiSquare_0005"}
SURFACE_VIEW_MODES = {True: "SurfaceAndPoints", "show": "SurfaceAndPoints", False: "SurfaceOnly",
                      "hide": "SurfaceOnly", "SurfaceAndPoints": "SurfaceAndPoints", "SurfaceOnly": "SurfaceOnly"}
#  "outliers": "SurfaceAndOutliers", "nonoutliers": "SurfaceAndNonOutliers"}
VISIBILITY_OPTIONS = {"true": True, "false": False, "show": True, "hide": False, "none": None, True: True, False: False}
# GLOBE_STYLE_OPTIONS = {"natural": 0, "dark": 1, "none": None, "0": 0, "1": 1, 0: 0, 1: 1}
GLOBE_STYLE_OPTIONS = {"natural": 0, "dark": 1, "black ocean": 2, "blackocean": 2, "blue ocean": 3, "blueocean": 3,
                       "gray ocean": 4, "greyocean": 4, "water color": 5, "watercolor": 5, "topographic": 6, "moon": 7,
                       "night": 8, "earthnight": 8, 0: 0, "0": 0, 1: 1, "1": 1, 2: 2, "2": 2, 3: 3, "3": 3, 4: 4,
                       "4": 4, 5: 5, "5": 5, 6: 6, "6": 6, 7: 7, "7": 7, 8: 8, "8": 8}
MAP_PROVIDERS = {"arcgis": 0, "openstreetmap": 1, "stamen": 2, "none": None, "0": 0, "1": 1, "2": 2, 0: 0, 1: 1, 2: 2}
MAP_STYLES = {0: {"topographic": 0, "ocean": 1, "imagery": 2, "gray": 3, "0": 0, "1": 1, "2": 2, "3": 3, 0: 0, 1: 1,
                  2: 2, 3: 3, "default": 0},
              1: {"mapnik": 0, "0": 0, 0: 0, "default": 0},
              2: {"dark": 0, "light": 1, "watercolor": 2, "terrain": 3, "0": 0, "1": 1, "2": 2, 0: 0, 1: 1, 2: 2,
                  "default": 0}}
COLOR_BIN_MODES = {"equal_bins": "EQUAL_BINS", "equal": "EQUAL_BINS", "equal_bin": "EQUAL_BINS",
                   "range_bins": "RANGE_BIN", "range": "RANGE_BIN", "range_bin": "RANGE_BIN"}
VOLUME_BY_MODES = {"bycount": "ByCount", "bysize": "BySize", "bysizesum": "BySizeSum", "count": "ByCount",
                   "avg": "BySize", "average": "BySize", "sum": "BySizeSum", "uniform": "Uniform","none": None}
VIEWBY_MODES = {"color": "ByColor", "groupby": "ByGroupBy"}
POINT_RENDER_MODES = {"shapes": "Shapes", "3d": "Shapes", "default": "Billboards", "2d": "Billboards",
                      "points": "Points", "dots": "Points", "point cloud": "Points", "pointcloud": "Points"}
CAMERA_ANGLE = {"default": "DEFAULT", "top": "TOP", "front": "FRONT", "side": "SIDE", "right": "SIDE"}
CULTURE_FORMATS = {"us": "US", "eu": "EUROPE", "europe": "EUROPE"}
PIVOT_TYPES = {"min": "Min", "max": "Max", "mean": "Mean", "median": "Median",
    "sum": "Sum", "std": "Std", "all": "All"}
HEATMAP_RADIUS_UNITS = {"kilometers": "Kilometers", "km": "Kilometers", "miles": "Miles", "mi": "Miles",
                        "nauticalmiles": "NauticalMiles", "nm": "NauticalMiles"}
STR_COL_DELIMETER = '\x01'
EXPLAINABLE_AI_FUNCTION = {"identificationtree": "IdentificationTree", "relativeedgedensity": "RelativeEdgeDensity",
                           "kolmogorovsmirnov" : "KolmogorovSmirnov"}

def case_insensitive_match(d: dict, val, var_name: str):
    """
    Get case-insensitive match from d to val if it exists. Raises exception if no match found.

    :param d: dictionary including keys to match against
    :param val: value to match against
    :param var_name: name of variable that is being matched; used if exception is raised
    :return: value in d associated with the key that matches val
    """
    if isinstance(val, str):
        val = val.casefold()
    for a in d.keys():
        c = a
        if isinstance(a, str):
            a = a.casefold()
        if a == val:
            return d[c]
    raise_invalid_argument_exception(str(type(val)), var_name, str(list(d.keys())))


def str_escape(s):
    """
    Escapes the input string. If input is NaN, empty string is returned.
    :param s: input string
    :returns escaped_string: escaped string bytes
    """
    tmpVal = s
    if not pd.api.types.is_scalar(tmpVal):
        tmpVal = "[" + ', '.join(tmpVal) + "]"

    try:
        if pd.isna(tmpVal) or (tmpVal is None):
            return b""
        else:
            return str(tmpVal).encode('unicode_escape')
    except:
        raise exceptions.InvalidInputTypeException("Failed to escape value: " + str(s) + " of type "+ str(type(s)))


def str_unescape(s):
    if s == b"":
        return ""
    else:
        return s.decode('unicode_escape')


_v_escaper = np.vectorize(str_escape)
_v_unescaper = np.vectorize(str_unescape)


def get_name(col):
    """
    Based on the type of the object passed (string or pd.Series), gets the column name
    :param col: string or pd.Series
    :return: string of the name of the column
    """
    if isinstance(col, str) and col != "":
        return col.strip()
    elif isinstance(col, pd.core.series.Series):
        return str(col.name).strip()
    else:
        raise exceptions.InvalidInputTypeException("Need to feed in an object that is either a non-empty string or a "
                                                   "Pandas Series with a name.")


def get_bytes(data, start, size):
    return data[start:start + size]


def compress(data):
    """
    Internal function to handle the compression of data before data
    transmission
    :param data: Serialized data. Currently assumes data is a string.
    :returns result: this contains the bytes of the compressed data
    """
    result = BytesIO()
    g = gzip.GzipFile(fileobj=result, mode='wb', compresslevel=6)
    g.write(data)
    g.close()
    return result.getvalue()


def decompress(data):
    """
    Internal function to handle the decompression of data received from
    Virtualitics Explore.
    :param data: compressed bytearray. to be decompressed and deserialized.
    :returns bytes: decompressed bytes.
    """
    data = BytesIO(data)
    return gzip.GzipFile(fileobj=data, mode='rb', compresslevel=6).read()


def serialize_column(data):
    """
    Helper function that calls the appropriate serialization function based
    on the data type of the input data
    :param data: input data
    :returns serialized_bytes: bytes of the serialized column. serialization
        method determined byte input data type.
    """
    #if np.issubdtype(data.dtype, np.number) or np.issubdtype(data.dtype, np.bool_): # Removed to resolve [EXPD-2363]
    if np.issubdtype(data.dtype, np.number):
        return _serialize_numeric_column(data)
    else:
        return _serialize_nonnumeric_column(data)


def _serialize_nonnumeric_column(data):
    """
    Returns the bytearray for non-numeric (string like) columns.
    :param data: ndarray of object (string) data.
    :returns serialized: serialized numeric column data
    """
    if np.issubdtype(data.dtype, np.datetime64):
        data = np.datetime_as_string(data, unit='auto')
        data[data == 'NaT'] = ''
    escaped_string = _v_escaper(data)
    result = compress(STR_COL_DELIMETER.encode('utf-8').join(escaped_string))
    return "string", result, len(result)


def _serialize_numeric_column(data):
    """
    Returns the bytearray for numeric based columns. All float/double type
    columns are casted to np.float64. All int type columns are casted to
    np.int32.
    :param data: np.ndarray containing the column of data
    :returns serialized: serialized numeric column data.
    """
    is_double = data.min() < np.iinfo(np.int32).min or data.max() > np.iinfo(np.int32).max

    if np.issubdtype(data.dtype, np.floating):
        #nan_index = np.isnan(data)
        #if not is_double and np.all(np.isfinite(data) ^ nan_index) and not np.any(np.mod(data[~nan_index], 1)):
        #    data[nan_index] = 0
        #    data = data.astype(np.int32)
        #    data[nan_index] = np.iinfo(np.int32).min
        #else:
        #    is_double = True
        is_double = True
    elif not data.dtype == np.bool_ and not np.issubdtype(data.dtype, np.integer):
        raise exceptions.SerializationException("This function cannot serialize a non-numeric column")

    if is_double:
        result = compress(data.astype(np.float64).tobytes())
        return "double", result, len(result)
    else:
        result = compress(data.astype(np.int32).tobytes())
        return "int", result, len(result)


def deserialize_column(data_type, data_bytes):
    """
    Deserializes the bytes into a np.ndarray of the appropriate data type
    :param data_type: string that contains the data type of the data bytes
    :param data_bytes: bytes containing the actual column data
    :return: np.ndarray of the correct type
    """
    data_bytes = decompress(data_bytes)
    try:
        if data_type == "string" or data_type == "date":
            return _deserialize_string_column(data_bytes)
        elif data_type == "double" or data_type == "empty":
            return _deserialize_double_column(data_bytes)
        elif data_type == "int":
            return _deserialize_int_column(data_bytes)
        else:
            raise exceptions.DeserializationException("The returned column was of an unsupported data type: " +
                                                      data_type)
    except Exception:
        raise exceptions.DeserializationException("There was an error in deserializing the columns returned from Virtualitics Explore.")


def _deserialize_string_column(data):
    """
    Deserializes the bytes into a np.ndarray of dtype=object
    :param data: bytes for the column
    :return: np.ndarray containing the data
    """
    # convert the bytes into a string
    try:
        escaped_string_list = data.decode().split(STR_COL_DELIMETER)
        return escaped_string_list
    except Exception:
        raise exceptions.DeserializationException("There was an error in deserialized the column of strings returned "
                                                  "from Virtualitics Explore. Contact Virtualitics at Support@Virtualitics.com")


def _deserialize_double_column(data):
    """
    Deserializes the bytes into a np.ndarray of dtype=np.float64
    :param data: bytes for the column
    :return: np.ndarray containing the data
    """
    try:
        return np.frombuffer(data, dtype=np.float64)
    except Exception:
        raise exceptions.DeserializationException("There was an error deserializing the column of dtype=np.float64 "
                                                  "returned from Virtualitics Explore. Contact Virtualitics at Support@Virtualitics.com")


def _deserialize_int_column(data):
    """
    Deserializaes the bytes into a np.ndarray of dtype.np.int32
    :param data: bytes for the column
    :return: np.ndarray containing the data
    """
    try:
        array = np.frombuffer(data, dtype=np.int32)

        # Virtualitics Explore uses int.MinValue to represent missing values/deleted values for integer columns. As such, if int.MinValue
        # is detected in the returned column, we convert the dtype of the array to float64 to support np.nan
        min_val = np.iinfo(np.int32).min
        if min_val in array:
            array = np.asarray(array, dtype=np.float64)
            array[array == min_val] = np.nan
        return array
    except Exception:
        raise exceptions.DeserializationException("There was an error deserializing the column of dtype=np.int32 "
                                                  "returned from Virtualitics Explore. Contact Virtualitics at Support@Virtualitics.com")


def get_features(features):
    """
    Returns the list of feature names from the list of features (mix of pd.Series and strings)
    :param features: enumerable of pd.Series and strings
    :return: list of feature names
    """

    # [EXPD-20]
    if isinstance(features, str):
        raise exceptions.InvalidUsageException(f"`{features}` is not a valid list of column names. "
                                                   "See documentation for how to pass input features.")

    try:
        return list(set([get_name(feat) for feat in features]))
    except Exception:
        raise exceptions.InvalidInputTypeException("There was an error fetching the list input features. "
                                                   "See documentation for how to pass input features.")


def raise_scaling_exception(dim: str):
    raise exceptions.InvalidScalingValueException("Invalid scaling value for {} dimension. ".format(dim) +
                                                  "Scaling values must be floats between 0 and 1")


def raise_normalization_exception(dim: str):
    raise exceptions.InvalidNormalizationValueException("Invalid normalization value for {} dimension. ".format(dim) +
                                                        "Valid values are: " + str(NORMALIZATION_OPTIONS))


def raise_invalid_argument_exception(arg_type: str, arg_name: str, valid_values):
    raise exceptions.InvalidInputTypeException("Invalid type ({t}) used for argument: {arg}. Valid argument "
                                               "is: {valid}".format(t=arg_type, arg=arg_name, valid=valid_values))


# noinspection PyPep8Naming,PyPep8Naming
class deprecated:
    def __init__(self, version=None, new_name=None, execute=True):
        """
        A decorator to be used to mark deprecated functions. A warning will be emitted when function is used.
        :param version: Version that last supported function
        :param new_name: Name of new function call that replaces deprecated function
        :param execute: Whether the deprecated function should still execute

        :return: :class:`None`
        """
        self.version = version
        self.new_name = new_name
        self.execute = execute

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # Print warning
            message = "Call to deprecated function {}.".format(f.__name__)
            if self.version is not None:
                message += " Deprecated since version " + self.version + "."
            if self.new_name is not None:
                message += " Please use " + self.new_name + " instead."
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter

            # And also still execute function
            if self.execute:
                return f(*args, **kwargs)

        return wrapped_f
