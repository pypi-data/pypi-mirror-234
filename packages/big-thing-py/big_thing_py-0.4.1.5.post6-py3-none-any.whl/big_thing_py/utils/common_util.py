from big_thing_py.common import *

import inspect
import socket
import json
import time
import platform
import os
import copy
import random
from pathlib import Path
import getmac
import re
import sys
import typing


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def get_type_name(typ: typing.Type) -> str:
    origin = typing.get_origin(typ)
    if origin is None:
        return typ.__name__
    args = typing.get_args(typ)
    args_str = ", ".join(get_type_name(arg) for arg in args)
    return f"{origin.__name__}[{args_str}]"


def get_function_info(func: Callable) -> Dict[str, Union[str, List[Tuple[str, Any]]]]:
    sig = inspect.signature(func)
    params = [(param.name, param.annotation) for param in sig.parameters.values()]
    ret_type = sig.return_annotation
    if not ret_type is None:
        if isinstance(ret_type, str):
            try:
                ret_type = eval(ret_type)
            except NameError:
                pass
        ret_type = get_type_name(ret_type)
    return dict(name=func.__name__, args=params, return_type=ret_type)


def get_current_function_name() -> str:
    return inspect.stack()[1].function


def get_upper_function_name(step: int = 1, frame=None) -> str:
    if frame is None:
        frame = inspect.stack()[1].frame
    if step == 1:
        co_name = frame.f_back.f_code.co_name
    elif step > 1:
        co_name = get_upper_function_name(step - 1, frame.f_back)
    else:
        co_name = 'too many steps... return MAX upper function name'
    return co_name


def get_mac_address(interface: str = None) -> str:
    mac_address = getmac.get_mac_address(interface)

    if mac_address:
        mac_address = mac_address.replace(':', '').upper()
        return mac_address
    else:
        return None


def get_current_time(mode: TimeFormat = TimeFormat.UNIXTIME) -> Union[str, float]:
    if mode == TimeFormat.DATETIME1:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif mode == TimeFormat.DATETIME2:
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())
    elif mode == TimeFormat.DATE:
        return time.strftime("%Y-%m-%d", time.localtime())
    elif mode == TimeFormat.TIME:
        return time.strftime("%H:%M:%S", time.localtime())
    elif mode == TimeFormat.UNIXTIME:
        return time.time()
    return time.time()


def type_converter(in_type: Union[MXType, type, str, None]) -> Union[type, MXType]:
    if type(in_type) == MXType:
        if in_type in (MXType.BINARY, MXType.STRING):
            return str
        elif in_type == MXType.BOOL:
            return bool
        elif in_type == MXType.DOUBLE:
            return float
        elif in_type == MXType.INTEGER:
            return int
        elif in_type in (MXType.VOID, MXType.UNDEFINED):
            return None
        else:
            raise MXNotSupportedError('Unexpected python type!!!')
    elif type(in_type) == type:
        if in_type == int:
            return MXType.INTEGER
        elif in_type == float:
            return MXType.DOUBLE
        elif in_type == bool:
            return MXType.BOOL
        elif in_type == bytes:
            return MXType.BINARY
        elif in_type == str:
            return MXType.STRING
        elif in_type == type(None):
            return MXType.VOID
        else:
            raise MXNotSupportedError('Unexpected MXType type!!!')
    elif type(in_type) == str:
        if in_type == 'int':
            return MXType.INTEGER
        elif in_type == 'void':
            return MXType.VOID
        elif in_type == 'double':
            return MXType.DOUBLE
        elif in_type == 'bool':
            return MXType.BOOL
        elif in_type == 'binary':
            return MXType.BINARY
        elif in_type == 'string':
            return MXType.STRING
        elif in_type == 'undefined':
            return MXType.UNDEFINED
        else:
            raise MXNotSupportedError('Unexpected MXType type!!!')
    elif in_type == None or type(in_type) == type(None):
        return MXType.VOID


def json_file_read(path: str) -> Union[dict, bool]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return False


def json_file_write(path: str, data: Union[str, dict], indent: int = 4) -> None:
    with open(path, 'w') as f:
        if isinstance(data, (dict, str)):
            json.dump(data, f, indent=indent)
        else:
            raise Exception(f'common_util.json_file_write: data type error - {type(data)}')


def get_project_root(project_name: str = 'big-thing-py') -> Path:
    start_path = Path(__file__)
    while True:
        if str(start_path).split('/')[-1] == project_name:
            return str(start_path)
        else:
            start_path = start_path.parent


def check_valid_identifier(identifier: str) -> bool:
    pattern = r'^[a-zA-Z0-9_]*$'
    return bool(re.match(pattern, identifier))


def convert_url_to_ip(url: str) -> str:
    ip_list = url.split(".")
    not_ip = False

    for ip_token in ip_list:
        if not ip_token.isdigit():
            not_ip = True
            break

    if not_ip:
        host_ip = socket.gethostbyname(url.strip())
        return host_ip
    elif not all([(0 <= int(ip_token) <= 255) for ip_token in ip_list]) or len(ip_list) != 4:
        raise Exception('wrong ip format')
    else:
        return url


def check_python_version():
    if sys.version_info[0] <= 3 and sys.version_info[1] < 6:
        raise Exception(
            'Avahi feature is not supported on python3.6<=. try python3.7 or higher. or disable avahi feature. (avahi_enable=False)'
        )


def is_valid_ip_address(ip_address: str) -> bool:
    if ip_address:
        octets = ip_address.split('.')
    else:
        return False

    if len(octets) != 4:
        return False
    for octet in octets:
        try:
            value = int(octet)
        except ValueError:
            return False
        if not 0 <= value <= 255:
            return False
    return True


def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        return (platform.uname().system == 'Linux') and ('Raspberry Pi' in cpuinfo)
    except:
        return False


def check_os_architecture() -> str:
    architecture = platform.architecture()[0]
    return architecture


def install_missing_package(error):
    package_name = str(error).split("'")[1]
    os.system(f'pip install {package_name}')


def dummy_func(arg_list: list):
    args = ', '.join([str(arg) for arg in arg_list])
    lambda_str = f"lambda {args}: None"
    exec(lambda_str)
    return eval(lambda_str)


if __name__ == '__main__':
    pass
