from logging import raiseExceptions
import xml
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import Locator

from .utils import split_wildcards
from .config import *
from .tags import *
from .parser_utils import TagStack
from pydantic import ValidationError

class KomlCheckError(Exception):
    pass

class KomlHandler(ContentHandler):
    _BEGIN = 0
    _INSIDE_CASE=3
    _INSIDE_FOLLOW = 4
    _INSIDE_PATTERN = 5 
    _INSIDE_SUBPAT = 6 
    _INSIDE_TEMPLATE = 7
    _INSIDE_SWITCH = 8

    def __init__(self):
        self.case_stack = TagStack()
        self.state = self._BEGIN
        self.case_item = {}
        self.cases = []
        self.current_pattern = ''
        # self.locator = Locator()
        # self.setDocumentLocator(self.locator)

    def _location(self):
        # line = self.locator.getLineNumber()
        # column = self.locator.getColumnNumber()
        # return f'(line {line}, column {column})' 
        return f'@case({self.current_pattern})'

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
            allowed = ['random', 'li', 'star', 'memo', 'think', 'func', 'arg', 'switch']
        elif self.state == self._INSIDE_SWITCH:
            allowed = ['pivot', 'scase', 'default', 'random', 'li', 'star', 'memo' , 'think', 'func', 'arg']
        if tag not in allowed:
            raise KomlCheckError(f'tag {tag} is not allowed in this scope' + self._location())

        self._start_element(tag, attributes)

        if tag == 'case':
            self.state = self._INSIDE_CASE
            self.current_pattern = 'NEXT TO @case - ' + self.current_pattern
        elif tag == 'follow':
            self.state = self._INSIDE_FOLLOW
        elif tag == 'pattern':
            self.state = self._INSIDE_PATTERN
        elif tag == 'subpat':
            self.state = self._INSIDE_SUBPAT
        elif tag == 'template':
            self.state = self._INSIDE_TEMPLATE
        elif tag == 'switch':
            self.state = self._INSIDE_SWITCH
    
    def _start_element(self, tag, attributes):
        if tag == 'koml':
            pass
        elif tag == 'case':
            self.case_stack.refresh()
            self.case_item = {k: v for k, v in attributes.items()}
        else:
            self.case_stack.push_tag(tag, attributes)


    def endElement(self, tag):
        if tag == 'koml':
            pass
        elif tag == 'case':
            try:
                case = Case(**self.case_item)
            except ValidationError:
                raise KomlCheckError('<case> check error.. make sure pattern-template is in case!' + self._location())
            self._check_case_valid(case)
            self.cases.append(case)
        else:
            closing_tag = self.case_stack.get_closing_tag()
            if  closing_tag!= tag:
                raise KomlCheckError(f'tag {closing_tag} should be closed before {tag}' + self._location())
            try:
                self._end_element(tag)
            except ValidationError:
                raise KomlCheckError(f'tag <{tag}> check error.. please check all required attribute is given.' + self._location())

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
        elif tag == 'switch':
            self.state = self._INSIDE_TEMPLATE

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
            # only template child is not a list type! 
            elif tag == 'template':
                template_child = self.case_stack.stack[0]
                self.case_item['template'] = Template(child=template_child, **attribute)
            self.case_stack.refresh()


    '''
    split wildcard and append 
    '''
    def _process_child(self, node, mode='default'):
        holder = []
        for item in node:
            if isinstance(item, str):
                words, is_wcs = split_wildcards(item, WILDCARDS)
                for word, is_wc in zip(words, is_wcs):
                    if is_wc:
                        optional = False if '!' in word else True
                        if optional == False and self.state in [self._INSIDE_TEMPLATE, self._INSIDE_SWITCH]:
                            raise KomlCheckError(f'wildcard {word} not allowed in template section. Did you mean {word[:-1]}?' + self._location())
                        holder.append(WildCard(val=word, optional=optional))
                    else:
                        holder.append(Text(val=word))
            else:
                holder.append(item)
        return holder


    def _process_node(self, tag, node, attribute):
        if tag == 'pattern':
            pattern = self._process_child(node)
            return pattern # pat li[union[....]]
        elif tag == 'subpat' or tag == 'follow': # [Li] or pattern
            if len(node) == 0:
                return []
            if isinstance(node[0], PatLi):
                return node # [li<pat>, li<pat> ...]
            else:
                pattern = self._process_child(node)
                return [PatLi(child=pattern)] # no attr
        elif tag == 'template': 
            if len(node) < 1:
                raise KomlCheckError('template should have at least one element' + self._location())
            if isinstance(node[0], Switch) or isinstance(node[0], Random) or isinstance(node[0], TemLi):
                return [node[0]]  # single element 
            else:
                template = self._process_child(node)
                return [TemLi(child=template)] # no attr
        elif tag == 'star' and self.state in [self._INSIDE_TEMPLATE, self._INSIDE_SWITCH]:
            return [Star(**attribute)]
        elif tag == 'star': 
            attr = {**attribute}
            if 'pos' in attr and isinstance(attr['pos'], str):
                attr['pos'] = [attr['pos']]
            if 'npos' in attr and isinstance(attr['npos'], str):
                attr['npos'] = [attr['npos']]
            return [PatStar(**attr)]
        elif tag == 'li':
            if self.state in [self._INSIDE_FOLLOW , self._INSIDE_SUBPAT]:
                pattern = self._process_child(node)
                return [PatLi(child=pattern, **attribute)]
            elif self.state == self._INSIDE_TEMPLATE:
                template = self._process_child(node)
                return [TemLi(child=template, **attribute)]
            else:
                raise KomlCheckError(f'<li> tag not allowed' + self._location())
        elif tag == 'think':
            think = self._process_child(node)
            return [Think(child=think, **attribute)]
        elif tag == 'memo':
            memo_child = self._process_child(node)
            return [Memo(child=memo_child, **attribute)]
        elif tag == 'arg':
            arg = self._process_child(node)
            return [Arg(child=arg, **attribute)]
        elif tag == 'func':
            assert all(isinstance(x, Arg) for x in node)
            assert 'name' in attribute
            return [Func(child=node, **attribute)]
        elif tag == 'pivot':
            pivot = self._process_child(node)
            return [Pivot(child=pivot, **attribute)]
        elif tag == 'scase':
            if isinstance(node[0], Random):
                assert len(node) == 1 , 'random can apear only one'
                return [Scase(child=node[0])]
            else:
                template = self._process_child(node)
                return [Scase(child=TemLi(child=template), **attribute)]
        elif tag == 'default':
            if isinstance(node[0], Random):
                assert len(node) == 1 , 'random can apear only one'
                return [Default(child=node[0])]
            else:
                template = self._process_child(node)
                return [Default(child=TemLi(child=template), **attribute)]
        elif tag == 'switch':
            pivot, scase, default = None, [], None
            for el in node:
                if isinstance(el, Pivot):
                    pivot = el
                elif isinstance(el, Default):
                    default = el
                elif isinstance(el, Scase):
                    scase.append(el)
                else:
                    raise KomlCheckError(f'tag {tag} not allowed in switch' + self._location())
            if not pivot or not default or scase == []:
                raise KomlCheckError(f'pivot, scase, default are needed for switch' + self._location())
            return [Switch(pivot=pivot, scase=scase, default=default, **attribute)]
        elif tag == 'random':
            assert len(node) > 0, f'random should have more than 1 element'
            if not all([isinstance(x, TemLi) for x in node]):
                raise KomlCheckError('all element in <random> tag should be <li>.. ' + self._location)
            return [Random(child=node, **attribute)]
        else:
            raise KomlCheckError(f'tag {tag} not allowed' + self._location())

    def characters(self, content):
        self._characters(content)
        if self.state == self._INSIDE_PATTERN:
            if self.current_pattern.startswith('NEXT'):
                self.current_pattern = ''
            self.current_pattern += content
    
    def _characters(self, content):
        if content == '\n' or content.isspace():
            return
        self.case_stack.push_content(content)

    def _check_case_valid(self, case):
        def _check_pattern_valid(pat_list: PatternT):
            for i in range(len(pat_list) - 1):
                a, b = pat_list[i], pat_list[i + 1]
                if (isinstance(a, PatStar) or a.val == '*') and isinstance(b, WildCard) and b.optional:
                    raise KomlCheckError(f'optional wildcard following Star or * is not allowed \n patern: {[a]} -> {[b]}' + self._location())
                if (isinstance(a, PatStar) or a.val == '*') and (isinstance(b, PatStar) or b.val == '*'):
                    raise KomlCheckError(f'(Star or *) following (Star or *) is not allowed \n patern: {[a]} -> {[b]}' + self._location())

        def _check_template_valid(tem_list: TemplateT, patstar_cnt: int):
            for tag in tem_list:
                if isinstance(tag, Star):
                    if tag.idx and tag.idx > patstar_cnt:
                        raise KomlCheckError(f'idx of <star> in template can\'t exceed number of <star> in pattern' + self._location())

        pattern = case.pattern
        subpat = case.subpat
        template = case.template
        # check case
        if case.id and ' ' in case.id:
            raise KomlCheckError(f'no space allowed in case id {case.id}')

        # check pattern
        patstar_cnt = 0
        _check_pattern_valid(pattern.child)
        for item in pattern.child:
            if isinstance(item, PatStar):
                patstar_cnt += 1
                if item.idx:
                    raise KomlCheckError('idx of <star> in pattern not allowed' + self._location())
        
        # check subpat
        if subpat:
            for spat in subpat.child:
                item_list = spat.child
                _check_pattern_valid(item_list)
                substar_cnt = 0
                substar_idx = [None for _ in range(patstar_cnt)]
                for item in item_list:
                    if isinstance(item, PatStar):
                        substar_cnt += 1
                        if item.idx:
                            if item.idx <= 0 or item.idx > patstar_cnt:
                                raise KomlCheckError(f'idx of star in subpat cannot exceed number of star in pattern \n {spat}' + self._location())
                            substar_idx[item.idx-1] = item.idx
                if substar_cnt != patstar_cnt:
                    raise KomlCheckError(f'star number should be same for pattern({patstar_cnt}) and subpat({substar_cnt}) \n subpat: {spat}' + self._location())
                if any(substar_idx) and None in substar_idx:
                    raise KomlCheckError(f'idx should include all number 1 ~ {patstar_cnt} \n subpat:{spat}' + self._location)
        
        if isinstance(template.child, list): 
            for temli in template.child:
                _check_template_valid(temli.child, patstar_cnt)
        
        if isinstance(template.child, Switch):
            scases = template.child.scase
            default = template.child.default
            for scase in scases:
                _check_template_valid(scase.child, patstar_cnt)

            _check_template_valid(default.child, patstar_cnt)



def create_parser():
    parser = xml.sax.make_parser()
    handler = KomlHandler()
    parser.setContentHandler(handler)
    return parser

