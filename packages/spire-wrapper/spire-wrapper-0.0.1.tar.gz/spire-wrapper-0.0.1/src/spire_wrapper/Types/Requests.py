from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass, field
from typing_extensions import TypedDict
from typing import Optional

from Types.Term import Term
from Types.Facility import Building, Room
from Types.Academic import Group
from Types.Academic import Subject
from Types.Course import Course, Offering, Section
from Types.Faculty import Instructor
from Types.Coverage import Coverage

@dataclass
class Error:
    detail: str

@dataclass
class Buildings:
    count: int
    next: str | None
    previous: str | None
    results: list[Building] = field(default_factory=list)

@dataclass
class Rooms:
    count: int
    next: str | None
    previous: str | None
    results: list[Room] = field(default_factory=list)

@dataclass
class Terms:
    count: int
    next: str | None
    previous: str | None
    results: list[Term] = field(default_factory=list)

@dataclass
class Groups:
    count: int
    next: str | None
    previous: str | None
    results: list[Group] = field(default_factory=list)

@dataclass
class Subjects:
    count: int
    next: str | None
    previous: str | None
    results: list[Subject] = field(default_factory=list)

@dataclass
class Courses:
    count: int
    next: str | None
    previous: str | None
    results: list[Course] = field(default_factory=list)

@dataclass
class Course_Instructor:
    offering: Offering
    instructors: list[Instructor] = field(default_factory=list)

@dataclass
class Course_Sections:
    count: int
    next: str | None
    previous: str | None
    results: list[Section] = field(default_factory=list)

@dataclass
class Offerings:
    count: int
    next: str | None
    previous: str | None
    results: list[Offering] = field(default_factory=list)

@dataclass
class Instructors:
    count: int
    next: str | None
    previous: str | None
    results: list[Instructor] = field(default_factory=list)

@dataclass
class Sections:
    count: int
    next: str | None
    previous: str | None
    results: list[Section] = field(default_factory=list)

@dataclass
class Coverages:
    count: int
    next: str | None
    previous: str | None
    results: list[Coverage] = field(default_factory=list)

class Options:
    PageSearch = TypedDict(
        "PageSearch",
        {
            "page": int,
            "search": str
        }
    )
    Page = TypedDict(
        "Page",
        {
            "page": int
        }
    )
    Search = TypedDict(
        "Search",
        {
            "search": str
        }
    )
