from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import BBox, Classification
from KMLPipePy.operations.utils import imageToBase64
import requests

from roboflow import Roboflow

class RoboflowClassificationAPI(CVNodeProcess):
    api_key = ""
    model_name = ""
    version = ""

    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.model_name = self.cvnode.parameters[0].value
        self.version = self.cvnode.parameters[1].value
        self.api_key = self.cvnode.parameters[2].value
        print(self.model_name, self.version, self.api_key)

    def execute(self):
        images = self.vars[self.cvnode.inputs[0].connection.id]
        image_strs = [imageToBase64(image) for image in images]

        results = []

        for image_str in image_strs:
            response = requests.post(
                url=f'https://detect.roboflow.com/{self.model_name}/{self.version}',
                params={'api_key': self.api_key},
                data=image_str,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            # Check the response status code to determine if the request was successful
            if response.status_code == 200:
                results.append(Classification([pred for pred in response.json()['predictions']]))
            else:
                print(f'Error: {response.status_code}')  # Print the error status code
        
        self.vars[self.cvnode.outputs[0].id] = results