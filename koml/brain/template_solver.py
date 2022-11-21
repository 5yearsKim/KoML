from korean_rule_helper import JosaHelper
import random
from .pattern_rule import PatternRule
from .errors import TemplateResolverError
from ..tags import * 
from ..context import Context
from ..customize import CustomBag
from .utils import josa2rule

class TemplateSolver:
    def __init__(self, custom_bag: CustomBag) -> None:
        self.josa_helper: JosaHelper = JosaHelper()
        self.custom_bag: CustomBag = custom_bag 

    def solve(self, pattern_rule: PatternRule, context: Context) -> str:
        def _solve_list(tag_list: list[Tag]) -> str:
            holder: list[str] = []
            for tag in tag_list:
                if isinstance(tag, Josa):
                    while holder and holder[-1].isspace():
                        holder.pop()
                    if holder:
                        word = holder[-1].strip()
                        js_rule = josa2rule(tag.val)
                        if js_rule is None:
                            raise TemplateResolverError(f'josa {tag.val} not supported', pattern_rule)
                        word_josa = self.josa_helper.add_josa(word, js_rule)
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
            elif isinstance(tag, Josa):
                raise TemplateResolverError('josa cannot be solved in child level', pattern_rule)
            elif isinstance(tag, Get):
                val = context.get_memo(tag.key)
                if val and isinstance(val, str):
                    return val
                elif tag.default:
                    return tag.default
                else:
                    return f'Get(key={tag.key})'
            elif isinstance(tag, Set):
                solved = _solve_list(tag.child) 
                context.set_memo(tag.key, solved)
                return solved
            elif isinstance(tag, Think):
                _solve_list(tag.child) # solve first
                return ''
            elif isinstance(tag, Func):
                func = self.custom_bag.get_func(tag.name)
                if func:
                    if func.is_var_arg and func.num_arg > len(tag.child):
                        raise TemplateResolverError(f'number of <Arg> {len(tag.child)} for function={tag.name} should be greater than {func.num_arg} ', pattern_rule)
                    if not func.is_var_arg and len(tag.child) != func.num_arg:
                        raise TemplateResolverError(f'number of <Arg>, {len(tag.child)} for function={tag.name}, {func.num_arg}  not matching', pattern_rule)
                    func_args = list(map(lambda x: _solve_list(x.child), tag.child)) # type: ignore
                    return func(*func_args, context=context)
                else:
                    return f'Func(name={tag.name})'
            elif isinstance(tag, Arg):
                solved = _solve_list(tag.child)
                return solved
            elif isinstance(tag, Random):
                weights = list(map(lambda x: x.weight, tag.child))
                tem_picked = random.choices(tag.child, weights=weights, k=1)[0]
                return _solve_single(tem_picked)
            elif isinstance(tag, Ri):
                return _solve_single(tag.child)
            elif isinstance(tag, Switch):
                pivot: str = _solve_single(tag.pivot)
                scase = tag.pick(pivot.strip())
                return _solve_single(scase)
            elif isinstance(tag, Pivot):
                solved = _solve_list(tag.child)
                return solved
            elif isinstance(tag, Scase):
                return _solve_single(tag.child)
            elif isinstance(tag, Default):
                return _solve_single(tag.child)
            else:
                raise TemplateResolverError(f'solving tag {tag} is not supported', pattern_rule)
        tem_child = pattern_rule.template.child
        return _solve_single(tem_child) #type: ignore


        