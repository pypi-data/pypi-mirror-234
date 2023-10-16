from big_thing_py.big_thing import *
from big_thing_py.staff_thing import *
from big_thing_py.manager import *
import uuid


class MXPollManagerThing(MXBigThing, metaclass=ABCMeta):
    MANAGER_THREAD_TIME_OUT = THREAD_TIME_OUT

    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        ip: str = None,
        port: int = None,
        ssl_ca_path: str = None,
        ssl_enable: bool = False,
        log_name: str = None,
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
        manager_mode: MXManagerMode = MXManagerMode.SPLIT,
        scan_cycle=5,
    ):
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

        self._scan_cycle = scan_cycle
        self._manager_mode = MXManagerMode.get(manager_mode) if isinstance(manager_mode, str) else manager_mode

        self._staff_thing_list: List[MXStaffThing] = []
        self._manager_mode_handler = ManagerModeHandler(mode=self._manager_mode)

        self._last_scan_time = 0

        self._register_waiting_staff_thing_queue: Queue = Queue()

        # Threading
        self._thread_func_list += [
            self._scan_staff_message_thread_func,
        ]

    @override
    def run(self):
        try:
            self._connect(self._ip, self._port)

            # Start main threads
            for thread in self._comm_thread_list + self._thread_list:
                thread.start()

            if self._manager_mode == MXManagerMode.JOIN:
                self._register_try(period=10, retry=5)
            elif self._manager_mode == MXManagerMode.SPLIT:
                # SPLIT 모드일 땐, manager thing 자기자신은 등록하지 않는다.
                pass
            else:
                pass

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
        except KeyboardInterrupt as e:
            MXLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError as e:
            MXLOG_DEBUG('Connection error while connect to broker. Check ip and port', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    @override
    def wrapup(self):
        try:
            for staff_thing in self._staff_thing_list:
                self._send_TM_UNREGISTER(staff_thing)
            cur_time = get_current_time()

            self._g_exit.set()
            for thread in self._thread_list:
                thread.join()
                MXLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            while not (
                (self._publish_queue.empty() and self._receive_queue.empty()) or (get_current_time() - cur_time > 3)
            ):
                time.sleep(THREAD_TIME_OUT)

            self._g_comm_exit.set()
            for thread in self._comm_thread_list:
                thread.join()
                MXLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            self._mqtt_client.disconnect()
            MXLOG_DEBUG('Thing Exit', 'red')
            return True
        except Exception as e:
            print_error(e)
            return False

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    @override
    def _alive_publishing_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._manager_mode == MXManagerMode.JOIN:
                    current_time = get_current_time()
                    if not current_time - self._last_alive_time > self._alive_cycle:
                        continue
                    for staff_thing in self._staff_thing_list:
                        self._send_TM_ALIVE(staff_thing)
                        staff_thing._last_alive_time = current_time
                elif self._manager_mode == MXManagerMode.SPLIT:
                    # check staff thing is alive
                    current_time = get_current_time()
                    for staff_thing in self._staff_thing_list:
                        if not current_time - staff_thing._last_alive_time > staff_thing._alive_cycle:
                            continue
                        self._send_TM_UNREGISTER(staff_thing)
                        staff_thing._is_connected = False
                        self._staff_thing_list.remove(staff_thing)
                    pass
                else:
                    raise Exception('Invalid Manager Mode')
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    @override
    def _value_publishing_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                for staff_thing in self._staff_thing_list:
                    if not staff_thing._is_registered:
                        continue
                    current_time = get_current_time()
                    for value in staff_thing._value_list:
                        if not (current_time - value.get_last_update_time()) > value.get_cycle():
                            continue

                        is_updated = value.update()
                        if is_updated is not None:
                            self._send_TM_VALUE_PUBLISH(staff_thing=staff_thing, value=value)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    ############################################################################################################################

    def _scan_staff_message_thread_func(self, stop_event: Event):
        '''
        scan staff thing periodically and create staff thing instance

        if scanned staff thing is not in self._staff_thing_list, create staff thing instance and
        connect to staff thing
        else if scanned staff thing is in self._staff_thing_list, send alive packet.
        '''
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                if not (get_current_time() - self._last_scan_time > self._scan_cycle):
                    continue

                scanned_staff_thing_info_list = self._scan_staff_thing()
                if len(scanned_staff_thing_info_list) == 0:
                    MXLOG_DEBUG('No staff thing found', 'yellow')
                    continue

                for staff_thing_info in scanned_staff_thing_info_list:
                    # create staff thing instance
                    staff_thing = self._create_staff(staff_thing_info)
                    if not staff_thing:
                        continue

                    # if scanned staff thing is already in self._staff_thing_list, send alive packet
                    # and update last_alive_time
                    exist_staff_thing = self._get_staff_thing_by_name(staff_thing.get_name())
                    if exist_staff_thing:
                        self._send_TM_ALIVE(exist_staff_thing)
                        continue

                    MXLOG_DEBUG(f'New staff_thing!!! name: [{staff_thing.get_name()}]', 'green')
                    staff_thing._is_connected = True

                    # else if scanned staff thing is not in self._staff_thing_list, create staff
                    # connect & register staff thing to middleware
                    self._send_TM_REGISTER(staff_thing)
                    self._send_TM_ALIVE(staff_thing)

                # update the scan cycle to half the minimum alive cycle of all staff thing
                self._scan_cycle = (
                    (min([staff_thing.get_alive_cycle() for staff_thing in self._staff_thing_list]) / 2.5)
                    if len(self._staff_thing_list) > 0
                    else self._scan_cycle
                )
                self._last_scan_time = get_current_time()
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

    # ===========================
    #            _____   _____
    #     /\    |  __ \ |_   _|
    #    /  \   | |__) |  | |
    #   / /\ \  |  ___/   | |
    #  / ____ \ | |      _| |_
    # /_/    \_\|_|     |_____|
    # ===========================

    @abstractmethod
    def _scan_staff_thing(self, timeout: float) -> List[dict]:
        '''
        지속적으로 staff thing을 발견하여 정보를 수집하여 반환하는 함수.
        timeout을 지정하여 한 번 staff thing을 검색하는데 소요될 시간을 지정할 수 있다.

        Args:
            timeout (float): staff thing을 검색하는데 소요될 시간

        Returns:
            List[dict]: staff thing의 정보를 담고 있는 리스트
        '''
        pass

    @abstractmethod
    def _create_staff(self, staff_thing_info: dict) -> Union[MXStaffThing, None]:
        '''
        _scan_staff_thing() 함수를 통해 수집된 staff thing 정보를 바탕으로 staff thing을 생성하는 함수.
        만약 스캔하는 것만으로 완벽한 staff thing의 정보를 수집할 수 없다면, staff thing의 register 메시지를 받아 처리하는
        _handle_REGISTER_staff_message() 함수에서 staff thing을 self._staff_thing_list에서 찾아 정보를 추가할 수 있다.

        Args:
            staff_thing_info (dict): staff thing의 정보를 담고 있는 딕셔너리

        Returns:
            staff_thing(MXStaffThing): 생성한 staff thing 인스턴스
        '''
        pass

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    @override
    def _handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage) -> MXErrorCode:
        register_result_msg = MXRegisterResultMessage(msg)
        staff_thing: MXStaffThing = self._register_waiting_staff_thing_queue.get(timeout=5)
        error = register_result_msg.error

        if staff_thing.get_name() != register_result_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {staff_thing.get_name()} should be arrive, not {register_result_msg.thing_name}'
            )
            return error

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(
                f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {staff_thing.get_name()} register success!'
            )
            staff_thing.set_middleware_name(register_result_msg.middleware_name)
            staff_thing.set_registered(True)
            self._subscribe_service_topic_list(staff_thing)
            self._staff_thing_list.append(staff_thing)
            return error
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Thing {staff_thing.get_name()} register packet is not valid. error code: {register_result_msg.error}',
                'red',
            )
            return error
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Unexpected error occurred!!! error code: {register_result_msg.error}',
                'red',
            )
            return error

    @override
    def _handle_MT_RESULT_UNREGISTER(self, msg: mqtt.MQTTMessage) -> MXErrorCode:
        unregister_result_msg = MXUnregisterResultMessage(msg)
        staff_thing = self._get_staff_thing_by_name(unregister_result_msg.thing_name)
        error = unregister_result_msg.error

        if staff_thing.get_name() != unregister_result_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {staff_thing.get_name()} should be arrive, not {unregister_result_msg.thing_name}',
                'red',
            )
            return error

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(
                f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {staff_thing.get_name()} register success!'
            )
            staff_thing.set_registered(False)
            self._unsubscribe_all_topic_list(staff_thing)
            return error
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Thing {staff_thing.get_name()} unregister packet is not valid. error code: {unregister_result_msg.error}',
                'red',
            )
            return error
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Unexpected error occurred!!! error code: {unregister_result_msg.error}',
                'red',
            )
            return error

    @override
    def _handle_MT_RESULT_BINARY_VALUE(self, msg: mqtt.MQTTMessage) -> bool:
        execute_msg = MXBinaryValueResultMessage(msg)
        staff_thing = self._get_staff_thing_by_name(execute_msg.thing_name)

        if staff_thing.get_name() != execute_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {staff_thing.get_name()} should be arrive, not {execute_msg.thing_name}',
                'red',
            )
            return False

        for value in staff_thing.get_value_list():
            if value.get_name() == execute_msg.value_name and value.get_type() == MXType.BINARY:
                value.set_binary_sending(False)
                return True
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Value {execute_msg.value_name} does not exist!!!', 'red')
            return False

    @override
    def _handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage) -> bool:
        execute_msg = MXExecuteMessage(msg)
        staff_thing = self._get_staff_thing_by_name(execute_msg.thing_name)
        target_function = staff_thing._get_function(execute_msg.function_name)

        if target_function:
            execute_thread = target_function.start_execute_thread(execute_msg)
            return True
        else:
            MXLOG_DEBUG('function not exist', 'red')
            return False

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    @override
    def _send_TM_REGISTER(self, staff_thing: MXThing) -> None:
        self._staff_thing_list.append(staff_thing)
        staff_thing._last_alive_time = get_current_time()
        self._subscribe_init_topic_list(staff_thing)
        self._register_waiting_staff_thing_queue.put(staff_thing)

        register_msg = staff_thing.generate_register_message()
        if not register_msg:
            raise Exception('TM_REGISTER packet error')

        register_mqtt_msg = register_msg.mqtt_message()
        self._publish_queue.put(register_mqtt_msg)

    @override
    def _send_TM_UNREGISTER(self, staff_thing: MXThing):
        self._staff_thing_list.remove(staff_thing)
        unregister_msg = staff_thing.generate_unregister_message()
        unregister_mqtt_msg = unregister_msg.mqtt_message()
        self._publish_queue.put(unregister_mqtt_msg)

    @override
    def _send_TM_ALIVE(self, staff_thing: MXThing):
        staff_thing._last_alive_time = get_current_time()
        alive_msg = staff_thing.generate_alive_message()
        alive_mqtt_msg = alive_msg.mqtt_message()
        self._publish_queue.put(alive_mqtt_msg)
        staff_thing.set_last_alive_time(get_current_time())

    @override
    def _send_TM_VALUE_PUBLISH(self, staff_thing: MXThing, value: MXValue) -> None:
        value_publish_msg = staff_thing.generate_value_publish_message(value=value)
        value_publish_mqtt_msg = value_publish_msg.mqtt_message()

        if value.get_type() == MXType.BINARY:
            value.set_binary_sending(True)
        self._publish_queue.put(value_publish_mqtt_msg)

    @override
    def _send_TM_VALUE_PUBLISH(self, staff_thing: MXThing, value: MXValue) -> None:
        value_publish_msg = staff_thing.generate_value_publish_message(value=value)
        value_publish_mqtt_msg = value_publish_msg.mqtt_message()

        if value.get_type() == MXType.BINARY:
            value.set_binary_sending(True)
        self._publish_queue.put(value_publish_mqtt_msg)

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    @override
    def _subscribe_init_topic_list(self, staff_thing: MXThing) -> None:
        topic_list = [
            MXProtocolType.Base.MT_RESULT_REGISTER.value % staff_thing.get_name(),
            MXProtocolType.Base.MT_RESULT_UNREGISTER.value % staff_thing.get_name(),
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE.value % staff_thing.get_name(),
        ]

        for topic in topic_list:
            self._subscribe(topic)

    @override
    def _subscribe_service_topic_list(self, staff_thing: MXThing):
        topic_list = []

        for function in staff_thing.get_function_list():
            topic_list += [
                MXProtocolType.Base.MT_EXECUTE.value % (function.get_name(), staff_thing.get_name(), '+', '+'),
                (MXProtocolType.Base.MT_EXECUTE.value % (function.get_name(), staff_thing.get_name(), '', '')).rstrip(
                    '/'
                ),
            ]

        for topic in topic_list:
            self._subscribe(topic)

    @override
    def _unsubscribe_all_topic_list(self, staff_thing: MXThing):
        # whenever _unsubscribe function execute, it remove target topic from self._subscribed_topic_set
        # so it need to iterate with copy of self._subscribed_topic_set
        topic_list = list(staff_thing.get_subscribed_topic_set())

        for topic in topic_list:
            self._unsubscribe(topic)

    def generate_staff_thing_id(self) -> str:
        return str(uuid.uuid4())

    def _get_staff_thing_by_name(self, staff_name: str, staff_thing_pool: List[MXStaffThing] = None) -> MXStaffThing:
        if staff_thing_pool is None:
            staff_thing_pool = self._staff_thing_list

        for staff_thing in staff_thing_pool:
            if staff_thing.get_name() == staff_name:
                return staff_thing

        return False

    def _get_staff_thing_by_staff_thing_id(
        self, staff_thing_id: str, staff_thing_pool: List[MXStaffThing] = None
    ) -> MXStaffThing:
        if staff_thing_pool is None:
            staff_thing_pool = self._staff_thing_list

        for staff_thing in staff_thing_pool:
            if staff_thing._staff_thing_id == staff_thing_id:
                return staff_thing

        return False
