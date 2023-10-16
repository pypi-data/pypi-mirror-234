from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import Label
from KMLPipePy.base_structs import DataType
from .utils import calc3PtAngle

class CalcJointAngles(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        input = self.vars[self.cvnode.inputs[0].connection.id];
        if self.catchNoDetections(input):
            return
        pts = input.keypoints
        """
        left elbow
        right elbow
        left shoulder
        right shoulder
        left hip outer
        right hip outer
        left hip inner
        right hip inner
        left knee
        right knee
        left thigh
        right thigh
        """
        angles = [
            calc3PtAngle(pts[5], pts[7], pts[9]), # left elbow
            calc3PtAngle(pts[6], pts[8], pts[10]), # right elbow
            calc3PtAngle(pts[11], pts[5], pts[7]), # left shoulder
            calc3PtAngle(pts[12], pts[6], pts[8]), # right shoulder
            calc3PtAngle(pts[5], pts[11], pts[13]), # left hip outer
            calc3PtAngle(pts[6], pts[12], pts[14]), # right hip outer
            calc3PtAngle(pts[5], pts[11], pts[12]), # left hip inner
            calc3PtAngle(pts[6], pts[12], pts[11]), # right hip inner
            calc3PtAngle(pts[11], pts[13], pts[15]), # left knee
            calc3PtAngle(pts[12], pts[14], pts[16]), # right knee
            calc3PtAngle(pts[13], pts[11], pts[12]), # left thigh
            calc3PtAngle(pts[14], pts[12], pts[11]), # right thigh
        ]
        labels = [
            Label(pts[7].x, pts[7].y, str(round(angles[0]))),
            Label(pts[8].x, pts[8].y, str(round(angles[1]))),
            Label(pts[5].x, pts[5].y, str(round(angles[2]))),
            Label(pts[6].x, pts[6].y, str(round(angles[3]))),
            Label(pts[11].x, pts[11].y, str(round(angles[4]))),
            Label(pts[12].x, pts[12].y, str(round(angles[5]))),
            Label(pts[11].x, pts[11].y, str(round(angles[6]))),
            Label(pts[12].x, pts[12].y, str(round(angles[7]))),
            Label(pts[13].x, pts[13].y, str(round(angles[8]))),
            Label(pts[14].x, pts[14].y, str(round(angles[9]))),
            Label(pts[11].x, pts[11].y, str(round(angles[10]))),
            Label(pts[12].x, pts[12].y, str(round(angles[11]))),
        ]
        self.vars[self.cvnode.outputs[0].id] = angles
        self.vars[self.cvnode.outputs[1].id] = labels
