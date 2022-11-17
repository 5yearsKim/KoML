from ..tags import Case

class PatternMatcherError(Exception):
    def __init__(self, message: str, case: Case):
        err_msg = f'****************************\n{case}\n{message}' 
        super().__init__(err_msg)
