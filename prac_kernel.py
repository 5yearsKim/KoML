from koml.koml_parser import create_parser
from koml import Kernel, Context, CustomFunction
from customs import funcs

context = Context()
funcs = CustomFunction(funcs)

if __name__ == '__main__':
    from glob import glob
    kernel = Kernel(custom_func=funcs)
    files = glob('cases/*.xml', recursive=True)
    print(files)
    # kernel.remember('brain.pickle')
    kernel.learn(files)
    kernel.converse()