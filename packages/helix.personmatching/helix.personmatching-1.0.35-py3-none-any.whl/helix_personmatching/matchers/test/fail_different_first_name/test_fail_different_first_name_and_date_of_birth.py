import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher
from helix_personmatching.models.rules.RuleWeight import RuleWeight
from helix_personmatching.models.scoring_option import ScoringOption


def test_fail_different_first_name_and_date_of_birth() -> None:
    print("")
    data_dir: Path = Path(__file__).parent.joinpath("./person_data")

    with open(data_dir.joinpath("bwell_master_person.json")) as file:
        bwell_master_person_json = file.read()

    with open(data_dir.joinpath("person.json")) as file:
        walgreens_person_json = file.read()

    matcher = Matcher()

    only_matches: bool = False

    scores: List[MatchScore] = matcher.match(
        source_json=walgreens_person_json,
        target_json=bwell_master_person_json,
        verbose=True,
        only_matches=only_matches,
        options=[
            ScoringOption(
                rule_name="Rule-050",
                weight=RuleWeight(
                    exact_match=0.0, partial_match=0.0, missing=0.0, boost=0.051
                ),
            ),
        ],
        # False by default, but here explicitly set to False for unit testing purposes
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
        print(f"scores_json: {scores_json}")

        with open(data_dir.joinpath("expected_scores.json")) as file:
            expected_scores = json.loads(file.read())

        assert json.loads(scores_json) == expected_scores
