from pydantic import BaseModel
from typing import Optional, Union, List, Any

class Tag(BaseModel):
    child: Any 

class Text(Tag):
    val: str

class WildCard(Tag):
    val: str

class PatStar(Tag):
    key: Optional[str]
    pos: Optional[List[str]]
    npos: Optional[List[str]]

class Star(Tag):
    index: Optional[int]
    set: Optional[str]
    get: Optional[str]

class Bot(Tag):
    set: Optional[str]
    get: Optional[str]