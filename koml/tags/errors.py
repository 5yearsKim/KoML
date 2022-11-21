from .abstracts import Tag

class TagError(Exception):
    def __init__(self, message: str, tag: Tag|None=None):
        if tag:
            err_msg = f'\n**************\n{tag}\n{message}'
        else:
            err_msg = message
        super().__init__(err_msg)