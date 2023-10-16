import unittest
from KMLPipePy.operations.addInputs import AddInputs
from KMLPipePy.operations.divideInputs import DivideInputs
from KMLPipePy.operations.multiplyInputs import MultiplyInputs
from KMLPipePy.operations.subtractInputs import SubtractInputs
from KMLPipePy.operations.constant import Constant
from KMLPipePy.operations.round import Round
from KMLPipePy.operations.clamp import Clamp
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
        res.execute()

        return res

    def test_add_node(self):
        node = self.__construct_node__(AddInputs, [3, 5], 1, [])
        self.assertEqual(node.vars["output-0"], 8)

        node = self.__construct_node__(AddInputs, [10, -4], 1, [])
        self.assertEqual(node.vars["output-0"], 6)
    
    def test_divide_node(self):
        node = self.__construct_node__(DivideInputs, [10, 3], 1, [])
        self.assertEqual(node.vars["output-0"], 10 / 3.0)
        
        node = self.__construct_node__(DivideInputs, [10, 2], 1, [])
        self.assertEqual(node.vars["output-0"], 5)
    
    def test_multiply_node(self):
        node = self.__construct_node__(MultiplyInputs, [10, 3], 1, [])
        node.execute()
        self.assertEqual(node.vars["output-0"], 30)
        
        node = self.__construct_node__(MultiplyInputs, [10, 0.5], 1, [])
        self.assertEqual(node.vars["output-0"], 5)
    
    def test_subtract_node(self):
        node = self.__construct_node__(SubtractInputs, [50, 7], 1, [])
        self.assertEqual(node.vars["output-0"], 43)
        
    def test_constant_node(self):
        node = self.__construct_node__(Constant, [], 1, [5])
        self.assertEqual(node.vars["output-0"], 5)

    def test_round_node(self):
        node = self.__construct_node__(Round, [5.4], 1, [])
        self.assertEqual(node.vars["output-0"], 5)

        node = self.__construct_node__(Round, [5.6], 1, [])
        self.assertEqual(node.vars["output-0"], 6)
    
    def test_clamp_node(self):
        node = self.__construct_node__(Clamp, [50], 1, [0, 100])
        self.assertEqual(node.vars["output-0"], 50)

        node = self.__construct_node__(Clamp, [-50], 1, [0, 100])
        self.assertEqual(node.vars["output-0"], 0)

        node = self.__construct_node__(Clamp, [150], 1, [0, 100])
        self.assertEqual(node.vars["output-0"], 100)