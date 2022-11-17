from ..tags import Case
from .pattern_rule import PatternRule

class PatternMatcherError(Exception):
    def __init__(self, message: str, case: Case):
        err_msg = f'\n****************************\n{case}\n{message}' 
        super().__init__(err_msg)


class TemplateResolverError(Exception):
    def __init__(self, message: str, pattern_rule: PatternRule):
        err_msg = f'\n*************************\n{pattern_rule.template}\n{message}'
        super().__init__(err_msg)