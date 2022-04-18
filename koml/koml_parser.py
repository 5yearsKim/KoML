from xml.sax.xmlreader import Locator
import xml.sax
import xml.sax.handler
import xml
from .tags import *
from .utils import split_wildcards
from .config import *

class KomlParserError(Exception):
    pass

class TagStack:
    def __init__(self):
        self.tag_dict = {}
        self.stack = []
        self.tag_history = [] # for assertion

    def __len__(self):
        return len(self.stack)

    def is_resolved(self):
        return self.stack != [] and self.tag_history == []

    def refresh(self):
        self.tag_dict.clear()
        self.stack.clear()
        self.tag_history.clear()
    
    def push_tag(self, tag, attributes):
        item = (len(self.stack), tag, attributes)
        if tag in self.tag_dict:
            self.tag_dict[tag].append(item)
        else:
            self.tag_dict[tag] = [item]
        self.stack.append(None)
        self.tag_history.append(tag)

    def push_content(self, content):
        if self.tag_history == []: 
            return
        self.stack.append(content)

    def get_node(self, tag):
        tag_idx, _, attribute = self.tag_dict[tag][-1]
        item = self.stack[tag_idx:]
        if item[0] == None:
            item.pop(0)
        return item, attribute

    def resolve(self, tag, resolved):
        assert tag == self.tag_history[-1], f'tag {tag} is not the last node!'
        tag_idx, _, _ = self.tag_dict[tag][-1]
        self.stack = self.stack[:tag_idx] + [*resolved]
        self.tag_dict[tag].pop()
        self.tag_history.pop()
    
    def get_closing_tag(self):
        if self.tag_history == []:
            return None
        return self.tag_history[-1]


