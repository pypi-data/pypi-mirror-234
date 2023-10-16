from KMLPipePy.base_structs import Project, Version, CVPipeline, CVNode
from KMLPipePy.CVNodeProcess import CVNodeProcess
from KMLPipePy.operations import NodeCatalog
from typing import List, Dict, Union
from KMLPipePy.api import get_project_version


class KMLPipeline:
    projectName: str
    projectVersion: int
    apiKey: str
    project: Project = None
    version: Version = None
    pipeline: CVPipeline = None
    nodes: List[CVNode] = []
    execNodes: Dict[str, CVNodeProcess] = {}
    vars: Dict[str, any] = {}

    def __init__(self, projectName, projectVersion, apiKey):
        self.projectName = projectName
        self.projectVersion = projectVersion
        self.apiKey = apiKey

    def load_config(self, project, version):
        self.project = project
        self.version = version

    def initialize(self):
        # get project and version details from firebase
        if not self.project or not self.version:
            project, version = get_project_version(
                self.projectName, self.projectVersion, self.apiKey
            )
            self.project = project
            self.version = version

        self.pipeline = self.version.pipeline
        self.nodes = self.version.pipeline.nodes

        for node in [n for n in self.pipeline.nodes if n.id not in self.execNodes]:
            new_exec_node = NodeCatalog[node.operation](node, self.vars)
            new_exec_node.initialize()
            self.execNodes[node.id] = new_exec_node

    def execute(self, input_values):
        if len(input_values) != len(self.pipeline.inputs):
            expected = len(self.pipeline.inputs)
            given = len(input_values)
            raise ValueError(f"[Pipeline Execution Error] Incorrect Number of Inputs. Expected: {expected} but got: {given}")

        clear_vars(self.vars)

        for i, value in enumerate(input_values):
            self.vars[self.pipeline.inputs[i].id] = value  # assumed as CVImage

        executed_nodes = []
        ready_nodes = check_ready_nodes(self.nodes, executed_nodes, self.vars)

        if not ready_nodes:
            raise ValueError("No Nodes to Execute")

        while ready_nodes:
            [self.execNodes[node.id].execute() for node in ready_nodes]
            executed_nodes.extend(ready_nodes)
            ready_nodes = check_ready_nodes(self.nodes, executed_nodes, self.vars)

        outputs = [output for output in self.pipeline.outputs]
        for output in outputs:
            output.connection.value = self.vars[output.connection.id]
        return outputs


def clear_vars(vars):
    for key in vars:
        vars[key] = None


def check_ready_nodes(nodes, executed_nodes, vars):
    return [
        node for node in nodes
        if node.id not in [n.id for n in executed_nodes] and
        all([input.connection and input.connection.id in vars and vars[input.connection.id] is not None for input in node.inputs])
    ]