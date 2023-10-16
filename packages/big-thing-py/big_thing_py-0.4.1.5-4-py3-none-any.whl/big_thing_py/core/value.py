from big_thing_py.core.service import *


class MXValue(MXService):
    def __init__(
        self,
        func: Callable,
        tag_list: List[MXTag],
        type: MXType,
        bound: Tuple[float, float],
        cycle: float,
        name: str = '',
        energy: float = 0,
        desc: str = '',
        thing_name: str = '',
        middleware_name: str = '',
        format: str = '',
    ) -> None:
        super().__init__(
            func=func,
            tag_list=tag_list,
            name=name,
            energy=energy,
            desc=desc,
            thing_name=thing_name,
            middleware_name=middleware_name,
        )

        self._type = type
        self._min, self._max = bound
        self._cycle = cycle
        self._format = format

        self._last_value: Union[float, str, bool] = None
        self._last_update_time: float = 0
        self._binary_sending: bool = False

        if len(get_function_info(self._func)['args']) > 0 or get_function_info(self._func)['return_type'] == None:
            raise MXValueError('callback function must not have any argument and must return value')
        if self._min >= self._max:
            raise MXValueError('bound must be min < max')
        if self._type in [MXType.UNDEFINED, MXType.VOID]:
            raise MXValueError('type cannot be undefined or void')
        if (self._cycle <= 0) if self._cycle != None else False:
            raise MXValueError('cycle must be > 0')
        if not isinstance(self._format, str):
            raise MXValueError('format must be str')

    def __eq__(self, o: 'MXValue') -> bool:
        instance_check = isinstance(o, MXValue)
        type_check = o._type == self._type
        bound_check = o._max == self._max and o._min == self._min
        format_check = o._format == self._format
        cycle_check = o._cycle == self._cycle

        return super().__eq__(o) and instance_check and type_check and bound_check and format_check and cycle_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_type'] = self._type
        state['_min'] = self._min
        state['_max'] = self._max
        state['_cycle'] = self._cycle
        state['_format'] = self._format

        del state['_last_value']
        del state['_last_update_time']
        del state['_binary_sending']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._type = state['_type']
        self._min = state['_min']
        self._max = state['_max']
        self._cycle = state['_cycle']
        self._format = state['_format']

        self._last_value = None
        self._last_update_time = 0
        self._binary_sending = False

    def update(self, *arg_list, **kwargs) -> Union[int, float, str, bool]:
        try:
            new_value = self._func(*arg_list, **kwargs)
            self._last_update_time = get_current_time()

            if not self._last_value == new_value:
                self._last_value = new_value
                return new_value
            else:
                return None
        except Exception as e:
            print_error(e)
            return None

    def dict(self) -> dict:
        return {
            "name": self._name,
            "description": self._desc,
            "tags": [tag.dict() for tag in self._tag_list],
            "type": self._type.value,
            "bound": {"min_value": self._min, "max_value": self._max},
            "format": self._format,
        }

    def publish_dict(self) -> dict:
        return {"type": self._type.value, "value": self._last_value}

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

    def get_type(self) -> MXType:
        return self._type

    def get_bound(self) -> Tuple[float, float]:
        return (self._min, self._max)

    def get_max(self) -> float:
        return self._max

    def get_min(self) -> float:
        return self._min

    def get_cycle(self) -> float:
        return self._cycle

    def get_format(self) -> str:
        return self._format

    def get_last_value(self) -> float:
        return self._last_value

    def get_last_update_time(self) -> float:
        return self._last_update_time

    def get_func(self) -> Callable:
        return self._func

    def get_binary_sending(self) -> bool:
        return self._binary_sending

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_type(self, type: MXType) -> None:
        self._type = type

    def set_bound(self, bound: Tuple[float, float]) -> None:
        self._min = bound[0]
        self._max = bound[1]

    def set_max(self, max: float) -> None:
        self._max = max

    def set_min(self, min: float) -> None:
        self._min = min

    def set_cycle(self, cycle: float) -> None:
        self._cycle = cycle

    def set_format(self, format: str) -> None:
        self._format = format

    def set_last_value(self, last_value: Union[float, str, bool]) -> None:
        self._last_value = last_value

    def set_last_update_time(self, last_update_time: float) -> None:
        self._last_update_time = last_update_time

    def set_func(self, func: Callable) -> None:
        self._func = func

    def set_binary_sending(self, binary_send: bool) -> bool:
        self._binary_sending = binary_send
