
def show_date(context=None):
    import time
    tick = time.localtime()
    h, m = tick.tm_hour, tick.tm_min

    if h > 12:
        h -= 12
        am_pm = '오후'
    else:
        am_pm = '오전'
    return f'{am_pm} {h}시 {m}분'


def plus(a: str, b: str, context=None) -> str:
    try:
        a_num = int(a)
        b_num = int(b)
        return str(a_num + b_num)
    except:
        return '???'

def know(key: str, context= None) -> str:
    if key in context.memo:
        return 'true'
    else:
        return 'false'