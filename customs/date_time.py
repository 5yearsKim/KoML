
funcs = {}

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

funcs['show_date'] = show_date