from koml import CustomFunction 
            
funcs = {}

def test(a: str, b:str, *args, context =3):
    print(a,b)

funcs['test'] = test

def test2(a: str, b: str, *args, context=None):
    pass
funcs['test2'] = test2

cf = CustomFunction(funcs)