from .chat import Chat

class Context:
    def __init__(self) -> None:
        self.history: list[Chat] = []
        self.memo: dict[str, str] = {}

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


    