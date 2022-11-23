import sys
import os

sys.path.append('../../')

# main.py
from koml import KomlBot

bot = KomlBot()
bot.learn(['getting_started.xml'])
bot.converse()