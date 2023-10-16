from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import Keypoint2D, KPFrame, Canvas, Annotation, BBox
from KMLPipePy.base_structs import DataType
from numpy import ndarray

class DrawBBoxFrame (CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        bboxes : list[BBox] = self.vars[self.cvnode.inputs[0].connection.id]
        canvas : Canvas = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(bboxes, canvas):
            return

        canvas.add_bboxes(bboxes)