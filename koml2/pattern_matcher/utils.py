from korean_rule_helper import Rule
from ..tags import * 

def pattern2rule(pattern: PatItem) -> list[Rule]:
    holder: list[Rule] = []
    for item in pattern.child:
        if isinstance(item, Text):
            rule: Rule = Rule(surface=item.val)
        elif isinstance(item, WildCard):
            rule = convert_wildcard(item) 
        elif isinstance(item, PatBlank):
            rule = Rule(blank=True, pos=item.pos, npos=item.npos)
        else:
            raise Exception(f'pattern converting for {item} not supported')
        holder.append(rule)
    return holder
        
'''
WILDCARDS = ['*', '_', '_?'] + \
    ['_s',  '_c',  '_x',  '_o'] + \
     ['_s?', '_c?', '_x?', '_o?', '_i']
'''
def convert_wildcard(wildcard: WildCard) -> Rule:
    wc: str = wildcard.val 
    optional = wildcard.optional
    if wc == '*':
        return Rule(surface='*')
    elif wc in ['_', '_?']:
        return Rule(pos='J', optional=optional)
    elif wc in ['_s', '_s?']:
        return Rule(pos='JKS', optional=optional)
    elif wc in ['_c' , '_c?']:
        return Rule(pos='JKC', optional=optional)
    elif wc in ['_x' , '_x?']:
        return Rule(pos='JX', optional=optional)
    elif wc in ['_o' , '_o?']:
        return Rule(pos='JKO', optional=optional)
    elif wc == '_i':
        raise Exception('wildcard _i is not allowed in pattern range')
    else:
        raise Exception(f'wildcard {wc} is not supported')

