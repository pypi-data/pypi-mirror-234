from big_thing_py.core.function import *
from big_thing_py.core.value import *


class MXThing:
    DEFAULT_NAME = 'default_big_thing'

    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool,
        is_parallel: bool,
        middleware_name: str = None,
    ):
        # base info
        self._name = name
        self._service_list = service_list
        self._alive_cycle = alive_cycle
        self._is_super = is_super
        self._is_parallel = is_parallel
        self._middleware_name = middleware_name

        self._last_alive_time = 0
        self._is_connected = False
        self._is_registered = False
        self._subscribed_topic_set: Set[str] = set()
        self._function_list: List[MXFunction] = []
        self._value_list: List[MXValue] = []

        # Queue
        self._receive_queue: Queue = Queue()
        self._publish_queue: Queue = Queue()

        if not self._name:
            self._name = MXThing.DEFAULT_NAME
        elif not check_valid_identifier(self._name):
            raise MXValueError(
                f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}'
            )

        if self._alive_cycle <= 0:
            raise MXValueError(f'alive cycle must be greater than 0')

        for service in self._service_list:
            if isinstance(service, (MXFunction, MXValue)):
                self.add_service(service)
            else:
                raise MXTypeError(f'service_list must contain MXFunction or MXValue object')

    def __eq__(self, o: 'MXThing') -> bool:
        instance_check = isinstance(o, MXThing)
        name_check = o._name == self._name
        service_list_check = (o._function_list == self._function_list) and (o._value_list == self._value_list)
        alive_cycle_check = o._alive_cycle == self._alive_cycle
        is_super_check = o._is_super == self._is_super
        is_parallel_check = o._is_parallel == self._is_parallel

        return (
            instance_check
            and name_check
            and service_list_check
            and alive_cycle_check
            and is_super_check
            and is_parallel_check
        )

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['_last_alive_time']
        del state['_is_connected']
        del state['_is_registered']
        del state['_subscribed_topic_set']
        del state['_receive_queue']
        del state['_publish_queue']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self._last_alive_time = 0
        self._is_connected = False
        self._is_registered = False
        self._subscribed_topic_set = set()
        self._receive_queue = Queue()
        self._publish_queue = Queue()

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _get_function(self, function_name: str) -> MXFunction:
        for function in self._function_list:
            if function.get_name() == function_name:
                return function

    def add_service(self, service: MXService) -> 'MXThing':
        # service_copy = copy.deepcopy(service)
        # service_copy = copy.copy(service)
        service.add_tag(MXTag(name=self._name))
        service.set_thing_name(self._name)

        if isinstance(service, MXFunction):
            service.set_publish_queue(self._publish_queue)
            self._function_list.append(service)
        elif isinstance(service, MXValue):
            self._value_list.append(service)
            value_getter_function = MXFunction(
                func=service.get_func(),
                return_type=service.get_type(),
                name=f'__{service.get_name()}',
                tag_list=service.get_tag_list(),
                energy=service.get_energy(),
                desc=service.get_desc(),
                thing_name=service.get_thing_name(),
                middleware_name=service.get_middleware_name(),
                arg_list=[],
            )
            self._function_list.append(value_getter_function)
        self._value_list = sorted(self._value_list, key=lambda x: x.get_name())
        self._function_list = sorted(self._function_list, key=lambda x: x.get_name())

        return self

    def dict(self) -> dict:
        return {
            "name": self._name,
            "alive_cycle": self._alive_cycle,
            "is_super": self._is_super,
            "is_parallel": self._is_parallel,
            "values": [value.dict() for value in self._value_list],
            "functions": [function.dict() for function in self._function_list],
        }

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    def get_name(self) -> str:
        return self._name

    def get_middleware_name(self) -> str:
        return self._middleware_name

    def get_last_alive_time(self) -> float:
        return self._last_alive_time

    def get_alive_cycle(self) -> float:
        return self._alive_cycle

    def get_subscribed_topic_set(self) -> Set[str]:
        return self._subscribed_topic_set

    def get_registered(self) -> bool:
        return self._is_registered

    def get_function_list(self) -> List[MXFunction]:
        return self._function_list

    def get_value_list(self) -> List[MXValue]:
        return self._value_list

    def get_is_super(self) -> bool:
        return self._is_super

    def get_is_parallel(self) -> bool:
        return self._is_parallel

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_name(self, name: str) -> None:
        self._name = name
        for service in self._value_list + self._function_list:
            service.set_thing_name(name)

    def set_middleware_name(self, middleware_name: str) -> None:
        self._middleware_name = middleware_name
        for service in self._value_list + self._function_list:
            service.set_middleware_name(middleware_name)

    def set_last_alive_time(self, last_alive_time: float) -> None:
        self._last_alive_time = last_alive_time

    def set_alive_cycle(self, alive_cycle: float) -> None:
        self._alive_cycle = alive_cycle

    def set_subscribe_topic_set(self, subscribe_topic_set: Set[str]) -> None:
        self._subscribed_topic_set = subscribe_topic_set

    def set_registered(self, registered: bool) -> None:
        self._is_registered = registered

    def set_function_list(self, function_list: List[MXFunction]) -> None:
        self._function_list = function_list

    def set_value_list(self, value_list: List[MXValue]) -> None:
        self._value_list = value_list

    def set_is_super(self, is_super: bool) -> bool:
        self._is_super = is_super

    def set_is_parallel(self, is_parallel: bool) -> bool:
        self._is_parallel = is_parallel

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_thing_id(self, name: str, append_mac_address: bool, interface: str = None) -> str:
        mac_address = get_mac_address(interface=interface)

        if not check_valid_identifier(name):
            raise MXValueError(
                f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}'
            )

        if not append_mac_address:
            return f'{name}'
        elif mac_address:
            return f'{name}_{mac_address}'
        else:
            mac = [random.randint(0x00, 0xFF) for _ in range(6)]
            rand_mac_address = ''.join(map(lambda x: "%02x" % x, mac)).upper()
            return f'{name}_{rand_mac_address}'

    def generate_register_message(self) -> MXRegisterMessage:
        if self._is_super:
            for function in self._function_list:
                if not hasattr(function, '_sub_service_request_list'):
                    return False
        else:
            for function in self._function_list:
                if hasattr(function, '_sub_service_request_list'):
                    return False

        for function in self._function_list:
            for arg in function.get_arg_list():
                bound = arg.get_bound()
                if not arg._name:
                    return False
                if bound[1] - bound[0] <= 0:
                    return False

        for value in self._value_list:
            bound = value.get_bound()
            if bound[1] - bound[0] <= 0:
                return False

        register_msg = MXRegisterMessage(thing=self)
        return register_msg

    def generate_unregister_message(self) -> MXUnregisterMessage:
        return MXUnregisterMessage(thing=self)

    def generate_alive_message(self) -> MXAliveMessage:
        return MXAliveMessage(thing=self)

    def generate_value_publish_message(self, value: MXValue) -> MXValuePublishMessage:
        return MXValuePublishMessage(thing=self, value=value)

    # need for middleware detect
    def generate_client_refresh_message(self) -> MXClientRefreshMessage:
        return MXClientRefreshMessage(thing=self)
