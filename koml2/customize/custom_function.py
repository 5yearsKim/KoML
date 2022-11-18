from typing import Callable
import inspect

class CustomFunction:
    def __init__(self, funcs: dict[str, Callable]={}) -> None:
        self.funcs: dict[str, Callable] = {}
        self.update(funcs)

    def __getitem__(self, key: str) -> Callable|None:
        if key in self.funcs:
            return self.funcs[key]
        else:
            return None
    
    def __contains__(self, key:str) -> bool:
        return key in self.funcs

    def update(self, funcs: dict[str, Callable]) -> None:
        self.funcs.update(funcs)