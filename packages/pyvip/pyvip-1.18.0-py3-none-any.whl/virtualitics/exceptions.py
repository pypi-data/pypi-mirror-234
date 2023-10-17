class AuthenticationException(Exception):
    """
    Used to catch any issues in authenticating the API session with Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class VersionMismatchException(Exception):
    """
    Used to catch any issues with mismatched versions between the API and Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class EncodeCompressException(Exception):
    """
    Used to catch any issues in byte encoding and compressing the data before
    data transmission.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class EncryptionException(Exception):
    """
    Used to catch any issues in encrypting the byte array before data
    transmission
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class VipTaskExecutionException(Exception):
    """
    Denotes issues in the execution of Virtualitics Explore Tasks when processing an API request
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class VipTaskUnknownExecutionException(Exception):
    """
    Denotes issue in the execution of Virtualitics Explore Tasks when the reason is not known.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class SerializationException(Exception):
    """
    Denotes issue in the serialization of data to be transmitted to Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidPlotTypeException(Exception):
    """
    Denotes issue in the specified plot type for Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidTargetException(Exception):
    """
    Denotes issue with target not being in dataframe or part of features
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidFeatureException(Exception):
    """
    Denotes issue with feature not being in dataframe
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class LoadDataFirstException(Exception):
    """
    Dataframe needs to be loaded in before operation can occur
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidInputTypeException(Exception):
    """
    Invalid function input
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class DeserializationException(Exception):
    """
    Denotes an issue occurred while trying to deserialize the column data returned from Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidColorTypeException(Exception):
    """
    Denotes an issue occurred while trying to deserialize the column data returned from Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidResultTypeException(Exception):
    """
    Denotes an issue occurred while trying to deserialize the column data returned from Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidPlotHistoryIndexException(Exception):
    """
    Denotes an issue occurred while trying to deserialize the column data returned from Virtualitics Explore.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class MultipleObjectsToReturnException(Exception):
    """
    Denotes an issue with having more than one object to return to caller. This should never occur if the Python
    library is written correctly.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidScalingValueException(Exception):
    """
    Denotes an issue with with a scaling value. Scaling values must be floats between .4 and 2.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidNormalizationValueException(Exception):
    """
    Denotes an issue with with a normalization value. Valid values are "Log10", "IHST", and "Softmax"
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidColumnTypeException(Exception):
    """
    Denotes an issue with with a normalization value. Valid values are "Categorical" and "Continuous"
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidSavePathException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class ProjectAlreadyExistsException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidEllipsoidPlotException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidShowPointsException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidConfidenceException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class NothingToPlotException(Exception):
    """
    Denotes the requested path is not valid.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class InvalidUsageException(Exception):
    """
    Function is not being used appropriately.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class ResponseFormatException(Exception):
    """
    Response from API request could not be parsed properly.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter


class VipTaskRetryLimitExceededException(Exception):
    """
    Denotes issue in the connection between WebSocket client and server.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return self.parameter
