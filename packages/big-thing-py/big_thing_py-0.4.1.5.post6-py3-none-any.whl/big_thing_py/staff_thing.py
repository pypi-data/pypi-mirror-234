from big_thing_py.core.thing import *
import functools


class MXStaffThing(MXThing, metaclass=ABCMeta):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
    ):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel)
        self._staff_thing_id = staff_thing_id
        self._is_connected = False

        self._receive_queue: Queue = Queue()
        self._publish_queue: Queue = Queue()

    def __eq__(self, o: 'MXStaffThing') -> bool:
        instance_check = isinstance(o, MXStaffThing)
        staff_thing_id_check = o._staff_thing_id == self._staff_thing_id

        return super().__eq__(o) and instance_check and staff_thing_id_check

    def get_staff_thing_id(self) -> str:
        return self._staff_thing_id

    def set_staff_thing_id(self, id: str) -> None:
        self._staff_thing_id = id

    def is_connected(self) -> bool:
        return self._is_connected

    def set_function_result_queue(self, queue: Queue) -> None:
        for function in self._function_list:
            function.set_publish_queue(queue)

    def print_func_info(func: Callable):
        @functools.wraps(func)  # save function metadata
        def wrap(self: MXStaffThing, *args, **kwargs):
            MXLOG_DEBUG(f'{func.__name__} at {self._name} actuate!!!', 'green')
            ret = func(self, *args, **kwargs)
            return ret

        # TODO: 함수가 데코레이팅 되었으면 staff thing의 service list에 추가하는 기능을 구현하고자 추가함
        # TODO: 근데 위에 @functools.wraps(func)기능과 동시에 사용이 가능한지 확인해야함
        wrap.is_decorated = True
        return wrap

    def add_staff_service(self, service_list: List[MXService]):
        for staff_service in service_list:
            self.add_service(staff_service)

    @abstractmethod
    def make_service_list(self):
        pass
