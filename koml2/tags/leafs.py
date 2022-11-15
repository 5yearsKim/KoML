from .abstracts import Tag


class Text(Tag):
    def __init__(self, val: str) -> None:
        super().__init__()
        self.val: str = val

# class WildCard(Tag):
    