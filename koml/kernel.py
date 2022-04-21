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

    
    def learn(self, files):
        for file in files:
            parser = create_parser()
            handler = parser.getContentHandler()
            try:
                parser.parse(file)
            except xml.sax.SAXParseException as err:
                print('error:', err)
                continue

            for case in handler.cases:
                self._brain.add(case)
        self._brain.save('brain.pickle')
    
    def recall(self, path):
        self._brain.load(path)

    def respond(self, question:str, context:Context):
        matched, args = self._brain.match(question, context)
        if not matched:
            return None, context
        answer = self._resolve(matched, args, context)
        context.push_history(question, answer)
        return answer, context

    def converse(self):
        context = Context()
        while True:
            question = input('<< ')
            answer, context = self.respond(question, context)
            print(context.history)
            print(f'>> {answer}')
    
    def _resolve(self, case: Case, args: Tuple[str], context: Context):
        template = case.template
        if isinstance(template.child, Switch):
            return 'switch need to be resolved'
        elif isinstance(template.child, list):
            temli = random.choice(template.child)
            return self._resolve_template(temli.child, args, context)
        else:
            raise KomlKernelError(f'template type {template.child} not possible')

    def _resolve_template(self, template: TemplateT, args: Tuple[str], context: Context):
        cnt_list = []
        def resolve_helper(tag):
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
            if tag.child:
                tag.child = resolve_helper(tag.child)
            if isinstance(tag, Text):
                return tag.val
            if isinstance(tag, WildCard):
                return tag # do not resolve - resolve in higher level
            if isinstance(tag, Star):
                if tag.get:
                    return context.get_star(tag.get)
                if tag.idx:
                    assert 0 < tag.idx <= len(args)
                    return args[tag.idx - 1]
                if tag.set:
                    context.set_star(tag.child)
                    return tag.child
                cnt_list.append('*') # to make arg_idx
                arg_idx = min(len(cnt_list) - 1, len(args - 1) )
                return args[arg_idx]
            if isinstance(tag, User):
                return ('not implemented')
            if isinstance(tag, Bot):
                return ('not implemented')
            if isinstance(tag, Func):
                return ('not implemented')
            if isinstance(tag, Arg):
                return ('not implemented')
                
            raise KomlKernelError(f'tag {tag} ({type(tag)}) not supported')
        return resolve_helper(template)

            


    

    

