from typing import Callable
from .custom_function import CustomFunction

class CustomBag:
    def __init__(self, funcs: dict[str, Callable]={}) -> None:
        self.funcs: dict[str, CustomFunction] = {}
        self.update_func(funcs)

    def update_func(self, funcs: dict[str, Callable]) -> None:
        for name, func in funcs.items():
            self.funcs[name] = CustomFunction(name, func)

    def get_func(self, name:str) -> CustomFunction|None :
        if name in self.funcs:
            return self.funcs[name]
        else:
            return None 

