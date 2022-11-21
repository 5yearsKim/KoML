from abc import ABC, abstractmethod
import textwrap

class Tag(ABC):
    def __init__(self, attr: dict[str, str]={}):
        self.attr = attr
        self._decode_attr()
        self._check()

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod 
    def _check(self) -> None:
        pass

    @abstractmethod 
    def _decode_attr(self) -> None:
        pass

class TemCandidate(Tag):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod 
    def _check(self) -> None:
        pass

    @abstractmethod 
    def _decode_attr(self) -> None:
        pass

class SwitchCandidate(Tag):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod 
    def _check(self) -> None:
        pass

    @abstractmethod 
    def _decode_attr(self) -> None:
        pass

# class Node(Tag):
#     def __init__(self, child: list[Tag], attr: dict[str, str]={}):
#         self.child: list[Tag] = child
#         super().__init__(attr=attr)

#     def __repr__(self) -> str:
#         att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
#         if att_str:
#             return f'{self.__class__.__name__}({self.child}, {att_str})' 
#         else :
#             return f'{self.__class__.__name__}({self.child})' 

#     @abstractmethod 
#     def _check(self) -> None:
#         pass

#     @abstractmethod 
#     def _decode_attr(self) -> None:
#         pass



    


