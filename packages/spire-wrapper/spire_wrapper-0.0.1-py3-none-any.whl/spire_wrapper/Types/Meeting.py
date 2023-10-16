from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass, field
from typing import Literal

from Types.Faculty import Instructor
from Types.Facility import Room


@dataclass
class Schedule:
    days: list[Literal[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]]
    start_time: str
    end_time: str

@dataclass
class Information:
    schedule: Schedule | None
    instructors: list[Instructor]
    room: Room
    room_raw: str
