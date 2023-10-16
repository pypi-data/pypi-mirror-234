from dataclasses import dataclass, field
from typing import Optional, Union, List

@dataclass
class Instructor:
	url: str
	name: str
	email: Optional[str]