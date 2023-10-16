from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
from numpy import ndarray

class CreateCrop(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]
        image : ndarray = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(frame, image):
            return
        
        height = len(image)
        width = len(image[0])

        firstKP = frame.keypoints[0]
        minX, maxX = firstKP.x, firstKP.x
        minY, maxY = firstKP.y, firstKP.y
        for kp in frame.keypoints[1:]:
            x = kp.x
            y = kp.y
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y

        minY = minY / height - 0.05
        maxY = maxY / height + 0.05
        minX = minX / width - 0.05
        maxX = maxX / width + 0.05

        self.vars[self.cvnode.outputs[0].id] = [minY, minX, maxY, maxX]