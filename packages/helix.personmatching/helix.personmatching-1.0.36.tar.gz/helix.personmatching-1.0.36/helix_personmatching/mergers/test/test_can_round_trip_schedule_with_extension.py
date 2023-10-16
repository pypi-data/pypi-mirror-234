import json
from pathlib import Path
from typing import Any, Dict

from fhir.resources.R4B.schedule import Schedule

from helix_personmatching.utils.fhir_resource_helpers import FhirResourceHelpers


def test_can_round_trip_schedule_with_extension() -> None:
    print()
    data_dir: Path = Path(__file__).parent.joinpath("./fixtures")

    with open(data_dir.joinpath("schedule1.json")) as file:
        schedule1_text = file.read()

    schedule1_dict: Dict[str, Any] = json.loads(schedule1_text)

    schedule1: Schedule = Schedule.parse_obj(schedule1_dict)

    actual_schedule1_dict: Dict[str, Any] = json.loads(schedule1.json())
    FhirResourceHelpers.fix_last_updated_time_zone_in_resources([actual_schedule1_dict])

    assert actual_schedule1_dict == schedule1_dict
