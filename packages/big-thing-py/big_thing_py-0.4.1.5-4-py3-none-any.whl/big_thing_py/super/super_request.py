from big_thing_py.core.request import *
from big_thing_py.super.super_mqtt_message import *
from big_thing_py.core.function import *


class MXSuperScheduleRequest(MXRequest):
    def __init__(
        self, trigger_msg: MXSuperScheduleMessage = None, result_msg: MXSuperScheduleResultMessage = None
    ) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = MXActionType.SUPER_SCHEDULE

        self.trigger_msg: MXSuperScheduleMessage
        self.result_msg: MXSuperScheduleResultMessage
        self._check_duration: float = 0.0
        self._confirm_duration: float = 0.0
        self._status: MXScheduleStatus = MXScheduleStatus.INIT
        self._running: bool = False

        # sub_request_key = make_sub_request_key(subschedule_result_msg.sub_service_name, subschedule_result_msg.sub_service_request_order)
        # sub_request_key: {sub_service_name}@{sub_service_request_order}
        self._sub_service_request_table: Dict[str, MXSubServiceRequest] = {}

    def set_result_msg(self, result_msg: MXSuperScheduleResultMessage):
        self.result_msg = result_msg

    def get_result_msg(self):
        return self.result_msg

    def is_completed(self):
        if self.result_msg:
            return True
        else:
            return False

    def check_duration(self):
        return self._check_duration

    def confirm_duration(self):
        return self._confirm_duration

    def put_sub_service_schedule_result_msg(
        self, sub_service_request_key: str, result_msg: MXSubScheduleResultMessage, timeout: float = None
    ) -> bool:
        if sub_service_request_key not in self._sub_service_request_table:
            MXLOG_DEBUG(
                f'Could not find key {sub_service_request_key} in sub_service_request_table... This key is not mine!',
                'yellow',
            )
            return False

        target_sub_service_request = self._sub_service_request_table[sub_service_request_key]
        for candidate_request in target_sub_service_request._candidate_request_list:
            thing_check = candidate_request.trigger_msg.target_thing_name == result_msg.target_thing_name
            middleware_check = candidate_request.trigger_msg.target_middleware_name == result_msg.target_middleware_name
            request_ID_check = candidate_request.trigger_msg.request_ID == result_msg.request_ID
            status_check = (
                result_msg.status == MXScheduleStatus.CONFIRM and candidate_request._status == MXScheduleStatus.SELECT
            ) or (result_msg.status == MXScheduleStatus.CHECK)

            if thing_check and middleware_check and request_ID_check and status_check:
                candidate_request.put_result_msg(result_msg, timeout=timeout)
                return True
        else:
            raise Exception(f'No sub_service {sub_service_request_key} found in _sub_service_request_table')

    def generate_sub_service_schedule_request(
        self,
        sub_service_request_list: List['MXSubServiceRequest'],
        hierarchical_function_service_table: List[MXFunction],
    ):
        for sub_service_request in sub_service_request_list:
            target_sub_service_request = MXSubServiceRequest(
                sub_service_type=sub_service_request._sub_service_type,
                sub_service_request_order=sub_service_request._sub_service_request_order,
            )
            # TODO: 해당 로직 부분 분리하기
            # 미들웨어 마다 sub_service_request가 실행하고자 하는 sub_service이 존재하는 지 체크한다.
            target_sub_service = target_sub_service_request._sub_service_type

            candidate_middleware_name_list = []
            for function_service in hierarchical_function_service_table:
                name_check = target_sub_service.get_name() == function_service.get_name()
                if name_check and function_service.get_middleware_name() not in candidate_middleware_name_list:
                    candidate_middleware_name_list.append(function_service.get_middleware_name())
                    target_sub_service.set_middleware_name(function_service.get_middleware_name())

            candidate_request_list = []
            for middleware_name in candidate_middleware_name_list:
                sub_service_schedule_msg = MXSubScheduleMessage(
                    sub_service_name=target_sub_service.get_name(),
                    target_thing_name='SUPER',
                    target_middleware_name=middleware_name,
                    requester_middleware_name=self.trigger_msg.requester_middleware_name,
                    super_thing_name=self.trigger_msg.super_thing_name,
                    super_service_name=self.trigger_msg.super_service_name,
                    sub_service_request_order=target_sub_service_request._sub_service_request_order,
                    scenario=self.trigger_msg.scenario,
                    period=self.trigger_msg.period,
                    tag_list=[dict(name=tag.get_name()) for tag in target_sub_service.get_tag_list()],
                    range_type=target_sub_service.get_range_type(),
                    request_ID=None,
                    status=MXScheduleStatus.INIT,
                )

                # NOTE:sub_service_request에 대한 부분이 미들웨어당 1개만 생성될 것으로 예상됨. len(candidate_request_list) == 1 ?
                # TODO: _result_msg도 생성해서 넣어서 나중에 결과 토픽을 구독할 때 topic()으로 간단하게 사용할 수 있게 하면 좋을 것 같다.
                sub_service_schedule_request = MXSubScheduleRequest(trigger_msg=sub_service_schedule_msg)
                candidate_request_list.append(sub_service_schedule_request)

            target_sub_service_request._candidate_request_list = candidate_request_list
            sub_service_request_key = make_sub_service_request_key(
                sub_service_name=target_sub_service.get_name(),
                sub_service_request_order=target_sub_service_request._sub_service_request_order,
            )
            self._sub_service_request_table[sub_service_request_key] = target_sub_service_request

            if len(target_sub_service_request._candidate_request_list) == 0:
                for function_service in hierarchical_function_service_table:
                    MXLOG_DEBUG(
                        f'sub_service found! - {function_service.get_name()}|{function_service.get_thing_name()}|{function_service.get_middleware_name()}'
                    )
                raise Exception(
                    f'No candidate sub_service found in key:{sub_service_request_key} {self.trigger_msg.super_service_name} super service'
                )


