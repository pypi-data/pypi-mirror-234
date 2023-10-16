from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D

class SmoothKeyPoints(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.bufferSize = self.cvnode.parameters[0].value
        
        self.index = 0
        self.runningTotalX = {}
        self.runningTotalY = {}
        self.runningWeights = {}
        self.runningCounts = {}
        self.buffer = []
    
    def generateAverageFrame(self):
        return KPFrame(keypoints=[
            Keypoint2D(x=int(self.runningTotalX[p] / self.runningWeights[p]),
                       y=int(self.runningTotalY[p] / self.runningWeights[p]),
                       score=self.runningWeights[p] / self.runningCounts[p],
                       name=p) for p in self.runningCounts.keys() if self.runningWeights[p] > 0])

    def execute(self):
        frame : KPFrame = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(frame):
            return
        
        # running tally: add new vector and remove one at end of buffer
        if len(self.buffer) == 0:
            for kp in frame.keypoints:
                self.runningTotalX[kp.name] = kp.x * kp.score
                self.runningTotalY[kp.name] = kp.y * kp.score
                self.runningWeights[kp.name] = kp.score
                self.runningCounts[kp.name] = 1
            self.buffer.append(frame)
            self.index = 0
            self.vars[self.cvnode.outputs[0].id] = frame
            return

        self.index = (self.index + 1) % self.bufferSize
        if len(self.buffer) == self.bufferSize:
            removed = self.buffer[self.index]
            
            for kp in removed.keypoints:
                self.runningTotalX[kp.name] -= (kp.x * kp.score)
                self.runningTotalY[kp.name] -= (kp.y * kp.score)
                self.runningWeights[kp.name] -= kp.score
                self.runningCounts[kp.name] -= 1
                if self.runningCounts[kp.name] == 0:
                    self.runningCounts.pop(kp.name)
            self.buffer[self.index] = frame
        else:
            self.buffer.append(frame)

        for kp in frame.keypoints:
            self.runningTotalX[kp.name] = self.runningTotalX.get(kp.name, 0) + (kp.x * kp.score)
            self.runningTotalY[kp.name] = self.runningTotalY.get(kp.name, 0) + (kp.y * kp.score)
            self.runningWeights[kp.name] = self.runningWeights.get(kp.name, 0) + kp.score
            self.runningCounts[kp.name] = self.runningCounts.get(kp.name, 0) + 1

        self.vars[self.cvnode.outputs[0].id] = self.generateAverageFrame()