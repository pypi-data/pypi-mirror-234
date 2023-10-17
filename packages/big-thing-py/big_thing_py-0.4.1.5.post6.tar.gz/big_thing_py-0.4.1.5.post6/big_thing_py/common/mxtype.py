from enum import Enum, auto
from typing import Union


class MXNetworkType(Enum):
    MQTT = 0
    API = 1
    BLUETOOTH = 2
    BLE = 3
    RF = 4
    XBEE = 5


class MXType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    INTEGER = 'int'
    DOUBLE = 'double'
    STRING = 'string'
    BOOL = 'bool'
    BINARY = 'binary'
    VOID = 'void'

    def __str__(self):
        return str(self.name)

    @classmethod
    def get(cls, name: Union[str, type]) -> 'MXType':
        try:
            if isinstance(name, str):
                name = name.lower()
                if name is not None:
                    for mxtype in MXType:
                        if mxtype.value == name:
                            return mxtype
                        elif mxtype.value == 'int' and name == 'integer':
                            return cls.INTEGER
                        elif mxtype.value == 'double' and name == 'float':
                            return cls.DOUBLE
                        elif mxtype.value == 'string' and name == 'str':
                            return cls.STRING
                        elif mxtype.value == 'bool' and name == 'boolean':
                            return cls.BOOL
                    return cls.UNDEFINED
                else:
                    return cls.UNDEFINED
            elif isinstance(name, type):
                if name == int:
                    return MXType.INTEGER
                elif name == float:
                    return MXType.DOUBLE
                elif name == bool:
                    return MXType.BOOL
                elif name == str:
                    return MXType.STRING
                elif name == str:
                    return MXType.BINARY
                elif name is None:
                    return MXType.VOID
        except Exception:
            return cls.UNDEFINED

    def to_pytype(self):
        if self == MXType.INTEGER:
            return int
        elif self == MXType.DOUBLE:
            return float
        elif self == MXType.BOOL:
            return bool
        elif self == MXType.STRING:
            return str
        elif self == MXType.BINARY:
            return str
        elif self == MXType.VOID:
            return None


class MXActionType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    REGISTER = auto()
    EXECUTE = auto()
    ALIVE = auto()
    VALUE_PUBLISH = auto()
    AVAILABILITY = auto()
    REFRESH = auto()
    SUPER_SCHEDULE = auto()
    SUPER_EXECUTE = auto()
    SUB_SCHEDULE = auto()
    SUB_EXECUTE = auto()


