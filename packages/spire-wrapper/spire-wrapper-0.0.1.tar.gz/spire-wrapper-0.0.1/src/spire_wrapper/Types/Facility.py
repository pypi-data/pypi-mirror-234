# Allow for future references
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union, List

@dataclass
class Room:
    url: str
    id: int
    number: Optional[str]
    alt: str
    building: Optional[Building]

@dataclass
class Building:
    id: int
    name: str
    address: str | None
    url: Optional[str]
    rooms: Optional[list[Room]]