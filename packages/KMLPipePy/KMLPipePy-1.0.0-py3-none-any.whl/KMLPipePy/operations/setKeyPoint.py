from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D

class SetKeyPoint(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.index : int = self.cvnode.parameters[0].value

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]
        kp : Keypoint2D = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(frame, kp):
            return

        newFrame = KPFrame(keypoints=[x if i != self.index else kp for i, x in enumerate(frame.keypoints)])

        self.vars[self.cvnode.outputs[0].id] = newFrame