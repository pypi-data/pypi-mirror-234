from typing import Any, Dict, Optional, List, cast, Callable


# noinspection PyPackageRequirements
from fhir.resources.R4B.coding import Coding

# noinspection PyPackageRequirements
from fhir.resources.R4B.domainresource import DomainResource
from fhir.resources.R4B.element import Element
from fhir.resources.R4B.endpoint import Endpoint

# noinspection PyPackageRequirements
from fhir.resources.R4B.extension import Extension

# noinspection PyPackageRequirements
from fhir.resources.R4B.fhirtypes import (
    ContactPointType,
    HumanNameType,
    IdentifierType,
    CodeableConceptType,
    AttachmentType,
    PractitionerQualificationType,
)

# noinspection PyPackageRequirements
from fhir.resources.R4B.group import Group

# noinspection PyPackageRequirements
from fhir.resources.R4B.insuranceplan import InsurancePlan

# noinspection PyPackageRequirements
from fhir.resources.R4B.location import Location

# noinspection PyPackageRequirements
from fhir.resources.R4B.measurereport import MeasureReport

# noinspection PyPackageRequirements
from fhir.resources.R4B.meta import Meta

# noinspection PyPackageRequirements
from fhir.resources.R4B.organization import Organization

# noinspection PyPackageRequirements
from fhir.resources.R4B.practitioner import Practitioner

# noinspection PyPackageRequirements
from fhir.resources.R4B.practitionerrole import PractitionerRole

# noinspection PyPackageRequirements
from fhir.resources.R4B.schedule import Schedule

from helix_personmatching.mergers.merge_config import (
    MergeConfig,
    MergeRule,
    FieldType,
    DataSetConfig,
)
from helix_personmatching.mergers.merge_struct import MergeStruct
from helix_personmatching.utils.list_utils import get_first_element_or_null

CLIENT_EXTENSION_URL = "https://www.icanbwell.com/client"


