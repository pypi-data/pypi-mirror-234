import json
from typing import Any, Dict

from helix_personmatching.utils.fhir_resource_helpers import FhirResourceHelpers


def test_fhir_resource_helpers_extension() -> None:
    item_json = """{
      "extension": "[{\\"extension\\":[{\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/longitude\\",\\"valueDecimal\\":-77.0461},{\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/latitude\\",\\"valueDecimal\\":38.904484}],\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/position\\"}]"
    }"""
    item: Dict[str, Any] = json.loads(item_json)
    result: Dict[str, Any] = FhirResourceHelpers.remove_none_values_from_dict(item=item)
    assert result == {}
