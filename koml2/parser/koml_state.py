from enum import Enum

class KomlState(Enum):
    BEGIN = 0
    IN_CASE=1
    IN_FOLLOW=2
    IN_PATTERN=3
    IN_TEMPLATE=4