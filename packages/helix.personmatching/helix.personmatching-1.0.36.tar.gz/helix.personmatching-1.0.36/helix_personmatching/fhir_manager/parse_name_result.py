from dataclasses import dataclass
from typing import Optional


@dataclass
class ParseNameResult:
    first: Optional[str]
    middle: Optional[str]
    last: Optional[str]
