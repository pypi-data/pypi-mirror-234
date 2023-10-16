from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Types.Academic import Group
from Types.Term import Term
from Types.Meeting import Information

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import Optional, Literal
from dacite import from_dict


@dataclass
class Class:
	id: str
	url: str
	title: str

@dataclass
class Subject:
	id: str
	url: str
	title: str
	groups: Optional[list[Group]]
	courses: Optional[list[Class]]

@dataclass
class Unit:
	base: int | float
	min: int | None
	max: int | None

@dataclass
class Detail:
	units: Unit | None
	career: str
	grading_basis: Optional[str]
	course_components: Optional[list[str]]
	academic_group: Optional[str]
	academic_organization: Optional[str]
	campus: Optional[str]
	status: Optional[str]
	class_number: Optional[int]
	session: Optional[str]
	topic: str | None
	rap_tap_hlc: str | None
	gened: dict | None
	class_components: None | list[str]

@dataclass
class Enrollment:
	add_consent: str | None
	enrollment_requirement: str | None
	course_attribute: list[str] | None

@dataclass
class Offering:
	id: int
	url: str
	term: Term

@dataclass
class Course:
	id: str
	url: str
	subject: Subject
	number: str
	title: str
	description: str | None
	details: Detail | None
	enrollment_information: Enrollment | None
	offerings: list[Offering]
	_updated_at: str

@dataclass
class Offering_Section:
	id: int
	url: str
	spire_id: str

@dataclass
class Offering:
	id: Optional[int]
	url: str
	subject: Optional[Subject]
	course: Optional[Class]
	alternative_title: Optional[str]
	term: Term
	section: Optional[list[Offering_Section]]

@dataclass
class Availability:
	capacity: int
	enrollment_total: int
	available_seats: int
	wait_list_capacity: int
	wait_list_total: int
	nso_enrollment_capacity: int | None

@dataclass
class Restrictions:
	drop_consent: str | None
	enrollment_requirements: str
	add_consent: str | None

@dataclass
class Section:
	url: str
	spire_id: str
	offering: Offering
	description: str
	overview: str | None
	details: Detail
	availability: Availability
	restrictions: Restrictions
	meeting_information: list[Information]
	_updated_at: str
