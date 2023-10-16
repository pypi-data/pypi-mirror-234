from dataclasses import dataclass, field
from typing import Optional, Union, List


@dataclass
class Event:
    date: str
    description: str

@dataclass
class Term:
    url: str
    id: str
    season: str
    year: int
    ordinal: int
    start_date: Optional[str]
    end_date: Optional[str]
    events: list[Event] = field(default_factory=list)
