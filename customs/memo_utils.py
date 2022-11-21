from koml import Context
funcs = {}
def know(name: str, context: Context|None=None) -> str:
    if name in context.memo:
        return 'true'
    else:
        return 'false'
funcs['know'] = know
