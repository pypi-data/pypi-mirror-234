from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
class Constant(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.value = self.cvnode.parameters[0].value

    def execute(self):
        self.vars[self.cvnode.outputs[0].id] = self.value