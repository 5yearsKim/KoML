import inspect
from pydantic import BaseModel
from typing import Dict, Callable

class KomlFunctionError(Exception):
    pass

class CustomFunction:
    def __init__(self, funcs: Dict[str, Callable]={}):
        self._funcs = {}
        self.update_funcs(funcs)

    def has_key(self, k):
        return k in self._funcs

    def __getitem__(self, key):
        try:
            return self._funcs[key]
        except:
            return None

    def update(self, *args, **kwargs):
        return self._funcs.update(*args, **kwargs)

    def update_funcs(self, funcs: Dict[str, Callable]):
        self.check_funcs_valid(funcs)
        self._funcs.update(funcs)

    def check_funcs_valid(self, funcs: Dict[str, Callable]):
        for fname, func in funcs.items():
            if len(fname) == 0:
                raise KomlFunctionError('function key should not be empty')
            self._koml_strict(func)

    def _koml_strict(self, func):
        spec = inspect.signature(func)
        items = spec.parameters.items()
        if len(items) == 0:
            raise KomlFunctionError(f'no function argument for {func.__name__}: koml function should get \'context\' as kwarg')
        for i, (param_name, param) in enumerate(items):
            if param.kind== param.POSITIONAL_OR_KEYWORD:
                if param.annotation is not str:
                    raise KomlFunctionError(f'arg type not enforced for {func.__name__}: all arg type should be enforced as str')
            if i == len(items) - 1:
                if param_name != 'context':
                    raise KomlFunctionError(f'no context for {func.__name__}: koml function should get \'context\' as kwarg')
                if param.kind!= param.KEYWORD_ONLY:
                    raise KomlFunctionError(f'*arg should preceed context for {func.__name__}: koml function should get flexible number of input')