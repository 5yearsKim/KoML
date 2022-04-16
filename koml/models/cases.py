from pydantic import BaseModel
from .tags import *
from typing import  List, Union

PatternT = List[Union[Text, WildCard, PatStar]]
TemplateT = List[Union[Text, Star, Bot]]

class Case(BaseModel):
    pattern: PatternT 
    subpat: List[PatternT]
    template: TemplateT

