# 컨텍스트 

context 는 KomlBot 이 대화에 필요한 문맥과 기억을 모두 저장하는 객체에요. KomlBot은 사용자와 context 를 주고받으며 대화를 기록해요.

## 구성 요소
```python
class Context:
    def __init__(self) -> None:
        self.history: list[Chat] = []
        self.memo: dict[str, str] = {}
```

### memo

\<get>/\<set>을 할 때 사용되는 dict 에요. 해당되는 키-값을 조회해서 \<get>/\<set>을 실행해요.


다음은 커스텀 함수에서 memo 를 조회하는 예시에요.
```python
def know(name: str, context: Context|None=None) -> str:
    if name in context.memo:
        return 'true'
    else:
        return 'false'
```

<br>

### history

대화 기록을 저장해놓는 list 에요. list 의 아이템인 Chat 의 구성 요소는 다음과 같아요.
```python
class Chat:
    def __init__(self, question: str, answer: str, cid: str|None=None) -> None:
        self.question: str = question
        self.answer:str = answer
        self.cid: str|None = cid
```
<br>

## Json 직렬화

context 는 json 직렬화를 지원해요. json 데이터로 쉽게 주고받을 수 있어요.


```json
// context.json
{
  "history": [{"question": "뭐야", "answer": "뭐긴 뭐야"}],
  "memo": {
    "user_name": "어니언",
    "user_age": 26 
  }
}
```

```python
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
# {'history': [{'question': '뭐야', 'answer': '뭐긴 뭐야'}], 'memo': {'user_name': '어니언', 'user_age': 26}}
```


## context 를 이용한 대화처리 
`bot.converse()` 를 통해서 뿐만 아니라 context 만 가지고 있다면 어떤 KomlBot 으로부터 `bot.respond()`를 통해 답변을 받을 수 있어요.

```python
import json
from koml import KomlBot, Context

with open('context.json', 'r') as fr:
    ctx_json= json.load(fr)
    context = Context.from_json(ctx_json)

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
```



