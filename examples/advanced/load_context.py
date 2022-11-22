import sys
import os

sys.path.append('../../')
import json
from koml import Context

with open('context.json', 'r') as fr:
    ctx_json= json.load(fr)
    context = Context.from_json(ctx_json)

print(context)
# ==================================
# Context:
#     - history
#       Chat(뭐야 -> 뭐긴 뭐야)
#     - memo
#       {'user_name': '어니언', 'user_age': 26}
# ===================================

json_ctx = context.to_json()
print(json_ctx)
# {'history': [{'question': '뭐야', 'answer': '뭐긴 뭐야'}], 'memo': {'user_name': 'OnionKim', 'user_age': 26}}


from koml import KomlBot

bot = KomlBot()
bot.learn(['hello.xml'])

# context의 memo에서 key=user_name 조회
rsp = bot.respond('내 이름 뭐게', context)

print(rsp)
# 어니언이잖아ㅋㅋ 
print(context)
# ==================================
# Context:
#     - history
#       Chat(내 이름 뭐게 -> 어니언이잖아ㅋㅋ)
#       Chat(뭐야 -> 뭐긴 뭐야)
#     - memo
#       {'user_name': '어니언', 'user_age': 26}
# ===================================