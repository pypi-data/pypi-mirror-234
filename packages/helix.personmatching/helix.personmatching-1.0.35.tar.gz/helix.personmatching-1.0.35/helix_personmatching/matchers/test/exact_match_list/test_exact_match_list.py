import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher


def test_exact_match_list() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./")

    with open(data_dir.joinpath("patient1.json")) as file:
        resource1_json = file.read()

    with open(data_dir.joinpath("patient2.json")) as file:
        resource2_json = file.read()

    matcher = Matcher()

    scores: List[MatchScore] = matcher.match(
        source_json=[resource1_json],
        target_json=[resource2_json],
        only_matches=True,
        verbose=True,
    )

    assert len(scores) == 1
    score = scores[0]
    assert score.matched is True

    assert score.total_score > 0.995

    scores_json = score.to_json()
    print(scores_json)

    with open(data_dir.joinpath("expected_scores.json")) as file:
        expected_scores = json.loads(file.read())

    assert json.loads(scores_json) == expected_scores
