import json
from pathlib import Path

import pytest
from fhir.resources.R4B.patient import Patient

from helix_personmatching.fhir_manager.fhir_to_dict_manager.fhir_to_dict_manager import (
    FhirToAttributeDict,
)
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.utils.json_serializer import EnhancedJSONEncoder


@pytest.mark.parametrize("patient", ["patient1", "patient2"])
def test_fhir_to_dict_manager(patient: str) -> None:
    # Arrange
    data_dir: Path = Path(__file__).parent.joinpath("./")

    test_file_dir = data_dir.joinpath(patient)
    with open(test_file_dir.joinpath("patient.json")) as file:
        contents = file.read()
        # json_dict = json.loads(contents)

    patient = Patient.parse_raw(contents)

    scoring_input: ScoringInput = FhirToAttributeDict.get_scoring_input(
        resource=patient
    )

    scoring_json = json.dumps(scoring_input, cls=EnhancedJSONEncoder)
    print(scoring_json)

    with open(test_file_dir.joinpath("expected.json")) as file:
        expected_contents = file.read()
        expected_dict = json.loads(expected_contents)

    assert scoring_input.__dict__ == expected_dict
