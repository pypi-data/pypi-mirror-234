from big_thing_py.manager.manager_common import *
from big_thing_py.staff_thing import *


class ManagerModeHandler:
    def __init__(self, mode: MXManagerMode) -> None:
        self._mode = mode

    def dump_register_packet(self, staff_thing: MXStaffThing) -> mqtt.MQTTMessage:
        if self._mode == MXManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's register packet
            # it's only need to send manager thing's register packet to middleware
            pass
        elif self._mode == MXManagerMode.SPLIT:
            if staff_thing.get_registered():
                MXLOG_DEBUG('[dump_register_packet] staff thing already registered')
                return False

            topic = MXProtocolType.Base.TM_REGISTER.value % (staff_thing.get_name())
            payload = staff_thing.dict()
            msg = mqtt.MQTTMessage(topic, payload)
            return staff_thing.get_name(), payload
        else:
            raise MXInvalidRequestError(
                '[dump_register_packet] please set mode {MXManagerMode.JOIN|MXManagerMode.SPLIT}'
            )

    def dump_alive_packet(
        self, staff_thing_list: List[MXStaffThing]
    ) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == MXManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's alive packet
            # it's only need to send manager thing's alive packet to middleware
            pass
        elif self._mode == MXManagerMode.SPLIT:
            packet_list = []

            for staff_thing in staff_thing_list:
                if staff_thing.get_registered():
                    continue
                topic = MXProtocolType.Base.TM_ALIVE.value % (staff_thing.get_name())
                payload = str(EMPTY_JSON)
                msg = mqtt.MQTTMessage(topic, payload)
                packet_list.append(msg)

            return packet_list
        else:
            raise MXInvalidRequestError('[dump_alive_packet] please set mode {MXManagerMode.JOIN|MXManagerMode.SPLIT}')

    def dump_value_packet(
        self, staff_thing_list: List[MXStaffThing]
    ) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == MXManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's value packet
            # it's only need to send manager thing's value packet to middleware
            pass
        elif self._mode == MXManagerMode.SPLIT:
            packet_list = []

            for staff_thing in staff_thing_list:
                if staff_thing.get_registered():
                    continue
                for value in staff_thing.get_value_list():
                    value_dump = value.dict()

                    topic = MXProtocolType.Base.TM_ALIVE.value % (staff_thing.get_name())
                    payload = str(EMPTY_JSON)
                    msg = mqtt.MQTTMessage(topic, payload)
                    packet_list.append(msg)

            return packet_list
        else:
            raise MXInvalidRequestError('[dump_value_packet] please set mode {MXManagerMode.JOIN|MXManagerMode.SPLIT}')

    def dump_execute_result_packet(
        self, staff_thing_list: List[MXStaffThing]
    ) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == MXManagerMode.JOIN:
            pass
        elif self._mode == MXManagerMode.SPLIT:
            pass
        else:
            raise MXInvalidRequestError(
                '[dump_execute_result_packet] please set mode {MXManagerMode.JOIN|MXManagerMode.SPLIT}'
            )
