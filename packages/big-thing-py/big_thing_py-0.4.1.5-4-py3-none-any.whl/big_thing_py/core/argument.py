from big_thing_py.utils import *


class MXArgument:
    def __init__(self, name: str, type: MXType, bound: Tuple[float, float]):
        self._name = name
        self._type = type
        self._min, self._max = bound

        if not check_valid_identifier(self._name):
            raise MXValueError(
                f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}'
            )

        if self._min >= self._max:
            raise MXValueError('bound must be min < max')

        if self._type in [MXType.UNDEFINED, MXType.VOID]:
            raise MXValueError('type cannot be undefined or void')

    def __str__(self) -> str:
        return self._name

    def __eq__(self, o: 'MXArgument') -> bool:
        instance_check = isinstance(o, MXArgument)
        name_check = o._name == self._name
        type_check = o._type == self._type
        min_check = o._min == self._min
        max_check = o._max == self._max

        return instance_check and name_check and type_check and min_check and max_check

    def dict(self) -> dict:
        return {'name': self._name, 'type': self._type.value, 'bound': {'min_value': self._min, 'max_value': self._max}}

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> MXType:
        return self._type

    def get_bound(self) -> Tuple[float, float]:
        return self._min, self._max

    def set_name(self, name: str):
        self._name = name

    def set_type(self, type: MXType):
        self._type = type

    def set_bound(self, bound: Tuple[float, float]):
        self._min = bound[0]
        self._max = bound[1]
