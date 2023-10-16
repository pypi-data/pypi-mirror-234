from typing import Dict, Any, List
import re


class FhirResourceHelpers:
    @staticmethod
    def remove_none_values_from_dict_or_list(
        item: Dict[str, Any]
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        if isinstance(item, list):
            return [
                FhirResourceHelpers.remove_none_values_from_dict_or_list(i)
                for i in item
            ]
        if not isinstance(item, dict):
            return item
        return {
            k: FhirResourceHelpers.fix_id(fhir_id=v)
            if k == "id"
            else FhirResourceHelpers.remove_none_values_from_dict_or_list(v)
            for k, v in item.items()
            if v is not None and not (k == "extension" and isinstance(v, str))
        }

    @staticmethod
    def remove_none_values_from_dict(item: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(item, dict):
            return item
        return {
            k: FhirResourceHelpers.remove_none_values_from_dict_or_list(v)
            for k, v in item.items()
            if v is not None and not (k == "extension" and isinstance(v, str))
        }

    @staticmethod
    def fix_id(fhir_id: str) -> str:
        # Replace all characters not matching the allowed set with a hyphen
        sanitized_id = re.sub(r"[^A-Za-z0-9\-.]", "-", fhir_id)
        return sanitized_id

    @staticmethod
    def fix_last_updated_time_zone_in_resources(
        resources: List[Dict[str, Any]]
    ) -> None:
        for resource in resources:
            resource["meta"]["lastUpdated"] = resource["meta"]["lastUpdated"].replace(
                "+00:00", ".000Z"
            )
