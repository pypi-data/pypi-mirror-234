from big_thing_py.common.mxtype import *
from big_thing_py.core.mqtt_message import *


class MXRequest(metaclass=ABCMeta):
    def __init__(self, trigger_msg: MXMQTTMessage = None, result_msg: MXMQTTMessage = None) -> None:
        self._action_type: MXActionType = None
        self.trigger_msg = trigger_msg
        self.result_msg = result_msg

        # seconds
        self._duration: float = 0

    def duration(self):
        return self._duration

    def timer_start(self):
        self.trigger_msg.set_timestamp(get_current_time())

    def timer_end(self):
        try:
            self.result_msg.set_timestamp(get_current_time())
            self._duration = self.result_msg.timestamp - self.trigger_msg.timestamp
        except Exception:
            self._duration = time.time() - self.trigger_msg.timestamp
        return self.duration()


class MXRegisterRequest(MXRequest):
    def __init__(self, trigger_msg: MXMQTTMessage = None, result_msg: MXMQTTMessage = None) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = MXActionType.REGISTER

        self._trigger_msg: MXExecuteMessage
        self._result_msg: MXExecuteResultMessage


class MXExecuteRequest(MXRequest):
    def __init__(self, trigger_msg: MXExecuteMessage = None, result_msg: MXExecuteResultMessage = None) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = MXActionType.EXECUTE

        self.trigger_msg: MXExecuteMessage
        self.result_msg: MXExecuteResultMessage

    def set_return_msg(self, result: MXExecuteResultMessage):
        self.result_msg = result

    def get_return_msg(self):
        return self.result_msg
