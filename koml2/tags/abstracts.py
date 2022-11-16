from abc import ABC, abstractmethod
import textwrap

class Tag(ABC):
    def __init__(self, attr: dict[str, str]={}):
        self.attr = attr

    def __str__(self) -> str:
        attr_list = [f'{k}: {v}' for k, v in self.attr.items()]
        attr_str = ','.join(attr_list)
        title = f'{self.__class__.__name__}({attr_str})'
        if (self.child):
            return title + '\n' + textwrap.indent(str(self.child), '  ')
        return title

    @abstractmethod 
    def _check(self):
        pass


    