class MXSuperExecuteRequest(MXRequest):
    def __init__(
        self, trigger_msg: MXSuperExecuteMessage = None, super_schedule_request: MXSuperScheduleRequest = None
    ) -> None:
        super().__init__(trigger_msg, None)
        self._action_type = MXActionType.SUPER_EXECUTE

        self.trigger_msg: MXSuperExecuteMessage
        self.result_msg: MXSuperExecuteResultMessage
        self._running: bool = False

        # scheduling이 끝나면 해당 scenario에 대해 어떤 sub_service_type에 대해 thing을 선택할 것인지 정해진다.
        # sub_request_key = make_sub_request_key(subschedule_result_msg.sub_service_name, subschedule_result_msg.sub_service_request_order)
        # sub_request_key: {sub_service_name}@{sub_service_request_order}
        self._sub_service_request_table: Dict[str, MXSubServiceRequest] = {}

        if super_schedule_request:
            self.generate_sub_service_execute_request_list(super_schedule_request=super_schedule_request)

    def set_result_msg(self, result_msg: MXSuperExecuteResultMessage):
        self.result_msg = result_msg

    def get_result_msg(self):
        return self.result_msg

    def is_completed(self):
        if self.result_msg:
            return True
        else:
            return False

    def put_sub_service_execute_result_msg(
        self, sub_service_request_key: str, result_msg: MXSubExecuteResultMessage, timeout: float = None
    ) -> bool:
        if sub_service_request_key not in self._sub_service_request_table:
            MXLOG_DEBUG(
                f'Could not find key {sub_service_request_key} in sub_service_request_table... This key is not mine!',
                'yellow',
            )
            return False

        target_sub_service_request = self._sub_service_request_table[sub_service_request_key]
        for target_request in target_sub_service_request._target_request_list:
            target_thing_check = target_request.trigger_msg.target_thing_name == result_msg.target_thing_name
            target_middleware_check = (
                target_request.trigger_msg.target_middleware_name == result_msg.target_middleware_name
            )
            request_ID_check = target_request.trigger_msg.request_ID == result_msg.request_ID
            if target_thing_check and target_middleware_check and request_ID_check:
                target_request.put_result_msg(result_msg, timeout=timeout)
                return True
        else:
            raise Exception(f'No sub_service {sub_service_request_key} found in _sub_service_request_table')

    def get_sub_service_execute_result_msg_list(
        self, sub_service_request_key: str, timeout: float = None
    ) -> List[MXSubExecuteResultMessage]:
        result_msg_list = []
        target_sub_service_request = self._sub_service_request_table[sub_service_request_key]
        for target_request in target_sub_service_request._target_request_list:
            result_msg_list.append(target_request.get_result_msg(timeout=timeout))
        return result_msg_list

    def generate_sub_service_execute_request_list(
        self, super_schedule_request: 'MXSuperScheduleRequest' = None
    ) -> 'MXSuperExecuteRequest':
        # schedule 단계에서 MXSuperExecuteRequest를 생성한다.
        for sub_service_request_key, sub_service_request in super_schedule_request._sub_service_request_table.items():
            self._sub_service_request_table[sub_service_request_key] = MXSubServiceRequest(
                sub_service_type=sub_service_request._sub_service_type,
                sub_service_request_order=sub_service_request._sub_service_request_order,
                candidate_request_list=sub_service_request._candidate_request_list,
            )
            target_request_list = []
            for candidate_request in sub_service_request._candidate_request_list:
                if candidate_request._status == MXScheduleStatus.CONFIRM:
                    target_request_list.append(to_sub_service_execute_request(candidate_request))
            self._sub_service_request_table[sub_service_request_key]._target_request_list = target_request_list
        return self


class MXSubScheduleRequest(MXRequest):
    def __init__(
        self, trigger_msg: MXSubScheduleMessage = None, result_mqtt_msg: MXSubScheduleResultMessage = None
    ) -> None:
        super().__init__(trigger_msg, result_mqtt_msg)
        self._action_type = MXActionType.SUB_SCHEDULE

        self.trigger_msg: MXSubScheduleMessage
        self.result_msg: MXSubScheduleResultMessage
        self._status: MXScheduleStatus = MXScheduleStatus.INIT
        self._result_queue = Queue()

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['_result_queue']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self._result_queue = Queue()

    def put_result_msg(self, result_msg: MXSubScheduleResultMessage, timeout: float = None):
        self._result_queue.put(result_msg, timeout=timeout)

    def get_result_msg(self, timeout: float = None):
        try:
            return self._result_queue.get(timeout=timeout)
        except Empty:
            raise FunctionTimedOut


