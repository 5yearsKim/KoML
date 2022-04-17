from pydantic import BaseModel
from typing import List, Any

class Tag(BaseModel):
    child: List[Any] | None
#--------------------#

class Text(Tag):
    val: str

class WildCard(Tag):
    val: str

class PatStar(Tag):
    idx: int | None
    set: str | None
    pos: List[str] | None
    npos: List[str] | None

class Star(Tag):
    idx: int | None
    set: str | None
    get: str | None

class Li(Tag):
    tmp: str | None

class User(Tag):
    set: str | None
    get: str | None

class Bot(Tag):
    set: str | None
    get: str | None

class Random(Tag):
    pass

#-----------------#

class Pattern(Tag):
    child: List[Text | WildCard | PatStar]

class Subpat(Tag):
    child: List[Li] 

class Template(Tag):
    child: List[Any] | Random

#-------------------#

class Case(Tag):
    following: Any
    pattern: Pattern
    subpat: Subpat| None
    template: Template
    