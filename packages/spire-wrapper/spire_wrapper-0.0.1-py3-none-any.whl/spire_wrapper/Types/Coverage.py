from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Types.Term import Term

from dataclasses import dataclass, field
from typing import Optional, Union, List


@dataclass
class Coverage:
    completed: bool
    term: Term
    start_time: str
    end_time: str
