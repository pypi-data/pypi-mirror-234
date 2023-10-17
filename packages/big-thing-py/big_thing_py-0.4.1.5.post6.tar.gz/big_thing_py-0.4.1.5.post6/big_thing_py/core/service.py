from big_thing_py.core.tag import *
from abc import *


class MXService(metaclass=ABCMeta):
    def __init__(
        self,
        name: str,
        func: Callable,
        tag_list: List[MXTag],
        energy: float,
        desc: str,
        thing_name: str,
        middleware_name: str,
    ) -> None:
        self._name = name
        self._func = func
        self._tag_list = tag_list
        self._energy = energy
        self._desc = desc
        self._thing_name = thing_name
        self._middleware_name = middleware_name

        if not callable(self._func):
            raise MXValueError(f'func must be callable')
        if not self._name:
            self._name = func.__name__
        if not check_valid_identifier(self._name):
            raise MXValueError(
                f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}'
            )
        if any([not isinstance(tag, MXTag) for tag in self._tag_list]) or len(self._tag_list) == 0:
            raise MXValueError('tag_list must contain MXTag object')
        else:
            self._tag_list = [MXTag(name=tag) for tag in sorted(list(set(self.get_tag_list(string_mode=True))))]
        if not isinstance(self._energy, (int, float)):
            raise MXValueError(f'energy must be int or float')
        if not isinstance(self._desc, str):
            raise MXValueError(f'desc must be str')
        if not isinstance(self._thing_name, str):
            raise MXValueError(f'thing_name must be str')
        if not isinstance(self._middleware_name, str):
            raise MXValueError(f'middleware_name must be str')

    def __eq__(self, o: 'MXService') -> bool:
        instance_check = isinstance(o, MXService)
        name_check = o._name == self._name
        thing_name_check = o._thing_name == self._thing_name
        middleware_name_check = o._middleware_name == self._middleware_name
        tag_list_check = o._tag_list == self._tag_list
        func_check = o._func == self._func
        energy_check = o._energy == self._energy

        return (
            instance_check
            and name_check
            and thing_name_check
            and middleware_name_check
            and tag_list_check
            and func_check
            and energy_check
        )

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['_func']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self._func = None

    def add_tag(self, tag: Union[MXTag, List[MXTag]]) -> 'MXService':
        if not isinstance(tag, (MXTag, list)):
            raise Exception('tag must be MXTag object')

        if isinstance(tag, MXTag):
            if not tag in self._tag_list:
                self._tag_list.append(tag)
        elif all(isinstance(t, MXTag) for t in tag):
            for t in tag:
                if not t in self._tag_list:
                    self._tag_list.append(t)
        self._tag_list = sorted(self._tag_list, key=lambda x: x.get_name())

        return self

    def remove_tag(self, tag: str) -> 'MXService':
        if not isinstance(tag, str):
            raise Exception('tag to remove must be str')

        for t in self._tag_list:
            if t.get_name() == tag:
                self._tag_list.remove(MXTag(tag))

    @abstractmethod
    def dict(self) -> dict:
        pass

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

    def get_thing_name(self) -> str:
        return self._thing_name

    def get_middleware_name(self) -> str:
        return self._middleware_name

    def get_tag_list(self, string_mode: bool = False) -> List[MXTag]:
        if string_mode:
            return [str(tag) for tag in self._tag_list]
        else:
            return self._tag_list

    def get_desc(self) -> str:
        return self._desc

    def get_func(self) -> Callable:
        return self._func

    def get_energy(self) -> float:
        return self._energy

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

    def set_thing_name(self, thing_name: str) -> None:
        self._thing_name = thing_name

    def set_middleware_name(self, middleware_name: str) -> None:
        self._middleware_name = middleware_name

    def set_tag_list(self, tag_list: List[MXTag]) -> None:
        self._tag_list = tag_list

    def set_desc(self, desc: str) -> None:
        self._desc = desc

    def set_func(self, func: Callable) -> None:
        self._func = func

    def set_energy(self, energy: float) -> None:
        self._energy = energy
