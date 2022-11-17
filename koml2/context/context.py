from .chat import Chat
from .memory import Memory

class Context:
    def __init__(self) -> None:
        self.history: list[Chat] = []
        self.memo: Memory = Memory()

    def push_history(self, question: str, answer: str, cid: str|None) -> None:
        chat = Chat(question, answer, cid=cid)
        self.history.insert(0, chat)

    