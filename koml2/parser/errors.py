
class FileLoc:
    def __init__(self, line: int|None=None, col: int|None=None) -> None:
        self.line = line
        self.col = col

    def __str__(self) -> str:
        return f'FileLoc(line {self.line}, col {self.col})'

class KomlCheckError(Exception):
    def __init__(self, message: str, loc: FileLoc|None) -> None:
        if (loc):
            divider = '********************************************'
            loc_msg = f'line {loc.line}, col {loc.col} \n {message}'
            message = f'\n{divider}\n{loc_msg}\n{message}'
        super().__init__(message)

    



