from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
import math

class NormKeyPointsSize(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(frame):
            return

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
        
        newKps = [self.__normalize_kp__(kp, minX, maxX, minY, maxY) for kp in frame.keypoints]
        self.vars[self.cvnode.outputs[0].id] = KPFrame(newKps)
    
    def __normalize_kp__(self, kp : Keypoint2D, minX, maxX, minY, maxY):
        deltaX = maxX - minX
        deltaY = maxY - minY
        if deltaX == 0:
            deltaX = 1
        if deltaY == 0:
            deltaY = 1
        newX = (kp.x - minX) / deltaX
        newY = (kp.y - minY) / deltaY
        return Keypoint2D(x=newX, y=newY, score=kp.score, name=kp.name)