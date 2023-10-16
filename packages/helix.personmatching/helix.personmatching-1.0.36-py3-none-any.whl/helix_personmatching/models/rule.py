from typing import Optional

from helix_personmatching.logics.rule_score import RuleScore
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.rule_option import RuleOption
from helix_personmatching.models.rules.RuleWeight import RuleWeight


class Rule:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        number: int,
        weight: RuleWeight,
        enabled: Optional[bool]
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.number: int = number
        self.weight: RuleWeight = weight
        self.enabled: Optional[bool] = enabled

    def score(
        self,
        source: ScoringInput,
        target: ScoringInput,
        rule_option: RuleOption,
        verbose: bool = False,
    ) -> Optional[RuleScore]:
        raise NotImplementedError()
