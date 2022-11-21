from korean_word_relay import WordRelay
from koml import Context
import re

funcs = {}

word_relay = WordRelay(words_path='customs/killing_words.txt', debug_print=False)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

def state_word_relay(word: str, context: Context|None=None) -> str:
    word = hangul.sub('', word)

    if len(word) < 2:
        return 'short'

    holder = []
    for item in context.history[:5]:
        holder.append(item.answer.strip())
        holder.append(item.question.strip())
    history = holder
    # print('*'*50)
    # print(word, history)
    # print(word in history)
    if word in history:
        return 'duplicated'

    if not history:
        return 'no_match'
    prev_word = hangul.sub('', history[0])

    is_start = '시작해' in prev_word
    is_continue = word_relay.check_continue(prev_word, word)
    if not is_start and not is_continue:
        return 'no_match'
    
    next_word = word_relay.get_next(word, log_history=False)
    if next_word:
        return 'found'
    return 'no_found'
funcs['state_word_relay'] = state_word_relay

def get_word_relay(word :str, context: Context|None=None) -> str:
    word = hangul.sub('', word)
    next_word = word_relay.get_next(word, log_history=True)
    if not next_word:
        return '멍청이ㅋㅋㅋ'
    return next_word
funcs['get_word_relay'] = get_word_relay

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