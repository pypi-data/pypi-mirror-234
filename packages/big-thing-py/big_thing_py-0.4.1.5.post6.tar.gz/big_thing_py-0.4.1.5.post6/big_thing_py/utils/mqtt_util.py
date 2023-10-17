from big_thing_py.utils.exception_util import *
from big_thing_py.utils.log_util import *
from big_thing_py.utils.json_util import *

import paho.mqtt.client as mqtt


def encode_MQTT_message(topic: str, payload: Union[str, dict], timestamp: float = None) -> mqtt.MQTTMessage:
    try:
        msg = mqtt.MQTTMessage()
        msg.topic = bytes(topic, encoding='utf-8')
        if isinstance(payload, str):
            msg.payload = bytes(payload, encoding='utf-8')
        elif isinstance(payload, dict):
            msg.payload = dict_to_json_string(payload)
        msg.timestamp = timestamp

        return msg
    except Exception as e:
        print_error(e)
        raise e


def decode_MQTT_message(msg: mqtt.MQTTMessage, mode=dict) -> Tuple[str, dict]:
    topic = msg.topic
    payload = msg.payload
    timestamp: float = msg.timestamp

    if isinstance(topic, bytes):
        topic = topic.decode()
    if isinstance(payload, bytes):
        payload = payload.decode()

    if isinstance(payload, str):
        if mode == str:
            return topic, payload, timestamp
        elif mode == dict:
            return topic, json_string_to_dict(payload), timestamp
        else:
            raise MXNotSupportedError(f'Unexpected mode!!! - {mode}')
    elif isinstance(payload, dict):
        if mode == str:
            return topic, dict_to_json_string(payload), timestamp
        elif mode == dict:
            return topic, payload, timestamp
        else:
            raise MXNotSupportedError(f'Unexpected mode!!! - {mode}')
    else:
        raise MXNotSupportedError(f'Unexpected type!!! - {type(payload)}')


def topic_split(topic: str):
    return topic.split('/')


def topic_join(topic: List[str]):
    return '/'.join(topic)


def unpack_mqtt_message(msg: mqtt.MQTTMessage) -> Tuple[List[str], str]:
    topic, payload, timestamp = decode_MQTT_message(msg, dict)
    topic = topic_split(topic)

    return topic, payload, timestamp


def pack_mqtt_message(topic_list: List[str], payload: str) -> mqtt.MQTTMessage:
    topic = topic_join(topic_list)
    msg = encode_MQTT_message(topic, payload)

    return msg
