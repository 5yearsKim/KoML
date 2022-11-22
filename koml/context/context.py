from __future__ import annotations
from typing import Any
import textwrap
from .chat import Chat

class Context:
    def __init__(self) -> None:
        self.history: list[Chat] = []
        self.memo: dict[str, str] = {}

    def __repr__(self) -> str:
        history_str = f'\n'.join(map(lambda x: str(x), self.history))
        return f'''==================================
Context:
    - history
{textwrap.indent(history_str, "      ")}
    - memo
{textwrap.indent(str(self.memo), "      ")}
==================================='''

    @property
    def prev_chat(self) -> Chat|None:
        if self.history:
            return self.history[0]
        else:
            return None

    def push_history(self, question: str, answer: str, cid: str|None) -> None:
        chat = Chat(question, answer, cid=cid)
        self.history.insert(0, chat)

    def get_memo(self, key:str) -> str|None:
        if key in self.memo:
            return self.memo.get(key)
        else:
            return None

    def set_memo(self, key:str, val:str) -> None:
        self.memo[key] = val

    def to_json(self) -> dict[str, Any] :
        history_list = list(map(lambda x: x.to_json(), self.history))
        obj = {'history': history_list, 'memo': self.memo}
        return obj

    @staticmethod
    def from_json(json: dict[str, Any]) -> Context:
        context = Context()
        memo = json.get('memo')
        assert isinstance(memo, dict)
        history = json.get('history')
        assert isinstance(history, list)
        history_list = list(map(lambda x: Chat.from_json(x), history))
        context.memo = memo
        context.history = history_list
        return context





    