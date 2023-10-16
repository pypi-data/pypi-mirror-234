from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D, BBox
from numpy import ndarray
import cv2

class CropBBoxes(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.crop_size = self.cvnode.parameters[0].value // 2

    def execute(self):
        boxes : list[BBox] = self.vars[self.cvnode.inputs[0].connection.id]
        image : ndarray = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(boxes, image):
            return

        out = []
        for box in boxes:
            x_start = int(box.x - self.crop_size)
            x_end = int(box.x + self.crop_size)
            y_start = int(box.y - self.crop_size)
            y_end = int(box.y + self.crop_size)
            out.append(image[y_start : y_end, x_start : x_end])
        self.vars[self.cvnode.outputs[0].id] = out