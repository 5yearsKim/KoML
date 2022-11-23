import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from koml import KomlBot, CustomBag 
# from customs import funcs
from glob import glob

# custom_bag = CustomBag(funcs=funcs, preprocessor=preprocesor)
# custom_bag = CustomBag(funcs=funcs)
bot = KomlBot(custom_bag=None , debug=True)
files = glob('cases/*.xml', recursive=True)
bot.learn(files, save_path='brain_pkl/brain.pkl')
# bot.learn(['cases/default.xml'], save_path='brain_pkl/brain.pkl')
# bot.load('brain_pkl/brain.pkl')
bot.converse()