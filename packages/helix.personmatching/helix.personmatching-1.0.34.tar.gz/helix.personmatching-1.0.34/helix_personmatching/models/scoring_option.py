from dataclasses import dataclass
from typing import Optional

from helix_personmatching.models.rules.RuleWeight import RuleWeight


@dataclass
class ScoringOption:
    rule_name: str
    weight: Optional[RuleWeight] = None
