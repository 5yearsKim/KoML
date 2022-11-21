from typing import Callable
from .custom_function import CustomFunction
from .preprocessor import Preprocessor, DefaultPreprocessor

class CustomBag:
    def __init__(self, funcs: dict[str, Callable]={}, preprocessor:Preprocessor|None=None) -> None:
        self.funcs: dict[str, CustomFunction] = {}
        self.preprocessor: Preprocessor = preprocessor or DefaultPreprocessor()
        self.update_func(funcs)

    def update_func(self, funcs: dict[str, Callable]) -> None:
        for name, func in funcs.items():
            self.funcs[name] = CustomFunction(name, func)

    def get_func(self, name:str) -> CustomFunction|None :
        if name in self.funcs:
            return self.funcs[name]
        else:
            return None 

