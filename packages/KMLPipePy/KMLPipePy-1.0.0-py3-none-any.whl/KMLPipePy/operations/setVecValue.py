from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class SetVecValue(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.index = self.cvnode.parameters[0].value
        
    def execute(self):
        vec = self.vars[self.cvnode.inputs[0].connection.id]
        value = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(vec, value):
            return
        
        vec[self.index] = value
        self.vars[self.cvnode.outputs[0].id] = vec