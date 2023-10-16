import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher


def test_match_zip_code_formatting() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./person_data")

    with open(data_dir.joinpath("bwell_master_person.json")) as file:
        bwell_master_person_json = file.read()

    with open(data_dir.joinpath("person.json")) as file:
        walgreens_person_json = file.read()

    matcher = Matcher()

    scores: List[MatchScore] = matcher.match(
        source_json=walgreens_person_json,
        target_json=bwell_master_person_json,
        verbose=True,
        only_matches=True,
        options=[
            # ScoringOption(
            #     rule_name="Rule-050",
            #     # weight=RuleWeight(
            #     #     exact_match=1.0, partial_match=1.0, missing=0.5, boost=0.051
            #     # ),
            # ),
        ],
    )

    assert len(scores) == 1
    score = scores[0]
    scores_json = score.to_json()
    print(f"scores_json: {scores_json}")

    print(f"score.matched: {score.matched}")
    assert score.matched is True

    with open(data_dir.joinpath("expected_scores.json")) as file:
        expected_scores = json.loads(file.read())

    assert json.loads(scores_json) == expected_scores