class KomlHandler(xml.sax.ContentHandler):
    _BEGIN = 0
    _INSIDE_CASE=3
    _INSIDE_FOLLOW = 4
    _INSIDE_PATTERN = 5 
    _INSIDE_SUBPAT = 6 
    _INSIDE_TEMPLATE = 7
    def __init__(self):
        self.case_stack = TagStack()
        self.state = self._BEGIN
        self.case_item = {}
        self.cases = []

    def startElement(self, tag, attributes):
        if self.state == self._BEGIN:
            allowed = ['koml', 'case']
        elif self.state == self._INSIDE_CASE:
            allowed = ['follow', 'pattern', 'subpat', 'template']
        elif self.state == self._INSIDE_FOLLOW:
            allowed = ['li']
        elif self.state == self._INSIDE_PATTERN:
            allowed = ['star']
        elif self.state == self._INSIDE_SUBPAT:
            allowed = ['li', 'star']
        elif self.state == self._INSIDE_TEMPLATE:
            allowed = ['li', 'bot', 'user', 'star']
        if tag not in allowed:
            raise KomlParserError(f'tag {tag} is not allowed in this scope')

        self._start_element(tag, attributes)

        if tag == 'case':
            self.state = self._INSIDE_CASE
        elif tag == 'follow':
            self.state = self._INSIDE_FOLLOW
        elif tag == 'pattern':
            self.state = self._INSIDE_PATTERN
        elif tag == 'subpat':
            self.state = self._INSIDE_SUBPAT
        elif tag == 'template':
            self.state = self._INSIDE_TEMPLATE
    
    def _start_element(self, tag, attributes):
        if tag == 'koml':
            print(tag)
        elif tag == 'case':
            self.case_stack.refresh()
            self.case_item = {}
        else:
            self.case_stack.push_tag(tag, attributes)


    def endElement(self, tag):
        if tag == 'koml':
            pass
        elif tag == 'case':
            case = Case(**self.case_item)
            self.cases.append(case)
        else:
            closing_tag = self.case_stack.get_closing_tag()
            if  closing_tag!= tag:
                raise KomlParserError(f'tag {closing_tag} should be closed before {tag}')

            self._end_element(tag)

        if tag == 'case':
            self.state = self._BEGIN
        elif tag == 'follow':
            self.state = self._INSIDE_CASE
        elif tag == 'pattern':
            self.state = self._INSIDE_CASE
        elif tag == 'subpat':
            self.state = self._INSIDE_CASE
        elif tag == 'template':
            self.state = self._INSIDE_CASE

    # process tag except [koml, case]
    def _end_element(self, tag): 
        node, attribute = self.case_stack.get_node(tag)
        resolved = self._process_node(tag, node, attribute)
        self.case_stack.resolve(tag, resolved)
        # print('tag', tag)
        if self.case_stack.is_resolved():
            if tag == 'follow':
                self.case_item['follow'] = Follow(child=self.case_stack.stack, **attribute)
            elif tag == 'pattern':
                self.case_item['pattern'] = Pattern(child=self.case_stack.stack, **attribute)
            elif tag == 'subpat':
                self.case_item['subpat'] = Subpat(child=self.case_stack.stack, **attribute)
            elif tag == 'template':
                self.case_item['template'] = Template(child=self.case_stack.stack, **attribute)
            self.case_stack.refresh()


    def _process_pattern(self, node):
        holder = []
        patstar_cnt = 1
        for item in node:
            if isinstance(item, str):
                words, is_wcs = split_wildcards(item, WILDCARDS)
                for word, is_wc in zip(words, is_wcs):
                    if is_wc:
                        holder.append(WildCard(val=word))
                    else:
                        holder.append(Text(val=word))
            elif isinstance(item, PatStar):
                item.idx = patstar_cnt
                patstar_cnt += 1
                holder.append(item)
            else:
                holder.append(item)
        return holder
    
    def _process_template(self, node):
        holder = []
        for item in node:
            if isinstance(item, str):
                words, is_wcs = split_wildcards(item, WILDCARDS)
                for word, is_wc in zip(words, is_wcs):
                    if is_wc:
                        holder.append(WildCard(val=word))
                    else:
                        holder.append(Text(val=word))
            else:
                holder.append(item)
        return holder


    def _process_node(self, tag, node, attribute):
        if tag == 'pattern':
            pattern = self._process_pattern(node)
            return pattern # pat
        elif tag == 'subpat' or tag == 'follow': # [Li] or pattern
            assert len(node) > 0, f'{tag} should have more than 1 Li element'
            if isinstance(node[0], PatLi):
                return node # [li<pat>, li<pat> ...]
            else:
                pattern = self._process_pattern(node)
                item = PatLi(child=pattern) # no attr
                return [item]
        elif tag == 'template':
            assert len(node) > 0, f'{tag} should have more than 1 Li element'
            if isinstance(node[0], TemLi):
                return node # [li<tem>, li<tem> ...]
            else:
                template = self._process_template(node)
                item = TemLi(child=template) # no attr
                return [item]
        elif tag == 'star' and self.state == self._INSIDE_TEMPLATE:
            item = Star(**attribute)
            return [item]
        elif tag == 'star': 
            item = PatStar(**attribute)
            return [item]
        elif tag == 'li':
            if self.state in [self._INSIDE_FOLLOW , self._INSIDE_SUBPAT]:
                pattern = self._process_pattern(node)
                item = PatLi(child=pattern, **attribute)
                return [item]
            elif self.state == self._INSIDE_TEMPLATE:
                template = self._process_template(node)
                item = TemLi(child=template, **attribute)
                return [item]
            else:
                raise KomlParserError('<li> tag not allowed')
        elif tag == 'user':
            item = User(child=node, **attribute)
            return [item]
        elif tag == 'bot':
            item = Bot(child=node, **attribute)
            return [item]
        else:
            raise KomlParserError(f'tag {tag} not allowed')


    def characters(self, content):
        self._characters(content)
    
    def _characters(self, content):
        if content == '\n' or content.isspace():
            return
        self.case_stack.push_content(content)

def create_parser():
    parser = xml.sax.make_parser()
    handler = KomlHandler()
    parser.setContentHandler(handler)
    return parser

