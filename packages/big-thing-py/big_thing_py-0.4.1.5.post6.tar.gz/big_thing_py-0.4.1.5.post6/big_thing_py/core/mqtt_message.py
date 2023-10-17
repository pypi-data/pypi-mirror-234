from big_thing_py.utils import *


def make_super_request_key(scenario_name: str, requester_middleware_name: str) -> str:
    return '@'.join([scenario_name, requester_middleware_name])


def make_sub_service_request_key(sub_service_name: str, sub_service_request_order: int) -> str:
    return '@'.join([sub_service_name, str(sub_service_request_order)])


def make_request_ID(
    requester_middleware_name: str, super_thing_name: str, super_service_name: str, sub_service_request_order: int
):
    return '@'.join([requester_middleware_name, super_thing_name, super_service_name, str(sub_service_request_order)])


class MXMQTTMessage:
    def __init__(self) -> None:
        self._protocol_type: Union[MXProtocolType.Base, MXProtocolType.Super, MXProtocolType.WebClient] = None
        self.timestamp: float = None
        self.topic: str = None

    def set_timestamp(self, timestamp: float = None) -> None:
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()


class MXMQTTSendMessage(MXMQTTMessage):
    def __init__(self) -> None:
        super().__init__()
        self.payload: dict = None

    def mqtt_message(self) -> mqtt.MQTTMessage:
        msg = encode_MQTT_message(self.topic, self.payload)
        return msg


