from big_thing_py.utils import *
from big_thing_py.core.mqtt_message import *


class MXScheduleStatus(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    INIT = auto()
    CHECK = auto()
    SELECT = auto()
    CONFIRM = auto()
    UNDEFINED = auto()

    @classmethod
    def get(cls, name: str) -> 'MXScheduleStatus':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class MXSuperRefreshMessage(MXMQTTSendMessage):
    def __init__(self, thing) -> None:
        from big_thing_py.core.thing import MXThing

        thing: MXThing = thing

        super().__init__()
        self._protocol_type = MXProtocolType.Super.SM_REFRESH
        self.topic = self._protocol_type.value % (thing.get_name())
        self.payload = EMPTY_JSON


class MXSuperServiceListResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Super.MS_RESULT_SERVICE_LIST
        self.super_thing_name: str = self.topic.split('/')[3]
        self.service_list: List[dict] = self.payload['services']


class MXSuperScheduleMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Super.MS_SCHEDULE

        # topic
        self.super_service_name = self.topic.split('/')[2]
        self.super_thing_name = self.topic.split('/')[3]
        self.super_middleware_name = self.topic.split('/')[4]
        self.requester_middleware_name = self.topic.split('/')[5]

        # payload
        self.scenario = self.payload['scenario']
        self.period = self.payload['period']

        if not isinstance(self.scenario, str) or not isinstance(self.period, (int, float)):
            self.payload_error = True


class MXSuperScheduleResultMessage(MXMQTTSendMessage):
    def __init__(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        error: MXErrorCode = MXErrorCode.UNDEFINED,
    ) -> None:
        super().__init__()
        self._protocol_type = MXProtocolType.Super.SM_RESULT_SCHEDULE

        self.topic = self._protocol_type.value % (
            super_service_name,
            super_thing_name,
            super_middleware_name,
            requester_middleware_name,
        )
        self.payload = dict(scenario=scenario, error=error.value)


class MXSubScheduleMessage(MXMQTTSendMessage):
    def __init__(
        self,
        sub_service_name: str,
        target_thing_name: str,
        target_middleware_name: str,
        requester_middleware_name: str = None,
        super_thing_name: str = None,
        super_service_name: str = None,
        sub_service_request_order: int = None,
        scenario: str = None,
        period: float = None,
        tag_list: List[str] = [],
        range_type: MXRangeType = None,
        request_ID: str = None,
        status: MXScheduleStatus = None,
    ) -> None:
        super().__init__()
        self._protocol_type = MXProtocolType.Super.SM_SCHEDULE

        # topic
        self.sub_service_name = sub_service_name
        self.target_thing_name = target_thing_name
        self.target_middleware_name = target_middleware_name

        self.requester_middleware_name = requester_middleware_name
        self.super_thing_name = super_thing_name
        self.super_service_name = super_service_name
        self.sub_service_request_order = sub_service_request_order

        self.scenario = scenario
        self.period = period
        self.tag_list = tag_list
        self.range_type = range_type

        self.request_ID = request_ID
        self._status = status

        if not self.request_ID:
            self.request_ID = make_request_ID(
                self.requester_middleware_name,
                self.super_thing_name,
                self.super_service_name,
                self.sub_service_request_order,
            )

        self.topic = self._protocol_type.value % (self.sub_service_name, self.target_middleware_name, self.request_ID)
        self.payload = dict(
            scenario=self.scenario,
            period=self.period,
            status=self._status.value,
            tag_list=self.tag_list,
            range=self.range_type.value,
        )

    @property
    def status(self) -> dict:
        return self._status

    @status.setter
    def status(self, status: MXScheduleStatus):
        if not isinstance(status, MXScheduleStatus):
            raise MXTypeError("status must be an MXScheduleStatus")
        self._status = status
        self.payload = dict(
            scenario=self.scenario,
            period=self.period,
            status=self._status.value,
            tag_list=self.tag_list,
            range=self.range_type.value,
        )


class MXSubScheduleResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Super.MS_RESULT_SCHEDULE

        # topic
        self.sub_service_name = self.topic.split('/')[3]
        self.target_thing_name = self.topic.split('/')[4]
        self.target_middleware_name = self.topic.split('/')[5]

        self.request_ID = self.topic.split('/')[6]
        self.requester_middleware_name = self.request_ID.split('@')[0]
        self.super_thing_name = self.request_ID.split('@')[1]
        self.super_service_name = self.request_ID.split('@')[2]
        self.sub_service_request_order = self.request_ID.split('@')[3]

        # payload
        self.scenario = self.payload['scenario']
        self.error = MXErrorCode.get(self.payload['error'])
        self.status = MXScheduleStatus.get(self.payload.get('status', None))  # 'check' or 'confirm'


class MXSuperExecuteMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Super.MS_EXECUTE

        # topic
        self.super_service_name = self.topic.split('/')[2]
        self.super_thing_name = self.topic.split('/')[3]
        self.super_middleware_name = self.topic.split('/')[4]
        self.requester_middleware_name = self.topic.split('/')[5]

        # payload
        self.scenario: str = self.payload.get('scenario', None)
        self.arguments: List[dict] = self.payload.get('arguments', None)

        if not self.scenario or self.arguments == None:
            self.payload_error = True
        elif not all([isinstance(arg.get('order', None), int) for arg in self.arguments]) or not all(
            [isinstance(arg.get('value', None), (int, float, str, bool)) for arg in self.arguments]
        ):
            self.payload_error = True

    def tuple_arguments(self) -> tuple:
        sorted_arguments = sorted(self.arguments, key=lambda x: int(x['order']))
        real_arguments = tuple([argument['value'] for argument in sorted_arguments])
        return real_arguments

    def dict_arguments(self) -> List[dict]:
        self.arguments = sorted(self.arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value']) for arg in self.arguments]
        return json_arguments


class MXSuperExecuteResultMessage(MXMQTTSendMessage):
    def __init__(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        return_type: MXType,
        return_value: Union[int, float, bool, str] = None,
        error: MXErrorCode = MXErrorCode.UNDEFINED,
    ) -> None:
        super().__init__()
        self._protocol_type = MXProtocolType.Super.SM_RESULT_EXECUTE

        # payload
        self.scenario = scenario
        self.return_type = return_type
        self.return_value = return_value
        self.error = error

        self.topic = self._protocol_type.value % (
            super_service_name,
            super_thing_name,
            super_middleware_name,
            requester_middleware_name,
        )
        self.payload = dict(
            scenario=scenario, return_type=return_type.value, return_value=return_value, error=error.value
        )


class MXSubExecuteMessage(MXMQTTSendMessage):
    def __init__(
        self,
        sub_service_name: str,
        target_thing_name: str,
        target_middleware_name: str,
        requester_middleware_name: str = None,
        super_thing_name: str = None,
        super_service_name: str = None,
        sub_service_request_order: int = None,
        scenario: str = None,
        arguments: List[dict] = None,
        request_ID: str = None,
    ) -> None:
        super().__init__()
        self._protocol_type = MXProtocolType.Super.SM_EXECUTE

        # topic
        self.sub_service_name = sub_service_name
        self.target_thing_name = target_thing_name
        self.target_middleware_name = target_middleware_name

        self.requester_middleware_name = requester_middleware_name
        self.super_thing_name = super_thing_name
        self.super_service_name = super_service_name
        self.sub_service_request_order = sub_service_request_order

        self.scenario = scenario
        self._arguments = arguments

        self.request_ID = request_ID

        if not self.request_ID:
            self.request_ID = make_request_ID(
                self.requester_middleware_name,
                self.super_thing_name,
                self.super_service_name,
                self.sub_service_request_order,
            )

        self.topic = self._protocol_type.value % (self.sub_service_name, self.target_middleware_name, self.request_ID)
        self.payload = dict(scenario=self.scenario, arguments=self._arguments)

    @property
    def arguments(self) -> dict:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments: tuple):
        if not isinstance(arguments, tuple):
            raise MXTypeError("arguments must be an tuple")
        self._arguments = arguments
        dict_arguments = [dict(order=i, value=arg) for i, arg in enumerate(self._arguments)]
        self.payload = dict(scenario=self.scenario, arguments=dict_arguments)

    # def json_arguments(self) -> List[dict]:
    #     self._arguments = sorted(self._arguments, key=lambda x: int(x['order']))
    #     json_arguments = [dict(order=arg['order'], value=arg['value']) for arg in self._arguments]
    #     return json_arguments


class MXSubExecuteResultMessage(MXMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = MXProtocolType.Super.MS_RESULT_EXECUTE

        # topic
        self.sub_service_name = self.topic.split('/')[3]
        self.target_thing_name = self.topic.split('/')[4]
        self.target_middleware_name = self.topic.split('/')[5]

        self.request_ID = self.topic.split('/')[6]
        self.requester_middleware_name = self.request_ID.split('@')[0]
        self.super_thing_name = self.request_ID.split('@')[1]
        self.super_service_name = self.request_ID.split('@')[2]
        self.sub_service_request_order = self.request_ID.split('@')[3]

        # payload
        self.scenario = self.payload['scenario']
        self.return_type = self.payload['return_type']
        # TODO: 추후에 return_value -> return_values로 변경
        self.return_value = self.payload['return_value']
        self.error = MXErrorCode.get(self.payload['error'])

    def tuple_arguments(self) -> tuple:
        sorted_arguments = sorted(self._arguments, key=lambda x: int(x['order']))
        tuple_arguments = tuple([argument['value'] for argument in sorted_arguments])
        return tuple_arguments

    def dict_arguments(self) -> List[dict]:
        sorted_arguments = sorted(self._arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value']) for arg in sorted_arguments]
        return json_arguments
