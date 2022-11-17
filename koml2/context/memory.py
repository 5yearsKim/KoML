

class Memory:
    def __init__(self) -> None:
        self.memo: dict[str, str] = {}

    def __getitem__(self, key:str) -> str|None :
        return self.get(key)
    
    def __setitem__(self, key: str, val: str) -> None:
        self.set(key, val)

    def get(self, key: str) -> str | None:
        if key in self.memo:
            return self.memo[key]
        else:
            return None
        
    def set(self, key: str, val: str) -> None:
        self.memo[key] = val
