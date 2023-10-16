import unittest
from KMLPipePy.operations.getVecValue import GetVecValue
from KMLPipePy.operations.setVecValue import SetVecValue
from KMLPipePy.operations.smoothVecs import SmoothVecs
from KMLPipePy.base_structs import CVNode, CVVariable, CVVariableConnection, CVParameter

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

        return res

    def test_get_vec_value(self):
        node = self.__construct_node__(GetVecValue, [[5, 3, 10], 1], 1, [])
        node.execute()
        self.assertEqual(node.vars["output-0"], 3)

    def test_set_vec_value(self):
        node = self.__construct_node__(SetVecValue, [[5, 3, 10], "a"], 1, [2])
        node.execute()
        self.assertEqual(node.vars["output-0"], [5, 3, "a"])

    def test_smooth_vecs(self):
        node = self.__construct_node__(SmoothVecs, [[1, 1, 1]], 1, [5])
        node.execute()
        self.assertEqual(node.vars["output-0"], [1, 1, 1])
        node.vars["input-0"] = [0, 0, 1]
        node.execute()
        self.assertEqual(node.vars["output-0"], [0.5, 0.5, 1])
        node.execute()
        self.assertEqual(node.vars["output-0"], [1.0 / 3, 1.0 / 3, 1])
        node.execute()
        self.assertEqual(node.vars["output-0"], [0.25, 0.25, 1]) 
        node.execute()
        self.assertEqual(node.vars["output-0"], [0.2, 0.2, 1]) 
        node.execute()
        self.assertEqual(node.vars["output-0"], [0, 0, 1]) 