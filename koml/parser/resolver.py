# from xml.sax.xmlreader import Locator
from typing import Callable
from ..tags import *
from .errors import KomlCheckError, FileLoc
from .koml_state import KomlState
from .raw_tag import RawTag
from .utils import split_wildcards
from ..config import WILDCARDS, JOSAS

class Resolver:
    def __init__(self, get_loc: Callable[[], FileLoc]) -> None:
        self.stack: list[str|RawTag|Tag] = []
        # self.used: bool = False
        self.get_loc = get_loc

    @property
    def location(self) -> FileLoc:
        return self.get_loc() 

    def _raw_tag_at(self, tag: str) -> int:
        for i in range(len(self.stack) -1, -1, -1):
            item = self.stack[i]
            if isinstance(item, RawTag) and item.tag == tag:
                return i
        return -1
    
    def push_tag(self, tag: str, attr: dict[str, str]={}) -> None:
        # self.used = True
        raw_tag = RawTag(tag, attr)
        self.stack.append(raw_tag)
    
    def push_content(self, content: str, state: KomlState) -> None:
        if not content:
            return
        if state in [KomlState.IN_FOLLOW, KomlState.IN_PATTERN]:
            content = content.strip()
        self.stack.append(content)

    def finalize(self) -> Case:
        if not (self.stack and isinstance(self.stack[0], Case)):
            raise KomlCheckError('tag <case> failed to resolved', self.location)
        case: Case = self.stack[0]
        self.stack.clear()
        return case
    
    def resolve(self, tag: str, state: KomlState) -> None:
        tag_idx = self._raw_tag_at(tag)
        if tag_idx < 0:
            print(self.stack)
            raise KomlCheckError(f'tag <{tag}> cannot be resolved', self.location)
        raw_tag: RawTag = self.stack[tag_idx] #type: ignore
        raw_items = self.stack[tag_idx + 1:]
        resolved = self._resolve(raw_tag, raw_items, state) 
        self.stack = self.stack[:tag_idx] + [resolved]

    
    def _resolve(self, raw: RawTag, items: list[str|RawTag|Tag], state: KomlState) -> Tag:
        tag , attr = raw.tag, raw.attr

        processed: list[Tag] = []
        # processing child
        if any([isinstance(x, str) for x in items]):
            for item in items:
                if isinstance(item, RawTag):
                    raise KomlCheckError(f'tag <{tag}> found in wrong place', self.location)
                # josa 
                elif isinstance(item, str) and state == KomlState.IN_TEMPLATE:
                    words, is_jss = split_wildcards(item, JOSAS)
                    for word, is_js in zip(words, is_jss):
                        if is_js:
                            josa = Josa(word)
                            processed.append(josa)
                        else:
                            processed.append(Text(word))
                # wildcard 
                elif isinstance(item, str):
                    words, is_wcs = split_wildcards(item, WILDCARDS)
                    for word, is_wc in zip(words, is_wcs):
                        if is_wc:
                            wildcard = WildCard(word)
                            processed.append(wildcard)
                        else:
                            processed.append(Text(word))
                elif isinstance(item, Tag):
                    processed.append(item)
                else:
                    raise KomlCheckError(f'tag <{tag}> is not supported', self.location)
        # all items are tag, not str
        else:
            assert all([not isinstance(x, RawTag) for x in items])
            processed = items # type: ignore


        ''' 
        items all processed above - no more str or RawTag
        processed is all tag
        '''

        def _process_tem_item(processed: list[Tag]) -> TemItem|Random:
            # Random
            if any([isinstance(x, Random) for x in processed]):
                assert len(processed) == 1 
                assert isinstance(processed[0], Random)
                return processed[0]
            # TemItem
            else:
                return TemItem(processed)

        try :
            if tag == 'case':
                follow: Follow|None = None
                pattern: Pattern|None = None
                template: Template|None = None
                for item in processed:
                    if isinstance(item, Follow):
                        follow = item
                    elif isinstance(item, Pattern):
                        pattern = item
                    elif isinstance(item, Template):
                        template = item
                    else:
                        raise KomlCheckError(f'tag {item} not supported for case', self.location)
                if pattern is None:
                    raise KomlCheckError('pattern is required for case', self.location)
                if template is None:
                    raise KomlCheckError('template is required for case', self.location)
                return Case(pattern, template, follow=follow, attr=attr)
            elif tag == 'follow':
                if all(isinstance(x, PatItem) for x in processed):
                    return Follow(processed, attr=attr) # type: ignore
                elif any(isinstance(x, PatItem ) for x in processed):
                    raise KomlCheckError(f'contents inside of <follow> maybe is outside of <li> tag', self.location)
                else:
                    pat_item = PatItem(processed)
                    return Follow([pat_item], attr=attr)
            elif tag == 'pattern':
                if all(isinstance(x, PatItem) for x in processed):
                    return Pattern(processed, attr=attr) # type: ignore
                elif any(isinstance(x, PatItem ) for x in processed):
                    raise KomlCheckError(f'contents inside of <pattern> maybe is outside of <li> tag', self.location)
                else:
                    pat_item = PatItem(processed)
                    return Pattern([pat_item], attr=attr)
            elif tag == 'template':
                tem_item = _process_tem_item(processed)
                return Template(tem_item, attr=attr)
            # processing leafs
            elif tag == 'blank'  and state in [KomlState.IN_FOLLOW, KomlState.IN_PATTERN]:
                return PatBlank(attr=attr)
            elif tag == 'blank':
                return Blank(attr=attr)
            elif tag == 'get':
                return Get(attr=attr)
            #processing nodes
            elif tag == 'li':
                if state in [KomlState.IN_FOLLOW, KomlState.IN_PATTERN]:
                    return PatItem(processed)
                else:
                    raise KomlCheckError(f'<li> tag is not applicable for state {state}', self.location)
            elif tag == 'set':
                return Set(processed, attr=attr)
            elif tag == 'think':
                return Think(processed, attr=attr)
            elif tag == 'func':
                return Func(processed, attr=attr) # type: ignore
            elif tag == 'arg':
                return Arg(processed, attr=attr)
            elif tag == 'random':
                return Random(processed, attr=attr) #type: ignore
            elif tag == 'ri':
                tem_item= _process_tem_item(processed)
                return Ri(tem_item, attr=attr)
            elif tag == 'switch':
                return Switch.from_children(processed)
            elif tag == 'pivot':
                return Pivot(processed, attr=attr)
            elif tag == 'scase':
                tem_item= _process_tem_item(processed)
                return Scase(tem_item, attr=attr)
            elif tag == 'default':
                tem_item= _process_tem_item(processed)
                return Default(tem_item, attr=attr)
            else:
                raise KomlCheckError(f'tag {tag} is not allowed', self.location)
        except TagError as e:
            raise KomlCheckError(f'Tag Error: {e}', self.location)

        







        