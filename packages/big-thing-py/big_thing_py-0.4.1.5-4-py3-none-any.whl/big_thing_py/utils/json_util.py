from big_thing_py.common import *
from big_thing_py.utils.log_util import *

import json


def json_string_to_dict(json_string: str) -> Union[str, dict]:
    try:
        if type(json_string) in [str, bytes]:
            return json.loads(json_string)
        else:
            return json_string

    except json.JSONDecodeError as e:
        MXLOG_DEBUG(f'[json_string_to_dict] input string must be json format string... return raw string...', 'red')
        return json_string


def dict_to_json_string(dict_object: Union[dict, list, str], pretty: bool = True, indent: int = 4) -> str:
    try:
        if type(dict_object) == dict:
            if pretty:
                return json.dumps(dict_object, sort_keys=True, indent=indent)
            else:
                return json.dumps(dict_object)
        elif type(dict_object) == list:
            if pretty:
                return '\n'.join([json.dumps(item, sort_keys=True, indent=indent) for item in dict_object])
            else:
                return '\n'.join([json.dumps(item) for item in dict_object])
        else:
            if pretty:
                json.dumps(json.loads(dict_object), sort_keys=True, indent=indent)
            else:
                return str(dict_object)
    except Exception as e:
        MXLOG_DEBUG('[dict_to_json_string] ' + str(e), 'red')
        return False
