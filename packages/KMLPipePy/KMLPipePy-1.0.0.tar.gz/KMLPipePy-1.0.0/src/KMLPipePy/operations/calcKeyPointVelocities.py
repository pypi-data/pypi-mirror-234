from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D
from time import time
from .utils import calcKPDist

class CalcKeyPointVelocities(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.last : KPFrame = None
        self.lastTime : int = None

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]

        prevFrame = self.last
        prevTime = self.lastTime
        self.last = frame
        self.lastTime = time()

        if self.catchNoDetections(frame) or prevFrame == None:
            return
        
        out = []

        dt = time() - prevTime
        for i, kp in enumerate(frame.keypoints):
            delta = calcKPDist(kp, prevFrame.keypoints[i])
            out.append(delta / dt)

        self.vars[self.cvnode.outputs[0].id] = out