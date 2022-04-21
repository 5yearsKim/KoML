from koml import CustomFunction 
            
funcs = {}

def test(a: str, b:str, *args, context =None):
    print(a,b)

funcs['test'] = test

def test2(a: str, b: str, *args, context=None):
    pass
funcs['test2'] = test2

def show_date(*args, context=None):
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

funcs = CustomFunction(funcs)

if __name__ == '__main__':
    print(show_date())