class MXMQTTReceiveMessage(MXMQTTMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__()
        self.topic, self.payload, self.timestamp = decode_MQTT_message(msg)
        self.topic_error: bool = False
        self.payload_error: bool = False


class MXRegisterMessage(MXMQTTSendMessage):
    def __init__(self, thing) -> None:
        from big_thing_py.core.thing import MXThing

        thing: MXThing = thing

        super().__init__()
        self._protocol_type = MXProtocolType.Base.TM_REGISTER
        self.topic = self._protocol_type.value % (thing.get_name())
        self.payload = thing.dict()


##############################################################################################################################


class MXRegisterResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Base.MT_RESULT_REGISTER
        self.thing_name = self.topic.split('/')[3]
        self.middleware_name: str = self.payload['middleware_name']
        self.error: MXErrorCode = MXErrorCode.get(self.payload['error'])


class MXUnregisterMessage(MXMQTTSendMessage):
    def __init__(self, thing) -> None:
        from big_thing_py.core.thing import MXThing

        thing: MXThing = thing

        super().__init__()
        self._protocol_type = MXProtocolType.Base.TM_UNREGISTER
        self.topic = self._protocol_type.value % (thing.get_name())
        self.payload = EMPTY_JSON


class MXUnregisterResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Base.MT_RESULT_UNREGISTER
        self.thing_name: str = self.topic.split('/')[3]
        self.error: MXErrorCode = MXErrorCode.get(self.payload['error'])


class MXExecuteMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Base.MT_EXECUTE
        self.function_name: str = self.topic.split('/')[2]
        self.thing_name: str = self.topic.split('/')[3]

        if len(self.topic.split('/')) == 6:
            self.middleware_name: str = self.topic.split('/')[4]
            self.request_ID: str = self.topic.split('/')[5]
            if not self.middleware_name or not self.request_ID:
                self.topic_error = True
        elif len(self.topic.split('/')) == 4:
            self.middleware_name: str = ''
            self.request_ID: str = ''
        else:
            self.topic_error = True

        self.scenario: str = self.payload.get('scenario', None)
        self.arguments: List[dict] = self.payload.get('arguments', None)

        if not self.scenario or self.arguments == None:
            self.payload_error = True
        elif not all([isinstance(arg.get('order', None), int) for arg in self.arguments]) or not all(
            [isinstance(arg.get('value', None), (int, float, str, bool)) for arg in self.arguments]
        ):
            self.payload_error = True

    def tuple_arguments(self) -> tuple:
        self.arguments = sorted(self.arguments, key=lambda x: int(x['order']))
        real_arguments = tuple([argument['value'] for argument in self.arguments])
        return real_arguments

    def dict_arguments(self) -> List[dict]:
        self.arguments = sorted(self.arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value']) for arg in self.arguments]
        return json_arguments


class MXExecuteResultMessage(MXMQTTSendMessage):
    def __init__(
        self, function, scenario: str, request_ID: str = '', error: MXErrorCode = MXErrorCode.UNDEFINED
    ) -> None:
        from big_thing_py.core.function import MXFunction

        super().__init__()
        self._protocol_type = MXProtocolType.Base.TM_RESULT_EXECUTE
        self.function: MXFunction = function
        self.request_ID = request_ID
        self.scenario = scenario
        self._error = error

        if self.request_ID:
            self.topic = self._protocol_type.value % (
                self.function.get_name(),
                self.function.get_thing_name(),
                self.function.get_middleware_name(),
                self.request_ID,
            )
        else:
            self.topic = (
                self._protocol_type.value % (self.function.get_name(), self.function.get_thing_name(), '', '')
            ).rstrip('/')

        self.payload = dict(
            error=self._error.value,
            scenario=self.scenario,
            return_type=self.function.get_return_type().value,
            return_value=self.function.get_return_value(),
        )

    @property
    def error(self) -> dict:
        return self._error

    @error.setter
    def error(self, error: MXErrorCode):
        if not isinstance(error, MXErrorCode):
            raise MXTypeError("error must be an MXErrorType")
        self._error = error
        self.payload = dict(
            error=self._error.value,
            scenario=self.scenario,
            return_type=self.function.get_return_type().value,
            return_value=self.function.get_return_value(),
        )


# TODO: binary 부분 구현 완료 후 작성하기
class MXBinaryValueResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Base.MT_RESULT_BINARY_VALUE
        self.thing_name = self.topic.split('/')[3]
        self.value_name = self.payload['value_name']


class MXAliveMessage(MXMQTTSendMessage):
    def __init__(self, thing) -> None:
        from big_thing_py.core.thing import MXThing

        thing: MXThing = thing

        super().__init__()
        self._protocol_type = MXProtocolType.Base.TM_ALIVE
        self.topic = self._protocol_type.value % (thing.get_name())
        self.payload = EMPTY_JSON


class MXValuePublishMessage(MXMQTTSendMessage):
    def __init__(self, thing, value) -> None:
        from big_thing_py.core.thing import MXThing
        from big_thing_py.core.value import MXValue

        thing: MXThing = thing
        value: MXValue = value

        super().__init__()
        self._protocol_type = MXProtocolType.Base.TM_VALUE_PUBLISH
        self.topic = self._protocol_type.value % (value.get_name(), thing.get_name())
        self.payload = value.publish_dict()


# for middleware detect
class MXClientServiceListResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.WebClient.ME_RESULT_SERVICE_LIST
        self._client_id = self.topic.split('/')[3]


class MXClientRefreshMessage(MXMQTTSendMessage):
    def __init__(self, thing) -> None:
        from big_thing_py.core.thing import MXThing

        thing: MXThing = thing

        super().__init__()
        self._protocol_type = MXProtocolType.WebClient.EM_REFRESH
        self.topic = self._protocol_type.value % (thing.get_name())
        self.payload = EMPTY_JSON


class MXNotifyMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.WebClient.ME_NOTIFY_CHANGE

        # topic
        self._client_id = self.topic.split('/')[2]

        # payload


if __name__ == '__main__':
    payload = {
        'scenario': 'test',
        'arguments': [
            {
                'order': 0,
                'value': 1,
            },
            {
                'order': 1,
                'value': 2,
            },
        ],
    }
    msg = encode_MQTT_message('MT/EXECUTE/test1/test2', payload)
    message = MXExecuteMessage(msg)
    print(message.tuple_arguments())
    print(message.dict_arguments(*(1, 2)))
