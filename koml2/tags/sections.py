from .abstracts import Tag
from .items import PatItem, TemItem
from .errors import TagError

class Follow(Tag):
    def __init__(self, children: list[PatItem], attr: dict[str, str] ) -> None:
        self.children: list[PatItem] = children
        # attributes
        self.cid: str|None = None 
        super().__init__(attr=attr)
    
    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        flist = list(map(lambda x: f' ㄴ {x}' ,self.children))
        return f'Follow {att_str}\n' + '\n'.join(flist) 

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'cid':
                self.cid = v
            else:
                raise TagError(f'<Follow> attribute {k}={v} not supported')

class Pattern(Tag):
    def __init__(self, children: list[PatItem], attr: dict[str, str]={}) -> None:
        self.children: list[PatItem] = children
        super().__init__(attr=attr)
    
    def __repr__(self) -> str:
        plist = list(map(lambda x: f' ㄴ {x}' ,self.children))
        return 'Pattern \n' + '\n'.join(plist)

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'<Pattern> attribute {k}={v} not supported')


class Template(Tag):
    def __init__(self, child: TemItem, attr: dict[str, str]={}) -> None :
        self.child: TemItem = child
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        return 'Template \n' + f' ㄴ {self.child}' 

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'<Template> attribute {k}={v} not supported')

