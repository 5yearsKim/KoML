from pydantic import BaseModel, Extra
from typing import List, Any, Optional, Union

#----------base setup ---------#
class Tag(BaseModel):
    class Config:
        smart_union = True
        extra = Extra.forbid 

class Leaf(Tag):
    pass

class Node(Tag):
    child: Any

#----------leaf tag----------#

class Text(Leaf):
    val: str

class WildCard(Leaf):
    val: str
    optional: bool = True
    # allow value --

class PatStar(Leaf):
    idx: Optional[int]
    pos: Optional[List[str]]
    npos: Optional[List[str]]
    # idx > 0

class Star(Leaf):
    idx: Optional[int]
    # idx > 0

class Get(Leaf):
    name: str

#-------------tag with child----------------#
class Think(Node):
    pass

class Set(Node):
    name: str

class Arg(Node):
    pass

class Func(Node):
    name: str
    child: List[Arg]

PatternT = List[Union[WildCard, Text, PatStar]]
TemplateT = List[Union[WildCard, Text, Set, Get, Think, Star, Func]]

class PatLi(Node):
    child: PatternT 


class TemLi(Node):
    child: TemplateT 


class Pivot(Node):
    child: List[Union[Text, Star, Func]]



#--------- section tag --------#
class Follow(Node):
    cid: Optional[str]
    child: Optional[List[PatLi]]
    # cid and child not none

class Pattern(Node):
    child: PatternT 
    # not empty list

class Subpat(Node):
    child: List[PatLi]

class Random(Node):
    child: List[TemLi]

class Scase(Node):
    pivot:  str
    child: Union[TemLi, Random] 

class Default(Node):
    child: Union[TemLi, Random]

class Switch(Node):
    pivot: Pivot
    scase: List[Scase]
    default: Default

# child of template is not list type!
class Template(Node):
    child: Union[TemLi, Switch, Random]
    # temli should not be empty
#--------- case ----------#

class Case(BaseModel):
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
