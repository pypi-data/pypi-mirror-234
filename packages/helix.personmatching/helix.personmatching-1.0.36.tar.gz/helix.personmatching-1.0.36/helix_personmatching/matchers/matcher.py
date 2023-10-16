import re
from os import environ
from typing import List, Optional, Union

# noinspection PyPackageRequirements
from fhir.resources.R4B.bundle import Bundle

# noinspection PyPackageRequirements
from fhir.resources.R4B.patient import Patient

# noinspection PyPackageRequirements
from fhir.resources.R4B.person import Person

# noinspection PyPackageRequirements
from fhir.resources.R4B.fhirtypes import Id

from helix_personmatching.fhir_manager.fhir_loader import FhirLoader
from helix_personmatching.fhir_manager.fhir_to_dict_manager.fhir_to_dict_manager import (
    FhirToAttributeDict,
)
from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.logics.rules_generator import RulesGenerator
from helix_personmatching.logics.score_calculator import ScoreCalculator
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.rule import Rule
from helix_personmatching.models.scoring_option import ScoringOption

# We multiply the average of all rule scores by this and add to the highest probability rule
AVERAGE_SCORE_BOOST = 0.01

# the standard probability for a rule is 0.95.  The high uniqueness rules are higher.
# the boost for average score is at max of 0.01
# So we want the threshold to be higher than 0.95 so if the average of the rules in 0.9 then it passes
# 0.095 + (0.9 * 0.001) = 0.0959
# or if the special boost of 0.5 is passed then a score of 0.90 + 0.05 will pass
MATCH_THRESHOLD = 0.955


regex = re.compile(
    r"^[A-Za-z0-9\-_.]+$"
)  # allow _ since some resources in our fhir server have that
# remove the 64-character limit on ids
Id.configure_constraints(min_length=1, max_length=1024 * 1024, regex=regex)


