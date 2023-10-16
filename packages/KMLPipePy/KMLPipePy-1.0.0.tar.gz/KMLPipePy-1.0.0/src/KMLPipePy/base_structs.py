from dataclasses import dataclass
from enum import Enum
from typing import List, Union
from json import JSONEncoder

class DataType(Enum):
    CVImage = "Image"
    KPFrame = "KPFrame"
    Vec = "Vec"
    Double = "Double"
    NoDetections = "NoDetections"
    String = "String"
    Canvas = "Canvas"
    AnyType = "Any"

class Platform(Enum):
    JS = "JS"
    SWIFT = "Swift"
    PYTHON = "Python"

@dataclass
class CVVariable:
    id: str
    name: str
    dataType: DataType
    value: any

@dataclass
class CVParameter:
    name: str
    label: str
    dataType: DataType
    value: any

@dataclass
class CVVariableConnection:
    id: str
    connection: Union[CVVariable, None]
    dataType: DataType

@dataclass
class CVNode:
    id: str
    label: str
    operation: str
    parameters: List[CVParameter]
    inputs: List[CVVariableConnection]
    outputs: List[CVVariable]
    platforms: List[Platform]

@dataclass
class Project(JSONEncoder):
    id: str
    projectName: str
    owner: str
    versions: List[int]

@dataclass
class CVPipeline:
    inputs: List[CVVariable]
    outputs: List[CVVariableConnection]
    nodes: List[CVNode]

@dataclass
class Version:
    id: str
    projectID: str
    version: int
    pipeline: CVPipeline