class PractitionerMerger:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def merge(
        self,
        *,
        row: Dict[str, Any],
        config: Optional[MergeConfig],
        graph: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Merge practitioner resources from multiple data sets into a single practitioner resource.
        Takes in a dictionary with the following fields as arrays:
        practitioner
        practitionerrole
        organization
        location
        insuranceplan
        endpoint
        schedule
        group
        measurereport


        :param row: the row to merge
        :param config: the merge config
        :param graph: the graph
        """
        merge_struct = MergeStruct(row)
        assert config

        if merge_struct.practitioners is None or len(merge_struct.practitioners) == 0:
            return row

        # merge Practitioner
        merge_struct.practitioners = cast(
            List[Practitioner],
            [
                self.merge_practitioner(
                    practitioner=merge_struct.practitioners[0],
                    config=config,
                )
            ],
        )

        # merge practitioner_role
        merge_struct.practitioner_roles = cast(
            List[PractitionerRole],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.practitioner_roles),
                config=config,
                resource_type="PractitionerRole",
            ),
        )

        # merge organization
        merge_struct.organizations = cast(
            List[Organization],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.organizations),
                config=config,
                resource_type="Organization",
            ),
        )

        # merge location
        merge_struct.locations = cast(
            List[Location],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.locations),
                config=config,
                resource_type="Location",
            ),
        )

        # merge insurance_plan
        merge_struct.insurance_plans = cast(
            List[InsurancePlan],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.insurance_plans),
                config=config,
                resource_type="InsurancePlan",
            ),
        )

        # merge endpoint
        merge_struct.endpoints = cast(
            List[Endpoint],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.endpoints),
                config=config,
                resource_type="Endpoint",
            ),
        )

        # merge schedule
        merge_struct.schedules = cast(
            List[Schedule],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.schedules),
                config=config,
                resource_type="Schedule",
            ),
        )

        # merge group
        merge_struct.groups = cast(
            List[Group],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.groups),
                config=config,
                resource_type="Group",
            ),
        )

        # merge measure_report
        merge_struct.measure_reports = cast(
            List[MeasureReport],
            self.merge_resources(
                resources=cast(List[DomainResource], merge_struct.measure_reports),
                config=config,
                resource_type="MeasureReport",
            ),
        )

        return merge_struct.to_dict()

    def merge_practitioner(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the fields in a Practitioner resource

        :param practitioner: the practitioner resource
        :param config: the merge config
        """
        # merge name
        practitioner = self.merge_practitioner_name(
            practitioner=practitioner,
            config=config,
        )

        # merge telecom
        practitioner = self.merge_practitioner_telecom(
            config=config, practitioner=practitioner
        )

        # merge communication
        practitioner = self.merge_practitioner_communication(
            config=config, practitioner=practitioner
        )

        # merge photo
        practitioner = self.merge_practitioner_photo(
            config=config, practitioner=practitioner
        )

        # merge qualification
        practitioner = self.merge_practitioner_qualification(
            config=config, practitioner=practitioner
        )

        # merge identifier
        practitioner = self.merge_practitioner_identifier(
            config=config, practitioner=practitioner
        )

        return practitioner

    def merge_practitioner_communication(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the communication field in a Practitioner resource

        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        def set_communication(communications: List[Element]) -> Practitioner:
            practitioner.communication = cast(List[CodeableConceptType], communications)
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.communication),
            fn_set_element=set_communication,
            field_type=FieldType.Communication,
        )
        return practitioner

    def merge_practitioner_photo(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the photo field in a Practitioner resource

        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        def set_photo(photos: List[Element]) -> Practitioner:
            practitioner.photo = cast(List[AttachmentType], photos)
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.photo),
            fn_set_element=set_photo,
            field_type=FieldType.Photo,
        )
        return practitioner

    def merge_practitioner_qualification(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the qualification field in a Practitioner resource

        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        def set_qualification(qualifications: List[Element]) -> Practitioner:
            practitioner.qualification = cast(
                List[PractitionerQualificationType], qualifications
            )
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.qualification),
            fn_set_element=set_qualification,
            field_type=FieldType.Qualification,
        )
        return practitioner

    def merge_practitioner_identifier(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the identifier field in a Practitioner resource

        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        def set_identifier(identifiers: List[Element]) -> Practitioner:
            practitioner.identifier = cast(List[IdentifierType], identifiers)
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.identifier),
            fn_set_element=set_identifier,
            field_type=FieldType.Identifier,
        )
        return practitioner

    def merge_practitioner_telecom(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the telecom field in a Practitioner resource


        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        # merge telecom
        def set_telecom(telecom: List[Element]) -> Practitioner:
            practitioner.telecom = cast(List[ContactPointType], telecom)
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.telecom),
            fn_set_element=set_telecom,
            field_type=FieldType.Telecom,
        )
        return practitioner

    # noinspection PyMethodMayBeStatic
    def merge_practitioner_name(
        self, *, practitioner: Practitioner, config: MergeConfig
    ) -> Practitioner:
        """
        Merges the name field in a Practitioner resource


        :param practitioner: the practitioner resource
        :param config: the merge config
        :return the merged practitioner resource
        """

        def set_name(names: List[Element]) -> Practitioner:
            practitioner.name = cast(List[HumanNameType], names)
            return practitioner

        practitioner = self.merge_practitioner_element(
            practitioner=practitioner,
            config=config,
            fn_get_element=lambda p: cast(List[Element], p.name),
            fn_set_element=set_name,
            field_type=FieldType.Name,
        )
        return practitioner

    # noinspection PyMethodMayBeStatic
    def merge_practitioner_element(
        self,
        *,
        practitioner: Practitioner,
        config: MergeConfig,
        field_type: FieldType,
        fn_get_element: Callable[[Practitioner], List[Element] | None],
        fn_set_element: Callable[[List[Element]], Practitioner],
    ) -> Practitioner:
        """
        Merges an element array in Practitioner resource.



        :param field_type: FieldType
        :param practitioner: the practitioner resource
        :param config: the merge config
        :param fn_get_element: the function to get the element array from the practitioner
        :param fn_set_element: the function to set the element array on the practitioner
        """
        # in Practitioner, for item field look at extension with valueCode of slug
        # same for item, language, communication, photo, qualification, identifier
        combined_items: List[Element] = []
        elements: List[Element] | None = fn_get_element(practitioner)
        if elements is None:
            return practitioner

        data_set: DataSetConfig
        for data_set in config.data_sets:
            # from the item array choose only names that have the extension with the client slug
            elements_for_data_set: List[Element] = self.get_elements_for_data_set(
                data_set=data_set, elements=elements
            )
            merge_rule = self.get_rule_for_field(
                data_set=data_set, field_type=field_type
            )
            # handle the rule
            if merge_rule == MergeRule.Ignore:
                # for ignore rule, just skip all resources for this dataset
                continue
            if merge_rule == MergeRule.Exclusive:
                # for exclusive rule, ignore any resources from other data sets
                if len(elements_for_data_set) > 0:
                    practitioner = fn_set_element(elements_for_data_set)
                    return practitioner
            if merge_rule == MergeRule.Merge:
                combined_items.extend(elements_for_data_set)

        # if no combined_items matched then just use elements without any extension
        if len(combined_items) == 0:
            elements_without_data_sets: List[
                Element
            ] = self.get_elements_without_data_set(elements=elements)
            combined_items.extend(elements_without_data_sets)

        # now set the filtered names on the practitioner
        practitioner = fn_set_element(combined_items)
        return practitioner

    # noinspection PyMethodMayBeStatic
    def get_rule_for_field(
        self, *, data_set: DataSetConfig, field_type: FieldType
    ) -> MergeRule:
        """
        Gets the effective rule for a field in a data set.
        If there is a rule specified at the field level then use else use the dataset level rule


        :param data_set: the data set
        :param field_type: the field type
        :return: the merge rule
        """
        # if there is a rule specified at the field level then use else use the dataset level rule
        merge_rule = data_set.merge_rule
        if data_set.field_rules is not None:
            field_rule = get_first_element_or_null(
                [r for r in data_set.field_rules if r.field == field_type]
            )
            if field_rule:
                merge_rule = field_rule.merge_rule
        return merge_rule

    # noinspection PyMethodMayBeStatic
    def get_elements_without_data_set(self, elements: List[Element]) -> List[Element]:
        """
        Gets elements from the provided list that have no dataset match


        :param elements: The list of elements
        :return: the list of elements without a dataset match
        """
        return [
            element
            for element in elements
            if element.extension is None
            or not any(
                extension
                for extension in element.extension
                if cast(Extension, extension).url == CLIENT_EXTENSION_URL
            )
        ]

    # noinspection PyMethodMayBeStatic
    def get_elements_for_data_set(
        self, *, data_set: DataSetConfig, elements: List[Element]
    ) -> List[Element]:
        return [
            item
            for item in elements
            if item.extension is not None
            and any(
                extension
                for extension in item.extension
                if cast(Extension, extension).url == CLIENT_EXTENSION_URL
                and cast(Extension, extension).valueCode == data_set.access_tag
            )
        ]

    def merge_resources(
        self,
        *,
        resources: List[DomainResource] | None,
        config: MergeConfig,
        resource_type: str,
    ) -> List[DomainResource]:
        assert config
        if resources is None:
            return []
        combined_resources: List[DomainResource] = []
        for data_set in config.data_sets:
            # if there are resources available for this data set then filter to those and return
            resources_for_data_set: List[
                DomainResource
            ] = self.filter_resources_by_access_tag(
                resources=resources, access_tag=data_set.access_tag
            )
            # if there is a rule specified at the resource level then use else use the dataset level rule
            merge_rule = data_set.merge_rule
            if data_set.resource_rules is not None:
                resource_rule = get_first_element_or_null(
                    [
                        r
                        for r in data_set.resource_rules
                        if r.resource_type == resource_type
                    ]
                )
                if resource_rule:
                    merge_rule = resource_rule.merge_rule
            # Process the rule
            if merge_rule == MergeRule.Ignore:
                # for ignore rule, just skip all resources for this dataset
                continue
            if merge_rule == MergeRule.Exclusive:
                # for exclusive rule, ignore any resources from other data sets
                if len(resources_for_data_set) > 0:
                    return resources_for_data_set
            if merge_rule == MergeRule.Merge:
                # for merge rule, combine these resources with the others
                combined_resources.extend(resources_for_data_set)

        return combined_resources

    # noinspection PyMethodMayBeStatic
    def filter_resources_by_access_tag(
        self, *, resources: List[DomainResource], access_tag: str
    ) -> List[DomainResource]:
        filter_resources: List[DomainResource] = []
        for resource in resources:
            security_tags: List[Coding] = cast(
                List[Coding], cast(Meta, resource.meta).security
            )
            access_tags: List[str] = [
                security_tag.code
                for security_tag in security_tags
                if security_tag.system == "https://www.icanbwell.com/access"
            ]
            if access_tag in access_tags:
                filter_resources.append(resource)
        return filter_resources
