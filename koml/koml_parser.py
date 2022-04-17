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

class KomlHandler(xml.sax.ContentHandler):
    _BEGIN = 0
    _INSIDE_CASE=3
    _INSIDE_PATTERN = 4
    _INSIDE_SUBPAT = 5
    _INSIDE_TEMPLATE = 6
    def __init__(self):
        self.case_stack = TagStack()
        self.state = self._BEGIN
        self.case_item = {}
        self.cases = []

    def startElement(self, tag, attributes):
        self._start_element(tag, attributes)
    
    def _start_element(self, tag, attributes):
        if tag == 'koml':
            print(tag)
        elif tag == 'case':
            self.case_stack.refresh()
            self.case_item = {}
        else:
            self.case_stack.push_tag(tag, attributes)

        if tag == 'case':
            self.state = self._INSIDE_CASE
        elif tag == 'pattern':
            self.state = self._INSIDE_PATTERN
        elif tag == 'subpat':
            self.state = self._INSIDE_SUBPAT
        elif tag == 'template':
            self.state = self._INSIDE_TEMPLATE


    def endElement(self, tag):
        self._end_element(tag)

    def _end_element(self, tag):
        if tag == 'koml':
            pass
        elif tag == 'case':
            case = Case(**self.case_item)
            self.cases.append(case)
        else:
            node, attribute = self.case_stack.get_node(tag)
            resolved = self._process_node(tag, node, attribute)
            self.case_stack.resolve(tag, resolved)
            # print('tag', tag)
            if self.case_stack.is_resolved():
                if tag == 'pattern':
                    self.case_item['pattern'] = Pattern(child=self.case_stack.stack)
                elif tag == 'subpat':
                    self.case_item['subpat'] = Subpat(child=self.case_stack.stack)
                elif tag == 'template':
                    self.case_item['template'] = Template(child=self.case_stack.stack)
                self.case_stack.refresh()

        if tag == 'case':
            self.state = self._BEGIN
        elif tag == 'pattern':
            self.state = self._INSIDE_CASE
        elif tag == 'subpat':
            self.state = self._INSIDE_CASE
        elif tag == 'template':
            self.state = self._INSIDE_CASE

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
                        print('word', word)
                        holder.append(Text(val=word))
            elif isinstance(item, PatStar):
                item.idx = patstar_cnt
                patstar_cnt += 1
                holder.append(item)
            else:
                holder.append(item)
        return holder

    def _process_node(self, tag, node, attribute):
        if tag == 'pattern':
            pattern = self._process_pattern(node)
            return pattern # pat
        elif tag == 'subpat':
            return node # [li<pat>, li<pat> ...]
        elif tag == 'template':
            return node
        elif tag == 'star' and self.state == self._INSIDE_PATTERN: 
            item = PatStar(**attribute)
            return [item]
        elif tag == 'star':
            item = Star(**attribute)
            return [item]
        elif tag == 'li':
            if self.state == self._INSIDE_SUBPAT:
                pattern = self._process_pattern(node)
                item = Li(child=pattern, **attribute)
                return [item] 
            elif self.state == self._INSIDE_TEMPLATE:
                item = Li(child=node, **attribute)
                return [item]
            else:
                raise KomlParserError('<li> tag not allowed')
        elif tag == 'user':
            item = User(child=node, **attribute)
            return [item]
        elif tag == 'bot':
            item = Bot(child=node, **attribute)
            return [item]
        return ['resolved']


    def characters(self, content):
        self._characters(content)
    
    def _characters(self, content):
        if content == '\n' or content.isspace():
            return
        self.case_stack.push_content(content)