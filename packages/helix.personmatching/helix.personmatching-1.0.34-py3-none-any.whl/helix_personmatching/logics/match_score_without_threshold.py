import json
from dataclasses import dataclass
from typing import List, Optional

from helix_personmatching.logics.rule_score import RuleScore
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.utils.json_serializer import EnhancedJSONEncoder


@dataclass
class MatchScoreWithoutThreshold:
    id_source: Optional[str]
    id_target: Optional[str]
    source: ScoringInput
    target: ScoringInput
    rule_scores: List[RuleScore]
    total_score: float
    total_score_unscaled: float
    average_score: float
    average_boost: Optional[float]

    def to_json(self) -> str:
        return json.dumps(self, cls=EnhancedJSONEncoder)
