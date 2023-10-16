from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class SmoothVecs(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.bufferSize = self.cvnode.parameters[0].value
        self.buffer = []
        self.index = 0
        self.runningTotal = []        
        
    def execute(self):
        vec = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(vec):
            return
        
        # running tally: add new vector and remove one at end of buffer
        if len(self.runningTotal) == 0:
            self.runningTotal = [x for x in vec]
            self.buffer.append(vec)
            self.index = 0
            self.vars[self.cvnode.outputs[0].id] = self.runningTotal
            return

        self.index = (self.index + 1) % self.bufferSize
        if len(self.buffer) == self.bufferSize:
            removed = self.buffer[self.index]
            self.runningTotal = [x - removed[i] for i, x in enumerate(self.runningTotal)]
            self.buffer[self.index] = vec
        else:
            self.buffer.append(vec)
        self.runningTotal = [x + vec[i] for i, x in enumerate(self.runningTotal)]
        self.vars[self.cvnode.outputs[0].id] = [x / len(self.buffer) for x in self.runningTotal]