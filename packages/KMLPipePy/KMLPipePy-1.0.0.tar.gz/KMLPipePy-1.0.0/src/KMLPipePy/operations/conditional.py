from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class Conditional(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.operator = self.cvnode.parameters[0].value

    def execute(self):
        input_value = self.vars[self.cvnode.inputs[0].connection.id]
        input2_value = self.vars[self.cvnode.inputs[1].connection.id]

        if self.catchNoDetections(input_value, input2_value):
            return
        
        self.vars[self.cvnode.outputs[0].id] = eval(f"{input_value}{self.operator}{input2_value}")