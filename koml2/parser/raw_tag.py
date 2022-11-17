class RawTag:
    def __init__(self, tag: str, attr: dict[str, str]={}):
        self.tag: str = tag
        self.attr: dict[str, str] = attr

    def __repr__(self) -> str:
        return f'RawTag({self.tag})'

