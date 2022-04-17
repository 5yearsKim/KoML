from koml.koml_parser import create_parser
from koml.kernel import Kernel

if __name__ == '__main__':
    # parser = create_parser()
    # parser.parse("koml.xml")
    # handler = parser.getContentHandler()

    # cases = handler.cases
    # for case in cases:
    #     print(case)
    #     print('------------')
    from glob import glob
    kernel = Kernel()
    files = glob('koml.xml')
    kernel.learn(files)
