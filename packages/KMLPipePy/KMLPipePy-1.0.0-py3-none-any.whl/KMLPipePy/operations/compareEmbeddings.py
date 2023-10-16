from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.base_structs import DataType
from KMLPipePy.types import KPFrame, Keypoint2D, Vector2D
from .utils import calcCosineSimilarity
from typing import List

class CompareKPFrames(CVNodeProcess):
    def initialize(self):
        """
        Initialization code
        :return:
        """

    def execute(self):
        e1 : List[List[float]] = self.vars[self.cvnode.inputs[0].connection.id]
        e2 : List[List[float]] = self.vars[self.cvnode.inputs[1].connection.id]

        out = []
        for x in e1:
            for y in e2:
                out.append(calcCosineSimilarity(x, y))

        self.vars[self.cvnode.outputs[0].id] = out