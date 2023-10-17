from big_thing_py.utils.log_util import *
import requests


class RequestMethod(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


def API_response_check(res: requests.Response):
    if res.status_code not in [200, 204]:
        return False
    else:
        return res


def API_request(
    url,
    method: RequestMethod = RequestMethod.GET,
    header: str = '',
    body: str = '',
    verify: bool = False,
    timeout: float = None,
) -> dict:
    try:
        if method == RequestMethod.GET:
            res = requests.get(url, headers=header, verify=verify, timeout=timeout)
            if API_response_check(res):
                if res.status_code == 200:
                    data = res.json()
                elif res.status_code == 204:
                    data = {}
                return data
            else:
                return False
        elif method == RequestMethod.POST:
            res = requests.post(url, headers=header, data=body, verify=verify, timeout=timeout)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.PUT:
            res = requests.put(url, headers=header, data=body, verify=verify, timeout=timeout)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.DELETE:
            MXLOG_DEBUG('Not implement yet')
        else:
            MXLOG_DEBUG(f'[decode_MQTT_message] Unexpected request!!!', 'red')
    except Exception as e:
        MXLOG_DEBUG(f'Failed to request API: {e}', 'red')
        return False


if __name__ == '__main__':
    res = API_request('https://www.google.com')
    print(res)
