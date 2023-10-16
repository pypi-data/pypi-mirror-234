from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D

class DeconstructKeyPoint(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        kp : Keypoint2D = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(kp):
            return

        self.vars[self.cvnode.outputs[0].id] = kp.x;
        self.vars[self.cvnode.outputs[1].id] = kp.y;
        self.vars[self.cvnode.outputs[2].id] = kp.score;
        self.vars[self.cvnode.outputs[3].id] = kp.name;
