import json
from typing import Union, Dict, Any, List

# noinspection PyPackageRequirements
from fhir.resources.R4B.bundle import Bundle, BundleEntry

# noinspection PyPackageRequirements
from fhir.resources.R4B.patient import Patient

# noinspection PyPackageRequirements
from fhir.resources.R4B.person import Person

from helix_personmatching.fhir_manager.fhir_to_dict_manager.fhir_to_dict_manager import (
    FhirToAttributeDict,
)
from helix_personmatching.logics.scoring_input import ScoringInput


class FhirLoader:
    @staticmethod
    def parse(
        resource_json: str, verbose: bool = False
    ) -> Union[Patient, Person, Bundle]:
        if verbose:
            print("FhirLoader:parse()...")

        resource_dict: Dict[str, Any] = json.loads(resource_json)
        resource_type = resource_dict.get("resourceType")

        if verbose:
            print(f"FhirLoader:parse() - {resource_type}.parse_raw()...")

        if resource_type == "Patient":
            return Patient.parse_raw(resource_json)
        elif resource_type == "Person":
            return Person.parse_raw(resource_json)
        elif resource_type == "Bundle":
            return Bundle.parse_raw(resource_json)
        else:
            raise Exception(f"resourceType {resource_type} is not Patient or Person")

    @staticmethod
    def get_scoring_inputs(
        resource_json: Union[str, List[str]],
        verbose: bool = False,
    ) -> List[ScoringInput]:
        if isinstance(resource_json, list):
            # make it into a bundle
            bundle = Bundle.construct(type="collection")
            bundle.total = len(resource_json)  # type: ignore
            bundle.entry = [
                BundleEntry(resource=FhirLoader.parse(resource_json=resource_json_item))  # type: ignore
                for resource_json_item in resource_json
            ]

            if verbose:
                print(
                    "FhirLoader:get_scoring_inputs() - running FhirToAttributeDict.get_scoring_inputs_for_resource() "
                    "on the input bundle"
                )

            return FhirToAttributeDict.get_scoring_inputs_for_resource(bundle, verbose)
        else:
            resource: Union[Patient, Person, Bundle] = FhirLoader.parse(
                resource_json=resource_json
            )
            if verbose:
                print(
                    "FhirLoader:get_scoring_inputs() - running FhirToAttributeDict.get_scoring_inputs_for_resource() "
                    "on the input resource"
                )

            return FhirToAttributeDict.get_scoring_inputs_for_resource(
                resource, verbose
            )