class MXProtocolType:
    class Base(Enum):
        # ===============
        # ___  ___ _____
        # |  \/  ||_   _|
        # | .  . |  | |
        # | |\/| |  | |
        # | |  | |  | |
        # \_|  |_/  \_/
        # ===============

        # MT/RESULT/REGISTER/[ThingName]
        MT_RESULT_REGISTER = 'MT/RESULT/REGISTER/%s'

        # MT/RESULT/UNREGISTER/[ThingName]
        MT_RESULT_UNREGISTER = 'MT/RESULT/UNREGISTER/%s'

        # MT/EXECUTE/[FunctionName]/[ThingName]/([TargetMiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MT_EXECUTE = 'MT/EXECUTE/%s/%s/%s/%s'

        # MT/RESULT/BINARY_VALUE/[ThingName]
        MT_RESULT_BINARY_VALUE = 'MT/RESULT/BINARY_VALUE/%s'

        # ===============
        #  _____ ___  ___
        # |_   _||  \/  |
        #   | |  | .  . |
        #   | |  | |\/| |
        #   | |  | |  | |
        #   \_/  \_|  |_/
        # ===============

        # TM/RESULT/EXECUTE/[FunctionName]/[ThingName]/([TargetMiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        TM_RESULT_EXECUTE = 'TM/RESULT/EXECUTE/%s/%s/%s/%s'

        # TM/REGISTER/[ThingName]
        TM_REGISTER = 'TM/REGISTER/%s'

        # TM/UNREGISTER/[ThingName]
        TM_UNREGISTER = 'TM/UNREGISTER/%s'

        # TM/ALIVE/[ThingName]
        TM_ALIVE = 'TM/ALIVE/%s'

        # [ValueName]/[ThingName]
        TM_VALUE_PUBLISH = '%s/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Manager(Enum):
        pass

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Super(Enum):
        # ===============
        # ___  ___ _____
        # |  \/  |/  ___|
        # | .  . |\ `--.
        # | |\/| | `--. \
        # | |  | |/\__/ /
        # \_|  |_/\____/
        # ===============

        # MS/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_SCHEDULE = 'MS/SCHEDULE/%s/%s/%s/%s'

        # MS/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_EXECUTE = 'MS/EXECUTE/%s/%s/%s/%s'

        # MS/RESULT/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MS_RESULT_SCHEDULE = 'MS/RESULT/SCHEDULE/%s/SUPER/%s/%s'

        # MS/RESULT/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        MS_RESULT_EXECUTE = 'MS/RESULT/EXECUTE/%s/SUPER/%s/%s'

        # MS/RESULT/SERVICE_LIST/[SuperThingName]
        MS_RESULT_SERVICE_LIST = 'MS/RESULT/SERVICE_LIST/%s'

        # ================
        #  _____ ___  ___
        # /  ___||  \/  |
        # \ `--. | .  . |
        #  `--. \| |\/| |
        # /\__/ /| |  | |
        # \____/ \_|  |_/
        # ================

        # SM/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        SM_SCHEDULE = 'SM/SCHEDULE/%s/SUPER/%s/%s'

        # SM/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_service@subrequest_order
        SM_EXECUTE = 'SM/EXECUTE/%s/SUPER/%s/%s'

        # SM/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_SCHEDULE = 'SM/RESULT/SCHEDULE/%s/%s/%s/%s'

        # SM/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_EXECUTE = 'SM/RESULT/EXECUTE/%s/%s/%s/%s'

        # SM/AVAILABILITY/[SuperThingName]
        SM_AVAILABILITY = 'SM/AVAILABILITY/%s'

        # SM/REFRESH/[SuperThingName]
        SM_REFRESH = 'SM/REFRESH/%s'

        # ==================
        #   _____    _____
        #  |  __ \  / ____|
        #  | |__) || |
        #  |  ___/ | |
        #  | |     | |____
        #  |_|      \_____|
        # ==================

        # PC/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        PC_SCHEDULE = 'PC/SCHEDULE/%s/SUPER/%s/%s'

        # PC/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        PC_EXECUTE = 'PC/EXECUTE/%s/SUPER/%s/%s'

        # PC/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_SCHEDULE = 'PC/RESULT/SCHEDULE/%s/%s/%s/%s'

        # PC/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_EXECUTE = 'PC/RESULT/EXECUTE/%s/%s/%s/%s'

        # PC/SERVICE_LIST/#
        PC_SERVICE_LIST = 'PC/SERVICE_LIST/%s'

        # PC/TRAVERSE/#
        PC_TRAVERSE = 'PC/TRAVERSE/%s'

        # ==================
        #    _____  _____
        #   / ____||  __ \
        #  | |     | |__) |
        #  | |     |  ___/
        #  | |____ | |
        #   \_____||_|
        # ==================

        # CP/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        CP_SCHEDULE = 'CP/SCHEDULE/%s/%s/%s/%s'

        # CP/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[Requester MWName]
        CP_EXECUTE = 'CP/EXECUTE/%s/%s/%s/%s'

        # CP/RESULT/SCHEDULE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_SCHEDULE = 'CP/RESULT/SCHEDULE/%s/SUPER/%s/%s'

        # CP/RESULT/EXECUTE/[TargetFunctionName]/SUPER/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_EXECUTE = 'CP/RESULT/EXECUTE/%s/SUPER/%s/%s'

        # CP/SERVICE_LIST/#
        CP_SERVICE_LIST = 'CP/SERVICE_LIST/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class WebClient(Enum):
        # ==================
        #   ______  __  __
        #  |  ____||  \/  |
        #  | |__   | \  / |
        #  |  __|  | |\/| |
        #  | |____ | |  | |
        #  |______||_|  |_|
        # ==================

        # EM/VERIFY_SCENARIO/[ClientID]
        EM_VERIFY_SCENARIO = 'EM/VERIFY_SCENARIO/%s'

        # EM/ADD_SCENARIO/[ClientID]
        EM_ADD_SCENARIO = 'EM/ADD_SCENARIO/%s'

        # EM/RUN_SCENARIO/[ClientID]
        EM_RUN_SCENARIO = 'EM/RUN_SCENARIO/%s'

        # EM/STOP_SCENARIO/[ClientID]
        EM_STOP_SCENARIO = 'EM/STOP_SCENARIO/%s'

        # EM/UPDATE_SCENARIO/[ClientID]
        EM_UPDATE_SCENARIO = 'EM/UPDATE_SCENARIO/%s'

        # EM/DELETE_SCENARIO/[ClientID]
        EM_DELETE_SCENARIO = 'EM/DELETE_SCENARIO/%s'

        # EM/ADD_TAG/[ClientID]
        EM_ADD_TAG = 'EM/ADD_TAG/%s'

        # EM/DELETE_TAG/[ClientID]
        EM_DELETE_TAG = 'EM/DELETE_TAG/%s'

        # EM/SET_ACCESS/[ClientID]
        EM_SET_ACCESS = 'EM/SET_ACCESS/%s'

        # EM/GET_TREE/[ClientID]
        EM_GET_TREE = 'EM/GET_TREE/%s'

        # EM/REFRESH/[ClientID]
        EM_REFRESH = 'EM/REFRESH/%s'

        # ==================
        #   __  __  ______
        #  |  \/  ||  ____|
        #  | \  / || |__
        #  | |\/| ||  __|
        #  | |  | || |____
        #  |_|  |_||______|
        # ==================

        # ME/RESULT/VERIFY_SCENARIO/[ClientID]
        ME_RESULT_VERIFY_SCENARIO = 'ME/RESULT/VERIFY_SCENARIO/%s'

        # ME/RESULT/RUN_SCENARIO/[ClientID]
        ME_RESULT_RUN_SCENARIO = 'ME/RESULT/RUN_SCENARIO/%s'

        # ME/RESULT/STOP_SCENARIO/[ClientID]
        ME_RESULT_STOP_SCENARIO = 'ME/RESULT/STOP_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_SCHEDULE_SCENARIO = 'ME/RESULT/SCHEDULE_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_ADD_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_UPDATE_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/DELETE_SCENARIO/[ClientID]
        ME_RESULT_DELETE_SCENARIO = 'ME/RESULT/DELETE_SCENARIO/%s'

        # ME/RESULT/ADD_TAG/[ClientID]
        ME_RESULT_ADD_TAG = 'ME/RESULT/ADD_TAG/%s'

        # ME/RESULT/DELETE_TAG/[ClientID]
        ME_RESULT_DELETE_TAG = 'ME/RESULT/DELETE_TAG/%s'

        # ME/RESULT/SET_ACCESS/[ClientID]
        ME_RESULT_SET_ACCESS = 'ME/RESULT/SET_ACCESS/%s'

        # ME/RESULT/GET_TREE/[ClientID]
        ME_RESULT_GET_TREE = 'ME/RESULT/GET_TREE/%s'

        # ME/RESULT/SERVICE_LIST/[ClientID]
        ME_RESULT_SERVICE_LIST = 'ME/RESULT/SERVICE_LIST/%s'

        # ME/RESULT/SCENARIO_LIST/[ClientID]
        ME_RESULT_SCENARIO_LIST = 'ME/RESULT/SCENARIO_LIST/%s'

        # ME/NOTIFY_CHANGE/[ClientID]
        ME_NOTIFY_CHANGE = 'ME/NOTIFY_CHANGE/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class SN(Enum):
        # TM/SN/REGISTER/VALUE/[Thing ID]
        TM_SN_REGISTER_VALUE = "TM/SN/REGISTER/VALUE/%s"

        # TM/SN/REGISTER/VALUEDESC/[Thing ID]
        TM_SN_REGISTER_VALUEDESC = "TM/SN/REGISTER/VALUEDESC/%s"

        # TM/SN/REGISTER/VALUETAG/[Thing ID]
        TM_SN_REGISTER_VALUETAG = "TM/SN/REGISTER/VALUETAG/%s"

        # TM/SN/REGISTER/FUNCTION/[Thing ID]
        TM_SN_REGISTER_FUNCTION = "TM/SN/REGISTER/FUNCTION/%s"

        # TM/SN/REGISTER/FUNCTIONDESC/[Thing ID]
        TM_SN_REGISTER_FUNCTIONDESC = "TM/SN/REGISTER/FUNCTIONDESC/%s"

        # TM/SN/REGISTER/FUNCTIONTAG/[Thing ID]
        TM_SN_REGISTER_FUNCTIONTAG = "TM/SN/REGISTER/FUNCTIONTAG/%s"

        # TM/SN/REGISTER/ARGUMENT/[Thing ID]
        TM_SN_REGISTER_ARGUMENT = "TM/SN/REGISTER/ARGUMENT/%s"

        # TM/SN/REGISTER/ALIVECYCLE/[Thing ID]
        TM_SN_REGISTER_ALIVECYCLE = "TM/SN/REGISTER/ALIVECYCLE/%s"

        # TM/SN/REGISTER/FINISH/[Thing ID]
        TM_SN_REGISTER_FINISH = "TM/SN/REGISTER/FINISH/%s"

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    @classmethod
    def get(self, topic: str) -> 'MXProtocolType':
        # MT
        if 'MT/RESULT/REGISTER/' in topic:
            return MXProtocolType.Base.MT_RESULT_REGISTER
        elif 'MT/RESULT/UNREGISTER/' in topic:
            return MXProtocolType.Base.MT_RESULT_UNREGISTER
        elif 'MT/EXECUTE/' in topic:
            return MXProtocolType.Base.MT_EXECUTE
        elif 'MT/RESULT/BINARY_VALUE/' in topic:
            return MXProtocolType.Base.MT_RESULT_BINARY_VALUE
        # TM
        elif 'TM/RESULT/EXECUTE/' in topic:
            return MXProtocolType.Base.TM_RESULT_EXECUTE
        elif 'TM/REGISTER/' in topic:
            return MXProtocolType.Base.TM_REGISTER
        elif 'TM/UNREGISTER/' in topic:
            return MXProtocolType.Base.TM_UNREGISTER
        elif 'TM/ALIVE/' in topic:
            return MXProtocolType.Base.TM_ALIVE
        elif len(topic.split('/')) == 2:
            return MXProtocolType.Base.TM_VALUE_PUBLISH
        # MS
        elif 'MS/SCHEDULE/' in topic:
            return MXProtocolType.Super.MS_SCHEDULE
        elif 'MS/EXECUTE/' in topic:
            return MXProtocolType.Super.MS_EXECUTE
        elif 'MS/RESULT/SCHEDULE/' in topic:
            return MXProtocolType.Super.MS_RESULT_SCHEDULE
        elif 'MS/RESULT/EXECUTE/' in topic:
            return MXProtocolType.Super.MS_RESULT_EXECUTE
        elif 'MS/RESULT/SERVICE_LIST/' in topic:
            return MXProtocolType.Super.MS_RESULT_SERVICE_LIST
        # SM
        elif 'SM/SCHEDULE/' in topic:
            return MXProtocolType.Super.SM_SCHEDULE
        elif 'SM/EXECUTE/' in topic:
            return MXProtocolType.Super.SM_EXECUTE
        elif 'SM/RESULT/SCHEDULE/' in topic:
            return MXProtocolType.Super.SM_RESULT_SCHEDULE
        elif 'SM/RESULT/EXECUTE/' in topic:
            return MXProtocolType.Super.SM_RESULT_EXECUTE
        elif 'SM/AVAILABILITY/' in topic:
            return MXProtocolType.Super.SM_AVAILABILITY
        elif 'SM/REFRESH/' in topic:
            return MXProtocolType.Super.SM_REFRESH
        # PC
        elif 'PC/SCHEDULE/' in topic:
            return MXProtocolType.Super.PC_SCHEDULE
        elif 'PC/EXECUTE/' in topic:
            return MXProtocolType.Super.PC_EXECUTE
        elif 'PC/RESULT/SCHEDULE/' in topic:
            return MXProtocolType.Super.PC_RESULT_SCHEDULE
        elif 'PC/RESULT/EXECUTE/' in topic:
            return MXProtocolType.Super.PC_RESULT_EXECUTE
        elif 'PC/SERVICE_LIST/' in topic:
            return MXProtocolType.Super.PC_SERVICE_LIST
        elif 'PC/TRAVERSE/' in topic:
            return MXProtocolType.Super.PC_TRAVERSE
        # CP
        elif 'CP/SCHEDULE/' in topic:
            return MXProtocolType.Super.CP_SCHEDULE
        elif 'CP/EXECUTE/' in topic:
            return MXProtocolType.Super.CP_EXECUTE
        elif 'CP/RESULT/SCHEDULE/' in topic:
            return MXProtocolType.Super.CP_RESULT_SCHEDULE
        elif 'CP/RESULT/EXECUTE/' in topic:
            return MXProtocolType.Super.CP_RESULT_EXECUTE
        elif 'CP/SERVICE_LIST/' in topic:
            return MXProtocolType.Super.CP_SERVICE_LIST
        # EM
        elif 'EM/VERIFY_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_VERIFY_SCENARIO
        elif 'EM/ADD_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_ADD_SCENARIO
        elif 'EM/RUN_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_RUN_SCENARIO
        elif 'EM/STOP_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_STOP_SCENARIO
        elif 'EM/UPDATE_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_UPDATE_SCENARIO
        elif 'EM/DELETE_SCENARIO/' in topic:
            return MXProtocolType.WebClient.EM_DELETE_SCENARIO
        elif 'EM/ADD_TAG/' in topic:
            return MXProtocolType.WebClient.EM_ADD_TAG
        elif 'EM/ADD_TAG/' in topic:
            return MXProtocolType.WebClient.EM_DELETE_TAG
        elif 'EM/SET_ACCESS/' in topic:
            return MXProtocolType.WebClient.EM_SET_ACCESS
        elif 'EM/GET_TREE/' in topic:
            return MXProtocolType.WebClient.EM_GET_TREE
        elif 'EM/REFRESH/' in topic:
            return MXProtocolType.WebClient.EM_REFRESH
        # ME
        elif 'ME/RESULT/VERIFY_SCENARIO/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_VERIFY_SCENARIO
        elif 'ME/RESULT/SCHEDULE_SCENARIO/' in topic:
            # ME_RESULT_ADD_SCENARIO, ME_RESULT_UPDATE_SCENARIO is same as ME_RESULT_SCHEDULE_SCENARIO
            return MXProtocolType.WebClient.ME_RESULT_SCHEDULE_SCENARIO
        elif 'ME/RESULT/RUN_SCENARIO/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_RUN_SCENARIO
        elif 'ME/RESULT/STOP_SCENARIO/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_STOP_SCENARIO
        elif 'ME/RESULT/DELETE_SCENARIO/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_DELETE_SCENARIO
        elif 'ME/RESULT/ADD_TAG/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_ADD_TAG
        elif 'ME/RESULT/ADD_TAG/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_DELETE_TAG
        elif 'ME/RESULT/SET_ACCESS/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_SET_ACCESS
        elif 'ME/RESULT/GET_TREE/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_GET_TREE
        elif 'ME/RESULT/SERVICE_LIST/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_SERVICE_LIST
        elif 'ME/RESULT/SCENARIO_LIST/' in topic:
            return MXProtocolType.WebClient.ME_RESULT_SCENARIO_LIST
        elif 'ME/NOTIFY_CHANGE/' in topic:
            return MXProtocolType.WebClient.ME_NOTIFY_CHANGE
        # TM/SN
        elif 'TM/SN/REGISTER/VALUE/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_VALUE
        elif 'TM/SN/REGISTER/VALUEDESC/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_VALUEDESC
        elif 'TM/SN/REGISTER/VALUETAG/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_VALUETAG
        elif 'TM/SN/REGISTER/FUNCTION/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_FUNCTION
        elif 'TM/SN/REGISTER/FUNCTIONDESC/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_FUNCTIONDESC
        elif 'TM/SN/REGISTER/FUNCTIONTAG/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_FUNCTIONTAG
        elif 'TM/SN/REGISTER/ARGUMENT/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_ARGUMENT
        elif 'TM/SN/REGISTER/ALIVECYCLE/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_ALIVECYCLE
        elif 'TM/SN/REGISTER/FINISH/' in topic:
            return MXProtocolType.SN.TM_SN_REGISTER_FINISH
        else:
            return None


class MXRangeType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    ALL = auto()
    SINGLE = auto()

    @classmethod
    def get(cls, name: str) -> 'MXRangeType':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class HierarchyType(Enum):
    LOCAL = 0
    PARENT = 1
    CHILD = 2


class MXServiceType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    VALUE = auto()
    FUNCTION = auto()

    @classmethod
    def get(cls, name: str) -> 'MXServiceType':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED
