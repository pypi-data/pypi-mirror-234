import json
import dataclasses
from enum import Enum

from typing import List, Optional


class MergeRule(str, Enum):
    Ignore = "ignore"
    Exclusive = "exclusive"
    Merge = "merge"

    @classmethod
    def from_json(cls, json_string) -> "MergeRule":  # type: ignore
        for member in cls:
            if member.value == json_string:
                return member
        raise ValueError(f'"{json_string}" is not a valid MergeRule')

    def to_json(self) -> str:
        return self.value


class FieldType(str, Enum):
    Name = "name"
    Address = "address"
    Phone = "phone"
    Language = "language"
    Photo = "photo"
    Qualification = "qualification"
    Identifier = "identifier"
    Specialty = "specialty"
    Insurance = "insurance"
    Telecom = "telecom"
    Communication = "communication"

    @classmethod
    def from_json(cls, json_string) -> "FieldType":  # type: ignore
        for member in cls:
            if member.value == json_string:
                return member
        raise ValueError(f'"{json_string}" is not a valid FieldType')

    def to_json(self) -> str:
        return self.value


@dataclasses.dataclass
class FieldRule:
    field: FieldType
    rule: MergeRule

    @classmethod
    def from_json(cls, json_string) -> "FieldRule":  # type: ignore
        data = json.loads(json_string)
        return cls(
            field=FieldType.from_json(data["field"]),
            rule=MergeRule.from_json(data["rule"]),
        )

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))


@dataclasses.dataclass
class ResourceRule:
    resource_type: str
    rule: MergeRule

    @classmethod
    def from_json(cls, json_string) -> "ResourceRule":  # type: ignore
        data = json.loads(json_string)
        return cls(
            resource_type=data["resource_type"], rule=MergeRule.from_json(data["rule"])
        )

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))


@dataclasses.dataclass
class DataSetConfig:
    access_tag: str
    merge_rule: MergeRule = MergeRule.Merge
    field_rules: Optional[List[FieldRule]] = None
    resource_rules: Optional[List[ResourceRule]] = None

    @classmethod
    def from_json(cls, json_string) -> "DataSetConfig":  # type: ignore
        data = json.loads(json_string)
        return cls(
            access_tag=data["access_tag"],
            merge_rule=MergeRule.from_json(data["merge_rule"]),
            field_rules=[
                FieldRule.from_json(json.dumps(rule)) for rule in data["field_rules"]
            ]
            if "field_rules" in data
            else None,
            resource_rules=[
                ResourceRule.from_json(json.dumps(rule))
                for rule in data["resource_rules"]
            ]
            if "resource_rules" in data
            else None,
        )

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))


@dataclasses.dataclass
class MergeConfig:
    data_sets: List[DataSetConfig]

    @classmethod
    def from_json(cls, json_string) -> "MergeConfig":  # type: ignore
        data = json.loads(json_string)
        return cls(
            data_sets=[
                DataSetConfig.from_json(json.dumps(item)) for item in data["data_sets"]
            ]
        )

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))
