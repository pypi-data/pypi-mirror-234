from dataclasses import dataclass, field
from typing import Optional, Union, List


@dataclass
class Subject:
    id: str
    url: str
    title: str

@dataclass
class Group:
    url: str
    id: int
    title: str
    subjects: Optional[list[Subject]]