from typing import Any, Dict

# noinspection PyPackageRequirements
from fhir.resources.R4B.practitioner import Practitioner

from helix_personmatching.mergers.merge_config import (
    MergeConfig,
    DataSetConfig,
    MergeRule,
)
from helix_personmatching.mergers.practitioner_merger import PractitionerMerger


def test_practitioner_merge_practitioner_only() -> None:
    print()

    practitioner1_dict: Dict[str, Any] = {
        "resourceType": "Practitioner",
        "id": "1194309690",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2023-03-30T10:53:17.000Z",
            "source": "http://medstarhealth.org/provider",
            "security": [
                {"system": "https://www.icanbwell.com/access", "code": "medstar"},
                {"system": "https://www.icanbwell.com/owner", "code": "medstar"},
                {
                    "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                    "code": "nppes",
                },
            ],
        },
        "identifier": [
            {
                "id": "medstar-gecb-provider-number",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "id": "id-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                        }
                    ]
                },
                "system": "http://medstarhealth.org",
                "value": "8106",
            },
            {
                "id": "npi",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "official",
                "type": {
                    "coding": [
                        {
                            "id": "npi-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "NPI",
                        }
                    ]
                },
                "system": "http://hl7.org/fhir/sid/us-npi",
                "value": "1194309690",
            },
            {
                "id": "sourceId",
                "system": "https://www.icanbwell.com/sourceId",
                "value": "1194309690",
            },
            {
                "id": "uuid",
                "system": "https://www.icanbwell.com/uuid",
                "value": "0001a1c9-d31f-5558-9813-bc4e91fc3761",
            },
        ],
        "active": True,
        "name": [
            {
                "id": "bwell-name",
                "extension": [
                    {
                        "id": "bwell-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "bwell",
                    }
                ],
                "use": "usual",
                "text": "Foo Bar",
                "family": "Bar Md",
                "given": ["Foo"],
            },
            {
                "id": "medstar-name",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "usual",
                "text": "Hala Marie Rogers Md",
                "family": "Rogers Md",
                "given": ["Hala Marie"],
            },
        ],
        "gender": "unknown",
        "communication": [
            {
                "id": "medstarEnglish",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "coding": [
                    {
                        "id": "comm-code",
                        "system": "urn:ietf:bcp:47",
                        "code": "en",
                        "display": "English",
                    }
                ],
            }
        ],
    }

    practitioner1: Practitioner = Practitioner.parse_obj(practitioner1_dict)
    expected_practitioner1: Practitioner = practitioner1.copy(deep=True)

    config: MergeConfig = MergeConfig(
        data_sets=[
            DataSetConfig(access_tag="medstar", merge_rule=MergeRule.Exclusive),
            DataSetConfig(access_tag="bwell", merge_rule=MergeRule.Exclusive),
        ]
    )

    result: Practitioner = PractitionerMerger().merge_practitioner(
        practitioner=practitioner1, config=config
    )

    # remove the identifiers that don't match the data set
    expected_practitioner1.identifier = expected_practitioner1.identifier[:2]
    # remove the b.well name
    expected_practitioner1.name = [expected_practitioner1.name[1]]
    assert result.json() == expected_practitioner1.json()


def test_practitioner_merge_practitioner_only_falls_back_to_second_data_set() -> None:
    print()

    practitioner1_dict: Dict[str, Any] = {
        "resourceType": "Practitioner",
        "id": "1194309690",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2023-03-30T10:53:17.000Z",
            "source": "http://medstarhealth.org/provider",
            "security": [
                {"system": "https://www.icanbwell.com/access", "code": "medstar"},
                {"system": "https://www.icanbwell.com/owner", "code": "medstar"},
                {
                    "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                    "code": "nppes",
                },
            ],
        },
        "identifier": [
            {
                "id": "medstar-gecb-provider-number",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "id": "id-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                        }
                    ]
                },
                "system": "http://medstarhealth.org",
                "value": "8106",
            },
            {
                "id": "npi",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "official",
                "type": {
                    "coding": [
                        {
                            "id": "npi-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "NPI",
                        }
                    ]
                },
                "system": "http://hl7.org/fhir/sid/us-npi",
                "value": "1194309690",
            },
            {
                "id": "sourceId",
                "system": "https://www.icanbwell.com/sourceId",
                "value": "1194309690",
            },
            {
                "id": "uuid",
                "system": "https://www.icanbwell.com/uuid",
                "value": "0001a1c9-d31f-5558-9813-bc4e91fc3761",
            },
        ],
        "active": True,
        "name": [
            {
                "id": "bwell-name",
                "extension": [
                    {
                        "id": "bwell-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "bwell",
                    }
                ],
                "use": "usual",
                "text": "Foo Bar",
                "family": "Bar Md",
                "given": ["Foo"],
            }
        ],
        "gender": "unknown",
        "communication": [
            {
                "id": "medstarEnglish",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "coding": [
                    {
                        "id": "comm-code",
                        "system": "urn:ietf:bcp:47",
                        "code": "en",
                        "display": "English",
                    }
                ],
            }
        ],
    }

    practitioner1: Practitioner = Practitioner.parse_obj(practitioner1_dict)
    expected_practitioner1: Practitioner = practitioner1.copy(deep=True)

    config: MergeConfig = MergeConfig(
        data_sets=[
            DataSetConfig(access_tag="medstar", merge_rule=MergeRule.Exclusive),
            DataSetConfig(access_tag="bwell", merge_rule=MergeRule.Exclusive),
        ]
    )

    result: Practitioner = PractitionerMerger().merge_practitioner(
        practitioner=practitioner1, config=config
    )

    # remove the identifiers that don't match the data set
    expected_practitioner1.identifier = expected_practitioner1.identifier[:2]
    # should fall back to the b.well name
    expected_practitioner1.name = [expected_practitioner1.name[0]]
    assert result.json() == expected_practitioner1.json()


