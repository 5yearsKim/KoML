import textwrap
from .abstracts import Tag
from .sections import Follow, Pattern, Template
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

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'id':
                self.id = v
            else:
                raise TagError(f'<Case> attribute {k}={v} not supported')
    