from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import Keypoint2D, KPFrame, Canvas, Annotation
from .utils import calc3PtAngle

class ThreeKPAngle(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        kp1 : Keypoint2D = self.vars[self.cvnode.inputs[0].connection.id]
        kp2 : Keypoint2D = self.vars[self.cvnode.inputs[1].connection.id]
        kp3 : Keypoint2D = self.vars[self.cvnode.inputs[2].connection.id]

        if self.catchNoDetections(kp1, kp2, kp3):
            return
        
        self.vars[self.cvnode.outputs[0].id] = calc3PtAngle(kp1, kp2, kp3)