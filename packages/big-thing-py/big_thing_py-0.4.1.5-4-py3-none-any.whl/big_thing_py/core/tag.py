from big_thing_py.utils import *


class MXTag:
    def __init__(self, name: str):
        self._name: str = name

        if not check_valid_identifier(self._name):
            raise MXValueError(
                f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}'
            )

    def __eq__(self, o: 'MXTag') -> bool:
        name_check = o._name == self._name

        return isinstance(o, MXTag) and name_check

    def __str__(self) -> str:
        return self._name

    def dict(self):
        return {'name': self._name}

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

    def get_name(self):
        return self._name

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_name(self, name):
        self._name = name
