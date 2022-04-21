from pydantic import BaseModel, Extra
from typing import List, Any, Optional, Union
from .config import WILDCARDS

class Tag(BaseModel):
    child: Optional[List[Any]]
    class Config:
        smart_union = True
        extra = Extra.forbid 
#----------single tag----------#

class Text(Tag):
    val: str

class WildCard(Tag):
    val: str
    optional: bool = True
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

#-------------tag with child----------------#
class Li(Tag):
    pass


class User(Tag):
    set: Optional[str]
    get: Optional[str]
    # child with get not allowed

class Bot(Tag):
    set: Optional[str]
    get: Optional[str]
    # child with get not allowed

PatternT = List[Union[WildCard, Text, PatStar]]
TemplateT = List[Union[WildCard, Text, User, Bot, Star]]

class PatLi(Li):
    child: PatternT 


class TemLi(Li):
    child: TemplateT 

class Arg(Tag):
    pass

class Func(Tag):
    name: str
    child: List[Arg]

class Pivot(Tag):
    child: List[Union[Text, Star]]

class Scase(Tag):
    pivot:  str
    child: TemplateT

class Default(Tag):
    child: TemplateT


#---------section tag --------#

class Follow(Tag):
    cid: Optional[str]
    child: Optional[List[PatLi]]
    # cid and child not none

class Pattern(Tag):
    child: PatternT 
    # not empty list

class Subpat(Tag):
    child: List[PatLi]

class Switch(Tag):
    pivot: Pivot
    scase: List[Scase]
    default: Default

class Template(Tag):
    child: Union[List[TemLi], Switch]
    # temli should not be empty
#--------- case ----------#

class Case(Tag):
    id: Optional[str]
    follow: Optional[Follow]
    pattern: Pattern
    subpat: Optional[Subpat]
    template: Template

#---------- rule case ----------#
RuleT = List[Union[dict[str, Any], str]]
class RuleCase(BaseModel):
    case: Case
    follow: List[RuleT]
    pattern: RuleT
    subpat: List[RuleT]
    pattern_priority: Optional[int]
    subpat_priority: Optional[List[int]]
