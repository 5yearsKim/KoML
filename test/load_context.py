import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
from koml import KomlBot, CustomBag, Context
from customs import funcs
from glob import glob

with open('context.json', 'r') as fr:
    ctx_json= json.load(fr)
    ctx_json['history'].append({'question': '안녕', 'answer': '안녕'})
    context = Context.from_json(ctx_json)


custom_bag = CustomBag(funcs=funcs)
bot = KomlBot(custom_bag=custom_bag, debug=True)
files = glob('cases/*.xml', recursive=True)
bot.learn(files, save_path='brain_pkl/brain.pkl')
# # bot.learn(['cases/default.xml'], save_path='brain_pkl/brain.pkl')
# # bot.load('brain_pkl/brain.pkl')
# bot.converse()

rsp = bot.respond('내 이름은 현우', context)
print(context)
print(rsp)