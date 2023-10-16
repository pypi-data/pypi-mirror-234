import unittest
import math
from KMLPipePy.operations.threeKPAngle import ThreeKPAngle 
from KMLPipePy.operations.kpDist import KPDist
from KMLPipePy.operations.smoothKeyPoints import SmoothKeyPoints
from KMLPipePy.operations.createKeyPoint import CreateKeyPoint
from KMLPipePy.operations.deconstructKeyPoint import DeconstructKeyPoint
from KMLPipePy.operations.getKeyPoint import GetKeyPoint
from KMLPipePy.operations.setKeyPoint import SetKeyPoint
from KMLPipePy.operations.compareKPFrames import CompareKPFrames
from KMLPipePy.operations.normKeyPoints import NormKeyPoints
from KMLPipePy.operations.normKeyPointsSize import NormKeyPointsSize
from KMLPipePy.base_structs import CVNode, CVVariable, CVVariableConnection, CVParameter
from KMLPipePy.types import Keypoint2D, KPFrame

class TestMathNodes(unittest.TestCase):
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
        res.execute()

        return res

    def test_3pt_angle(self):
        kp1 = Keypoint2D(x=1, y=1, score=None, name=None)
        kp2 = Keypoint2D(x=0, y=0, score=None, name=None)
        kp3 = Keypoint2D(x=1, y=0, score=None, name=None)
        node = self.__construct_node__(ThreeKPAngle, [kp1, kp2, kp3], 1, [])
        self.assertEqual(node.vars["output-0"], 45)
        
        kp1.x = 0
        node = self.__construct_node__(ThreeKPAngle, [kp1, kp2, kp3], 1, [])
        self.assertEqual(node.vars["output-0"], 90)

        kp1.x = -1
        node = self.__construct_node__(ThreeKPAngle, [kp1, kp2, kp3], 1, [])
        self.assertEqual(node.vars["output-0"], 135)

    def test_kp_dist(self):
        kp1 = Keypoint2D(x=2, y=4, score=None, name=None)
        kp2 = Keypoint2D(x=1, y=3, score=None, name=None)
        node = self.__construct_node__(KPDist, [kp1, kp2], 1, [])
        self.assertEqual(node.vars["output-0"], math.sqrt(2))
    
    def test_smooth_kps(self):
        kp1 = Keypoint2D(x=0, y=0, score=1, name="a")
        kp2 = Keypoint2D(x=1, y=1, score=1, name="b")
        
        kpa = Keypoint2D(x=1, y=1, score=0.5, name="a")
        kpb = Keypoint2D(x=1, y=1, score=0.5, name="b")

        frame1 = KPFrame(keypoints=[kp1, kp2])
        frame2 = KPFrame(keypoints=[kpa, kpb])

        node = self.__construct_node__(SmoothKeyPoints, [frame1], 1, [5])

        node.vars["input-0"] = frame2
        node.execute()
        node.execute()
        node.execute()
        node.execute()
        node.execute()

    def test_create_keypoint(self):
        node = self.__construct_node__(CreateKeyPoint, [1, 2, 0.5, "hi"], 1, [])
        res : Keypoint2D = node.vars["output-0"]

        self.assertEqual(res.x, 1)
        self.assertEqual(res.y, 2)
        self.assertEqual(res.score, 0.5)
        self.assertEqual(res.name, "hi")

    def test_deconstruct_keypoint(self):
        node = self.__construct_node__(DeconstructKeyPoint, [Keypoint2D(1, 2, 0.5, "hi")], 4, [])

        self.assertEqual(node.vars["output-0"], 1)
        self.assertEqual(node.vars["output-1"], 2)
        self.assertEqual(node.vars["output-2"], 0.5)
        self.assertEqual(node.vars["output-3"], "hi")
    
    def test_get_kp(self):
        kp1 = Keypoint2D(1, 2, 0.5, "hi")
        kp2 = Keypoint2D(2, 3, 0.7, "hi there")
        node = self.__construct_node__(GetKeyPoint, [KPFrame(keypoints=[kp1, kp2])], 1, [1])

        self.assertEqual(node.vars["output-0"], kp2)

    def test_set_kp(self):
        kp1 = Keypoint2D(1, 2, 0.5, "hi")
        kp2 = Keypoint2D(2, 3, 0.7, "hi there")
        kp3 = Keypoint2D(3, 4, 0.9, "howdy")
        node = self.__construct_node__(SetKeyPoint, [KPFrame(keypoints=[kp1, kp2]), kp3], 1, [1])

        self.assertEqual(node.vars["output-0"], KPFrame([kp1, kp3]))
    
    def test_compare_kpframes(self):
        # Create two KPFrames
        kp1 = KPFrame(keypoints=[Keypoint2D(1, 2, 0.5, "hi"), Keypoint2D(2, 3, 0.7, "hi there"),
                                 Keypoint2D(1, 2, 0.5, "hi"), Keypoint2D(1, 1, 0.7, "hi there")])
        kp2 = KPFrame(keypoints=[Keypoint2D(2, 3, 0.7, "hi there"), Keypoint2D(3, 4, 0.9, "howdy"),
                                 Keypoint2D(1, 2, 0.7, "hi there"), Keypoint2D(-1, 1, 0.9, "howdy")])

        # Create a CompareKPFrames node and pass in the two KPFrames
        node = self.__construct_node__(CompareKPFrames, [kp1, kp2], 1, [])

        out = node.vars["output-0"]
        self.assertAlmostEqual(out[0], 0.9922, 3)
        self.assertAlmostEqual(out[1], 0.99846, 3)
        self.assertAlmostEqual(out[2], 1, 3)
        self.assertAlmostEqual(out[3], 0, 3)

    def test_norm_kpframe(self):
        frame = KPFrame(keypoints=[Keypoint2D(2, 0, 0.7, "hi there"), Keypoint2D(3, 4, 0.9, "howdy"),
                                 Keypoint2D(0, 0, 0.7, "hi there")])

        # Create a CompareKPFrames node and pass in the two KPFrames
        node = self.__construct_node__(NormKeyPoints, [frame], 1, [])

        out = node.vars["output-0"].keypoints
        self.assertEquals(out[0].x, 1)
        self.assertEquals(out[0].y, 0)
        self.assertEquals(out[1].x, 0.6)
        self.assertEquals(out[1].y, 0.8)
        self.assertEquals(out[2].x, 0)
        self.assertEquals(out[2].y, 0)

    def test_norm_kpframe_size(self):
        frame = KPFrame(keypoints=[Keypoint2D(0, 0, 0.7, "hi there"), Keypoint2D(4, 3, 0.9, "howdy"),
                                 Keypoint2D(2, 4, 0.7, "hi there")])

        # Create a CompareKPFrames node and pass in the two KPFrames
        node = self.__construct_node__(NormKeyPointsSize, [frame], 1, [])

        out = node.vars["output-0"].keypoints
        self.assertEquals(out[0].x, 0)
        self.assertEquals(out[0].y, 0)
        self.assertEquals(out[1].x, 1)
        self.assertEquals(out[1].y, 0.75)
        self.assertEquals(out[2].x, 0.5)
        self.assertEquals(out[2].y, 1)