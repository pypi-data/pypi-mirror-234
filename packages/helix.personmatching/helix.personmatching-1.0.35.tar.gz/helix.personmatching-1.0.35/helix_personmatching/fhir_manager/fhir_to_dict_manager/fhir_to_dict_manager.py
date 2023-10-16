from datetime import date
from typing import Any, List, Mapping, Optional, OrderedDict, Tuple, Union, cast

import phonenumbers
import usaddress

# noinspection PyPackageRequirements
from fhir.resources.R4B.humanname import HumanName

# noinspection PyPackageRequirements
from fhir.resources.R4B.bundle import Bundle

# noinspection PyPackageRequirements
from fhir.resources.R4B.fhirtypes import (
    AddressType,
    ContactPointType,
    IdentifierType,
)

# noinspection PyPackageRequirements
from fhir.resources.R4B.patient import Patient

# noinspection PyPackageRequirements
from fhir.resources.R4B.person import Person
from nominally import parse_name
from phonenumbers import PhoneNumber
from scourgify import normalize_address_record

from helix_personmatching.fhir_manager.parse_name_result import ParseNameResult
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.utils.list_utils import get_first_element_or_null


class FhirToAttributeDict:
    @staticmethod
    def get_scoring_input(
        resource: Union[Patient, Person],
        verbose: bool = False,
    ) -> ScoringInput:
        if verbose:
            print("FhirToAttributeDict:get_scoring_input()")

        patient_name: Optional[HumanName] = FhirToAttributeDict.get_human_name(
            cast(Optional[List[HumanName]], resource.name)
        )
        address: Optional[AddressType] = FhirToAttributeDict.get_address(
            resource.address, verbose
        )

        # https://github.com/GreenBuildingRegistry/usaddress-scourgify
        # noinspection PyUnresolvedReferences
        address_dict = (
            {
                "address_line_1": address.line[0]
                if address.line and len(address.line) > 0
                else None,
                "address_line_2": None,
                # "address_line_2": address.line[1]
                # if address.line and len(address.line) > 1
                # else None,
                "city": address.city if address.city else None,
                "state": address.state if address.state else None,
                "postal_code": address.postalCode[0:5]
                if address.postalCode and len(address.postalCode) >= 5
                else None,
            }
            if address and address.postalCode and address.city and address.state
            else None
        )

        combined_address = (
            f"{address_dict['address_line_1'] or ''} "
            f"{address_dict['address_line_2'] or ''} "
            f"{address_dict['city']} {address_dict['state']} {address_dict['postal_code']}"
            if address_dict
            else None
        )

        parsed_address: Optional[OrderedDict[str, Union[List[str], str]]]
        parsed_address_type: Optional[str]
        parsed_address, parsed_address_type = (
            FhirToAttributeDict.safe_tag_address(
                address_line=combined_address,
                tag_mapping={
                    "Recipient": "recipient",
                    "AddressNumber": "address_line_1",
                    "AddressNumberPrefix": "address_line_1",
                    "AddressNumberSuffix": "address_line_1",
                    "StreetName": "address_line_1",
                    "StreetNamePreDirectional": "address_line_1",
                    "StreetNamePreModifier": "address_line_1",
                    "StreetNamePreType": "address_line_1",
                    "StreetNamePostDirectional": "address_line_1",
                    "StreetNamePostModifier": "address_line_1",
                    "StreetNamePostType": "address_line_1",
                    "CornerOf": "address_line_1",
                    "IntersectionSeparator": "address_line_1",
                    "LandmarkName": "address_line_1",
                    "USPSBoxGroupID": "address_line_1",
                    "USPSBoxGroupType": "address_line_1",
                    "USPSBoxID": "address_line_1",
                    "USPSBoxType": "address_line_1",
                    "BuildingName": "address_line_2",
                    "OccupancyType": "address_line_2",
                    "OccupancyIdentifier": "address_line_2",
                    "SubaddressIdentifier": "address_line_2",
                    "SubaddressType": "address_line_2",
                    "PlaceName": "city",
                    "StateName": "state",
                    "ZipCode": "postal_code",
                },
                verbose=verbose,
            )
            if combined_address
            else (None, None)
        )

        address_formatted: Optional[Mapping[str, str]] = (
            FhirToAttributeDict.safe_normalize_address_record(address_dict, verbose)
            if address_dict  # normalization fails on PO Boxes
            and (
                not parsed_address_type
                or parsed_address_type not in ["PO Box", "Ambiguous"]
            )
            and address_dict.get("postal_code")
            and address_dict.get("city")
            and address_dict.get("state")
            else FhirToAttributeDict.safe_normalize_address_record(parsed_address, verbose)  # type: ignore
            if parsed_address
            # normalization fails on PO Boxes
            and (
                not parsed_address_type
                or parsed_address_type not in ["PO Box", "Ambiguous"]
            )
            else None
        )

        # https://github.com/datamade/usaddress
        address_tagged: Optional[OrderedDict[str, Union[List[Any], str]]]
        address_type: Optional[str]
        # noinspection PyUnresolvedReferences
        address_tagged, address_type = (
            (
                FhirToAttributeDict.safe_tag_address(
                    address_line=combined_address,
                    verbose=verbose,
                )
            )
            if address and address.line and len(address.line) > 0
            else (None, None)
        )

        # noinspection PyUnresolvedReferences
        address_street_num: Optional[str] = (
            cast(Optional[str], address_tagged.get("AddressNumber"))
            if address_tagged
            else None
        )

        # phone
        phone: Optional[str] = FhirToAttributeDict.get_phone_number(
            resource.telecom, verbose
        )
        # phone_formatted = re.sub("[+\s()-]+", "", phone)
        # https://github.com/daviddrysdale/python-phonenumbers
        phone_formatted: Optional[PhoneNumber] = (
            FhirToAttributeDict.safe_phone_parse(phone, "US", verbose)
            if phone
            else None
        )
        phone_clean = str(phone_formatted.national_number) if phone_formatted else None

        # email
        email: Optional[str] = FhirToAttributeDict.get_email(resource.telecom, verbose)
        email_user_name = email.split("@")[0] if email else None

        # ssn
        ssn = FhirToAttributeDict.get_ssn(resource.identifier, verbose)

        # noinspection PyUnresolvedReferences
        meta_security_code = (
            FhirToAttributeDict.get_access_tag(resource.meta.security, verbose)
            if resource.meta and resource.meta.security
            else None
        )

        age_in_years = FhirToAttributeDict.calculate_age_in_years(
            resource.birthDate, verbose
        )

        # Get postal code in any way we can
        address_postal_code: Optional[str] = None
        if address_formatted and "postal_code" in address_formatted:
            address_postal_code = address_formatted.get("postal_code")
        if not address_postal_code and address_tagged and "ZipCode" in address_tagged:
            address_tagged_zip_code = address_tagged.get("ZipCode")
            if (
                isinstance(address_tagged_zip_code, list)
                and len(address_tagged_zip_code) > 0
            ):
                address_postal_code = address_tagged_zip_code[0]
            elif not isinstance(address_tagged_zip_code, list):
                address_postal_code = address_tagged_zip_code
        if (
            not address_postal_code
            and parsed_address
            and "postal_code" in parsed_address
        ):
            parsed_address_zip_code = parsed_address.get("postal_code")
            if (
                isinstance(parsed_address_zip_code, list)
                and len(parsed_address_zip_code) > 0
            ):
                address_postal_code = parsed_address_zip_code[0]
            elif not isinstance(parsed_address_zip_code, list):
                address_postal_code = parsed_address_zip_code
        # noinspection PyUnresolvedReferences
        if not address_postal_code and address and address.postalCode:
            # noinspection PyUnresolvedReferences
            address_postal_code = address.postalCode

        # Get address line 1 any way we can
        address_line_1: Optional[str] = None
        if address_formatted and "address_line_1" in address_formatted:
            address_line_1 = address_formatted.get("address_line_1")
        if not address_line_1 and parsed_address and "address_line_1" in parsed_address:
            parsed_address_line_1 = parsed_address.get("address_line_1")
            if (
                isinstance(parsed_address_line_1, list)
                and len(parsed_address_line_1) > 0
            ):
                address_line_1 = parsed_address_line_1[0]
            elif not isinstance(parsed_address_line_1, list):
                address_line_1 = parsed_address_line_1
        # noinspection PyUnresolvedReferences
        if not address_line_1 and address and address.line and len(address.line) > 0:
            # noinspection PyUnresolvedReferences
            address_line_1 = address.line[0]

        # noinspection PyUnresolvedReferences
        first_name: Optional[str] = (
            patient_name.given[0]
            if patient_name and patient_name.given and len(patient_name.given) > 0
            else None
        )
        # noinspection PyUnresolvedReferences
        family_name: Optional[str] = patient_name.family if patient_name else None
        # noinspection PyUnresolvedReferences
        middle_name: Optional[str] = (
            patient_name.given[1]
            if patient_name and patient_name.given and len(patient_name.given) > 1
            else None
        )

        # try to parse names using nominally since the names can be stored in wrong fields
        parsed_name: Optional[ParseNameResult] = FhirToAttributeDict.safe_name_parse(
            name=patient_name,
            verbose=verbose,
        )
        if parsed_name is not None:
            if parsed_name.first:
                first_name = parsed_name.first
            if parsed_name.middle:
                middle_name = parsed_name.middle
            if parsed_name.last:
                family_name = parsed_name.last

        # noinspection PyUnresolvedReferences
        scoring_input: ScoringInput = ScoringInput(
            id_=resource.id,
            name_given=first_name,
            name_family=family_name,
            name_middle=middle_name,
            name_middle_initial=middle_name[0]
            if middle_name and len(middle_name) > 0
            else None,
            gender=resource.gender,
            birth_date=resource.birthDate.strftime("%Y-%m-%d")
            if resource.birthDate
            else None,
            address_postal_code=address_postal_code,
            address_postal_code_first_five=address_postal_code[0:5]
            if address_postal_code and len(address_postal_code) >= 5
            else None,
            address_line_1=address_line_1,
            email=email,
            phone=phone_clean,
            birth_date_year=str(resource.birthDate.year)
            if resource.birthDate and resource.birthDate.year
            else None,
            birth_date_month=str(resource.birthDate.month)
            if resource.birthDate and resource.birthDate.month
            else None,
            birth_date_day=str(resource.birthDate.day)
            if resource.birthDate and resource.birthDate.day
            else None,
            phone_area=phone_clean[0:3] if phone_clean else None,
            phone_local=phone_clean[3:6] if phone_clean else None,
            phone_line=phone_clean[6:10] if phone_clean else None,
            address_line_1_st_num=address_street_num,
            email_username=email_user_name,
            is_adult_today=age_in_years >= 18 if age_in_years else None,
            ssn=ssn,
            ssn_last4=ssn[-4] if ssn and len(ssn) >= 4 else None,
            meta_security_client_slug=meta_security_code,
        )
        return scoring_input

    @staticmethod
    def get_human_name(name: Optional[List[HumanName]]) -> Optional[HumanName]:
        if name is None:
            return None

        # The order of preference is:
        # https://hl7.org/FHIR/valueset-name-use.html
        # 1. usual
        # 2. official
        # 3. maiden
        # 4. others
        usual_name: Optional[HumanName] = get_first_element_or_null(
            [name1 for name1 in name if name1.use == "usual"]
        )
        if usual_name:
            return usual_name

        official_name: Optional[HumanName] = get_first_element_or_null(
            [name1 for name1 in name if name1.use == "official"]
        )
        if official_name:
            return official_name

        maiden_name: Optional[HumanName] = get_first_element_or_null(
            [name1 for name1 in name if name1.use == "maiden"]
        )
        if maiden_name:
            return maiden_name

        return cast(Optional[HumanName], get_first_element_or_null(name))

    @staticmethod
    def safe_normalize_address_record(
        address: Union[str, Mapping[str, str]],
        verbose: bool = False,
    ) -> Mapping[str, str]:
        if verbose:
            print(
                "FhirToAttributeDict.safe_normalize_address_record() - normalizing the address..."
            )

        if not isinstance(address, str) and (
            not address.get("postal_code")
            or not address.get("city")
            or not address.get("state")
        ):
            return address
        try:
            return cast(Mapping[str, str], normalize_address_record(address=address))
        except Exception as e:
            if verbose:
                print(
                    f"Exception (graceful-handling): Standardizing Address: {address!r} {e}"
                )

            # Handle this exception gracefully,
            #  returning address object 'as is' and not normalized.
            return cast(Mapping[str, str], address)

    @staticmethod
    def safe_tag_address(
        address_line: Optional[str],
        tag_mapping: Optional[Mapping[str, str]] = None,
        verbose: bool = False,
    ) -> Tuple[OrderedDict[str, Union[List[str], str]], str]:
        if verbose:
            print("FhirToAttributeDict.safe_tag_address() - tagging address...")

        if not address_line:
            tagged_address = OrderedDict[str, Union[List[Any], str]]()
            return tagged_address, "Ambiguous"
        try:
            return cast(
                Tuple[OrderedDict[str, Union[List[str], str]], str],
                usaddress.tag(address_line, tag_mapping=tag_mapping),
            )
        except Exception as e:
            if verbose:
                print(
                    f"Exception (graceful-handling): Tagging Address: {address_line} {e}"
                )

            tagged_address = OrderedDict[str, Union[List[Any], str]]()
            return tagged_address, "Ambiguous"

    @staticmethod
    def safe_phone_parse(
        phone: str,
        country: str,
        verbose: bool = False,
    ) -> Optional[PhoneNumber]:
        if verbose:
            print("FhirToAttributeDict:safe_phone_parse()...")

        try:
            return phonenumbers.parse(phone, country)
        except Exception as e:
            if verbose:
                print(f"Exception (returning None): Parsing Phone: {phone}: {e}")

            return None

    @staticmethod
    def get_scoring_inputs_for_resource(
        resource: Union[Patient, Person, Bundle],
        verbose: bool = False,
    ) -> List[ScoringInput]:
        if isinstance(resource, Bundle):
            # noinspection PyUnresolvedReferences
            resources = [e.resource for e in resource.entry]
        else:
            resources = [resource]

        if verbose:
            print("FhirToAttributeDict:get_scoring_inputs_for_resource()...")

        return [
            FhirToAttributeDict.get_scoring_input(
                resource=resource,
                verbose=verbose,
            )
            for resource in resources
        ]

    @staticmethod
    def get_access_tag(
        security_tags: Optional[List[Any]], verbose: bool = False
    ) -> Optional[str]:
        if not security_tags or len(security_tags) == 0:
            return None

        if verbose:
            print("FhirToAttributeDict:get_access_tag()...")

        access_tags = [
            tag
            for tag in security_tags
            if tag.system == "https://www.icanbwell.com/access"
        ]
        return access_tags[0].code if len(access_tags) > 0 else None

    @staticmethod
    def get_ssn(
        identifiers: Optional[List[IdentifierType]], verbose: bool = False
    ) -> Optional[str]:
        if not identifiers or len(identifiers) == 0:
            return None

        if verbose:
            print("FhirToAttributeDict:get_ssn()...")

        ssn_identifiers = [
            identifier
            for identifier in identifiers
            if identifier.system == "http://hl7.org/fhir/sid/us-ssn"
        ]
        return ssn_identifiers[0].value if len(ssn_identifiers) > 0 else None

    @staticmethod
    def get_phone_number(
        telecom: Optional[List[ContactPointType]], verbose: bool = False
    ) -> Optional[str]:
        if not telecom or len(telecom) == 0:
            return None

        if verbose:
            print("FhirToAttributeDict:get_phone_number()...")

        phones = FhirToAttributeDict.get_telecom_with_system(telecom, "phone", verbose)
        if phones and len(phones) > 0:
            # prefer use=mobile
            mobile_phones = [phone for phone in phones if phone.use == "mobile"]
            if len(mobile_phones) > 0:
                return cast(Optional[str], mobile_phones[0].value)
            # noinspection PyUnresolvedReferences
            return cast(Optional[str], phones[0].value)
        else:
            return None

    @staticmethod
    def get_email(
        telecom: Optional[List[ContactPointType]], verbose: bool = False
    ) -> Optional[str]:
        if not telecom or len(telecom) == 0:
            return None

        if verbose:
            print("FhirToAttributeDict:get_email()...")

        emails = FhirToAttributeDict.get_telecom_with_system(telecom, "email", verbose)
        if emails and len(emails) > 0:
            # noinspection PyUnresolvedReferences
            return cast(Optional[str], emails[0].value)
        else:
            return None

    @staticmethod
    def get_telecom_with_system(
        telecom: List[ContactPointType], telecom_system: str, verbose: bool = False
    ) -> Optional[List[ContactPointType]]:
        if not telecom or len(telecom) == 0:
            return None

        if verbose:
            print(
                f"FhirToAttributeDict:get_telecom_with_system() for {telecom_system}..."
            )

        # noinspection PyUnresolvedReferences
        matching_telecoms = [t for t in telecom if t.system == telecom_system]
        return matching_telecoms

    @staticmethod
    def get_address(
        addresses: Optional[List[AddressType]], verbose: bool = False
    ) -> Optional[AddressType]:
        if not addresses or len(addresses) == 0:
            return None

        # https://hl7.org/FHIR/valueset-address-use.html

        if verbose:
            print("FhirToAttributeDict:get_address()...")

        # 1. use == "official"
        official_address: Optional[AddressType] = get_first_element_or_null(
            [address for address in addresses if address.use == "official"]
        )
        if official_address:
            return official_address

        # 2. use == "home"
        home_address: Optional[AddressType] = get_first_element_or_null(
            [address for address in addresses if address.use == "home"]
        )
        if home_address:
            return home_address

        # 2. use == "work"
        work_address: Optional[AddressType] = get_first_element_or_null(
            [address for address in addresses if address.use == "work"]
        )
        if work_address:
            return work_address

        # 3. IF there is no use property, use the first address element by default
        return cast(Optional[AddressType], get_first_element_or_null(addresses))

    @staticmethod
    def calculate_age_in_years(
        birthdate: Optional[date], verbose: bool = False
    ) -> Optional[int]:
        if not birthdate:
            return None

        if verbose:
            print("FhirToAttributeDict:calculate_age_in_years()...")

        # Get today's date object
        today = date.today()

        # A bool that represents if today's day/month precedes the birthday/month
        one_or_zero = (today.month, today.day) < (birthdate.month, birthdate.day)

        # Calculate the difference in years from the date object's components
        year_difference = today.year - birthdate.year

        # The difference in years is not enough.
        # To get it right, subtract 1 or 0 based on if today precedes the
        # birthdate's month/day.

        # To do this, subtract the 'one_or_zero' boolean
        # from 'year_difference'. (This converts
        # True to 1 and False to 0 under the hood.)
        age = year_difference - one_or_zero

        return age

    @staticmethod
    def safe_name_parse(
        name: Optional[HumanName],
        verbose: bool = False,
    ) -> Optional[ParseNameResult]:
        # noinspection PyUnresolvedReferences
        if name is None or name.family is None:
            return None

        if verbose:
            print("FhirToAttributeDict:safe_name_parse()...")

        combined_name = ""
        try:
            # noinspection PyUnresolvedReferences
            if name.given is not None:
                # noinspection PyUnresolvedReferences
                combined_name += " ".join([str(g) for g in name.given])
            # noinspection PyUnresolvedReferences
            if name.family is not None:
                # noinspection PyUnresolvedReferences
                combined_name += f" {name.family}"
            result = parse_name(combined_name)
            return ParseNameResult(
                first=result.get("first"),
                middle=result.get("middle"),
                last=result.get("last"),
            )
        except Exception as e:
            if verbose:
                print(f"Exception (returning None): Parsing Name: {combined_name}: {e}")

            return None
