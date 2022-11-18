from koml2.parser import create_parser
from koml2 import KomlBot, CustomFunction
from .customs import funcs
# from koml import Kernel, Context, CustomFunction
# from customs import funcs

# context = Context()
# funcs = CustomFunction(funcs)

if __name__ == '__main__':
    from glob import glob
    custom_function = CustomFunction(funcs=funcs)
    bot = KomlBot(custom_function=custom_function)
    files = glob('cases2/*.xml', recursive=True)
    # print(files)
    # kernel.remember('brain.pickle')
    bot.learn(files)
    # matched  =bot.respond('내 이름은 고기')
    # print(matched)
    bot.converse()