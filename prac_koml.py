from koml.koml_parser import create_parser
from koml import Kernel, Context

context = Context()

context.push_history('너 아이스크림 좋아해?','응ㅋㅋ좋아하')


if __name__ == '__main__':
    from glob import glob
    kernel = Kernel()
    files = glob('koml.xml')
    # kernel.converse()
    # kernel.remember('brain.pickle')
    kernel.learn(files)
    # kernel.respond('너는 고기가 좋아 치킨이 좋아', context)
    # kernel.respond('넌 똥 좋아해?', context)
    # kernel.respond('너는 고기랑 치킨중에 뭐가 더 좋아?', context)
    kernel.respond('왜?', context)