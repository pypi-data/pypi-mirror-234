from KMLPipePy.base_structs import CVNode, DataType
from typing import Dict
from numpy import ndarray

class CVNodeProcess:
    cvnode: CVNode
    vars: Dict[str, any]

    def __init__(self, cvnode: CVNode, vars: Dict[str, any]):
        self.cvnode = cvnode
        self.vars = vars

    def initialize(self):
        """
        Should be overridden
        :return:
        """

    def execute(self):
        """
        Should be overridden
        :return:
        """

    def catchNoDetections(self, *args):
        return any([type(x) != ndarray and x == DataType.NoDetections for x in args])