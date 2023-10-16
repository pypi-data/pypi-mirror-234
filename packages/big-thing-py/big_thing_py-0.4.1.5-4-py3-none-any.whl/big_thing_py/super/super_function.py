from big_thing_py.super.super_request import *
from big_thing_py.super.super_mqtt_message import *


class MXSuperFunction(MXFunction):
    '''
    [Whole super service structure]
    super_thing┬── super_service1┬── sub_service1┬────── target_thing1(at Middleware1)
               │                  │               ╲
               │                  │                ╲──── target_thing2(at Middleware1)
               │                  │                 ╲
               │                  │                  ╲── target_thing3(at Middleware2)
               │                  │                   ╲
               │                  ├── sub_service2      ╲ ....
               │                  │
               │                  ├── ...
               │
               │
               └── super_service2 ── sub_service1(target Thing1, target Middleware2)
    '''

    def __init__(
        self,
        func: Callable,
        return_type: MXType,
        name: str = '',
        tag_list: List[MXTag] = [],
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
            return_type=return_type,
            name=name,
            tag_list=tag_list,
            energy=energy,
            desc=desc,
            thing_name=thing_name,
            middleware_name=middleware_name,
            arg_list=arg_list,
            exec_time=exec_time,
            timeout=timeout,
            range_type=range_type,
        )

        # 사용자가 super thing코드에 명세한 sub_service 조건에 맞는 sub_service 종류. 해당 조건에 맞는 sub_service 여러 디바이스에 여러 개 존재할 수 있다.
        # super service에 명세된 req() 라인 수 만큼 존재한다.
        self._sub_service_request_list: List[MXSubServiceRequest] = []

        # SuperService 안에 있는 req()들에 대한 정보가 스캔되었는지 여부. 스캔된 req()들에 대한 정보는 _sub_service_type_list에 저장된다.
        self._is_scanned: bool = False

        # scheduling에 대한 결과를 super thing이 넣어주기 위해 존재함
        #     super_service_request_key: str = make_super_request_key(requester_middleware, scenario)
        #     super_service_request_key: {requester_middleware}@{scenario}, value: MXSuperScheduleRequest
        self._temporary_scheduling_table: Dict[str, MXSuperScheduleRequest] = {}

        # scheduling이 끝나면 해당 scenario에 대해 어떤 sub_service_type에 대해 thing을 선택할 것인지 정해진다.
        # 이렇게 하는 이유는 scenario를 반복해서 돌릴 때마다 다른 thing을 선택하는 것이 아니라 전에 선택했던 thing에 있는 service를 실행하기 위함이다.
        #     super_service_request_key: str = make_super_request_key(requester_middleware, scenario)
        #     super_service_request_key: {requester_middleware}@{scenario}, value: MXSuperExecuteRequest
        self._mapping_table: Dict[str, MXSuperExecuteRequest] = {}

        self._schedule_running: bool = False

        if not inspect.ismethod(func):
            raise MXTypeError('self._func must be a instance method')

    def __eq__(self, o: 'MXSuperFunction') -> bool:
        instance_check = isinstance(o, MXSuperFunction)

        return super().__eq__(o) and instance_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_sub_service_request_list'] = self._sub_service_request_list
        state['_is_scanned'] = self._is_scanned
        state['_temporary_scheduling_table'] = self._temporary_scheduling_table
        state['_mapping_table'] = self._mapping_table

        del state['_schedule_running']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._sub_service_request_list = state['_sub_service_request_list']
        self._is_scanned = state['_is_scanned']
        self._temporary_scheduling_table = state['_temporary_scheduling_table']
        self._mapping_table = state['_mapping_table']

        self._schedule_running = False

    def _add_sub_service_request(self, sub_service_request: MXSubServiceRequest):
        sub_service_request._sub_service_request_order = len(self._sub_service_request_list)
        self._sub_service_request_list.append(sub_service_request)

    def _remove_sub_service_request(self, sub_service_request: MXSubServiceRequest):
        if sub_service_request in self._sub_service_request_list:
            self._sub_service_request_list.remove(sub_service_request)

    def _request_subschedule(self, subschedule_request: MXSubScheduleRequest) -> None:
        subschedule_request.timer_start()
        subschedule_msg = subschedule_request.trigger_msg

        # 필요한 토픽 구독과 발행을 한번에 수행한다.
        if not isinstance(subschedule_request, MXSubScheduleRequest):
            raise MXTypeError(f'Invalid type of subschedule_request: {type(subschedule_request)}')

        self._send_SM_SCHEDULE(subschedule_msg)

    def _select_target_sub_service_by_range_type(
        self, super_schedule_request: MXSuperScheduleRequest, single_select_func: Callable
    ) -> MXSubScheduleRequest:
        for sub_service_request in self._sub_service_request_list:
            sub_service_request_range_type = sub_service_request._sub_service_type.get_range_type()
            sub_service_request_key = make_sub_service_request_key(
                sub_service_name=sub_service_request._sub_service_type.get_name(),
                sub_service_request_order=sub_service_request._sub_service_request_order,
            )
            target_sub_service_request = super_schedule_request._sub_service_request_table[sub_service_request_key]

            if sub_service_request_range_type == MXRangeType.ALL:
                for candidate_request in target_sub_service_request._candidate_request_list:
                    if candidate_request._status == MXScheduleStatus.CHECK:
                        candidate_request._status = MXScheduleStatus.SELECT
            elif sub_service_request_range_type == MXRangeType.SINGLE:
                while True:
                    selected_request = single_select_func(target_sub_service_request._candidate_request_list)
                    if selected_request._status == MXScheduleStatus.CHECK:
                        selected_request._status = MXScheduleStatus.SELECT
                        break

    def _subschedule_parallel(
        self,
        super_schedule_request: MXSuperScheduleRequest,
        target_schedule_status: MXScheduleStatus,
        result_schedule_status: MXScheduleStatus,
    ) -> List[MXSubScheduleRequest]:
        subschedule_start_time = get_current_time()

        # 병렬로 subschedule 요청을 보낸다.
        for sub_service_request in super_schedule_request._sub_service_request_table.values():
            candidate_subschedule_request_list = [
                candidate_request
                for candidate_request in sub_service_request._candidate_request_list
                if candidate_request._status == target_schedule_status
            ]

            for candidate_subschedule_request in candidate_subschedule_request_list:
                # 미들웨어에게 현재 요청인 check 인지 confirm인지 알려주기 위해 trigger_msg에 status를 추가함.
                candidate_subschedule_request.trigger_msg.status = result_schedule_status
                candidate_subschedule_msg = candidate_subschedule_request.trigger_msg
                MXLOG_DEBUG(
                    f'[SUB_SCHEDULE {candidate_subschedule_msg._status.value.upper()} START] '
                    f'{candidate_subschedule_msg.sub_service_name}|{candidate_subschedule_msg.target_thing_name}|'
                    f'{candidate_subschedule_msg.target_middleware_name}',
                    'cyan',
                )
                self._request_subschedule(candidate_subschedule_request)

            # 해당 super service의 sub_service들에게 subschedule 요청을 보낸 후, 모든 subschedule 결과를 받을 때까지 기다린다.
            for candidate_subschedule_request in candidate_subschedule_request_list:
                candidate_subschedule_request.result_msg = candidate_subschedule_request.get_result_msg()
                candidate_subschedule_request._status = result_schedule_status

                candidate_subschedule_request.timer_end()
                MXLOG_DEBUG(
                    f'[SUB_SCHEDULE {candidate_subschedule_request._status.value.upper()} END] '
                    f'{candidate_subschedule_request.trigger_msg.sub_service_name}|{candidate_subschedule_request.trigger_msg.target_thing_name}|'
                    f'{candidate_subschedule_request.trigger_msg.target_middleware_name}, duration: {candidate_subschedule_request.duration():.4f} Sec',
                    'cyan',
                )

                # 굳이 구독 해제를 할 필요가 없다. 재호출될 가능성이 높음.
                # subschedule_result_msg: MXSubScheduleResultMessage = candidate_subschedule_request._result_msg
                # self._unsubscribe_queue.put(subschedule_result_msg.topic)
                # while not self._unsubscribe_queue.empty():
                #     time.sleep(0.001)

        super_schedule_request._status = result_schedule_status
        if super_schedule_request._status == MXScheduleStatus.CHECK:
            super_schedule_request._check_duration = get_current_time() - subschedule_start_time
            MXLOG_DEBUG(
                f'[SUPER_SCHEDULE CHECK END] '
                f'{super_schedule_request.trigger_msg.super_service_name}|{super_schedule_request.trigger_msg.super_thing_name}|'
                f'{super_schedule_request.trigger_msg.super_middleware_name}, duration: {super_schedule_request.confirm_duration():.4f} Sec',
                'green',
            )
        elif super_schedule_request._status == MXScheduleStatus.CONFIRM:
            super_schedule_request._confirm_duration = get_current_time() - subschedule_start_time
            MXLOG_DEBUG(
                f'[SUPER_SCHEDULE CONFIRM END] '
                f'{super_schedule_request.trigger_msg.super_service_name}|{super_schedule_request.trigger_msg.super_thing_name}|'
                f'{super_schedule_request.trigger_msg.super_middleware_name}, duration: {super_schedule_request.confirm_duration():.4f} Sec',
                'green',
            )

    def _check_parallel(self, super_schedule_request: MXSuperScheduleRequest) -> List[MXSubScheduleRequest]:
        self._subschedule_parallel(
            super_schedule_request=super_schedule_request,
            target_schedule_status=MXScheduleStatus.INIT,
            result_schedule_status=MXScheduleStatus.CHECK,
        )

    def _confirm_parallel(self, super_schedule_request: MXSuperScheduleRequest) -> bool:
        self._subschedule_parallel(
            super_schedule_request=super_schedule_request,
            target_schedule_status=MXScheduleStatus.SELECT,
            result_schedule_status=MXScheduleStatus.CONFIRM,
        )

    def _check_sub_service_request_confirm(self, super_schedule_request: MXSuperScheduleRequest) -> bool:
        # 스케쥴링 과정에서 super service의 sub_service_request 중 confirm 된 request가 하나도 없는 sub_service_request가 존재한다면 에러를 발생시킨다.
        for sub_service_request in super_schedule_request._sub_service_request_table.values():
            for candidate_request in sub_service_request._candidate_request_list:
                if candidate_request._status == MXScheduleStatus.CONFIRM:
                    break
            else:
                return False
        else:
            return True

    def _check_confirm_parallel(self, super_schedule_request: MXSuperScheduleRequest) -> bool:
        self._check_parallel(super_schedule_request=super_schedule_request)
        self._select_target_sub_service_by_range_type(
            super_schedule_request=super_schedule_request, single_select_func=lambda x: x[0]
        )
        self._confirm_parallel(super_schedule_request=super_schedule_request)

        return True

    def _print_schedule_result(self, scenario_name: str, requester_middleware_name: str):
        schedule_result_string = '\n[SCHEDULE RESULT] ============================================\n'
        super_request_key = make_super_request_key(
            scenario_name=scenario_name, requester_middleware_name=requester_middleware_name
        )
        for super_k, super_execute_req in self._mapping_table.items():
            if super_k != super_request_key:
                continue
            schedule_result_string += f'super_key: {super_k} -> super_service: {self._name}\n'
            for sub_k, sub_service_req in super_execute_req._sub_service_request_table.items():
                schedule_result_string += (
                    ' ' * 4
                    + f'sub_key: {sub_k} -> sub_service: {sub_service_req._sub_service_type.get_name()}|{sub_service_req._sub_service_request_order}\n'
                )
                for target_req in sub_service_req._target_request_list:
                    schedule_result_string += (
                        ' ' * 8
                        + f'target: {target_req.trigger_msg.sub_service_name}|{target_req.trigger_msg.target_middleware_name}\n'
                    )
        schedule_result_string += '==============================================================\n'
        MXLOG_DEBUG(schedule_result_string, 'green')

    def _super_schedule_wrapper(
        self,
        super_schedule_request: MXSuperScheduleRequest,
        hierarchical_service_table: Dict[str, List[MXService]],
        timeout: float = 1000,
    ):
        '''
        super service의 하위 함수에 대한 정보를 추출한다.
        service_list 구조는

        ============================================
        super_service -> sub_function_type_list
                       -> sub_function_list
        ============================================

        로 이루어져있다.
        sub_function_type_list과 sub_function_list는 독립적인 공간을 가진다.
        super_service 내부에 req함수 가 존재하여 사용자가 요청하고 싶은 sub_service이 명세되어있는데 여기서 명세되어지는
        sub_service은 실제 타겟 sub_service이 아닌 sub_service_type이다. 실제 sub_service 정보는 middleware로 부터 받은
        service_list를 통해 추출한다. 그리고 해당 정보는 super_service의 sub_service_list에 저장된다.
        '''
        if not isinstance(super_schedule_request, MXSuperScheduleRequest):
            raise MXTypeError(f'[{get_current_function_name()}] Wrong Request type: {type(super_schedule_request)}')

        super_schedule_msg = super_schedule_request.trigger_msg
        requester_middleware_name = super_schedule_msg.requester_middleware_name
        scenario = super_schedule_msg.scenario
        super_service_request_key = make_super_request_key(
            scenario_name=scenario, requester_middleware_name=requester_middleware_name
        )

        MXLOG_DEBUG(f'[SUPER_SCHEDULE START] {self._name} by scenario {scenario}.', 'green')

        try:
            super_schedule_request._running = True
            self._schedule_running = True
            error = MXErrorCode.NO_ERROR

            # 후보 sub_service들에 대해서 스케쥴링을 진행한다.
            super_schedule_request.generate_sub_service_schedule_request(
                self._sub_service_request_list, hierarchical_service_table['functions']
            )

            # func_timeout(timeout, self._check_confirm_parallel, args=(super_schedule_request, ))
            current_thread = threading.current_thread()
            self._run_with_timeout(
                timeout=timeout,
                func=self._check_confirm_parallel,
                name=current_thread.name,
                user_data=dict(scenario=super_schedule_msg.scenario, requester_middleware=requester_middleware_name),
                args=(super_schedule_request,),
            )

            # 만약 현재 super service의 sub_service_list가 비어있는 경우 에러를 발생시킨다.
            if len(super_schedule_request._sub_service_request_table) == 0 and len(self._sub_service_request_list) != 0:
                raise Exception(f'No target_sub_service_list found in {self._name} super service')
        except KeyboardInterrupt as e:
            print_error(e)
            MXLOG_DEBUG('Function scheduling exit by user', 'red')
            raise e
        except FunctionTimedOut as e:
            MXLOG_DEBUG(
                f'[SUPER_SCHEDULE TIMEOUT] {super_schedule_request._action_type.value} of {self._name}'
                'by scenario {requester_middleware_name}|{scenario} timeout...',
                'red',
            )

            error = MXErrorCode.TIMEOUT
            return False
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(
                f'[SUPER_SCHEDULE FAILED] {super_schedule_request._action_type.value} of {self._name}'
                'by scenario {requester_middleware_name}|{scenario} failed...',
                'red',
            )

            error = MXErrorCode.FAIL
            return False
        else:
            if not self._check_sub_service_request_confirm(super_schedule_request):
                return False

            super_service_execute_request = MXSuperExecuteRequest(super_schedule_request=super_schedule_request)
            self._mapping_table[super_service_request_key] = super_service_execute_request

            error = error = MXErrorCode.NO_ERROR
            return True
        finally:
            self._send_SM_RESULT_SCHEDULE(
                super_service_name=super_schedule_msg.super_service_name,
                super_thing_name=super_schedule_msg.super_thing_name,
                super_middleware_name=super_schedule_msg.super_middleware_name,
                requester_middleware_name=requester_middleware_name,
                scenario=scenario,
                error=error,
            )

            super_schedule_request.timer_end()
            super_schedule_request._running = False
            self._schedule_running = False
            self._temporary_scheduling_table.pop(super_service_request_key)
            MXLOG_DEBUG(
                f'[SUPER_SCHEDULE END] {self._name} by scenario {scenario}. duration: {super_schedule_request.duration():.4f} Sec',
                'green',
            )
            self._print_schedule_result(scenario_name=scenario, requester_middleware_name=requester_middleware_name)

    def _super_execute_wrapper(self, super_service_execute_request: MXSuperExecuteRequest):
        '''
        super service의 하위 함수에 대한 정보를 추출한다.
        service_list 구조는

        ============================================
        super_service -> sub_function_type_list
                       -> sub_function_list
        ============================================

        로 이루어져있다.
        sub_function_type_list과 sub_function_list는 독립적인 공간을 가진다.
        super_service 내부에 req함수 가 존재하여 사용자가 요청하고 싶은 sub_service이 명세되어있는데 여기서 명세되어지는
        sub_service은 실제 타겟 sub_service이 아닌 sub_service_type이다. 실제 sub_service 정보는 middleware로 부터 받은
        service_list를 통해 추출한다. 그리고 해당 정보는 super_service의 sub_service_list에 저장된다.
        '''

        if not isinstance(super_service_execute_request, MXSuperExecuteRequest):
            raise MXTypeError(
                f'[{get_current_function_name()}] Wrong Request type: {type(super_service_execute_request)}'
            )

        super_execute_msg = super_service_execute_request.trigger_msg
        requester_middleware_name = super_execute_msg.requester_middleware_name
        scenario = super_execute_msg.scenario

        MXLOG_DEBUG(f'[SUPER_EXECUTE START] {self._name} by scenario {scenario}.', 'green')

        try:
            super_service_execute_request._running = True
            self._running = True
            error = MXErrorCode.NO_ERROR

            # super service argument check
            arguments = list(super_execute_msg.tuple_arguments())
            for i, (arg, real_arg) in enumerate(zip(self._arg_list, arguments)):
                if arg.get_type() in [MXType.INTEGER, MXType.DOUBLE] and MXType.get(type(real_arg)) in [
                    MXType.INTEGER,
                    MXType.DOUBLE,
                ]:
                    arguments[i] = float(real_arg)
                elif arg.get_type() != MXType.get(type(real_arg)):
                    raise Exception(
                        f'Argument type is not matched: {arg.get_name()}: {arg.get_type()} != {MXType.get(real_arg)}'
                    )

            if self._timeout:
                # self._return_value = func_timeout(self._timeout, self._func, args=(*tuple(arguments), ))
                current_thread = threading.current_thread()
                self._return_value = self._run_with_timeout(
                    timeout=self._timeout,
                    func=self._func,
                    name=current_thread.name,
                    user_data=dict(scenario=super_execute_msg.scenario, requester_middleware=requester_middleware_name),
                    args=(*tuple(arguments),),
                )
            else:
                self._return_value = self._func(*tuple(arguments))
        except KeyboardInterrupt as e:
            print_error(e)
            MXLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except FunctionTimedOut as e:
            MXLOG_DEBUG(
                f'[SUPER_EXECUTE TIMEOUT] {super_service_execute_request._action_type.value} of {self._name} \
                    by scenario {requester_middleware_name}|{scenario} timeout...',
                'red',
            )

            # Timeout이 발생했다고 해서 mapping_table에서 삭제하지는 않는다.
            # if super_service_execute_request._action_type == MXActionType.SUPER_EXECUTE:
            #     self._mapping_table.pop(super_service_request_key)

            error = MXErrorCode.TIMEOUT
            self._return_value = None
            return False
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(
                f'[SUB_EXECUTE FAILED] {super_service_execute_request._action_type.value} of {self._name} \
                by scenario {requester_middleware_name}|{scenario} failed...',
                'red',
            )

            # Exception이 발생했다고 해서 mapping_table에서 삭제하지는 않는다.
            # if super_service_execute_request._action_type == MXActionType.SUPER_EXECUTE:
            #     self._mapping_table.pop(super_service_request_key)

            error = MXErrorCode.FAIL
            self._return_value = None
            return False
        else:
            error = MXErrorCode.NO_ERROR
            return True
        finally:
            self._send_SM_RESULT_EXECUTE(
                super_service_name=super_execute_msg.super_service_name,
                super_thing_name=super_execute_msg.super_thing_name,
                super_middleware_name=super_execute_msg.super_middleware_name,
                requester_middleware_name=requester_middleware_name,
                scenario=scenario,
                error=error,
            )

            super_service_execute_request.timer_end()
            super_service_execute_request._running = False
            self._running = False
            self._running_scenario_list.remove(super_execute_msg.scenario)
            MXLOG_DEBUG(
                f'[SUPER_EXECUTE END] {self._name} by scenario {scenario}. duration: {super_service_execute_request.duration():.4f} Sec',
                'green',
            )

    def start_super_schedule_thread(
        self,
        super_schedule_msg: MXSuperScheduleMessage,
        hierarchical_service_table: Dict[str, List[MXService]],
        timeout: float = 1000,
    ) -> MXThread:
        super_service_request_key = make_super_request_key(
            scenario_name=super_schedule_msg.scenario,
            requester_middleware_name=super_schedule_msg.requester_middleware_name,
        )
        if super_service_request_key in self._temporary_scheduling_table:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super request with key: {super_service_request_key} is currently in the scheduling phase!',
                'red',
            )
            return False

        super_schedule_result_msg = MXSuperScheduleResultMessage(
            super_service_name=self._name,
            super_thing_name=self._thing_name,
            super_middleware_name=self._middleware_name,
            requester_middleware_name=super_schedule_msg.requester_middleware_name,
            scenario=super_schedule_msg.scenario,
        )
        super_schedule_request = MXSuperScheduleRequest(
            trigger_msg=super_schedule_msg, result_msg=super_schedule_result_msg
        )
        super_service_request_key = make_super_request_key(
            scenario_name=super_schedule_msg.scenario,
            requester_middleware_name=super_schedule_msg.requester_middleware_name,
        )
        self._temporary_scheduling_table[super_service_request_key] = super_schedule_request
        super_schedule_request.timer_start()

        super_schedule_thread = MXThread(
            target=self._super_schedule_wrapper,
            name=f'{self._func.__name__}_{super_schedule_request._action_type.value}_thread',
            daemon=True,
            args=(
                super_schedule_request,
                hierarchical_service_table,
                timeout,
            ),
        )
        super_schedule_thread.start()

        return super_schedule_thread

    def start_super_execute_thread(
        self, super_execute_msg: MXSuperExecuteMessage, SUPER_SERVICE_REQUEST_KEY_TABLE: Dict[str, List[str]]
    ) -> MXThread:
        super_service_request_key = make_super_request_key(
            scenario_name=super_execute_msg.scenario,
            requester_middleware_name=super_execute_msg.requester_middleware_name,
        )
        if super_service_request_key in self._temporary_scheduling_table:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super request with key: {super_service_request_key} is currently in the scheduling phase!',
                'red',
            )
            return False

        super_service_execute_request = self._mapping_table[super_service_request_key]
        if super_service_execute_request._running:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Execute of Super request key: {super_service_request_key} is already executed!',
                'red',
            )
            return False

        super_service_execute_request.trigger_msg = super_execute_msg
        super_service_execute_request.result_msg = MXSuperExecuteResultMessage(
            super_service_name=self._name,
            super_thing_name=self._thing_name,
            super_middleware_name=self._middleware_name,
            requester_middleware_name=super_execute_msg.requester_middleware_name,
            scenario=super_execute_msg.scenario,
            return_type=self._return_type,
        )
        self._running_scenario_list.append(super_execute_msg.scenario)
        super_service_execute_request.timer_start()

        thread_name = f'{self._func.__name__}_{super_execute_msg.scenario}_thread'
        super_execute_thread = MXThread(
            target=self._super_execute_wrapper, name=thread_name, daemon=True, args=(super_service_execute_request,)
        )
        super_execute_thread.start()

        sub_service_request_key_list = list(super_service_execute_request._sub_service_request_table)
        SUPER_SERVICE_REQUEST_KEY_TABLE[super_service_request_key] = sub_service_request_key_list

        return super_execute_thread

    # FIXME: hardcoding 된 부분 수정하기 (DUMMY_ARG_)
    def add_sub_service_request_info(
        self,
        sub_service_name: str,
        arg_list: Union[Tuple[MXArgument], Tuple],
        tag_list: List[MXTag],
        return_type: MXType,
        range_type: MXRangeType,
    ):
        mx_arg_list = [
            arg
            if isinstance(arg, MXArgument)
            else MXArgument(name=f'DUMMY_ARG_{i}', bound=(-sys.maxsize - 1, sys.maxsize), type=MXType.get(type(arg)))
            for i, arg in enumerate(arg_list)
        ]
        sub_service_request_order = len(self._sub_service_request_list)
        sub_service_type = MXFunction(
            name=sub_service_name,
            func=dummy_func(arg_list=mx_arg_list),
            return_type=return_type,
            arg_list=mx_arg_list,
            tag_list=tag_list,
            range_type=range_type,
        )
        sub_service_request = MXSubServiceRequest(
            sub_service_type=sub_service_type, sub_service_request_order=sub_service_request_order
        )
        self._add_sub_service_request(sub_service_request)

        MXLOG_DEBUG(f'sub_service: {sub_service_name}:{sub_service_request_order}', 'green')
        return True

    def put_subschedule_result(
        self,
        super_service_request_key: str,
        sub_service_request_key: str,
        subschedule_result_msg: MXSubScheduleResultMessage,
    ) -> bool:
        if super_service_request_key not in self._temporary_scheduling_table:
            MXLOG_DEBUG(
                f'Could not find key {super_service_request_key} in temporary_scheduling_table... This key is not mine!',
                'yellow',
            )
            return False

        super_schedule_request = self._temporary_scheduling_table[super_service_request_key]
        result = super_schedule_request.put_sub_service_schedule_result_msg(
            sub_service_request_key, subschedule_result_msg
        )
        return result

    def put_sub_service_execute_result(
        self,
        super_service_request_key: str,
        sub_service_request_key: str,
        sub_service_execute_result_msg: MXSubExecuteResultMessage,
    ) -> bool:
        if super_service_request_key not in self._mapping_table:
            MXLOG_DEBUG(
                f'Could not find key {super_service_request_key} in mapping_table... This key is not mine!', 'yellow'
            )
            return False

        super_service_execute_request = self._mapping_table[super_service_request_key]
        result = super_service_execute_request.put_sub_service_execute_result_msg(
            sub_service_request_key, sub_service_execute_result_msg
        )
        return result

    def _send_SM_SCHEDULE(self, subschedule_msg: MXSubScheduleMessage) -> None:
        subschedule_mqtt_msg = subschedule_msg.mqtt_message()
        self._publish_queue.put(subschedule_mqtt_msg)

    def _send_SM_EXECUTE(self, sub_service_execute_msg: MXSubExecuteMessage) -> None:
        sub_service_execute_mqtt_msg = sub_service_execute_msg.mqtt_message()
        self._publish_queue.put(sub_service_execute_mqtt_msg)

    def _send_SM_RESULT_SCHEDULE(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        error: MXErrorCode,
    ) -> None:
        super_schedule_result_msg = self.generate_super_schedule_result_message(
            super_service_name=super_service_name,
            super_thing_name=super_thing_name,
            super_middleware_name=super_middleware_name,
            requester_middleware_name=requester_middleware_name,
            scenario=scenario,
            error=error,
        )
        super_schedule_result_mqtt_msg = super_schedule_result_msg.mqtt_message()
        self._publish_queue.put(super_schedule_result_mqtt_msg)

    def _send_SM_RESULT_EXECUTE(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        error: MXErrorCode,
    ):
        super_execute_result_msg = self.generate_super_execute_result_message(
            super_service_name=super_service_name,
            super_thing_name=super_thing_name,
            super_middleware_name=super_middleware_name,
            requester_middleware_name=requester_middleware_name,
            scenario=scenario,
            error=error,
        )
        super_execute_result_mqtt_msg = super_execute_result_msg.mqtt_message()
        self._publish_queue.put(super_execute_result_mqtt_msg)

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_super_schedule_result_message(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        error: MXErrorCode,
    ) -> MXSuperScheduleResultMessage:
        super_schedule_result_msg = MXSuperScheduleResultMessage(
            super_service_name=super_service_name,
            super_thing_name=super_thing_name,
            super_middleware_name=super_middleware_name,
            requester_middleware_name=requester_middleware_name,
            scenario=scenario,
            error=error,
        )
        return super_schedule_result_msg

    def generate_super_execute_result_message(
        self,
        super_service_name: str,
        super_thing_name: str,
        super_middleware_name: str,
        requester_middleware_name: str,
        scenario: str,
        error: MXErrorCode,
    ) -> MXSuperExecuteResultMessage:
        super_execute_result_msg = MXSuperExecuteResultMessage(
            super_service_name=super_service_name,
            super_thing_name=super_thing_name,
            super_middleware_name=super_middleware_name,
            requester_middleware_name=requester_middleware_name,
            scenario=scenario,
            return_type=self._return_type,
            return_value=self._return_value,
            error=error,
        )
        return super_execute_result_msg

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

    def get_sub_service_type_list(self) -> List[MXSubServiceRequest]:
        return self._sub_service_request_list

    def get_is_scanned(self) -> bool:
        return self._is_scanned

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_sub_service_type_list(self, target_sub_service_request_list: List[MXSubServiceRequest]) -> None:
        self._sub_service_request_list = target_sub_service_request_list

    def set_is_scanned(self, is_scanned: bool) -> None:
        self._is_scanned = is_scanned
