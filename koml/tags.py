from pydantic import BaseModel
from typing import List, Any, Optional, Union
from .config import WILDCARDS

class Tag(BaseModel):
    child: Optional[List[Any]]
#--------------------#

class Text(Tag):
    val: str

class WildCard(Tag):
    val: str
    # allow value --

class PatStar(Tag):
    idx: Optional[int]
    set: Optional[str]
    pos: Optional[List[str]]
    npos: Optional[List[str]]
    # idx > 0

class Star(Tag):
    idx: Optional[int]
    set: Optional[str]
    get: Optional[str]
    # idx > 0

class Li(Tag):
    pass


class User(Tag):
    set: Optional[str]
    get: Optional[str]

class Bot(Tag):
    set: Optional[str]
    get: Optional[str]

# PatternT = List[Union[ PatStar, WildCard, Text]]
PatternT = List[Any]
# TemplateT = List[Union[User, Bot, WildCard, Text, Star, ]]
TemplateT = List[Any]

class PatLi(Li):
    child: PatternT 

class TemLi(Li):
    child: TemplateT 
#-----------------#

class Follow(Tag):
    cid: Optional[str]
    child: Optional[List[PatLi]]
    # cid and child not none

class Pattern(Tag):
    # child: List[Union[Text, WildCard, PatStar]]
    child: PatternT 
    # child: List[Any]
    # not empty list

class Subpat(Tag):
    child: List[PatLi]

class Template(Tag):
    child: List[TemLi]
    # not empty list

#-------------------#

class Case(Tag):
    id: Optional[str]
    follow: Optional[Follow]
    pattern: Pattern
    subpat: Optional[Subpat]
    template: Template

#--------------------#
RuleT = List[Union[dict[str, Any], str]]
class RuleCase(BaseModel):
    case: Case
    follow: Optional[List[RuleT]]
    pattern: RuleT
    subpat: Optional[List[RuleT]]
