from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
import math

class NormKeyPoints(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(frame):
            return

        newKps = [self.__normalize_kp_l2__(kp) for kp in frame.keypoints]

        self.vars[self.cvnode.outputs[0].id] = KPFrame(newKps)
    
    def __normalize_kp_l2__(self, kp : Keypoint2D):
        length = math.sqrt(kp.x ** 2 + kp.y ** 2)
        if length == 0:
            return Keypoint2D(0, 0, score=kp.score, name=kp.name)
        return Keypoint2D(kp.x / length, kp.y / length, score=kp.score, name=kp.name)