from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType

class Clamp(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.min = self.cvnode.parameters[0].value
        self.max = self.cvnode.parameters[1].value

    def execute(self):
        input_value = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(input_value):
            return
        
        self.vars[self.cvnode.outputs[0].id] = max(self.min, min(self.max, input_value))