def test_practitioner_merge_practitioner_only_falls_back_to_normal_name() -> None:
    print()

    practitioner1_dict: Dict[str, Any] = {
        "resourceType": "Practitioner",
        "id": "1194309690",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2023-03-30T10:53:17.000Z",
            "source": "http://medstarhealth.org/provider",
            "security": [
                {"system": "https://www.icanbwell.com/access", "code": "medstar"},
                {"system": "https://www.icanbwell.com/owner", "code": "medstar"},
                {
                    "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                    "code": "nppes",
                },
            ],
        },
        "identifier": [
            {
                "id": "medstar-gecb-provider-number",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "id": "id-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                        }
                    ]
                },
                "system": "http://medstarhealth.org",
                "value": "8106",
            },
            {
                "id": "npi",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "use": "official",
                "type": {
                    "coding": [
                        {
                            "id": "npi-type",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "NPI",
                        }
                    ]
                },
                "system": "http://hl7.org/fhir/sid/us-npi",
                "value": "1194309690",
            },
            {
                "id": "sourceId",
                "system": "https://www.icanbwell.com/sourceId",
                "value": "1194309690",
            },
            {
                "id": "uuid",
                "system": "https://www.icanbwell.com/uuid",
                "value": "0001a1c9-d31f-5558-9813-bc4e91fc3761",
            },
        ],
        "active": True,
        "name": [
            {
                "id": "bwell-name",
                "use": "usual",
                "text": "Foo Bar",
                "family": "Bar Md",
                "given": ["Foo"],
            }
        ],
        "gender": "unknown",
        "communication": [
            {
                "id": "medstarEnglish",
                "extension": [
                    {
                        "id": "medstar-client",
                        "url": "https://www.icanbwell.com/client",
                        "valueCode": "medstar",
                    }
                ],
                "coding": [
                    {
                        "id": "comm-code",
                        "system": "urn:ietf:bcp:47",
                        "code": "en",
                        "display": "English",
                    }
                ],
            }
        ],
    }

    practitioner1: Practitioner = Practitioner.parse_obj(practitioner1_dict)

    config: MergeConfig = MergeConfig(
        data_sets=[
            DataSetConfig(access_tag="medstar", merge_rule=MergeRule.Exclusive),
            DataSetConfig(access_tag="bwell", merge_rule=MergeRule.Exclusive),
        ]
    )

    result: Practitioner = PractitionerMerger().merge_practitioner(
        practitioner=practitioner1, config=config
    )

    # should fall back to the normal name
    expected_practitioner1: Practitioner = Practitioner.parse_obj(
        {
            "resourceType": "Practitioner",
            "id": "1194309690",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2023-03-30T10:53:17.000Z",
                "source": "http://medstarhealth.org/provider",
                "security": [
                    {"system": "https://www.icanbwell.com/access", "code": "medstar"},
                    {"system": "https://www.icanbwell.com/owner", "code": "medstar"},
                    {
                        "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                        "code": "nppes",
                    },
                ],
            },
            "identifier": [
                {
                    "id": "medstar-gecb-provider-number",
                    "extension": [
                        {
                            "id": "medstar-client",
                            "url": "https://www.icanbwell.com/client",
                            "valueCode": "medstar",
                        }
                    ],
                    "use": "usual",
                    "type": {
                        "coding": [
                            {
                                "id": "id-type",
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "PRN",
                            }
                        ]
                    },
                    "system": "http://medstarhealth.org",
                    "value": "8106",
                },
                {
                    "id": "npi",
                    "extension": [
                        {
                            "id": "medstar-client",
                            "url": "https://www.icanbwell.com/client",
                            "valueCode": "medstar",
                        }
                    ],
                    "use": "official",
                    "type": {
                        "coding": [
                            {
                                "id": "npi-type",
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "NPI",
                            }
                        ]
                    },
                    "system": "http://hl7.org/fhir/sid/us-npi",
                    "value": "1194309690",
                },
            ],
            "active": True,
            "name": [
                {
                    "id": "bwell-name",
                    "use": "usual",
                    "text": "Foo Bar",
                    "family": "Bar Md",
                    "given": ["Foo"],
                }
            ],
            "gender": "unknown",
            "communication": [
                {
                    "id": "medstarEnglish",
                    "extension": [
                        {
                            "id": "medstar-client",
                            "url": "https://www.icanbwell.com/client",
                            "valueCode": "medstar",
                        }
                    ],
                    "coding": [
                        {
                            "id": "comm-code",
                            "system": "urn:ietf:bcp:47",
                            "code": "en",
                            "display": "English",
                        }
                    ],
                }
            ],
        }
    )
    print(result.json())
    assert result.json() == expected_practitioner1.json()