class Matcher:
    def __init__(
        self,
        threshold: Optional[float] = None,
        average_score_boost: Optional[float] = None,
    ) -> None:
        """


        the standard probability for a rule is 0.95.  The high uniqueness rules are higher.
        the boost for average score is at max of 0.01
        So we want the threshold to be higher than 0.95 so if the average of the rules in 0.9 then it passes
        0.095 + (0.9 * 0.001) = 0.0959
        or if the special boost of 0.5 is passed then a score of 0.90 + 0.05 will pass

        :param threshold: all matches below this threshold are rejected
        :param average_score_boost: We multiply the average of all rule scores by this and add to the
                                    highest probability rule
        """
        self.match_threshold: float = (
            threshold
            if threshold is not None
            else float(environ.get("PERSON_MATCH_THRESHOLD", MATCH_THRESHOLD))
        )
        self.average_score_boost: float = (
            average_score_boost
            if average_score_boost is not None
            else float(
                environ.get("PERSON_MATCH_AVERAGE_SCORE_BOOST", AVERAGE_SCORE_BOOST)
            )
        )

        assert (
            self.match_threshold < 1.0
        ), f"threshold {self.match_threshold} should be a value between 0 and 1 since it is a probability"

        assert (
            self.average_score_boost < 1.0
        ), f"average_score_boost {self.average_score_boost} should be a value between 0 and 1 since it is a probability"

    # noinspection PyMethodMayBeStatic
    def score_inputs(
        self,
        *,
        source: List[ScoringInput],
        target: List[ScoringInput],
        options: Optional[List[ScoringOption]] = None,
        only_matches: Optional[bool] = None,
        verbose: bool = False,
        only_use_passed_in_rules: Optional[bool] = None,
    ) -> List[MatchScore]:
        assert source
        assert target

        if verbose:
            print("Matcher:score_inputs()...")

        # If only_use_passed_in_rules is set to True,
        #  then configure rules to disable normal rules and
        #  enable the configured/specified rules in the given options parameter
        rules: List[Rule] = RulesGenerator.generate_rules(
            only_use_passed_in_rules=only_use_passed_in_rules,
            options=options,
        )

        result: List[MatchScore] = []

        source_resource: ScoringInput
        for source_resource in source:
            found_match: bool = False
            highest_scoring_match: Optional[MatchScore] = None
            result_for_current_source: List[MatchScore] = []

            target_resource: ScoringInput
            for target_resource in target:
                score = ScoreCalculator.calculate_total_score(
                    rules=rules,
                    source=source_resource,
                    target=target_resource,
                    average_score_boost=self.average_score_boost,
                    verbose=verbose,
                )
                matched_threshold = score.total_score >= self.match_threshold
                match_score = MatchScore(
                    id_source=score.id_source,
                    id_target=score.id_target,
                    rule_scores=score.rule_scores,
                    total_score=score.total_score,
                    threshold=self.match_threshold,
                    matched=matched_threshold,
                    average_boost=score.average_boost,
                    average_score=score.average_score,
                    total_score_unscaled=score.total_score_unscaled,
                    source=source_resource,
                    target=target_resource,
                    diagnostics=None,
                )
                if (
                    not highest_scoring_match
                    or highest_scoring_match.total_score < match_score.total_score
                ):
                    highest_scoring_match = match_score
                if matched_threshold:
                    found_match = True

                result_for_current_source.append(match_score)

            # now scale down the scores if highest score is over 1.0
            if (
                highest_scoring_match is not None
                and highest_scoring_match.total_score > 1.0
            ):
                highest_match_total_score = highest_scoring_match.total_score
                for score in result_for_current_source:
                    score.total_score = score.total_score / highest_match_total_score
                    score.matched = score.total_score >= self.match_threshold

            # add to list
            if only_matches is not None and only_matches is True:
                result_for_current_source = [
                    s for s in result_for_current_source if s.matched
                ]

            result = result + result_for_current_source

            # if no match found, add the highest scoring match for troubleshooting
            if (
                only_matches is not None
                and only_matches is False
                and not found_match
                and highest_scoring_match is not None
            ):
                result.append(highest_scoring_match)

        return result

    def match_scoring_inputs(
        self,
        *,
        source: List[ScoringInput],
        target: List[ScoringInput],
        verbose: bool = False,
        options: Optional[List[ScoringOption]] = None,
        only_matches: Optional[bool] = None,
        only_use_passed_in_rules: Optional[bool] = None,
    ) -> List[MatchScore]:
        assert source
        assert isinstance(source, list)
        assert target
        assert isinstance(target, list)

        if verbose:
            print("Matcher:match_scoring_inputs()...")

        match_results = self.score_inputs(
            source=source,
            target=target,
            options=options,
            only_matches=only_matches,
            verbose=verbose,
            only_use_passed_in_rules=only_use_passed_in_rules,
        )
        return match_results

    def match(
        self,
        *,
        source_json: Union[str, List[str]],
        target_json: Union[str, List[str]],
        verbose: bool = False,
        options: Optional[List[ScoringOption]] = None,
        only_matches: Optional[bool] = None,
        only_use_passed_in_rules: Optional[bool] = None,
    ) -> List[MatchScore]:
        assert source_json
        assert isinstance(source_json, str) or isinstance(source_json, list)
        assert target_json
        assert isinstance(target_json, str) or isinstance(target_json, list)

        if verbose:
            print("Matcher:match() - FhirLoader.get_scoring_inputs() for source")

        source: List[ScoringInput] = FhirLoader.get_scoring_inputs(
            resource_json=source_json,
            verbose=verbose,
        )

        if verbose:
            print("Matcher:match() - FhirLoader.get_scoring_inputs() for target")

        target: List[ScoringInput] = FhirLoader.get_scoring_inputs(
            resource_json=target_json,
            verbose=verbose,
        )

        if verbose:
            print(
                "Matcher:match() - Matcher.match_scoring_inputs() for running matching"
            )

        match_score: List[MatchScore] = self.match_scoring_inputs(
            source=source,
            target=target,
            verbose=verbose,
            options=options,
            only_matches=only_matches,
            only_use_passed_in_rules=only_use_passed_in_rules,
        )

        if verbose:
            print("Matcher:match() - DONE.")

        return match_score

    def match_resources(
        self,
        *,
        source: Union[Patient, Person, Bundle],
        target: Union[Patient, Person, Bundle],
        verbose: bool = False,
        options: Optional[List[ScoringOption]] = None,
        only_matches: Optional[bool] = None,
        only_use_passed_in_rules: Optional[bool] = None,
    ) -> List[MatchScore]:
        source_scoring_inputs: List[
            ScoringInput
        ] = FhirToAttributeDict.get_scoring_inputs_for_resource(resource=source)
        target_scoring_inputs: List[
            ScoringInput
        ] = FhirToAttributeDict.get_scoring_inputs_for_resource(resource=target)
        return self.match_scoring_inputs(
            source=source_scoring_inputs,
            target=target_scoring_inputs,
            verbose=verbose,
            options=options,
            only_matches=only_matches,
            only_use_passed_in_rules=only_use_passed_in_rules,
        )
