import unittest
from KMLPipePy.operations.conditional import Conditional
from KMLPipePy.operations.switch import Switch
from KMLPipePy.base_structs import CVNode, CVVariable, CVVariableConnection, CVParameter

class TestLogicNodes(unittest.TestCase):
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

    def test_conditional_node(self):
        node = self.__construct_node__(Conditional, [4, 7], 1, ["<"])
        self.assertEqual(node.vars["output-0"], True)

        node = self.__construct_node__(Conditional, [5, 5], 1, [">"])
        self.assertEqual(node.vars["output-0"], False)
    
    
    def test_switch_node(self):
        node = self.__construct_node__(Switch, [True, "a"], 1, [])
        self.assertEqual(node.vars["output-0"], "a")

        node = self.__construct_node__(Switch, [False, "a"], 1, [])
        self.assertNotEqual(node.vars["output-0"], "a")