import sys
import os

sys.path.append('../../')

# main.py
from koml import KomlBot, RemovePosPreprocessor, CustomBag
from func import get_word_relay, state_word_relay

# 부사 제거 전처리
# preprocessor = RemovePosPreprocessor(npos=['MAG'])
# bag = CustomBag(preprocessor=preprocessor)

bag = CustomBag(funcs={'get_word_relay': get_word_relay, 'state_word_relay': state_word_relay})

bot = KomlBot(bag)
bot.learn(['preprocessor.xml', 'word_relay.xml'])
bot.converse()