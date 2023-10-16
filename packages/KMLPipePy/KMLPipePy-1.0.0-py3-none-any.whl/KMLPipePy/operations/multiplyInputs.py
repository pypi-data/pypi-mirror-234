from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class MultiplyInputs(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        input_value = self.vars[self.cvnode.inputs[0].connection.id]
        input2_value = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(input_value, input2_value):
            return
        
        self.vars[self.cvnode.outputs[0].id] = input_value * float(input2_value)