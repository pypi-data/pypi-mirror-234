from big_thing_py.common import *
from big_thing_py.core.request import *
from big_thing_py.core.mqtt_message import *
from big_thing_py.core.argument import *
from big_thing_py.core.service import *

from func_timeout import StoppableThread, FunctionTimedOut
import threading


class MXFunction(MXService):
    def __init__(
        self,
        func: Callable,
        tag_list: List[MXTag],
        return_type: MXType,
        name: str = '',
        energy: float = 0,
        desc: str = '',
        thing_name: str = '',
        middleware_name: str = '',
        arg_list: List[MXArgument] = [],
        exec_time: float = 0,
        timeout: float = 0,
        range_type: MXRangeType = MXRangeType.SINGLE,
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

        self._return_type = return_type
        self._arg_list = arg_list
        self._exec_time = exec_time
        self._timeout = timeout
        # TODO: range_type will be removed from MXFunction
        self._range_type = range_type

        self._return_value = None
        self._running = False
        self._running_scenario_list: List[str] = []

        # Queue
        self._publish_queue: Queue = None

        if self._return_type in [MXType.UNDEFINED]:
            raise MXValueError('return_type cannot be undefined')
        if (not len(self._arg_list) == len(get_function_info(self._func)['args'])) if self._func else False:
            raise MXValueError('Length of argument list must be same with callback function')

        # TODO: return type detection feature
        # if not self._return_type or self._return_type in [MXType.UNDEFINED]:
        #     func_info = get_function_info(self._func)
        #     self._return_type = MXType().get(func_info[2])
        #     raise MXValueError('type must be specified')
        # elif self._return_type in [MXType.UNDEFINED]:
        #     raise MXValueError('type cannot be undefined or void')

    def __eq__(self, o: 'MXFunction') -> bool:
        instance_check = isinstance(o, MXFunction)
        arg_list_check = o._arg_list == self._arg_list
        return_type_check = o._return_type == self._return_type
        exec_time_check = o._exec_time == self._exec_time
        timeout_check = o._timeout == self._timeout
        range_type_check = o._range_type == self._range_type

        return (
            super().__eq__(o)
            and instance_check
            and arg_list_check
            and return_type_check
            and exec_time_check
            and timeout_check
            and range_type_check
        )

    def __getstate__(self):
        state = super().__getstate__()

        state['_return_type'] = self._return_type
        state['_arg_list'] = self._arg_list
        state['_exec_time'] = self._exec_time
        state['_timeout'] = self._timeout
        state['_range_type'] = self._range_type

        del state['_return_value']
        del state['_running']
        del state['_publish_queue']
        del state['_running_scenario_list']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._type = state['_type']
        self._min = state['_min']
        self._max = state['_max']
        self._cycle = state['_cycle']
        self._format = state['_format']

        self._return_value = None
        self._running = False
        self._publish_queue = None
        self._running_scenario_list = []

    def _wrapper(self, execute_request: MXExecuteRequest) -> bool:
        execute_msg = execute_request.trigger_msg
        MXLOG_DEBUG(f'[FUNC RUN] run {self._name} function by {execute_msg.scenario}', 'green')

        try:
            if not isinstance(execute_msg, MXExecuteMessage):
                raise Exception(
                    f'[{get_current_function_name()}] Wrong ExecuteMessage type - execute_msg: {type(execute_msg)}'
                )

            self._running = True
            error = MXErrorCode.NO_ERROR

            if self._timeout:
                # self._return_value = func_timeout(self._timeout, self._func, args=(*execute_msg.tuple_arguments(), ))
                current_thread = threading.current_thread()
                self._return_value = self._run_with_timeout(
                    timeout=self._timeout,
                    func=self._func,
                    name=current_thread.name,
                    user_data=dict(scenario=execute_msg.scenario),
                    args=(*execute_msg.tuple_arguments(),),
                )
            else:
                self._return_value = self._func(*execute_msg.tuple_arguments())
        except KeyboardInterrupt as e:
            # TODO: for wrapup main thread, but not test it yet
            print_error(e)
            MXLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except FunctionTimedOut as e:
            MXLOG_DEBUG(
                f'[FUNC TIMEOUT] function {self._name} by scenario {execute_msg.scenario} was timeout!!!', 'yellow'
            )
            error = MXErrorCode.TIMEOUT
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(
                f'[FUNC FAIL] function {self._name} by scenario {execute_msg.scenario} is failed while executing!!!',
                'red',
            )
            error = MXErrorCode.FAIL
        else:
            error = MXErrorCode.NO_ERROR
        finally:
            # result_msg = MXExecuteResultMessage(function=self,
            #                                      scenario=execute_msg.scenario,
            #                                      request_ID=execute_request.trigger_msg.request_ID,
            #                                      error=error)
            # execute_request.set_return_msg(result_msg)
            self._send_TM_RESULT_EXECUTE(scenario=execute_msg.scenario, error=error, request_ID=execute_msg.request_ID)

            execute_request.timer_end()
            self._running = False
            self._running_scenario_list.remove(execute_msg.scenario)
            MXLOG_DEBUG(
                f'[FUNC END] function {self._name} end. -> return value : {self._return_value}, duration: {execute_request.duration():.4f} Sec',
                'green',
            )

    def start_execute_thread(self, execute_msg: MXExecuteMessage) -> MXThread:
        execute_result_msg = MXExecuteResultMessage(function=self, scenario=execute_msg.scenario)
        execute_request = MXExecuteRequest(trigger_msg=execute_msg, result_msg=execute_result_msg)
        self._running_scenario_list.append(execute_msg.scenario)
        execute_request.timer_start()

        execute_thread = MXThread(
            target=self._wrapper,
            name=f'{self._func.__name__}_{execute_msg.scenario}_thread',
            daemon=True,
            args=(execute_request,),
        )
        execute_thread.start()

        return execute_thread

    def _run_with_timeout(
        self,
        timeout: float,
        func: Callable,
        name: str = '',
        user_data: dict = None,
        args: tuple = (),
        kwargs: dict = None,
    ):
        if not kwargs:
            kwargs = {}
        if not args:
            args = ()

        ret = []
        exception = []
        isStopped = False

        def funcwrap(args2, kwargs2):
            try:
                ret.append(func(*args2, **kwargs2))
            except FunctionTimedOut:
                # Don't print traceback to stderr if we time out
                pass
            except Exception as e:
                exc_info = sys.exc_info()
                if isStopped is False:
                    # Assemble the alternate traceback, excluding this function
                    #  from the trace (by going to next frame)
                    # Pytohn3 reads native from __traceback__,
                    # python2 has a different form for "raise"
                    e.__traceback__ = exc_info[2].tb_next
                    exception.append(e)

        thread = StoppableThread(target=funcwrap, name=name, args=(args, kwargs))
        thread.daemon = True
        thread.user_data = user_data

        thread.start()
        thread.join(timeout)

        stopException = None
        if thread.is_alive():
            isStopped = True

            class FunctionTimedOutTempType(FunctionTimedOut):
                def __init__(self):
                    return FunctionTimedOut.__init__(self, '', timeout, func, args, kwargs)

            FunctionTimedOutTemp = type(
                'FunctionTimedOut' + str(hash("%d_%d_%d_%d" % (id(timeout), id(func), id(args), id(kwargs)))),
                FunctionTimedOutTempType.__bases__,
                dict(FunctionTimedOutTempType.__dict__),
            )

            stopException = FunctionTimedOutTemp
            thread._stopThread(stopException)
            thread.join(min(0.1, timeout / 50.0))
            raise FunctionTimedOut('', timeout, func, args, kwargs)
        else:
            # We can still cleanup the thread here..
            # Still give a timeout... just... cuz..
            thread.join(0.5)

        if exception:
            raise exception[0] from None

        if ret:
            return ret[0]

    def _send_TM_RESULT_EXECUTE(self, scenario: str, error: MXErrorCode, request_ID: str = None) -> None:
        execute_result_msg = self.generate_execute_result_message(scenario=scenario, error=error, request_ID=request_ID)
        execute_result_mqtt_msg = execute_result_msg.mqtt_message()
        self._publish_queue.put(execute_result_mqtt_msg)

    def dict(self) -> dict:
        return {
            "name": self._name,
            "description": self._desc,
            "exec_time": self._exec_time * 1000 if self._exec_time is not None else 0,
            "return_type": self._return_type.value,
            "energy": self._energy,
            "tags": [tag.dict() for tag in self._tag_list],
            "use_arg": 1 if self._arg_list else 0,
            "arguments": [argument.dict() for argument in self._arg_list] if self._arg_list else [],
        }

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_execute_result_message(
        self, scenario: str, error: MXErrorCode, request_ID: str
    ) -> MXExecuteResultMessage:
        execute_result_msg = MXExecuteResultMessage(
            function=self, scenario=scenario, request_ID=request_ID, error=error
        )
        return execute_result_msg

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

    def get_exec_time(self) -> float:
        return self._exec_time

    def get_timeout(self) -> float:
        return self._timeout

    def get_arg_list(self) -> List[MXArgument]:
        return self._arg_list

    def get_return_type(self) -> MXType:
        return self._return_type

    def get_return_value(self) -> Union[int, float, str, bool]:
        return self._return_value

    def get_running(self) -> bool:
        return self._running

    def get_range_type(self) -> MXRangeType:
        return self._range_type

    def get_running_scenario_list(self) -> List[str]:
        return self._running_scenario_list

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_exec_time(self, exec_time: float) -> None:
        self._exec_time = exec_time

    def set_timeout(self, timeout: float) -> None:
        self._timeout = timeout

    def set_arg_list(self, arg_list: List[MXArgument]) -> None:
        self._arg_list = arg_list

    def set_return_type(self, return_type: MXType) -> None:
        self._return_type = return_type

    def set_return_value(self, return_value: Union[int, float, str, bool]) -> None:
        self._return_value = return_value

    def set_running(self, running: bool) -> None:
        self._running = running

    def set_range_type(self, range_type: MXRangeType) -> None:
        self._range_type = range_type

    # for link to big_thing's publish_queue
    def set_publish_queue(self, queue: Queue):
        self._publish_queue = queue
