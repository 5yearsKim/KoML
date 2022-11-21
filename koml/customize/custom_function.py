import inspect
from typing import Callable, Any
from .errors import CustomFunctionError
from ..context import Context

class CustomFunction:
    def __init__(self, name: str, func: Callable) -> None:
        self.name: str = name
        self.func: Callable = func
        self.num_arg: int = 0 # initial
        self.is_var_arg: bool = False 
        self._inspect()

    def __call__(self, *args: str, **kwargs: Context) -> str:
        return self.func(*args, **kwargs) # type: ignore
    
    def __repr__(self) -> str:
        return f'function(name={self.name}, num_arg={self.num_arg}{"+" if self.is_var_arg else ""}, )'
    
    def _inspect(self) -> None:
        if not self.name :
            raise CustomFunctionError(f'function key {self.name} should not be empty', self.func)

        spec = inspect.signature(self.func)
        params = spec.parameters.values()

        arg_cnt: int = 0
        has_var_pos: bool= False
        
        if len(params) == 0:
            raise CustomFunctionError(f'no function argument for {self.func.__name__}: koml function must have \'context\' as kwarg', self.func)
        for i, param in enumerate(params):
            # if param.annotation is not str:
            #     raise CustomFunctionError(f'arg type not enforced for {func.__name__}: all arg type should be enforced as str')
            if i == (len(params) - 1) and param.name != 'context':
                raise CustomFunctionError(f'koml function must have context as kwarg', self.func)
            elif i == (len(params) - 1):
                pass
            elif param.kind == param.POSITIONAL_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD:
                arg_cnt += 1
            elif param.kind == param.VAR_POSITIONAL:
                has_var_pos = True
        self.num_arg = arg_cnt
        self.is_var_arg = has_var_pos



    