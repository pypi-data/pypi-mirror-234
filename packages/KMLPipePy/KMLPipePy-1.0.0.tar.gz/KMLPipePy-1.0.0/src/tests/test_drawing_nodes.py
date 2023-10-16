import unittest
from KMLPipePy.operations.pose2D import Pose2D
from KMLPipePy.operations.drawKeyPoints import DrawKeyPoints
from KMLPipePy.operations.smoothKeyPoints import SmoothKeyPoints
from KMLPipePy.operations.calcKeyPointVelocities import CalcKeyPointVelocities
from KMLPipePy.base_structs import CVNode, CVVariable, CVVariableConnection, CVParameter
from KMLPipePy.types import Canvas
import cv2
import time

# python -m unittest

class TestModelNodes(unittest.TestCase):
    DO_TEST = False

    def __construct_node__(self, node, inputs : list, num_outputs : int, parameters : list):
        cv_node = CVNode(
            parameters = [
                CVParameter(name=None, label=None, dataType=None, value=x) for x in parameters
            ],
            inputs = [
                CVVariableConnection(connection=CVVariable(id = "input-" + str(x),
                                    name=None, dataType=None, value=None),
                                    id=None, dataType=None) for x in range(len(inputs))],
            outputs = [CVVariable(id = "output-" + str(x), name=None, value=None, dataType=None)
                       for x in range(num_outputs)],
            id=None, label=None, operation=None, platforms=None)
            
        vars = {}
        for i, input in enumerate(inputs):
            vars["input-" + str(i)] = input
        for i in range(num_outputs):
            vars["output-" + str(i)] = None

        res = node(cv_node, vars)
        res.initialize()

        return res

    def test_pose2d(self):
        if not self.DO_TEST:
            return
        
        out = Canvas(None)
        node1 = self.__construct_node__(Pose2D, [None], 1, [])
        node2 = self.__construct_node__(DrawKeyPoints, [None, None, out], 0, [10])
        node3 = self.__construct_node__(SmoothKeyPoints, [None], 1, [5])
        node4 = self.__construct_node__(CalcKeyPointVelocities, [None], 1, [])

        # Set the frame rate to unlimited
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FPS, -1)

        while True:
            result, image = cam.read()
            if image is not None and image.any():
                node1.vars["input-0"] = image

                start_time = time.time()

                node1.execute()
                res = node1.vars["output-0"]

                node3.vars["input-0"] = res
                node3.execute()
                res = node3.vars["output-0"]

                node4.vars["input-0"] = res
                node4.execute()

                node2.vars["input-0"] = res
                node2.vars["input-1"] = image
                node2.execute()

                end_time = time.time()

                if out.show(1): # exit w/ esc
                    break

                curr = time.time()
                delta = end_time - start_time
                prevTime = curr
                if delta == 0:
                    print(delta)
                else:
                    print(f"{round(1 / delta)} fps -- Nose speed: {node4.vars['output-0'][0] if node4.vars['output-0'] else 'TBD'}")
                
            else:
                print("invalid frame")
        
        out.close()