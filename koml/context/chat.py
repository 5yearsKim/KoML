from __future__ import annotations

class Chat:
    def __init__(self, question: str, answer: str, cid: str|None=None) -> None:
        self.question: str = question
        self.answer:str = answer
        self.cid: str|None = cid

    def __repr__(self) -> str:
        if self.cid:
            return f'Chat({self.question} -> {self.answer}, cid: {self.cid})'
        else:
            return f'Chat({self.question} -> {self.answer})'

    def to_json(self) -> dict[str, str]:
        obj = {'question': self.question, 'answer': self.answer}
        if self.cid:
            obj['cid'] = self.cid
        return obj

    @staticmethod
    def from_json(json: dict[str, str]) -> Chat:
        question = json.get('question')
        answer = json.get('answer')
        cid = json.get('cid')
        assert question is not None
        assert answer is not None
        chat = Chat(question, answer)
        if cid is not None:
            chat.cid = cid
        return chat

