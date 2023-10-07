import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher


def test_fail_person_person_list() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./")

    with open(data_dir.joinpath("master_person.json")) as file:
        master_person_json = file.read()

    with open(data_dir.joinpath("client_person.json")) as file:
        client_person_json = file.read()

    matcher = Matcher()

    only_matches: bool = True

    scores: List[MatchScore] = matcher.match(
        source_json=[master_person_json],
        target_json=[client_person_json],
        only_matches=only_matches,
        verbose=True,
    )

    print(f"len(scores): {len(scores)}")

    if only_matches:
        assert len(scores) == 0
        print("No matching results returned when no match found!")
    else:
        assert len(scores) == 2
        score = scores[0]

        assert score.matched is False
        print(f"score.matched: {score.matched}")

        assert score.total_score < 0.995

        scores_json = score.to_json()
        print(f"\nscores_json: {scores_json}\n")

        with open(data_dir.joinpath("expected_scores.json")) as file:
            expected_scores = json.loads(file.read())

        assert json.loads(scores_json) == expected_scores
