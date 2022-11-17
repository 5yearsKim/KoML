

class Chat:
    def __init__(self, question: str, answer: str, cid: str|None) -> None:
        self.question: str = question
        self.answer:str = answer
        self.cid: str|None = cid

    def __repr__(self) -> str:
        if self.cid:
            return f'Chat({self.question} -> {self.answer}, cid: {self.cid})'
        else:
            return f'Chat({self.question} -> {self.answer})'