import unittest
from KMLPipePy.operations.pose2D import Pose2D
from KMLPipePy.base_structs import CVNode, CVVariable, CVVariableConnection, CVParameter
import cv2

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
        image = cv2.imread("./KMLPipePy/test/test_media/testimage.jpeg")
        image = cv2.resize(image, (400, 600))

        node = self.__construct_node__(Pose2D, [image], 1, [])
        node.execute()

        print(node.vars["output-0"])

        for point in node.vars["output-0"].keypoints:
            print(point)
            image = cv2.circle(image, (int(point.x), int(point.y)), radius=0, color=(255, 0, 0), thickness=10)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()