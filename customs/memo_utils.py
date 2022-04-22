
funcs = {}
def know(name: str, *args, context=None):
    if name in context.memo:
        return 'true'
    else:
        return 'false'
funcs['know'] = know
