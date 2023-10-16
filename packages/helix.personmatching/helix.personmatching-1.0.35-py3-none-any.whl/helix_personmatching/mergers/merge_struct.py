import dataclasses
import json
from typing import List, Any, Dict

# noinspection PyPackageRequirements
from fhir.resources.R4B.endpoint import Endpoint
from fhir.resources.R4B.group import Group
from fhir.resources.R4B.insuranceplan import InsurancePlan
from fhir.resources.R4B.location import Location
from fhir.resources.R4B.measurereport import MeasureReport
from fhir.resources.R4B.organization import Organization
from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.practitionerrole import PractitionerRole
from fhir.resources.R4B.schedule import Schedule

from helix_personmatching.utils.fhir_resource_helpers import FhirResourceHelpers


@dataclasses.dataclass
class MergeStruct:
    practitioners: List[Practitioner]
    practitioner_roles: List[PractitionerRole]
    locations: List[Location]
    organizations: List[Organization]
    schedules: List[Schedule]
    endpoints: List[Endpoint]
    insurance_plans: List[InsurancePlan]
    groups: List[Group]
    measure_reports: List[MeasureReport]

    def __init__(self, dict_data: Dict[str, Any]) -> None:
        self.practitioners: List[Practitioner] = []
        self.practitioner_roles = []
        self.locations = []
        self.organizations = []
        self.schedules = []
        self.endpoints = []
        self.insurance_plans = []
        self.groups = []
        self.measure_reports = []

        item: Dict[str, Any]

        for key, value in dict_data.items():
            if key == "practitioner":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.practitioners.append(Practitioner.parse_obj(item))
            if key == "practitionerrole":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.practitioner_roles.append(PractitionerRole.parse_obj(item))
            if key == "location":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.locations.append(Location.parse_obj(item))
            if key == "organization":
                for item in value:
                    try:
                        item = FhirResourceHelpers.remove_none_values_from_dict(item)
                        self.organizations.append(Organization.parse_obj(item))
                    except Exception as e:
                        print(f"Parsing Error: {e}: {item}")
                        raise e
            if key == "schedule":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.schedules.append(Schedule.parse_obj(item))
            if key == "endpoint":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.endpoints.append(Endpoint.parse_obj(item))
            if key == "insuranceplan":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.insurance_plans.append(InsurancePlan.parse_obj(item))
            if key == "group":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.groups.append(Group.parse_obj(item))
            if key == "measurereport":
                for item in value:
                    item = FhirResourceHelpers.remove_none_values_from_dict(item)
                    self.measure_reports.append(MeasureReport.parse_obj(item))

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.practitioners:
            result["practitioner"] = [
                json.loads(item.json()) for item in self.practitioners
            ]
        if self.practitioner_roles:
            result["practitionerrole"] = [
                json.loads(item.json()) for item in self.practitioner_roles
            ]
        if self.locations:
            result["location"] = [json.loads(item.json()) for item in self.locations]
        if self.organizations:
            result["organization"] = [
                json.loads(item.json()) for item in self.organizations
            ]
        if self.schedules:
            result["schedule"] = [json.loads(item.json()) for item in self.schedules]
        if self.endpoints:
            result["endpoint"] = [json.loads(item.json()) for item in self.endpoints]
        if self.insurance_plans:
            result["insuranceplan"] = [
                json.loads(item.json()) for item in self.insurance_plans
            ]
        if self.groups:
            result["group"] = [json.loads(item.json()) for item in self.groups]
        if self.measure_reports:
            result["measurereport"] = [
                json.loads(item.json()) for item in self.measure_reports
            ]

        # take it through json to make sure we have a clean dict
        result: Dict[str, Any] = json.loads(json.dumps(result))
        return result
