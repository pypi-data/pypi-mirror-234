from big_thing_py.big_thing import *
from big_thing_py.super import *
import threading


class MXSuperThing(MXBigThing):
    DEFAULT_NAME = 'default_super_thing'

    # Super Service Execution 요청이 들어왔을때 mapping_table에 있는 super_request를 찾기 위한 super_service_request_key 리스트
    # Super Service는 자신의 이름으로 super_request_key를 찾을 수 있다.
    # {
    #     'super_service_request_key1': ['sub_service_request_key1', 'sub_service_request_key2', ...]},
    #     'super_service_request_key2': ['sub_service_request_key3', 'sub_service_request_key4', ...]},
    #      ...
    # }
    _SUPER_SERVICE_REQUEST_KEY_TABLE: Dict[str, List[str]] = dict()

    def __init__(
        self,
        name: str = DEFAULT_NAME,
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        is_super: bool = True,
        is_parallel: bool = True,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_enable: bool = False,
        log_name: str = '',
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
        refresh_cycle: float = 30,
    ):
        self._global_service_table: Dict[str, Union[List[MXFunction], List[MXValue]]] = dict(values=[], functions=[])
        self._SUPER_SERVICE_REQUEST_KEY_TABLE = dict()

        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            ip,
            port,
            ssl_ca_path,
            ssl_enable,
            log_name,
            log_enable,
            log_mode,
            append_mac_address,
        )

        self._refresh_cycle = refresh_cycle

        self._last_refresh_time = 0

        self._function_list: List[MXSuperFunction] = self._function_list

        self._thread_func_list += [
            self._refresh_thread_func,
        ]

    def __eq__(self, o: 'MXSuperThing'):
        instance_check = isinstance(o, MXSuperThing)
        refresh_cycle_check = self._refresh_cycle == o._refresh_cycle

        return super().__eq__(o) and instance_check and refresh_cycle_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_refresh_cycle'] = self._refresh_cycle

        del state['_last_refresh_time']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._refresh_cycle = state['_refresh_cycle']

        self._last_refresh_time = 0
        self._thread_func_list = self._thread_func_list + [
            self._refresh_thread_func,
        ]

    @override
    def setup(self, avahi_enable=True) -> 'MXSuperThing':
        self._init_logger()
        self._extract_sub_service_request_info()
        return super().setup(avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def _refresh_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._is_registered:
                    if (get_current_time() - self._last_refresh_time) > self._refresh_cycle:
                        self._send_SM_REFRESH()
                        self._last_refresh_time = get_current_time()
                        # time.sleep(self._refresh_cycle / 2)

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

        # def _unsubscribe_thread_func(self, stop_event: Event):
        #     try:
        #         while not stop_event.wait(THREAD_TIME_OUT):
        #             if self._is_registered:
        #                 if not self._unsubscribe_queue.empty():
        #                     topic = self._unsubscribe_queue.queue[0]
        #                     self._unsubscribe(topic)
        #                     topic = self._unsubscribe_queue.get()

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    @override
    def _classify_topic(self, topic: str) -> Union[MXProtocolType, bool]:
        topic_token = topic_split(topic)
        if topic_token[0] == 'MS':
            if topic_token[1] == 'RESULT':
                if topic_token[2] == 'SCHEDULE':
                    protocol = MXProtocolType.Super.MS_RESULT_SCHEDULE
                elif topic_token[2] == 'EXECUTE':
                    protocol = MXProtocolType.Super.MS_RESULT_EXECUTE
                elif topic_token[2] == 'SERVICE_LIST':
                    protocol = MXProtocolType.Super.MS_RESULT_SERVICE_LIST
                else:
                    return False
            elif topic_token[1] == 'SCHEDULE':
                protocol = MXProtocolType.Super.MS_SCHEDULE
            elif topic_token[1] == 'EXECUTE':
                protocol = MXProtocolType.Super.MS_EXECUTE
            else:
                return False
        elif topic_token[0] == 'ME':
            if topic_token[1] == 'NOTIFY_CHANGE':
                protocol = MXProtocolType.WebClient.ME_NOTIFY_CHANGE
            else:
                return False
        else:
            protocol = super()._classify_topic(topic)

        return protocol

    @override
    def _handle_mqtt_message(self, msg: mqtt.MQTTMessage) -> bool:
        topic_string = decode_MQTT_message(msg)[0]
        protocol = self._classify_topic(topic_string)
        msg.timestamp = time.time()

        if protocol == MXProtocolType.Super.MS_RESULT_SCHEDULE:
            rc = self._handle_MS_RESULT_SCHEDULE(msg)
        elif protocol == MXProtocolType.Super.MS_RESULT_EXECUTE:
            rc = self._handle_MS_RESULT_EXECUTE(msg)
        elif protocol == MXProtocolType.Super.MS_RESULT_SERVICE_LIST:
            rc = self._handle_MS_RESULT_SERVICE_LIST(msg)
        elif protocol == MXProtocolType.Super.MS_SCHEDULE:
            rc = self._handle_MS_SCHEDULE(msg)
        elif protocol == MXProtocolType.Super.MS_EXECUTE:
            rc = self._handle_MS_EXECUTE(msg)
        elif protocol == MXProtocolType.WebClient.ME_NOTIFY_CHANGE:
            rc = self._handle_ME_NOTIFY(msg)

        elif protocol == MXProtocolType.Base.MT_RESULT_REGISTER:
            rc = self._handle_MT_RESULT_REGISTER(msg)
        elif protocol == MXProtocolType.Base.MT_RESULT_UNREGISTER:
            rc = self._handle_MT_RESULT_UNREGISTER(msg)
        elif protocol == MXProtocolType.Base.MT_RESULT_BINARY_VALUE:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Not permitted topic! topic: {topic_string}')
            return False
        elif protocol == MXProtocolType.Base.MT_EXECUTE:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Not permitted topic! topic: {topic_string}')
            return False
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected topic! topic: {topic_string}')
            return False

        if not rc:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected topic! topic: {topic_string}')
            return False

        return rc

    # ================
    # ___  ___ _____
    # |  \/  |/  ___|
    # | .  . |\ `--.
    # | |\/| | `--. \
    # | |  | |/\__/ /
    # \_|  |_/\____/
    # ================

    def _handle_MS_SCHEDULE(self, msg: mqtt.MQTTMessage) -> bool:
        super_schedule_msg = MXSuperScheduleMessage(msg)
        target_super_service = self._get_function(super_schedule_msg.super_service_name)

        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {super_schedule_msg.super_service_name} does not exist...',
                'red',
            )
            return False
        if self._name != super_schedule_msg.super_thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Thing name {super_schedule_msg.super_thing_name} is not matched...',
                'red',
            )
            return False
        if self._middleware_name != super_schedule_msg.super_middleware_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Middleware name {super_schedule_msg.super_middleware_name} is not matched...',
                'red',
            )
            return False
        if super_schedule_msg.topic_error or super_schedule_msg.payload_error:
            MXLOG_DEBUG(f'[{get_current_function_name()}] super_schedule_msg Message has error!', 'red')
            return False
        if not self._check_super_service_exist(target_super_service):
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {target_super_service.get_name()} does not exist...',
                'red',
            )
            return False

        schedule_thread = target_super_service.start_super_schedule_thread(
            super_schedule_msg, self._global_service_table, timeout=1000
        )
        if not schedule_thread:
            return False
        elif schedule_thread.is_alive():
            return True
        else:
            return False

    def _handle_MS_EXECUTE(self, msg: mqtt.MQTTMessage) -> bool:
        super_execute_msg = MXSuperExecuteMessage(msg)
        target_super_service = self._get_function(super_execute_msg.super_service_name)

        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {super_execute_msg.super_service_name} does not exist...',
                'red',
            )
            return False
        if self._name != super_execute_msg.super_thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Thing name {super_execute_msg.super_thing_name} is not matched...',
                'red',
            )
            return False
        if self._middleware_name != super_execute_msg.super_middleware_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Middleware name {super_execute_msg.super_middleware_name} is not matched...',
                'red',
            )
            return False
        if super_execute_msg.topic_error or super_execute_msg.payload_error:
            MXLOG_DEBUG(f'[{get_current_function_name()}] super_execute_msg Message has error!', 'red')
            return False

        # 중복된 시나리오로부터 온 실행 요청이면 -4 에러코드를 보낸다.
        if super_execute_msg.scenario in target_super_service.get_running_scenario_list():
            target_super_service._send_SM_RESULT_EXECUTE(
                super_service_name=super_execute_msg.super_service_name,
                super_thing_name=super_execute_msg.super_thing_name,
                super_middleware_name=super_execute_msg.super_middleware_name,
                requester_middleware_name=super_execute_msg.requester_middleware_name,
                scenario=super_execute_msg.scenario,
                error=MXErrorCode.DUPLICATE,
            )
            return True

        super_execute_thread = target_super_service.start_super_execute_thread(
            super_execute_msg, self._SUPER_SERVICE_REQUEST_KEY_TABLE
        )
        if not super_execute_thread:
            return False
        else:
            return True

    def _handle_MS_RESULT_SCHEDULE(self, msg: mqtt.MQTTMessage) -> bool:
        subschedule_result_msg = MXSubScheduleResultMessage(msg)
        subschedule_result_msg.set_timestamp()
        super_service_request_key = make_super_request_key(
            scenario_name=subschedule_result_msg.scenario,
            requester_middleware_name=subschedule_result_msg.requester_middleware_name,
        )
        sub_service_request_key = make_sub_service_request_key(
            sub_service_name=subschedule_result_msg.sub_service_name,
            sub_service_request_order=subschedule_result_msg.sub_service_request_order,
        )

        target_super_service = self._get_function(subschedule_result_msg.super_service_name)
        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {subschedule_result_msg.super_service_name} does not exist...',
                'yellow',
            )
            return False

        result = target_super_service.put_subschedule_result(
            super_service_request_key, sub_service_request_key, subschedule_result_msg
        )
        return result

    def _handle_MS_RESULT_EXECUTE(self, msg: mqtt.MQTTMessage) -> bool:
        sub_service_execute_result_msg = MXSubExecuteResultMessage(msg)
        sub_service_execute_result_msg.set_timestamp()
        super_service_request_key = make_super_request_key(
            scenario_name=sub_service_execute_result_msg.scenario,
            requester_middleware_name=sub_service_execute_result_msg.requester_middleware_name,
        )
        sub_service_request_key = make_sub_service_request_key(
            sub_service_name=sub_service_execute_result_msg.sub_service_name,
            sub_service_request_order=sub_service_execute_result_msg.sub_service_request_order,
        )

        target_super_service = self._get_function(sub_service_execute_result_msg.super_service_name)
        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {sub_service_execute_result_msg.super_service_name} does not exist...',
                'yellow',
            )
            return False

        result = target_super_service.put_sub_service_execute_result(
            super_service_request_key, sub_service_request_key, sub_service_execute_result_msg
        )
        return result

    def _handle_MS_RESULT_SERVICE_LIST(self, msg: mqtt.MQTTMessage) -> bool:
        try:
            service_list = MXSuperServiceListResultMessage(msg)
            service_list.set_timestamp()

            for middleware in service_list.service_list:
                hierarchy_type = middleware['hierarchy']
                if not hierarchy_type in ['local', 'child']:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] Parent middleware is not supported', 'red')
                    return False

                middleware_name = middleware['middleware']
                if not middleware_name:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] Middleware name does not exist', 'red')
                    return False

                thing_list = middleware['things']
                for thing in thing_list:
                    is_alive = thing['is_alive']
                    if is_alive != 1:
                        continue

                    is_super = thing['is_super']
                    alive_cycle = thing['alive_cycle']

                    # value 정보를 추출
                    value_service_list = self._extract_value_info(thing=thing, middleware_name=middleware_name)
                    self._global_service_table['values'].extend(value_service_list)

                    function_service_list = self._extract_function_info(
                        thing_info=thing, middleware_name=middleware_name
                    )
                    self._global_service_table['functions'].extend(function_service_list)

            self._last_refresh_time = get_current_time()
            return True
        except KeyError as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] KeyError', 'red')
            return False
        except ValueError as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] ValueError', 'red')
            return False
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unknown Exception', 'red')
            return False

    # ===================
    #   __  __   ______
    #  |  \/  | |  ____|
    #  | \  / | | |__
    #  | |\/| | |  __|
    #  | |  | | | |____
    #  |_|  |_| |______|
    # ===================

    def _handle_ME_NOTIFY(self, msg: mqtt.MQTTMessage):
        notify_msg = MXNotifyMessage(msg)
        notify_msg.set_timestamp()
        self._send_SM_REFRESH()

    # ================
    #  _____ ___  ___
    # /  ___||  \/  |
    # \ `--. | .  . |
    #  `--. \| |\/| |
    # /\__/ /| |  | |
    # \____/ \_|  |_/
    # ================

    def _send_SM_EXECUTE(self, sub_service_execute_msg: MXSubExecuteMessage) -> None:
        sub_service_execute_mqtt_msg = sub_service_execute_msg.mqtt_message()
        self._publish_queue.put(sub_service_execute_mqtt_msg)

    def _send_SM_REFRESH(self):
        super_refresh_msg = self.generate_super_refresh_message()
        super_refresh_mqtt_msg = super_refresh_msg.mqtt_message()
        self._publish_queue.put(super_refresh_mqtt_msg)

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_super_refresh_message(self) -> MXSuperRefreshMessage:
        super_refresh_msg = MXSuperRefreshMessage(self)
        return super_refresh_msg

    @override
    def _get_function(self, function_name: str) -> MXSuperFunction:
        for function in self._function_list:
            if function.get_name() == function_name:
                return function

    @override
    def _subscribe_init_topic_list(self):
        super()._subscribe_init_topic_list()

        topic_list = [MXProtocolType.Super.MS_RESULT_SERVICE_LIST.value % "#"]

        for topic in topic_list:
            self._subscribe(topic)

    @override
    def _subscribe_service_topic_list(self):
        for function in self._function_list:
            # Super Schedule, Super Execute에 필요한 토픽들을 미리 구독을 해놓는다.
            topic_list = [
                MXProtocolType.Super.MS_SCHEDULE.value % (function.get_name(), self._name, self._middleware_name, '#'),
                MXProtocolType.Super.MS_RESULT_SCHEDULE.value % ('+', '+', '#'),
                MXProtocolType.Super.MS_EXECUTE.value % (function.get_name(), self._name, self._middleware_name, '#'),
                MXProtocolType.Super.MS_RESULT_EXECUTE.value % ('+', '+', '#'),
            ]

            for topic in topic_list:
                self._subscribe(topic)

    def _request_sub_service_execute(self, sub_service_execute_request: MXSubExecuteRequest) -> None:
        if not isinstance(sub_service_execute_request, MXSubExecuteRequest):
            raise MXTypeError(
                f'[{get_current_function_name()}] Invalid type of sub_service_execute_request: {type(sub_service_execute_request)}'
            )

        sub_service_execute_msg = sub_service_execute_request.trigger_msg
        self._send_SM_EXECUTE(sub_service_execute_msg)

    # 하나의 sub_service_request에 있는 sub_service_execute_request들을 병렬로 실행한다.
    def _sub_service_execute_parallel(
        self, sub_service_execute_request_list: List[MXSubExecuteRequest], arg_list: List[Union[int, float, str, bool]]
    ) -> List[Union[int, float, str, bool]]:
        result_list = []
        for i, sub_service_execute_request in enumerate(sub_service_execute_request_list):
            sub_service_execute_request.timer_start()
            sub_service_execute_request.trigger_msg.arguments = tuple(arg_list)

            sub_service_execute_msg = sub_service_execute_request.trigger_msg
            MXLOG_DEBUG(
                f'[SUB_EXECUTE START] {sub_service_execute_msg.sub_service_name}|{sub_service_execute_msg.target_middleware_name}|{sub_service_execute_msg.scenario}|{i}',
                'cyan',
            )
            self._request_sub_service_execute(sub_service_execute_request)

        for i, sub_service_execute_request in enumerate(sub_service_execute_request_list):
            sub_service_execute_request.result_msg = sub_service_execute_request.get_result_msg()
            sub_service_execute_request.timer_end()
            rc_msg = sub_service_execute_request.result_msg

            sub_service_execute_msg: MXSubExecuteMessage = sub_service_execute_request.trigger_msg
            sub_service_execute_result_msg: MXSubExecuteResultMessage = sub_service_execute_request.result_msg
            result_list.append(
                dict(
                    scenario=sub_service_execute_result_msg.scenario,
                    return_type=sub_service_execute_result_msg.return_type,
                    return_value=sub_service_execute_result_msg.return_value,
                    error=sub_service_execute_result_msg.error,
                )
            )

            MXLOG_DEBUG(
                f'[SUB_EXECUTE END] {sub_service_execute_msg.sub_service_name}|{sub_service_execute_msg.target_middleware_name}|{sub_service_execute_msg.scenario}|{i}'
                f'duration: {sub_service_execute_request.duration():.4f} Sec',
                'cyan',
            )

        return result_list

    def _get_sub_service_from_global_service_table(self, sub_service_name: str) -> MXFunction:
        for function in self._global_service_table['functions']:
            if function.get_name() == sub_service_name:
                return function
        return None

    def _check_sub_service_callable(self, sub_service_name: str, return_type: MXType):
        global_sub_service = self._get_sub_service_from_global_service_table(sub_service_name)
        if not global_sub_service:
            return False
        if not global_sub_service.get_return_type() == return_type:
            return False

        return True

    def _check_req_valid(
        self,
        sub_service_name: str,
        tag_list: List[str],
        arg_list: Union[Tuple[MXArgument], Tuple],
        return_type: MXType,
        service_type: MXServiceType,
        range_type: MXRangeType,
    ):
        if not sub_service_name:
            raise MXValueError(f'sub_service_name must be not empty')
        if not tag_list:
            raise MXValueError(f'tag_list must be not empty')
        if not all(tag_list):
            raise MXValueError(f'tag in tag_list must be not empty string')
        if not service_type in [MXServiceType.VALUE, MXServiceType.FUNCTION]:
            raise MXTypeError(f'Invalid service_type: {service_type}')
        if not return_type in [MXType.INTEGER, MXType.DOUBLE, MXType.STRING, MXType.BOOL, MXType.BINARY, MXType.VOID]:
            raise MXTypeError(f'Invalid return_type: {return_type}')
        elif service_type == MXServiceType.VALUE and return_type == MXType.VOID:
            raise MXTypeError(f'Value service cannot have a return_type of void')
        if not range_type in [MXRangeType.SINGLE, MXRangeType.ALL]:
            raise MXTypeError(f'Invalid range_type: {range_type}')

        return True

    def _check_req_return_type(
        self, sub_service_return_type: MXType, req_return_type: MXType, service_type: MXServiceType
    ):
        if req_return_type in [MXType.INTEGER, MXType.DOUBLE] and sub_service_return_type in [
            MXType.INTEGER,
            MXType.DOUBLE,
        ]:
            return True
        elif req_return_type == MXType.VOID and service_type == MXServiceType.VALUE:
            raise MXTypeError(
                f'Not matched return_type. Value service cannot have a return_type of void: {sub_service_return_type}'
            )
        elif req_return_type != sub_service_return_type:
            raise MXTypeError(f'Not matched return_type: {sub_service_return_type} != {req_return_type}')

        return True

    def _check_super_service_exist(self, super_service: MXSuperFunction):
        return all(
            [
                self._check_sub_service_callable(
                    sub_service_request._sub_service_type.get_name(),
                    sub_service_request._sub_service_type.get_return_type(),
                )
                for sub_service_request in super_service._sub_service_request_list
            ]
        )

    def req(
        self,
        sub_service_name: str,
        tag_list: List[str],
        arg_list: Union[Tuple[MXArgument], Tuple] = [],
        return_type: MXType = MXType.UNDEFINED,
        service_type: MXServiceType = MXServiceType.FUNCTION,
        range_type: MXRangeType = MXRangeType.SINGLE,
    ) -> Union[List[dict], bool]:
        # Detect fatal errors.
        # If an error occurs, the program terminates by raising an exception.
        if not self._check_req_valid(
            sub_service_name=sub_service_name,
            tag_list=tag_list,
            arg_list=arg_list,
            return_type=return_type,
            service_type=service_type,
            range_type=range_type,
        ):
            return False

        super_service_name = get_upper_function_name()
        target_super_service = self._get_function(super_service_name)
        target_sub_service = self._get_sub_service_from_global_service_table(sub_service_name)

        # Convert tag of type [str] to [MXTag]
        tag_list = [MXTag(str_tag) for str_tag in tag_list]

        if service_type == MXServiceType.VALUE:
            sub_service_name = f'__{sub_service_name}'
        elif service_type == MXServiceType.FUNCTION:
            sub_service_name = sub_service_name

        # When initiate a super thing, extract information about the super service.
        if not target_super_service.get_is_scanned():
            target_super_service.add_sub_service_request_info(
                sub_service_name=sub_service_name,
                arg_list=arg_list,
                tag_list=tag_list,
                return_type=return_type,
                range_type=range_type,
            )
            return []
        else:
            if not self._check_sub_service_callable(sub_service_name, return_type):
                MXLOG_DEBUG(f'sub_service {sub_service_name} is not callable', 'red')
                return False
            if not self._compare_arg_list(target_sub_service.get_arg_list(), list(arg_list)):
                MXLOG_DEBUG(f'Not matched arg_list')
                return False
            if not self._check_req_return_type(
                target_sub_service.get_return_type(), req_return_type=return_type, service_type=service_type
            ):
                MXLOG_DEBUG(f'Not matched return_type')
                return False

            current_thread = threading.current_thread()
            scenario_name = current_thread.user_data['scenario']
            requester_middleware_name = current_thread.user_data['requester_middleware']
            # super_service_request_key = scenario_name@requester_middleware_name
            super_service_request_key = make_super_request_key(scenario_name, requester_middleware_name)

            MXLOG_DEBUG(
                f'[DEBUG] before pop SUPER_SERVICE_REQUEST_KEY_TABLE: \n{dict_to_json_string(self._SUPER_SERVICE_REQUEST_KEY_TABLE, pretty=True)}'
                f'\n super_service_request_key: {super_service_request_key} '
            )
            sub_service_request_key_list = self._SUPER_SERVICE_REQUEST_KEY_TABLE[super_service_request_key]
            # sub_service_request_key = sub_service_name@sub_service_request_order
            sub_service_request_key = sub_service_request_key_list.pop(0)
            MXLOG_DEBUG(
                f'[DEBUG] after pop SUPER_SERVICE_REQUEST_KEY_TABLE: \n{dict_to_json_string(self._SUPER_SERVICE_REQUEST_KEY_TABLE, pretty=True)}'
                f'\n super_service_request_key: {super_service_request_key} '
            )
            if len(sub_service_request_key_list) == 0:
                self._SUPER_SERVICE_REQUEST_KEY_TABLE.pop(super_service_request_key)

            super_service_execute_request = target_super_service._mapping_table[super_service_request_key]
            sub_service_execute_request_list = super_service_execute_request._sub_service_request_table[
                sub_service_request_key
            ]._target_request_list

            result_list = self._sub_service_execute_parallel(sub_service_execute_request_list, arg_list)
            return result_list

    # TODO: implement this
    def r(self, line: str = None, *arg_list) -> Union[List[dict], bool]:
        super_service_name = get_upper_function_name()

        range_type = 'all' if 'all' in line else 'single'
        function_name = line.split('.')[1][0: line.split('.')[1].find('(')]
        bracket_parse: List[str] = re.findall(r'\(.*?\)', line)
        tags = [tag[1:] for tag in bracket_parse[0][1:-1].split(' ')]

        arguments = []
        for bracket_inner_element in bracket_parse[1][1:-1].split(','):
            bracket_inner_element = bracket_inner_element.strip(' ')
            if bracket_inner_element == '':
                continue
            else:
                arguments.append(bracket_inner_element)

        for i, arg in enumerate(arguments):
            if '$' in arg:
                index = int(arg[1:])
                arguments[i] = arg_list[index - 1]

        arguments = tuple(arguments)

    def _extract_sub_service_request_info(self) -> None:
        for function in self._function_list:
            if self._is_super and not function.get_is_scanned():
                arg_list = function.get_arg_list()
                try:
                    MXLOG_DEBUG(f'Detect super service: {function.get_name()}', 'green')
                    function._func(*tuple(arg_list))
                except MXError as e:
                    # req를 실행하다가 MySSIXError와 관련된 에러가 발생한다는 것은 req명세가 잘못
                    # 되었다는 것을 의미한다. 만약 MySSIXError에러가 아닌 다른 예외가 발생한 경우,
                    # super service안에 있는 코드 중, req() 코드 부분이 아닌 코드에 의한 예외이므로
                    # 정상적으로 req()에 대한 정보를 추출한 것이다.
                    raise e
                else:
                    function.set_is_scanned(True)

    def _extract_value_info(self, thing: dict, middleware_name: str) -> List[MXValue]:
        thing_name = thing['name']
        value_list = thing['values']

        value_service_list = []
        for value_info in value_list:
            value_tag_list = [MXTag(tag['name']) for tag in value_info['tags']]

            # TODO: cycle info is omit in service list
            value_service = MXValue(
                func=dummy_func(arg_list=[]),
                type=MXType.get(value_info['type']),
                bound=(float(value_info['bound']['min_value']), float(value_info['bound']['max_value'])),
                cycle=None,
                name=value_info['name'],
                tag_list=value_tag_list,
                desc=value_info['description'],
                thing_name=thing_name,
                middleware_name=middleware_name,
                format=value_info['format'] if not '(null)' in value_info['format'] else '',
            )
            if value_service not in self._global_service_table['values']:
                value_service_list.append(value_service)

        return value_service_list

    def _extract_function_info(self, thing_info: dict, middleware_name: str) -> List[MXFunction]:
        thing_name = thing_info['name']
        function_list = thing_info['functions']

        function_service_list = []
        for function_info in function_list:
            function_tag_list = [MXTag(tag['name']) for tag in function_info['tags']]
            arg_list = []
            if bool(function_info['use_arg']):
                for argument in function_info['arguments']:
                    arg_list.append(
                        MXArgument(
                            name=argument['name'],
                            type=MXType.get(argument['type']),
                            bound=(float(argument['bound']['min_value']), float(argument['bound']['max_value'])),
                        )
                    )

            function_service = MXFunction(
                func=dummy_func(arg_list=arg_list),
                return_type=MXType.get(function_info['return_type']),
                name=function_info['name'],
                tag_list=function_tag_list,
                desc=function_info['description'],
                thing_name=thing_name,
                middleware_name=middleware_name,
                arg_list=arg_list,
                exec_time=function_info['exec_time'],
            )
            if function_service not in self._global_service_table['functions']:
                function_service_list.append(function_service)

        return function_service_list

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

    @override
    def get_function_list(self) -> List[MXSuperFunction]:
        return self._function_list

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    @override
    def set_function_list(self, function_list: List[MXSuperFunction]) -> None:
        self._function_list = function_list
