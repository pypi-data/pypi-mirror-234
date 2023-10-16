import json
from pathlib import Path
from typing import Any, Dict, List, cast

from fhir.resources.R4B.domainresource import DomainResource
from fhir.resources.R4B.practitionerrole import PractitionerRole

from helix_personmatching.mergers.merge_config import (
    MergeConfig,
    DataSetConfig,
    MergeRule,
)
from helix_personmatching.mergers.practitioner_merger import PractitionerMerger


def test_practitioner_merge_resources_exclusive() -> None:
    print()
    data_dir: Path = Path(__file__).parent.joinpath("./fixtures")

    with open(data_dir.joinpath("practitioner_roles1.json")) as file:
        practitioner_roles1_text = file.read()

    practitioner_roles_list: List[Dict[str, Any]] = json.loads(practitioner_roles1_text)
    practitioner_roles: List[PractitionerRole] = [
        PractitionerRole.parse_obj(role_dict) for role_dict in practitioner_roles_list
    ]

    config: MergeConfig = MergeConfig(
        data_sets=[
            DataSetConfig(access_tag="medstar", merge_rule=MergeRule.Exclusive),
            DataSetConfig(access_tag="bwell", merge_rule=MergeRule.Exclusive),
        ]
    )

    result: List[DomainResource] = PractitionerMerger().merge_resources(
        resources=cast(List[DomainResource], practitioner_roles),
        config=config,
        resource_type="PractitionerRole",
    )
    assert len(result) == 2
    assert result == practitioner_roles[:2]
