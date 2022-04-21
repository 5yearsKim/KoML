from koml.koml_parser import create_parser
from koml import Kernel, Context
from customs import funcs

context = Context()


if __name__ == '__main__':
    from glob import glob
    kernel = Kernel(custom_func=funcs)
    files = glob('koml.xml')
    # kernel.remember('brain.pickle')
    kernel.learn(files)
    kernel.converse()