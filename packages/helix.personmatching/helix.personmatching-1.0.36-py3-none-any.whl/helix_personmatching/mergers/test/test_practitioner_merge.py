import json
from pathlib import Path
from typing import Any, Dict

from helix_personmatching.mergers.merge_config import (
    MergeConfig,
    DataSetConfig,
    MergeRule,
)
from helix_personmatching.mergers.practitioner_merger import PractitionerMerger
from helix_personmatching.utils.fhir_resource_helpers import FhirResourceHelpers


def test_practitioner_merge() -> None:
    print()
    data_dir: Path = Path(__file__).parent.joinpath("./fixtures")

    with open(data_dir.joinpath("practitioner1.json")) as file:
        practitioner1_text = file.read()

    practitioner1: Dict[str, Any] = json.loads(practitioner1_text)

    config: MergeConfig = MergeConfig(
        data_sets=[
            DataSetConfig(access_tag="medstar", merge_rule=MergeRule.Exclusive),
            DataSetConfig(access_tag="bwell", merge_rule=MergeRule.Exclusive),
        ]
    )

    result: Dict[str, Any] = PractitionerMerger().merge(
        row=practitioner1, config=config
    )
    FhirResourceHelpers.fix_last_updated_time_zone_in_resources(result["practitioner"])
    # remove the identifiers that don't match the data set
    expected_practitioner = practitioner1["practitioner"][0]
    expected_practitioner["identifier"] = expected_practitioner["identifier"][:2]
    assert result["practitioner"][0] == expected_practitioner

    result_practitioner_roles = result["practitionerrole"]
    FhirResourceHelpers.fix_last_updated_time_zone_in_resources(
        resources=result_practitioner_roles
    )
    assert len(result_practitioner_roles) == 2
    assert result_practitioner_roles == practitioner1["practitionerrole"][:2]
