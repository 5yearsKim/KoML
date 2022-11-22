import sys
import os

sys.path.append('../../')

# main.py
from koml import KomlBot, FilterPreprocessor, CustomBag
from func import get_word_relay, state_word_relay

# 특정 부사 제거 전처리
preprocessor = FilterPreprocessor(filter_words=['진짜', '아주', '정말'])
bag = CustomBag(preprocessor=preprocessor)

# bag = CustomBag(funcs={'get_word_relay': get_word_relay, 'state_word_relay': state_word_relay})

bot = KomlBot(bag, debug=False)
bot.learn(['preprocessor.xml', 'word_relay.xml'])
bot.converse()