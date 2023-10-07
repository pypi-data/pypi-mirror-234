from helix_personmatching.mergers.merge_config import (
    MergeConfig,
)


def test_creating_config_from_json() -> None:
    json_string = """
    {
        "data_sets": [
            {
                "access_tag": "medstar",
                "merge_rule": "merge",
                "field_rules": [
                    {"field": "name", "rule": "merge"},
                    {"field": "address", "rule": "ignore"}
                ],
                "resource_rules": [
                    {"resource_type": "Location", "rule": "exclusive"}
                ]
            }
        ]
    }
    """

    merge_config: MergeConfig = MergeConfig.from_json(json_string)

    created_json_string: str = merge_config.to_json()

    print(created_json_string)

    assert merge_config.data_sets[0].access_tag == "medstar"
