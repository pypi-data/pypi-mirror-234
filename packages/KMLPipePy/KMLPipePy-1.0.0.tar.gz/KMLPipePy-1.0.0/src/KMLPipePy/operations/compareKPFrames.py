from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
from .utils import calcCosineSimilarity

class CompareKPFrames(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        frame1 : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]
        frame2 : KPFrame = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(frame1, frame2):
            return

        out = []
        for i in range(len(frame1.keypoints)):
            kp1 = frame1.keypoints[i]
            kp2 = frame2.keypoints[i]
            res = calcCosineSimilarity([kp1.x, kp1.y], [kp2.x, kp2.y])
            out.append(res)

        self.vars[self.cvnode.outputs[0].id] = out