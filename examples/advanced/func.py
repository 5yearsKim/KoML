from korean_word_relay import WordRelay
from koml import Context
import re

word_relay = WordRelay()
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

def state_word_relay(word: str, context: Context|None=None) -> str:
    ''' 내 답안이 문제가 없는 답변안인지 확인 '''
    # 한글이 아닌 글자 모두 제거
    word = hangul.sub('', word)

    # 답변은 최소 2글자 이상!
    if len(word) < 2:
        return 'short'

    holder = []
    for item in context.history[:5]:
        holder.append(item.answer.strip())
        holder.append(item.question.strip())
    history = holder

    # 앞선 문맥에 중복된 단어 발견
    if word in history:
        return 'duplicated'

    # 앞에 단어와 내 답변이 끝말잇기 되지 않음
    if not history:
        return 'no_match'
    prev_word = hangul.sub('', history[0])

    is_start = '시작해' in prev_word
    is_continue = word_relay.check_continue(prev_word, word)
    if not is_start and not is_continue:
        return 'no_match'

    next_word = word_relay.get_next(word, log_history=False)
    # koml 봇이 대답할 수 있는 단어 찾음/못찾음
    if next_word:
        return 'found'
    else:
        return 'no_found'

def get_word_relay(word :str, context: Context|None=None) -> str:
    ''' koml 봇 끝말잇기 단어 리턴 '''
    word = hangul.sub('', word)
    next_word = word_relay.get_next(word, log_history=True)
    return next_word

if __name__ == '__main__':

    import sys
    import os

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from koml import Context
    context = Context()
    context.push_history('기분', '분기!')
    result = state_word_relay('사랑', context=context)
    print(result)

    print(get_word_relay('사랑'))