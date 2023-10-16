import json
from typing import Any, Dict

from helix_personmatching.utils.fhir_resource_helpers import FhirResourceHelpers


def test_fhir_resource_helpers() -> None:
    item_json = """{
      "resourceType": "Organization",
      "id": "Medstar-Alias-AL2-WDER",
      "meta": {
        "versionId": "1",
        "lastUpdated": "2023-02-15T17:51:29.000Z",
        "source": "http://medstarhealth.org/practice",
        "security": [
          {
            "system": "https://www.icanbwell.com/access",
            "code": "medstar"
          },
          {
            "system": "https://www.icanbwell.com/owner",
            "code": "medstar"
          },
          {
            "system": "https://www.icanbwell.com/sourceAssigningAuthority",
            "code": "medstar"
          }
        ]
      },
      "extension": "[{\\"extension\\":[{\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/longitude\\",\\"valueDecimal\\":-77.0461},{\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/latitude\\",\\"valueDecimal\\":38.904484}],\\"url\\":\\"https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/position\\"}]",
      "identifier": [
        {
          "use": "usual",
          "system": "http://medstarhealth.org",
          "value": "AL2-WDER"
        },
        {
          "id": "sourceId",
          "system": "https://www.icanbwell.com/sourceId",
          "value": "Medstar-Alias-AL2-WDER"
        },
        {
          "id": "uuid",
          "system": "https://www.icanbwell.com/uuid",
          "value": "4d8c9030-a9d8-5836-8952-caefbe897523"
        }
      ],
      "active": true,
      "type": [
        {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/organization-type",
              "code": "prov",
              "display": "Healthcare Provider"
            }
          ],
          "text": "Healthcare Organization"
        }
      ],
      "name": "MedStar Washington Hospital Center Dermatology at Lafayette Bldg 3",
      "alias": [
        "MedStar WHC Derm at Lafayette Bldg 2"
      ],
      "telecom": [
        {
          "id": "amp-office-phone",
          "system": "phone",
          "value": "(301) 951-2400",
          "use": "work",
          "rank": 1
        },
        {
          "id": "amp-office-tax",
          "system": "fax",
          "value": "(301) 951-2401",
          "use": "work",
          "rank": 2
        }
      ],
      "address": [
        {
          "line": [
            "1133 21st St NW Bldg 2"
          ],
          "city": "Washington",
          "state": "DC",
          "postalCode": "20036-3390"
        }
      ],
      "partOf": {
        "extension": "[{\\"id\\":\\"sourceId\\",\\"url\\":\\"https://www.icanbwell.com/sourceId\\",\\"valueString\\":\\"Organization/Medstar--292733691\\"},{\\"id\\":\\"uuid\\",\\"url\\":\\"https://www.icanbwell.com/uuid\\",\\"valueString\\":\\"Organization/8c1716b8-19e9-5e14-8be7-6710ea5cd342\\"},{\\"id\\":\\"sourceAssigningAuthority\\",\\"url\\":\\"https://www.icanbwell.com/sourceAssigningAuthority\\",\\"valueString\\":\\"medstar\\"}]",
        "reference": "Organization/Medstar--292733691",
        "display": "MedStar WHC Dermatology at Lafayette Bldg 2"
      },
      "contact": [
        {
          "purpose": {
            "coding": [
              {
                "system": "http://medstarhealth.org",
                "code": "Central Scheduling"
              }
            ]
          }
        }
      ]
    }"""
    item: Dict[str, Any] = json.loads(item_json)
    result: Dict[str, Any] = FhirResourceHelpers.remove_none_values_from_dict(item=item)
    assert result == {
        "resourceType": "Organization",
        "id": "Medstar-Alias-AL2-WDER",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2023-02-15T17:51:29.000Z",
            "source": "http://medstarhealth.org/practice",
            "security": [
                {"system": "https://www.icanbwell.com/access", "code": "medstar"},
                {"system": "https://www.icanbwell.com/owner", "code": "medstar"},
                {
                    "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                    "code": "medstar",
                },
            ],
        },
        "identifier": [
            {"use": "usual", "system": "http://medstarhealth.org", "value": "AL2-WDER"},
            {
                "id": "sourceId",
                "system": "https://www.icanbwell.com/sourceId",
                "value": "Medstar-Alias-AL2-WDER",
            },
            {
                "id": "uuid",
                "system": "https://www.icanbwell.com/uuid",
                "value": "4d8c9030-a9d8-5836-8952-caefbe897523",
            },
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider",
                    }
                ],
                "text": "Healthcare Organization",
            }
        ],
        "name": "MedStar Washington Hospital Center Dermatology at Lafayette Bldg 3",
        "alias": ["MedStar WHC Derm at Lafayette Bldg 2"],
        "telecom": [
            {
                "id": "amp-office-phone",
                "system": "phone",
                "value": "(301) 951-2400",
                "use": "work",
                "rank": 1,
            },
            {
                "id": "amp-office-tax",
                "system": "fax",
                "value": "(301) 951-2401",
                "use": "work",
                "rank": 2,
            },
        ],
        "address": [
            {
                "line": ["1133 21st St NW Bldg 2"],
                "city": "Washington",
                "state": "DC",
                "postalCode": "20036-3390",
            }
        ],
        "partOf": {
            "reference": "Organization/Medstar--292733691",
            "display": "MedStar WHC Dermatology at Lafayette Bldg 2",
        },
        "contact": [
            {
                "purpose": {
                    "coding": [
                        {
                            "system": "http://medstarhealth.org",
                            "code": "Central Scheduling",
                        }
                    ]
                }
            }
        ],
    }
