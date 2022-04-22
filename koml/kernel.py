import xml
from typing import Optional, Tuple
from .koml_parser import create_parser
from .pattern_matcher import PatternMatcher
from .context import Context
from .custom_function import CustomFunction
from .tags import *
import random

class KomlKernelError(Exception):
    pass

class Kernel:
    def __init__(self, custom_func :Optional[CustomFunction]=None):
        self._brain = PatternMatcher()
        if custom_func is None:
            self.funcs = CustomFunction()
        else:
            self.funcs = custom_func
    
    def learn(self, files, save_path=None):
        for file in files:
            print('@ ' + file)
            parser = create_parser()
            handler = parser.getContentHandler()
            try:
                parser.parse(file)
            except xml.sax.SAXParseException as err:
                print('error:', err)
                continue

            for case in handler.cases:
                self._brain.add(case)
        if save_path:
            self._brain.save('brain.pickle')
    
    def recall(self, path):
        self._brain.load(path)

    def respond(self, question:str, context:Context):
        matched, args = self._brain.match(question, context)
        # print(matched, args, context.history)
        if not matched:
            return None, context
        answer = self._resolve(matched, args, context)
        context.push_history(question, answer, cid=matched.id)
        return answer, context

    def converse(self):
        context = Context()
        while True:
            question = input('<< ')
            answer, context = self.respond(question, context)
            print(f'>> {answer}')
    
    def _resolve(self, case: Case, args: Tuple[str], context: Context):
        t_child = case.template.child
        def resolve_helper(t_child):
            if isinstance(t_child, Switch):
                switch = t_child
                pivot = self._resolve_template(switch.pivot.child, args, context)
                # scase's child = Random | TemLi
                for scase in switch.scase:
                    if scase.pivot == pivot:
                        return resolve_helper(scase.child)
                # default's child = Random | TemLi
                default = switch.default
                return resolve_helper(default.child)
            elif isinstance(t_child, Random):
                temli = random.choice(t_child.child)
                return self._resolve_template(temli.child, args, context)
            elif isinstance(t_child, TemLi):
                return self._resolve_template(t_child.child, args, context)
            else:
                raise KomlKernelError(f'template type {t_child} not possible')
        return resolve_helper(t_child)

    # only resolve TemplateT
    def _resolve_template(self, template: TemplateT, args: Tuple[str], context: Context):
        cnt_list = []
        def resolve_helper(tag):
            if isinstance(tag, str):
                return tag
            if isinstance(tag, list):
                holder = []
                for t in tag:
                    resolved = resolve_helper(t)
                    holder.append(resolved)
                sent = ''
                for t in holder:
                    if sent and isinstance(t, WildCard):
                        sent = self._brain.resolve_wildcard(sent, t)
                    elif isinstance(t, str):
                        sent += t
                    else:
                        raise KomlKernelError(f'tag {t} maybe not resolved?')
                return sent
            if isinstance(tag, Text):
                return tag.val
            if isinstance(tag, WildCard):
                return tag # do not resolve - resolve in higher level

            # exception: Func handle specially
            if isinstance(tag, Func):
                fargs = []
                for t in tag.child:
                    assert isinstance(t, Arg)
                    farg = resolve_helper(t)
                    fargs.append(farg)
                f = self.funcs[tag.name]
                if not f:
                    return f'undefined function {tag.name}'
                try:
                    return f(*fargs, context=context)
                except Exception as e:
                    raise KomlKernelError(f'custom function {tag.name} with args {fargs} raised error: {e}')
            # has child from below
            if isinstance(tag, Node) and tag.child:
                tag.child = resolve_helper(tag.child)

            if isinstance(tag, Star):
                if tag.idx:
                    assert 0 < tag.idx <= len(args)
                    return args[tag.idx - 1]
                else:
                    cnt_list.append('*') # to make arg_idx
                    arg_idx = min(len(cnt_list) - 1, len(args) - 1 )
                    return args[arg_idx]
            if isinstance(tag, Get):
                return context.get_memo(tag.name)
            if isinstance(tag, Set) and tag.child:
                context.set_memo(tag.name, tag.child)
                return tag.child
            if isinstance(tag, Think):
                return ''
            if isinstance(tag, Arg):
                return tag.child
            raise KomlKernelError(f'tag {tag} ({type(tag)}) not supported')
        return resolve_helper(template)

            


    

    

