import textwrap
from .abstracts import Tag, TemCandidate
from .sections import Follow, Pattern, Template
from .leafs import *
from .items import TemItem, PatItem, Random
from .errors import TagError

class Case(Tag):
    def __init__(self, pattern: Pattern, template: Template, follow: Follow|None=None, attr: dict[str, str]={}) -> None:
        self.follow: Follow | None = follow
        self.pattern: Pattern = pattern
        self.template: Template = template
        # attributes
        self.id: str|None = None
        super().__init__(attr=attr)
    
    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        content = f'{self.pattern} \n {self.template}'
        if (self.follow):
            content = f'{self.follow}\n{content}'
        return f'*Case* {att_str}\n' + textwrap.indent(content, '  ') 


    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'id':
                self.id = v
            else:
                raise TagError(f'<Case> attribute {k}={v} not supported')

    def _check(self) -> None:
        self._check_blank()

    def _check_blank(self) -> None:
        ''' check if pattern satisfy conditions for blanks of template '''
        key_set: set[str] = set()
        idx_set: set[int] = set()
        tem_items: list[TemItem] = []

        def _tem_item_search(tem_cand: TemCandidate)-> None:
            if isinstance(tem_cand, TemItem):
                tem_items.append(tem_cand)
            elif isinstance(tem_cand, Random):
                for ri in tem_cand.child:
                    _tem_item_search(ri.child)
            else:
                raise TagError(f'checking for {tem_cand} not implemented yet..')

        _tem_item_search(self.template.child)             

        def _blank_search(tag: Tag) -> None:
            ''' search all blank key and idx in template '''
            if hasattr(tag, 'child') and isinstance(tag.child, list):
                for t in tag.child: 
                    return _blank_search(t)
            elif hasattr(tag, 'child') and tag.child is not None: 
                return _blank_search(tag.child)
            else:
                if isinstance(tag, Blank):
                    if tag.key:
                        key_set.add(tag.key)
                    if tag.idx:
                        idx_set.add(tag.idx)
                else:
                    return None
                    
        for tem_item in tem_items:
            _blank_search(tem_item)

        def _assert_pattern(pat_item: PatItem, keys: list[str], max_idx:int|None=None) -> None:
            ''' assert all keys/idx satisfy for pattern '''
            # find all patblank first
            blanks: list[PatBlank] = []
            for tag in pat_item.child:
                if isinstance(tag, PatBlank):
                    blanks.append(tag)
            # check if all keys exist in pattern
            pat_blank_keys: list[str|None] = list(map(lambda x: x.key, blanks))
            for key in keys:
                if key not in pat_blank_keys:
                    raise TagError(f'key {key} should exist in pattern {pat_item}')
            # check if num blanks in pattern >= max_idx - 1
            if max_idx:
                if len(blanks) < max_idx:
                    raise TagError(f'number of blank should be greater than idx {max_idx} for pattern {pat_item}')
        for pat_item in self.pattern.children:
            _assert_pattern(pat_item, list(key_set), max_idx=max(idx_set) if idx_set else None)












    
    