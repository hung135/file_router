import os
import re
import json
import inspect
import requests
from utils.customexceptions import InvalidAPIVersion

def recurse_replace_yaml(p_trg_data, p_base_dict:dict):
    def inject_yaml_data(str_data, yaml:dict):

        dict_keys = yaml.keys()
        # print('before ', str_data)
        for key in dict_keys:
            if isinstance(yaml[key], dict):
                str_data=recurse_replace_yaml(str_data,yaml[key])
            elif not (isinstance(yaml[key], list) or isinstance(yaml[key], dict)):
                str_data = str_data.replace("{{" + key + "}}", str(yaml[key]))
        # print('after ', str_data)
        return str_data

    assert isinstance(p_base_dict, dict), "2nd parameter has to be TYPE dict: {}".format(type(p_base_dict))
    if isinstance(p_trg_data, list):
        new_list = []
        for trg_item in p_trg_data:
            if isinstance(trg_item, str):
                trg_item = inject_yaml_data(trg_item, p_base_dict)
            elif isinstance(trg_item, list) or isinstance(trg_item, dict):
                if isinstance(trg_item, dict):
                    trg_item = recurse_replace_yaml(trg_item, trg_item)
                trg_item = recurse_replace_yaml(trg_item, p_base_dict)
            new_list.append(trg_item)
        p_trg_data = new_list
        # pprint.pprint(p_trg_data)
    elif isinstance(p_trg_data, dict):
        # v_trg_dict = copy.deepcopy(p_trg_dict)
        # pprint.pprint(p_trg_data)
        new_dict = {}
        for trg_key in p_trg_data.keys():
            trg_item = p_trg_data[trg_key]
            if isinstance(trg_item, str):
                trg_item = inject_yaml_data(trg_item, p_base_dict)
            elif isinstance(trg_item, list) or isinstance(trg_item, dict):
                trg_item = recurse_replace_yaml(trg_item, p_base_dict)
            new_dict[trg_key] = trg_item
        p_trg_data = new_dict
    elif isinstance(p_trg_data, str):
        p_trg_data = inject_yaml_data(p_trg_data, p_base_dict)

    return p_trg_data

def traverse_replace_yaml_tree(yaml_data:dict):
    import pprint as pp
    return_dict={}
    for  project in yaml_data.items():
        x,y=project
        item = recurse_replace_yaml(y,y)
        #pp.pprint(item)
        return_dict[x]=item
    #pp.pprint(yaml_data)
    return return_dict

def replace_yaml_with_runtime(yaml : dict, runtime_data : dict):
    item = recurse_replace_yaml(yaml,runtime_data)

def get_logic_function_names():
    """ 
    Retreieves all the classes and function names

    Notes
    -----
    Changed from using pkgutil to only needing inspect since pyinstaller doesn't play well with
    pkgutil. 

    Returns
    -------
    dict
        Class_name: class_method_name
    """
    import logic
    package = logic
    prefix = package.__name__ + "."
    classes_methods = {}
    func_names = list(filter(lambda val: "__" not in val, dir(package)))
    for func in func_names:
        module = __import__(prefix+func, fromlist="dummy")
        for _class in inspect.getmembers(module, inspect.isclass):
            if prefix in _class[1].__module__:
                method_list = [func for func in dir(_class[1]) if callable(getattr(_class[1], func)) and not func.startswith("__")]
                name = re.findall(".\w+", _class[1].__module__)
                classes_methods[func] = method_list
    return classes_methods

def call_api(api, pipeline):
    """ 
    Calls the GoCD API for a given URL/Pipeline

    Notes
    -----
    API headers for GoCD.v > 19 
        headers = {"Content-Type": "application/json", "Accept":"application/vnd.go.cd.v1+json"}

    Parameters
    ----------
    api: str
        API URL
    pipeline: str
        Pipeline that is being targeted

    Returns
    -------
    dict
        Response of the POST call
    """
    version_request = requests.get(api + "/version", headers={"Accept":"application/vnd.go.cd.v1+json"})
    if version_request.status_code != requests.codes.ok:
        raise ConnectionError("Bad version check") 
        
    version = json.loads(version_request)["version"] 
    if version != "17.10.0":
        raise InvalidAPIVersion("We expected a GoCD verison of 17.10.0 but got %s" % (version))

    print("Calling API: %s/%s/schedule \n\t version: %s" % (api, pipeline, version))
    user, passwd = (os.environ["gocd-username"], os.environ["gocd-passwd"])
    headers =  {"Confirm": "true"}
    response = requests.post(
        "%s/%s/schedule" % (api, pipeline),
        auth=(user, passwd),
        headers=headers,
        verify=False
    )

    if response.status_code != requests.codes.ok:
        raise ConnectionError("Bad version check") 

    return response