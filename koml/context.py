from typing import Dict, List
from pydantic import BaseModel
import json

class Chat(BaseModel):
    question: str
    answer: str

class Memory(BaseModel):
    history: List[Chat]
    user: Dict[str, str]
    bot: Dict[str, str]
    star: Dict[str, str]


class Context:
    def __init__(self):
        self._memory:Memory = Memory(history=[], user={}, bot={}, star={})

    @property
    def memory(self):
        return self._memory

    @property
    def history(self):
        return self._memory.history

    @property
    def user(self):
        return self._memory.user
    
    @property
    def bot(self):
        return self._memory.bot
    
    @property
    def star(self):
        return self._memory.star


    def load(self, memory: Memory):
        self._memory = memory

    def load_from_json(self, path):
        with open(path) as f:
            data = json.load(f)
        self._memory = Memory(**data)
    
    def export(self):
        js = self._memory.dict()
        print(js)

    def push_history(self, question:str, answer:str):
        chat = Chat(question=question, answer=answer)
        self._memory.history.insert(0, chat)


if __name__ == '__main__':
    ctx = Context()
    ctx.load_from_json('context.json')
    print(ctx.user)

    