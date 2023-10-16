from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
from numpy import ndarray

class Crop(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        cropVec : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]
        image : ndarray = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(cropVec, image):
            return
    
        height = len(image)
        width = len(image[0])

        y_start = int(cropVec[0] * height)
        x_start = int(cropVec[1] * width)
        y_end = int(cropVec[2] * height)
        x_end = int(cropVec[3] * width)

        self.vars[self.cvnode.outputs[0].id] = image[y_start : y_end, x_start : x_end]