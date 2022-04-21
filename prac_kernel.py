from koml.koml_parser import create_parser
from koml import Kernel, Context

context = Context()


if __name__ == '__main__':
    from glob import glob
    kernel = Kernel()
    files = glob('koml.xml')
    # kernel.remember('brain.pickle')
    kernel.learn(files)
    kernel.converse()