from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import BBox, Classification
from KMLPipePy.operations.utils import imageToBase64
import requests
import json

from roboflow import Roboflow

class RoboflowEmbedImages(CVNodeProcess):
    api_key = ""

    def initialize(self):
        """
        Initialization code
        :return:
        """
        self.api_key = self.cvnode.parameters[0].value

    def execute(self):
        images = self.vars[self.cvnode.inputs[0].connection.id]
        image_strs = [imageToBase64(image) for image in images]
        payload = {"image": [{"type": "base64", "value": image_str} for image_str in image_strs]}
        if len(image_strs) > 0:
            response = requests.post(
                url=f'https://infer.roboflow.com/clip/embed_image',
                params={'api_key': self.api_key},
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )

        # Check the response status code to determine if the request was successful
        if len(image_strs) > 0 and response.status_code == 200:
            self.vars[self.cvnode.outputs[0].id] = response.json()['embeddings']
        else:
            #print(f'Error: {response.status_code}')  # Print the error status code
            self.vars[self.cvnode.outputs[0].id] = []
        
        