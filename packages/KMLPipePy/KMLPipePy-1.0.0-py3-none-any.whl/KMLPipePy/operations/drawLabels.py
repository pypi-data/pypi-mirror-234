from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import Label, Canvas
from numpy import ndarray

class DrawLabels(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        labels : list[Label] = self.vars[self.cvnode.inputs[0].connection.id]
        image : ndarray = self.vars[self.cvnode.inputs[1].connection.id]
        canvas : Canvas = self.vars[self.cvnode.inputs[2].connection.id]

        if self.catchNoDetections(labels, image, canvas):
            return

        for label in labels:
            canvas.add_labels([label])