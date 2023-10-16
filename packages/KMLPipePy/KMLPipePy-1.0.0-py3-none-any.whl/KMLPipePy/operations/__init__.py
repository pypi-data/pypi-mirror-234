from typing import Dict
from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.operations.addInputs import AddInputs
from KMLPipePy.operations.divideInputs import DivideInputs
from KMLPipePy.operations.multiplyInputs import MultiplyInputs
from KMLPipePy.operations.subtractInputs import SubtractInputs
from KMLPipePy.operations.constant import Constant
from KMLPipePy.operations.round import Round
from KMLPipePy.operations.clamp import Clamp
from KMLPipePy.operations.getVecValue import GetVecValue
from KMLPipePy.operations.setVecValue import SetVecValue
from KMLPipePy.operations.compareKPFrames import CompareKPFrames
from KMLPipePy.operations.normKeyPoints import NormKeyPoints
from KMLPipePy.operations.normKeyPointsSize import NormKeyPointsSize
from KMLPipePy.operations.smoothVecs import SmoothVecs
from KMLPipePy.operations.conditional import Conditional
from KMLPipePy.operations.switch import Switch
from KMLPipePy.operations.pose2D import Pose2D
from KMLPipePy.operations.drawKeyPoints import DrawKeyPoints
from KMLPipePy.operations.threeKPAngle import ThreeKPAngle 
from KMLPipePy.operations.createLabel import CreateLabel
from KMLPipePy.operations.drawLabel import DrawLabel
from KMLPipePy.operations.drawLabels import DrawLabels
from KMLPipePy.operations.calcJointAngles import CalcJointAngles
from KMLPipePy.operations.kpDist import KPDist
from KMLPipePy.operations.smoothKeyPoints import SmoothKeyPoints
from KMLPipePy.operations.calcKeyPointVelocities import CalcKeyPointVelocities
from KMLPipePy.operations.createKeyPoint import CreateKeyPoint
from KMLPipePy.operations.deconstructKeyPoint import DeconstructKeyPoint
from KMLPipePy.operations.getKeyPoint import GetKeyPoint
from KMLPipePy.operations.setKeyPoint import SetKeyPoint
from KMLPipePy.operations.createCrop import CreateCrop
from KMLPipePy.operations.crop import Crop
from KMLPipePy.operations.roboflowDetect import RoboflowDetect
from KMLPipePy.operations.drawBBoxFrame import DrawBBoxFrame
from KMLPipePy.operations.cropBBoxes import CropBBoxes
from KMLPipePy.operations.roboflowClassificationAPI import RoboflowClassificationAPI
from KMLPipePy.operations.roboflowEmbedImages import RoboflowEmbedImages
from KMLPipePy.operations.compareEmbeddings import CompareEmbeddings

NodeCatalog: Dict[str,CVNodeProcess] = {
    "AddInputs": AddInputs,
    "DivideInputs": DivideInputs,
    "MultiplyInputs": MultiplyInputs,
    "SubtractInputs": SubtractInputs,
    "Constant": Constant,
    "Round": Round,
    "Clamp": Clamp,
    "GetVecValues": GetVecValue,
    "SetVecValues": SetVecValue,
    "SetVecValues": SmoothVecs,
    "Conditional": Conditional,
    "Switch": Switch,
    "PoseDetection2D": Pose2D,
    "DrawKeyPoints": DrawKeyPoints,
    "ThreeKPAngle": ThreeKPAngle,
    "CreateLabel": CreateLabel,
    "DrawLabel": DrawLabel,
    "DrawLabels": DrawLabels,
    "CalcJointAngles": CalcJointAngles,
    "KPDist": KPDist,
    "SmoothKeyPoints": SmoothKeyPoints,
    "CalcKeyPointVelocities": CalcKeyPointVelocities,
    "CreateKeyPoint": CreateKeyPoint,
    "DeconstructKeyPoint": DeconstructKeyPoint,
    "GetKeyPoint": GetKeyPoint,
    "SetKeyPoint": SetKeyPoint,
    "CompareKPFrames": CompareKPFrames,
    "NormKeyPoints": NormKeyPoints,
    "NormKeyPointsSize": NormKeyPointsSize,
    "CreateCrop": CreateCrop,
    "Crop": Crop,
    "RoboflowDetect": RoboflowDetect,
    "DrawBBoxFrame": DrawBBoxFrame,
    "CropBBoxes": CropBBoxes,
    "RoboflowClassificationAPI": RoboflowClassificationAPI,
    "RoboflowEmbedImages": RoboflowEmbedImages,
    "CompareEmbeddings": CompareEmbeddings,
}