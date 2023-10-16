from enum import Enum, auto


class MXErrorCode(Enum):
    NO_ERROR = 0
    FAIL = -1
    TIMEOUT = -2
    NO_PARALLEL = -3
    DUPLICATE = -4
    NOT_SUPPORTED = -5
    INVALID_REQUEST = -7

    REGISTER_NO_ERROR = -8
    REGISTER_FAIL = -9
    REGISTER_DUPLICATE = -10

    EXECUTE_FAIL = -11
    EXECUTE_TIMEOUT = -12
    EXECUTE_NO_PARALLEL = -13
    EXECUTE_DUPLICATE = -14

    EXECUTE_ARG_FAIL = -15

    VALUE_ERROR = -16
    TYPE_ERROR = -18
    NOT_FOUND_ERROR = -19

    UNDEFINED = 'undefined'

    @classmethod
    def to_mx_error_code(cls, type: int):
        if type is not None:
            for mx_error_code in MXErrorCode:
                if mx_error_code.value == type:
                    return mx_error_code
        else:
            return MXErrorCode.get(type)

    @classmethod
    def get(cls, type: int) -> 'MXErrorCode':
        try:
            if type is not None:
                for mx_error_type in MXErrorCode:
                    if mx_error_type.value == type:
                        return mx_error_type
                return cls.UNDEFINED
            else:
                return MXErrorCode.get(type)
        except Exception:
            return cls.UNDEFINED

    def __str__(self):
        return self.name


class MXError(Exception):
    def __init__(self, error_code: MXErrorCode, *args: object, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self._error_code: MXErrorCode = error_code


class MXFailError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.FAIL, *args, **kwargs)


class MXTimeoutError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.TIMEOUT, *args, **kwargs)
        self._error_code = MXErrorCode.TIMEOUT


class MXNoParallelError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.NO_PARALLEL, *args, **kwargs)


class MXDuplicatedError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.DUPLICATE, *args, **kwargs)


class MXNotSupportedError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.NOT_SUPPORTED, *args, **kwargs)


class MXInvalidRequestError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.INVALID_REQUEST, *args, **kwargs)


class MXValueError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.VALUE_ERROR, *args, **kwargs)


class MXTypeError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.TYPE_ERROR, *args, **kwargs)


class MXNotFoundError(MXError):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        super().__init__(MXErrorCode.NOT_FOUND_ERROR, *args, **kwargs)
