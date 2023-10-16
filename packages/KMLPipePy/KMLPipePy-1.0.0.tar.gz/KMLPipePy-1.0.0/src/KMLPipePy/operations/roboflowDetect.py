from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import BBox

from roboflow import Roboflow
import cv2
import base64

class RoboflowDetect(CVNodeProcess):

    def initialize(self):
        """
        Initialization code
        :return:
        """
        model_name = self.cvnode.parameters[0].value
        version = self.cvnode.parameters[1].value
        api_key = self.cvnode.parameters[5].value
        self.confidence_threshhold = self.cvnode.parameters[3].value
        self.overlap_threshhold = self.cvnode.parameters[4].value

        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project(model_name)
        self.model = project.version(version).model

    def execute(self):
        image = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(image):
            return

        out = self.model.predict(image).json()
        out = [BBox(pred["x"], pred["y"], pred["width"], pred["height"],
                    (0, 0, 0), pred["class"], pred["confidence"])
                for pred in out["predictions"]]

        self.vars[self.cvnode.outputs[0].id] = out