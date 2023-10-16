from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.types import Keypoint2D, KPFrame

import tensorflow_hub as hub
import tensorflow as tf
import cv2

LABELS = ["nose"," left eye"," right eye"," left ear"," right ear"," left shoulder"," right shoulder"," left elbow"," right elbow"," left wrist"," right wrist"," left hip"," right hip"," left knee"," right knee"," left ankle"," right ankle"]

class Pose2D(CVNodeProcess):

    def initialize(self):
        """
        Initialization code
        :return:
        """
        model = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
        self.movenet = model.signatures["serving_default"]

    def process_image(self, image):
        ### convert cv2 image to correct size tensor
        image = cv2.resize(image, (192, 192))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = tf.convert_to_tensor(image)
        image = tf.expand_dims(image, axis=0)
        image = tf.cast(image, tf.int32)
        return image

    def execute(self):
        image = self.vars[self.cvnode.inputs[0].connection.id]

        if self.catchNoDetections(image):
            return

        width = image.shape[1]
        height = image.shape[0]

        image = self.process_image(image)
        res = self.movenet(image)

        out = KPFrame(keypoints=[Keypoint2D(x = int(p[1].numpy() * width), y = int(p[0].numpy() * height), score = p[2].numpy(), name = LABELS[i])
                for i, p in enumerate(res['output_0'][0][0])])

        self.vars[self.cvnode.outputs[0].id] = out