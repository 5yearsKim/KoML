from korean_rule_helper import JosaHelper
from .pattern_rule import PatternRule
from .errors import TemplateResolverError
from ..tags import * 

class TemplateSolver:
    def __init__(self) -> None:
        self.josa_helper: JosaHelper = JosaHelper()

    def solve(self, pattern_rule: PatternRule) -> str:
        def _solve_list(tag_list: list[Tag]) -> str:
            holder: list[str] = []
            for tag in tag_list:
                if isinstance(tag, Josa):
                    while holder and holder[-1].isspace():
                        holder.pop()
                    if holder:
                        word = holder[-1].strip()
                        if tag.val == '_s':
                            js_type =  'I_GA'
                        elif tag.val == '_c':
                            js_type = 'I_GA'
                        elif tag.val == '_x':
                            js_type = 'EUN_NEUN'
                        elif tag.val == '_o':
                            js_type = 'EUL_REUL'
                        elif tag.val == '_ee':
                            js_type = 'I_X'
                        elif tag.val == '_ya':
                            js_type = 'A_YA'
                        else:
                            raise TemplateResolverError(f'josa {tag.val} not supported', pattern_rule)
                        word_josa = self.josa_helper.add_josa(word, js_type)
                        holder[-1] = word_josa
                else:
                    solved = _solve_single(tag)
                    holder.append(solved)
            return ''.join(holder)

        def _solve_single(tag: Tag) -> str:
            if isinstance(tag, TemItem):
                return _solve_list(tag.child)
            elif isinstance(tag, Text):
                return tag.val
            elif isinstance(tag, Blank):
                if tag.key:
                    picked = pattern_rule.key_arg(tag.key)
                    if not picked:
                        raise TemplateResolverError(f'blank key {tag.key} is not given for pattern', pattern_rule)
                    return picked
                if tag.idx:
                    try:
                        picked = pattern_rule.idx_arg(tag.idx)
                        return picked if picked else ''
                    except IndexError as e:
                        raise TemplateResolverError(str(e), pattern_rule)
                else:
                    try:
                        picked = pattern_rule.idx_arg(1)
                        return picked if picked else ''
                    except IndexError as e:
                        raise TemplateResolverError(str(e), pattern_rule)
            elif isinstance(tag, WildCard):
                raise TemplateResolverError('wildcard cannot be solved in child level', pattern_rule)
            elif isinstance(tag, Get):
                return 'GET(TODO)'
            elif isinstance(tag, Set):
                # TODO
                return _solve_list(tag.child) 
            elif isinstance(tag, Think):
                return ''
            else:
                raise TemplateResolverError(f'solving tag {tag} is not supported', pattern_rule)
        template = pattern_rule.template.child
        return _solve_single(template)


        