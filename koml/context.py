from typing import Dict, List
from pydantic import BaseModel
import json

class Chat(BaseModel):
    question: str
    answer: str

class Memory(BaseModel):
    history: List[Chat]
    memo: Dict[str, str]


class Context:
    def __init__(self):
        self._memory:Memory = Memory(history=[], memo={})

    @property
    def memory(self):
        return self._memory

    @property
    def history(self):
        return self._memory.history

    @property
    def memo(self):
        return self._memory.memo
    
    def load(self, memory: Memory):
        self._memory = memory

    def load_from_json(self, path):
        with open(path) as f:
            data = json.load(f)
        self._memory = Memory(**data)
    
    def export(self):
        js = self._memory.dict()
        print(js)
        # todo: need to implement

    def push_history(self, question:str, answer:str):
        chat = Chat(question=question, answer=answer)
        self._memory.history.insert(0, chat)

    def set_memo(self, name :str, val :str):
        self._memory.memo[name] = val
    
    def get_memo(self, name :str):
        try:
            return self._memory.memo[name]
        except:
            return 'undefined'

if __name__ == '__main__':
    ctx = Context()
    ctx.load_from_json('context.json')
    print(ctx.user)

    