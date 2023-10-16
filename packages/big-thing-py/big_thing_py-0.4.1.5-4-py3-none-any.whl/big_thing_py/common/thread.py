from big_thing_py.common.common import *

from threading import Thread, Event, Lock
from queue import Queue, Empty


class MXThread:
    class Mode(Enum):
        LOCK = 0
        EVENT = 1

    def __init__(
        self,
        name: str = None,
        target: Callable = None,
        args: Tuple = None,
        kwargs: dict = None,
        daemon: bool = True,
        mode: List[str] = [],
    ) -> None:
        self._name: str = name
        self._target: Callable = target
        self._args: Tuple = args
        self._kwargs: dict = kwargs
        self._daemon: List[str] = daemon

        self._thread = Thread()

        if target:
            self.set_thread()
        else:
            raise Exception('[MXThread] No function to run')

    def set_thread(self) -> None:
        if isinstance(self._args, tuple):
            self._args: list = list(self._args)
        else:
            self._args = []

        self._args = tuple(self._args)

        if not self._name:
            self._name = '_'.join(self._target.__name__.split('_')[:-1])

        if self._kwargs:
            self._thread = Thread(target=self._target, name=self._name, kwargs=self._kwargs, daemon=self._daemon)
        else:
            self._thread = Thread(target=self._target, name=self._name, args=self._args, daemon=self._daemon)

    def start(self) -> None:
        self._thread.start()

    def join(self) -> None:
        self._thread.join()

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def get_name(self) -> str:
        return self._name