class MXSubExecuteRequest(MXRequest):
    def __init__(
        self, trigger_msg: MXSubExecuteMessage = None, result_mqtt_msg: MXSubExecuteResultMessage = None
    ) -> None:
        super().__init__(trigger_msg, result_mqtt_msg)
        self._action_type = MXActionType.SUB_EXECUTE

        self.trigger_msg: MXSubExecuteMessage
        self.result_msg: MXSubExecuteResultMessage
        self._result_queue = Queue()

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['_result_queue']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self._result_queue = Queue()

    def put_result_msg(self, result_msg: MXSubExecuteResultMessage, timeout: float = None):
        self._result_queue.put(result_msg, timeout=timeout)

    def get_result_msg(self, timeout: float = None) -> MXSubExecuteResultMessage:
        try:
            return self._result_queue.get(timeout=timeout)
        except Empty:
            raise FunctionTimedOut


class MXSubServiceRequest:
    def __init__(
        self,
        sub_service_type: MXFunction,
        candidate_request_list: List[MXSubScheduleRequest] = [],
        target_request_list: List[MXSubExecuteRequest] = [],
        sub_service_request_order: int = None,
    ) -> None:
        self._sub_service_type = sub_service_type
        self._candidate_request_list = candidate_request_list
        self._target_request_list = target_request_list
        self._sub_service_request_order = sub_service_request_order

    def __eq__(self, o: 'MXSubServiceRequest') -> bool:
        instance_check = isinstance(o, MXSubServiceRequest)
        # sub_service_type_check = (o._sub_service_type == self._sub_service_type)

        def sub_service_type_check():
            return_type_check = o._sub_service_type._return_type == self._sub_service_type._return_type
            exec_time_check = o._sub_service_type._exec_time == self._sub_service_type._exec_time
            timeout_check = o._sub_service_type._timeout == self._sub_service_type._timeout
            range_type_check = o._sub_service_type._range_type == self._sub_service_type._range_type

            if return_type_check and exec_time_check and timeout_check and range_type_check:
                return True
            else:
                return False

        candidate_request_list_check = o._candidate_request_list == self._candidate_request_list
        target_request_list_check = o._target_request_list == self._target_request_list
        sub_service_request_order_check = o._sub_service_request_order == self._sub_service_request_order

        return (
            instance_check
            and sub_service_type_check
            and candidate_request_list_check
            and target_request_list_check
            and sub_service_request_order_check
        )

    def __deepcopy__(self, memodict={}):
        new_instance = MXSubServiceRequest(self._sub_service_type, self._sub_service_request_order, list())
        new_instance.__dict__.update(self.__dict__)
        new_instance._sub_service_type = copy.deepcopy(self._sub_service_type, memodict)
        new_instance._sub_service_request_order = copy.deepcopy(self._sub_service_request_order, memodict)
        new_instance._candidate_request_list = list()
        new_instance._target_request_list = list()
        return new_instance


def to_sub_service_execute_request(sub_service_schedule_request: MXSubScheduleRequest) -> MXSubExecuteRequest:
    sub_service_schedule_msg: MXSubScheduleMessage = sub_service_schedule_request.trigger_msg
    sub_service_execute_msg = MXSubExecuteMessage(
        sub_service_schedule_msg.sub_service_name,
        'SUPER',
        sub_service_schedule_msg.target_middleware_name,
        sub_service_schedule_msg.requester_middleware_name,
        sub_service_schedule_msg.super_thing_name,
        sub_service_schedule_msg.super_service_name,
        sub_service_schedule_msg.sub_service_request_order,
        sub_service_schedule_msg.scenario,
        request_ID=sub_service_schedule_msg.request_ID,
    )
    sub_service_execute_request = MXSubExecuteRequest(trigger_msg=sub_service_execute_msg)
    return sub_service_execute_request


def to_sub_service_schedule_request(sub_service_execute_request: MXSubExecuteRequest) -> MXSubScheduleRequest:
    sub_service_execute_msg: MXSubExecuteMessage = sub_service_execute_request.trigger_msg
    sub_service_schedule_msg = MXSubScheduleMessage(
        sub_service_name=sub_service_execute_msg.sub_service_name,
        target_thing_name=sub_service_execute_msg.target_thing_name,
        target_middleware_name=sub_service_execute_msg.target_middleware_name,
        requester_middleware_name=sub_service_execute_msg.requester_middleware_name,
        super_thing_name=sub_service_execute_msg.super_thing_name,
        super_service_name=sub_service_execute_msg.super_service_name,
        sub_service_request_order=sub_service_execute_msg.sub_service_request_order,
        scenario=sub_service_execute_msg.scenario,
        request_ID=sub_service_execute_msg.request_ID,
    )
    sub_service_schedule_request = MXSubScheduleRequest(trigger_msg=sub_service_schedule_msg)
    return sub_service_schedule_request
