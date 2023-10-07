import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher


def test_walgreens_partial_match() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./person_data")

    with open(data_dir.joinpath("bwell_master_person.json")) as file:
        bwell_master_person_json = file.read()

    with open(data_dir.joinpath("walgreens_person.json")) as file:
        walgreens_person_json = file.read()

    matcher = Matcher()

    scores: List[MatchScore] = matcher.match(
        source_json=walgreens_person_json,
        target_json=bwell_master_person_json,
        only_matches=True,
        verbose=True,
    )

    assert len(scores) == 1
    score = scores[0]

    print(f"score.matched: {score.matched}")
    assert score.matched is True

    print(f"score.total_score: {score.total_score}")
    assert score.total_score > 0.995

    scores_json = score.to_json()
    print(scores_json)

    with open(data_dir.joinpath("expected_scores.json")) as file:
        expected_scores = json.loads(file.read())

    assert json.loads(scores_json) == expected_scores
