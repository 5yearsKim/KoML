from koml2.parser import create_parser
from koml2 import KomlBot
# from koml import Kernel, Context, CustomFunction
# from customs import funcs

# context = Context()
# funcs = CustomFunction(funcs)

if __name__ == '__main__':
    from glob import glob
    kernel = KomlBot()
    files = glob('cases/*.xml', recursive=True)
    # print(files)
    # kernel.remember('brain.pickle')
    kernel.learn(files)
    # kernel.converse()