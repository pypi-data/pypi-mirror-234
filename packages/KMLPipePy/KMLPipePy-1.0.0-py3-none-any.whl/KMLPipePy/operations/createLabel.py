from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import Label

class CreateLabel(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        x : int = self.vars[self.cvnode.inputs[0].connection.id]
        y : int = self.vars[self.cvnode.inputs[1].connection.id]
        name : str = self.vars[self.cvnode.inputs[2].connection.id]

        if self.catchNoDetections(x, y, name):
            return

        self.vars[self.cvnode.outputs[0].id] = Label(x = x, y = y, name = name)