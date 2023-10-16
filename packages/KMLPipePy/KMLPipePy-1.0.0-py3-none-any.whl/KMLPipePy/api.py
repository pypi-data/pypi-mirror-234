import requests
import json
from KMLPipePy.base_structs import Project, Version, CVNode, CVParameter, CVVariableConnection, CVVariable, CVPipeline  # assuming base_structs is a Python module containing the definitions

def get_project_version(project_name: str, project_version: int, api_key: str):
    url = f"https://getpipeline-kk2bzka6nq-uc.a.run.app/?projectName={project_name}&version={project_version}&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()  # this will raise an HTTPError if the HTTP request returned an unsuccessful status code

    res_json = response.json()
    p = res_json["project"]
    project = Project(p["id"], p["projectName"], p["owner"], p["versions"])#json.loads(json.dumps(res_json["project"]), object_hook=Project)
    v = res_json["version"]
    inputs = parse_cvvars(v["pipeline"]["inputs"])
    outputs = parse_cvvarcons(v["pipeline"]["outputs"])
    nodes = []
    for node in v["pipeline"]["nodes"]:
        params = parse_params(node["parameters"])
        node_inputs = parse_cvvarcons(node["inputs"])
        node_outputs = parse_cvvars(node["outputs"])
        cvnode = CVNode(node["id"], node["label"], node["operation"], params, node_inputs, node_outputs, node["supportedPlatforms"])
        nodes.append(cvnode)
    pipe = CVPipeline(inputs, outputs, nodes)
    version = Version(v["id"], v["projectID"], v["version"], pipe)#json.loads(json.dumps(res_json["version"]), object_hook=Version)
    # Assuming that Project and Version classes or dataclasses have a way to parse from dict or you just want to keep them as dict
    return (
        project,
        version,
    )

def parse_params(params):
    res = []
    for param in params:
        res.append(CVParameter(param["name"], param["label"], param["dataType"], param["value"]))
    return res

def parse_cvvarcons(inputs):
    res = []
    for input in inputs:
        c = input["connection"]
        connection = CVVariable(c["id"], c["name"], c["dataType"], None)

        res.append(CVVariableConnection(input["id"], connection, input["dataType"]))
    return res

def parse_cvvars(outputs):
    res = []
    for output in outputs:
        res.append(CVVariable(output["id"], output["name"], output["dataType"], None))
    return res

# Note: If Project and Version have some parsing methods, you might need to invoke them to convert res_json["project"] and res_json["version"] to respective types.