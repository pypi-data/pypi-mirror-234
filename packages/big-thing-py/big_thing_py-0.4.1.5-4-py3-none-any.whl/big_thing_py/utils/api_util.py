from big_thing_py.utils import *
import requests
from enum import Enum, auto


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
        print_error(e)
        return False


# def kakao_test():
#     api_client = KakaoAPIClient(api_key='feba82a01e28a99ca2c11322ef6896e9')
#     # print(api_client.OCR('./inspirational-1254724_960_720.png'))
#     # print(api_client.search('수리남'))
#     # print(api_client.pose(
#     #     'https://cdn.pixabay.com/photo/2016/03/09/09/30/woman-1245817_960_720.jpg'))
#     print(api_client.translation('안녕하세요.', 'kr', 'en'))


# def naver_test():
# api_client = NaverAPIClient(
#     client_id='RsSPHxj1l7VJsLTHs4eA', api_key='_nhJeYeoND')
# print(api_client.search())
# print(api_client.face_detect_celebrity(
#     './KakaoTalk_20220929_071045111.jpg'))
# print(api_client.papago('안녕하세요. 반갑습니다.', 'ko', 'en'))
# print(api_client.papago_detect_lang('안녕하세요. 반갑습니다.'))
if __name__ == '__main__':
    # naver_test()
    pass
