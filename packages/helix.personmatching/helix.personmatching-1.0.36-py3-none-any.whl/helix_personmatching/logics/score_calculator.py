from typing import List, Optional, Set, Dict

# noinspection PyPackageRequirements
from nicknames import NickNamer

from helix_personmatching.logics.match_score_without_threshold import (
    MatchScoreWithoutThreshold,
)
from helix_personmatching.logics.rule_score import RuleScore
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.rule import Rule
from helix_personmatching.models.rule_option import RuleOption
from helix_personmatching.nick_name_loader import NickNameLoader


class ScoreCalculator:
    nick_namer: Optional[NickNamer] = None

    @staticmethod
    def initialize_score(rules: List[Rule]) -> None:
        pass

    @staticmethod
    def calculate_total_score(
        rules: List[Rule],
        source: ScoringInput,
        target: ScoringInput,
        average_score_boost: Optional[float],
        verbose: bool = False,
    ) -> MatchScoreWithoutThreshold:
        """
        Runs matching on two records: source and target


        :param rules:
        :param source:
        :param target:
        :param average_score_boost:
        :param verbose: set to True to enable logging
        :return: match score
        """

        if verbose:
            print("ScoreCalculator:calculate_total_score()...")

        match_results: List[RuleScore] = ScoreCalculator.calculate_score(
            rules=rules, source=source, target=target
        )
        if len(match_results) == 0:
            return MatchScoreWithoutThreshold(
                id_source=source.id_,
                id_target=target.id_,
                rule_scores=match_results,
                total_score=0.0,
                total_score_unscaled=0.0,
                average_boost=None,
                average_score=0.0,
                source=source,
                target=target,
                diagnostics=None,
            )

        # Get the average match score as "final score" result

        final_score: float = 0

        sum_of_scores: float = 0
        rule_count: int = 0

        for match_result in match_results:
            # the score is uniqueness probability
            # pick the highest probability
            if match_result.rule_score > final_score:
                final_score = match_result.rule_score
            sum_of_scores += match_result.rule_score
            rule_count += 1
            if match_result.rule_boost is not None:
                final_score += match_result.rule_boost

        score_average_boost: Optional[float] = None
        score_average: float = 0
        # add a boost for average score
        if average_score_boost is not None:
            score_average = sum_of_scores / rule_count
            score_average_boost = score_average * average_score_boost
            final_score += score_average_boost

        return MatchScoreWithoutThreshold(
            id_source=source.id_,
            id_target=target.id_,
            rule_scores=match_results,
            total_score=final_score,
            total_score_unscaled=final_score,
            average_boost=score_average_boost,
            average_score=score_average,
            source=source,
            target=target,
            diagnostics=None,
        )

    @staticmethod
    def get_number_of_rules_with_present_attributes(results: List[RuleScore]) -> int:
        number_of_rules_with_present_attributes: int = sum(
            map(
                lambda result: any(
                    list(
                        filter(
                            lambda rule_attribute_score: getattr(
                                rule_attribute_score, "present"
                            )
                            is True,
                            result.attribute_scores,
                        )
                    )
                )
                is True,
                results,
            )
        )
        number_of_rules_with_present_attributes = (
            1
            if number_of_rules_with_present_attributes == 0
            else number_of_rules_with_present_attributes
        )

        return number_of_rules_with_present_attributes

    @staticmethod
    def calculate_score(
        rules: List[Rule],
        source: ScoringInput,
        target: ScoringInput,
        verbose: bool = False,
    ) -> List[RuleScore]:
        """
        Calculate matching scores for ALL rules between FHIR Person-Person, or Person-Patient, or Person/Patient-AppUser

        :param rules: generated rules by RulesGenerator
        :param source: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param target: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param verbose: set to True to enable logging
        :return: list of dictionary for rules score results for all rules
        """

        if verbose:
            print("ScoreCalculator.calculate_score()...")

        rules_score_results: List[RuleScore] = []

        if ScoreCalculator.nick_namer is None:
            if verbose:
                print(
                    "ScoreCalculator.calculate_score() - NickNameLoader.load_nick_names()..."
                )

            nickname_lookup: Dict[str, Set[str]] = NickNameLoader.load_nick_names()
            ScoreCalculator.nick_namer = NickNamer(nickname_lookup=nickname_lookup)

        for rule in rules:
            rule_score_result: Optional[
                RuleScore
            ] = ScoreCalculator.calculate_score_for_rule(
                rule=rule,
                source=source,
                target=target,
                rule_option=RuleOption(nick_namer=ScoreCalculator.nick_namer),
                verbose=verbose,
            )
            if rule_score_result:
                rules_score_results.append(rule_score_result)

        return rules_score_results

    @staticmethod
    def calculate_score_for_rule(
        *,
        rule: Rule,
        source: ScoringInput,
        target: ScoringInput,
        rule_option: RuleOption,
        verbose: bool = False,
    ) -> Optional[RuleScore]:
        if verbose:
            print("ScoreCalculator.calculate_score_for_rule()...")

        return (
            rule.score(
                source=source, target=target, rule_option=rule_option, verbose=verbose
            )
            if rule.enabled is True
            else None
        )
