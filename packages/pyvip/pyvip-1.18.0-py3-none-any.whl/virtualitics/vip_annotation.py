from virtualitics import utils
from virtualitics import exceptions
from virtualitics import api
from enum import Enum, unique, auto

class VipAnnotation:
    """
    The VipAnnotation class contains the basic data and metadata for creating and managing an Annotation in Virtualitics Explore.
    """

    def __init__(self, a_type=None, 
                    name=None, 
                    id=None, 
                    comment=None, 
                    userID=None, 
                    datasetName=None, mappingID=None, 
                    objectID=None, 
                    rowIndex=None,
                    linkedObjectID=None, 
                    linkedDatasetName=None, 
                    linkedMappingID=None,
                    windowColor=None, textColor=None,
                    pipPosition=None,
                    screenPositionX=None, screenPositionY=None,
                    screenOffsetX=None, screenOffsetY=None,
                    objectAnchorX=None, objectAnchorY=None, objectAnchorZ=None,
                    width=None, height=None,
                    isAttached=None, isCollapsed=None):
        """
        Constructor for a VipAnnotation instance. See parameter details.

        :param id: :class:`str` specifies a unique identifier provided by Virtualitics Explore.
        :param a_type: :class:`AnnotationType` specifies the type of annotation.
        :param name: :class:`str` The name of the annotation (will be displayed in the header bar of the Annotation UI.)
        :param comment: :class:`str` The main body text of the annotation. 
        :param id: :class:`str` The user-defined id (will be displayed in the pip/badge for the annotation).
        :param datasetName: :class:`str` The name of the dataset the annotation belongs to (if a DATASET, MAPPING, or POINT annotation).
        :param mappingID: :class:`int` The index of the mapping the annotation belongs to (if a MAPPING ANNOTATION).
        :param objectID: :class:`str` The id of the object the annotation belongs to (if an OBJECT annotation).
        :param rowIndex: :class:`int` The rowIndex of the data point the annotation belongs to (if a POINT annotation).
        :param linkedObjectID: :class:`str` The id of the object the annotation link refers to (if linked to an object). 
        :param linkedDatasetName: :class:`str` The name of the dataset the annotation link refers to (if linked to a dataset/mapping).
        :param linkedMappingID: :class:`int` The index of the mapping the annotation link refers to (if linked to a dataset/mapping).
        :param windowColor: :class:`str` The color of the annotation window, represented as an HTML color string (i.e. FF0000 for RED)
        :param textColor: :class:`str` The color of the annotation text, represented as an HTML color string (i.e. FF0000 for RED)
        :param pipPosition: :class:`AnnotationPipPosition` The position that the pip/badge should take with respect to the annotation (LEFT or RIGHT)
        :param screenPositionX: :class:`float` The screen-space X position of the annotation, normalized from 0 (left) to 1 (right).
        :param screenPositionY: :class:`float` The screen-space Y position of the annotation, normalized from 0 (bottom) to 1 (top).
        :param screenOffsetX: :class:`float` The screen-space X offset position of the annotation, normalized from 0 (left) to 1 (right). Used for POINT annotations and attached OBJECT annotations.
        :param screenOffsetY: :class:`float` The screen-space Y offset position of the annotation, normalized from 0 (bottom) to 1 (top). Used for POINT annotations and attached OBJECT annotations.
        :param objectAnchorX: :class:`float` The object-space X position of the object annotation attach point, or anchor.
        :param objectAnchorY: :class:`float` The object-space Y position of the object annotation attach point, or anchor.
        :param objectAnchorZ: :class:`float` The object-space Z position of the object annotation attach point, or anchor.
        :param width: :class:`int` The width, as a ratio of screen width, of the annotation window.
        :param height: :class:`int` The height, as a ratio of screen height, of the annotation window.
        :param isAttached: :class:`bool` The attached/detached state of an annotation (if an OBJECT annotation).
        :param isCollapsed: :class:`bool` The collapsed/expanded state of an annotation.
        """

        self.id = id
        self.name = name
        self.a_type = a_type
        self.comment = comment
        self.userID = userID
        self.datasetName = datasetName
        self.mappingID = mappingID
        self.objectID = objectID
        self.rowIndex = rowIndex
        self.linkedObjectID = linkedObjectID
        self.linkedDatasetName = linkedDatasetName
        self.linkedMappingID = linkedMappingID
        self.windowColor = windowColor
        self.textColor = textColor
        self.pipPosition = pipPosition
        self.screenPositionX = screenPositionX
        self.screenPositionY = screenPositionY
        self.screenOffsetX = screenOffsetX
        self.screenOffsetY = screenOffsetY
        self.objectAnchorX = objectAnchorX
        self.objectAnchorY = objectAnchorY
        self.objectAnchorZ = objectAnchorZ
        self.width = width
        self.height = height
        self.isAttached = isAttached
        self.isCollapsed = isCollapsed


    def to_string(self):
        val = '''\
        ID: {id}\n\
        Type: {a_type}\n\
        Name: {name}\n\
        Comment: {comment}\n\
        User ID: {userID}\n\
        Dataset Name: {datasetName}\n\
        Mapping ID: {mappingID}\n\
        Object ID: {objectID}\n\
        Row Index: {rowIndex}\n\
        Linked Object ID: {linkedObjectID}\n\
        Linked Dataset Name: {linkedDatasetName}\n\
        Linked Mapping ID: {linkedMappingID}\n\
        Window Color: {windowColor}\n\
        Text Color: {textColor}\n\
        Pip Position: {pipPosition}\n\
        Screen Position: ({screenPositionX},{screenPositionY})\n\
        Screen Offset: ({screenOffsetX},{screenOffsetY})\n\
        Object Anchor: ({objectAnchorX},{objectAnchorY},{objectAnchorZ})\n\
        Width/Height: ({width},{height})\n\
        Is Attached: {isAttached}\n\
        Is Collapsed: {isCollapsed}             
        '''.format( id=self.id,
                    a_type=self.a_type,
                    name=self.name,
                    comment=self.comment,
                    userID=self.userID,
                    datasetName=self.datasetName,
                    mappingID=self.mappingID,
                    objectID=self.objectID,
                    rowIndex=self.rowIndex,
                    linkedObjectID=self.linkedObjectID,
                    linkedDatasetName=self.linkedDatasetName,
                    linkedMappingID=self.linkedMappingID,
                    windowColor=self.windowColor,
                    textColor=self.textColor,
                    pipPosition=self.pipPosition,
                    screenPositionX=self.screenPositionX,
                    screenPositionY=self.screenPositionY,
                    screenOffsetX=self.screenOffsetX,
                    screenOffsetY=self.screenOffsetY,
                    objectAnchorX=self.objectAnchorX,
                    objectAnchorY=self.objectAnchorY,
                    objectAnchorZ=self.objectAnchorZ,
                    width=self.width,
                    height=self.height,
                    isAttached=self.isAttached,
                    isCollapsed=self.isCollapsed
                )
            
        return val

    #id
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
                                                    "must be a 'str' specifying the id of the annotation (generated by Virtualitics Explore).")

    @id.deleter
    def id(self):
        self.id = None

    #name
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
                                                    "must be a 'str' specifying the name of the annotation.")

    @name.deleter
    def name(self):
        self.name = None

    #a_type
    @property
    def a_type(self):
        return self._a_type

    @a_type.setter
    def a_type(self, val):
        if val is None:
            self._a_type = None
            return
        if isinstance(val, AnnotationType):
            self._a_type = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "a_type",
                                                    "must be a 'AnnotationType' specifying the a_type of the annotation (as DATASET, MAPPING, POINT, or OBJECT).")

    @a_type.deleter
    def a_type(self):
        self.a_type = None

    #comment
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, val):
        if val is None:
            self._comment = None
            return
        if isinstance(val, str):
            self._comment = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "comment",
                                                    "must be a 'str' specifying the comment of the annotation.")

    @comment.deleter
    def comment(self):
        self.comment = None

    #userID
    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, val):
        if val is None:
            self._userID = None
            return
        if isinstance(val, str):
            self._userID = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "userID",
                                                    "must be a 'str' specifying the userID of the annotation.")

    @userID.deleter
    def userID(self):
        self.userID = None

    #datasetName
    @property
    def datasetName(self):
        return self._datasetName

    @datasetName.setter
    def datasetName(self, val):
        if val is None:
            self._datasetName = None
            return
        if isinstance(val, str):
            self._datasetName = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "datasetName",
                                                    "must be a 'str' specifying the datasetName of the annotation (if a_type is dataset or mapping).")

    @datasetName.deleter
    def datasetName(self):
        self.datasetName = None

    #mappingID
    @property
    def mappingID(self):
        return self._mappingID

    @mappingID.setter
    def mappingID(self, val):
        if val is None:
            self._mappingID = None
            return
        if isinstance(val, int):
            self._mappingID = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "mappingID",
                                                    "must be a 'int' specifying the mappingID of the annotation (if a_type is mapping).")

    @mappingID.deleter
    def mappingID(self):
        self.mappingID = None

    #objectID
    @property
    def objectID(self):
        return self._objectID

    @objectID.setter
    def objectID(self, val):
        if val is None:
            self._objectID = None
            return
        if isinstance(val, str):
            self._objectID = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "objectID",
                                                    "must be a 'str' specifying the objectID of the annotation (if a_type is object).")

    @objectID.deleter
    def objectID(self):
        self.objectID = None

    #rowIndex
    @property
    def rowIndex(self):
        return self._rowIndex

    @rowIndex.setter
    def rowIndex(self, val):
        if val is None:
            self._rowIndex = None
            return
        if isinstance(val, int):
            self._rowIndex = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "rowIndex",
                                                    "must be a 'int' specifying the rowIndex of the annotation (if a_type is point).")

    @rowIndex.deleter
    def rowIndex(self):
        self.rowIndex = None

    #linkedObjectID
    @property
    def linkedObjectID(self):
        return self._linkedObjectID

    @linkedObjectID.setter
    def linkedObjectID(self, val):
        if val is None:
            self._linkedObjectID = None
            return
        if isinstance(val, str):
            self._linkedObjectID = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "linkedObjectID",
                                                    "must be a 'str' specifying the linkedObjectID of the annotation (if the annotation is linked to an object).")

    @linkedObjectID.deleter
    def linkedObjectID(self):
        self.linkedObjectID = None

    #linkedDatasetName
    @property
    def linkedDatasetName(self):
        return self._linkedDatasetName

    @linkedDatasetName.setter
    def linkedDatasetName(self, val):
        if val is None:
            self._linkedDatasetName = None
            return
        if isinstance(val, str):
            self._linkedDatasetName = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "linkedDatasetName",
                                                    "must be a 'str' specifying the linkedDatasetName of the annotation (if the annotation is linked to dataset/mapping).")

    @linkedDatasetName.deleter
    def linkedDatasetName(self):
        self.linkedDatasetName = None

    #linkedMappingID
    @property
    def linkedMappingID(self):
        return self._linkedMappingID

    @linkedMappingID.setter
    def linkedMappingID(self, val):
        if val is None:
            self._linkedMappingID = None
            return
        if isinstance(val, int):
            self._linkedMappingID = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "linkedMappingID",
                                                    "must be a 'int' specifying the linkedMappingID of the annotation (if the annotation is linked to a dataset/mapping).")

    @linkedMappingID.deleter
    def linkedMappingID(self):
        self.linkedMappingID = None

    #windowColor
    @property
    def windowColor(self):
        return self._windowColor

    @windowColor.setter
    def windowColor(self, val):
        if val is None:
            self._windowColor = None
            return
        if isinstance(val, str):
            self._windowColor = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "windowColor",
                                                    "must be a 'str' specifying the windowColor of the annotation as a HTML hex color string.")

    @windowColor.deleter
    def windowColor(self):
        self.windowColor = None

    #textColor
    @property
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, val):
        if val is None:
            self._textColor = None
            return
        if isinstance(val, str):
            self._textColor = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "textColor",
                                                    "must be a 'str' specifying the textColor of the annotation as a HTML hex color string.")

    @textColor.deleter
    def textColor(self):
        self.textColor = None

    #pipPosition
    @property
    def pipPosition(self):
        return self._pipPosition

    @pipPosition.setter
    def pipPosition(self, val):
        if val is None:
            self._pipPosition = None
            return
        if isinstance(val, AnnotationPipPosition):
            self._pipPosition = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "pipPosition",
                                                    "must be a 'AnnotationPipPosition' specifying the pipPosition of the annotation (as LEFT or RIGHT).")

    @pipPosition.deleter
    def pipPosition(self):
        self.pipPosition = None

    #screenOffsetX
    @property
    def screenOffsetX(self):
        return self._screenOffsetX

    @screenOffsetX.setter
    def screenOffsetX(self, val):
        if val is None:
            self._screenOffsetX = None
            return
        if isinstance(val, float):
            self._screenOffsetX = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "screenOffsetX",
                                                    "must be a 'float' specifying the screenOffsetX of the annotation (value between 0.0 and 1.0 indicating where on the screen the annotation should appear)")

    @screenOffsetX.deleter
    def screenOffsetX(self):
        self.screenOffsetX = None

    #screenOffsetY
    @property
    def screenOffsetY(self):
        return self._screenOffsetY

    @screenOffsetY.setter
    def screenOffsetY(self, val):
        if val is None:
            self._screenOffsetY = None
            return
        if isinstance(val, float):
            self._screenOffsetY = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "screenOffsetY",
                                                    "must be a 'float' specified the specified screenOffsetY of the annotation (value between 0.0 and 1.0 indicating where on the screen the annotation should appear).")

    @screenOffsetY.deleter
    def screenOffsetY(self):
        self.screenOffsetY = None

    #screenPositionX
    @property
    def screenPositionX(self):
        return self._screenPositionX

    @screenPositionX.setter
    def screenPositionX(self, val):
        if val is None:
            self._screenPositionX = None
            return
        if isinstance(val, float):
            self._screenPositionX = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "screenPositionX",
                                                    "must be a 'float' specifying the screenPositionX of the annotation (value between 0.0 and 1.0 indicating where on the screen the annotation should appear)")

    @screenPositionX.deleter
    def screenPositionX(self):
        self.screenPositionX = None

    #screenPositionY
    @property
    def screenPositionY(self):
        return self._screenPositionY

    @screenPositionY.setter
    def screenPositionY(self, val):
        if val is None:
            self._screenPositionY = None
            return
        if isinstance(val, float):
            self._screenPositionY = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "screenPositionY",
                                                    "must be a 'float' specified the specified screenPositionY of the annotation (value between 0.0 and 1.0 indicating where on the screen the annotation should appear).")

    @screenPositionY.deleter
    def screenPositionY(self):
        self.screenPositionY = None

    #objectAnchorX
    @property
    def objectAnchorX(self):
        return self._objectAnchorX

    @objectAnchorX.setter
    def objectAnchorX(self, val):
        if val is None:
            self._objectAnchorX = None
            return
        if isinstance(val, float):
            self._objectAnchorX = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "objectAnchorX",
                                                    "must be a 'float' specified the specified objectAnchorX of the annotation.")

    @objectAnchorX.deleter
    def objectAnchorX(self):
        self.objectAnchorX = None

    #objectAnchorY
    @property
    def objectAnchorY(self):
        return self._objectAnchorY

    @objectAnchorY.setter
    def objectAnchorY(self, val):
        if val is None:
            self._objectAnchorY = None
            return
        if isinstance(val, float):
            self._objectAnchorY = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "objectAnchorY",
                                                    "must be a 'float' specified the specified objectAnchorY of the annotation.")

    @objectAnchorY.deleter
    def objectAnchorY(self):
        self.objectAnchorY = None

    #objectAnchorZ
    @property
    def objectAnchorZ(self):
        return self._objectAnchorZ

    @objectAnchorZ.setter
    def objectAnchorZ(self, val):
        if val is None:
            self._objectAnchorZ = None
            return
        if isinstance(val, float):
            self._objectAnchorZ = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "objectAnchorZ",
                                                    "must be a 'float' specified the specified objectAnchorZ of the annotation.")

    @objectAnchorZ.deleter
    def objectAnchorZ(self):
        self.objectAnchorZ = None

    #width
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        if val is None:
            self._width = None
            return
        if isinstance(val, float) or isinstance(val, int):
            self._width = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "width",
                                                    "must be a 'float' or 'int' specifying the width (as a ratio of screen width) of the annotation.")

    @width.deleter
    def width(self):
        self.width = None

    #height
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        if val is None:
            self._height = None
            return
        if isinstance(val, float) or isinstance(val, int):
            self._height = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "height",
                                                    "must be a 'float' or 'int' specifying height (as a ratio of screen height) of the annotation.")

    @height.deleter
    def height(self):
        self.height = None

    #isAttached
    @property
    def isAttached(self):
        return self._isAttached

    @isAttached.setter
    def isAttached(self, val):
        if val is None:
            self._isAttached = None
            return
        if isinstance(val, bool):
            self._isAttached = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "isAttached",
                                                    "must be a 'bool' specifying whether the annotation is attached or detached (if a_type is object).")

    @isAttached.deleter
    def isAttached(self):
        self.isAttached = None

    #isCollapsed
    @property
    def isCollapsed(self):
        return self._isCollapsed

    @isCollapsed.setter
    def isCollapsed(self, val):
        if val is None:
            self._isCollapsed = None
            return
        if isinstance(val, bool):
            self._isCollapsed = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "isCollapsed",
                                                    "must be a 'bool' specifying whether the annotation is collapsed or not.")

    @isCollapsed.deleter
    def isCollapsed(self):
        self.isCollapsed = None
    
@unique
class AnnotationType(Enum):
    """
    Different types of annotations available in Virtualitics Explore.

    [DATASET, MAPPING, POINT, OBJECT]
    """
    DATASET = auto()
    MAPPING = auto()
    POINT = auto()
    OBJECT = auto()

@unique
class AnnotationPipPosition(Enum):
    """
    Options for pip/badge position.

    [LEFT, RIGHT]
    """
    LEFT = auto()
    RIGHT = auto()