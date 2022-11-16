from .abstracts import Tag

class PatItem(Tag):
    def __init__(self, child: list[Tag]):
        super().__init__(attr={})
        self.child: list[Tag] = child
        self._check()
    
    def _check(self):
        pass

class TemItem(Tag):
    def __init__(self, child: list[Tag]):
        super().__init__(attr={})
        self.child: list[Tag] = child
        self._check()

    def _check(self):
        pass


    

