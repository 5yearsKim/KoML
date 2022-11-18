from typing import Callable

class CustomFunctionError(Exception):
    def __init__(self, message: str, func: Callable):
        err_msg = f'\n**************\n{message}, func: {func}'
        super().__init__(err_msg)
