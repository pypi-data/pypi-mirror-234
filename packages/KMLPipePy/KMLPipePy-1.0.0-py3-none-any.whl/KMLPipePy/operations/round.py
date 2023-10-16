from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class Round(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        input_value = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(input_value):
            return

        self.vars[self.cvnode.outputs[0].id] = round(input_value, 0)