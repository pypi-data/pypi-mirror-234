import collections.abc
import decimal
import enum
import json
import typing

import pydantic

from ..serde import safe_dict_drill


class Comparator(str, enum.Enum):
    """The comparator to use when comparing a field to a value."""

    Equals = "EQUALS"
    NotEquals = "NOT_EQUALS"
    GreaterThan = "GREATER_THAN"
    GreaterThanOrEqual = "GREATER_THAN_OR_EQUAL"
    LessThan = "LESS_THAN"
    LessThanOrEqual = "LESS_THAN_OR_EQUAL"
    Contains = "CONTAINS"
    NotContains = "NOT_CONTAINS"
    IsNull = "IS_NULL"
    IsNotNull = "IS_NOT_NULL"
    Exists = "EXISTS"
    NotExists = "NOT_EXISTS"
    BeginsWith = "BEGINS_WITH"


class Condition(pydantic.BaseModel):
    """A filter for any arbitrary attribute for a Roboto resource."""

    field: str
    comparator: Comparator
    value: typing.Optional[typing.Union[str, bool, int, float, decimal.Decimal]] = None

    @pydantic.validator("value")
    def parse(cls, v):
        if v is None:
            return None
        try:
            return json.loads(v)
        except json.decoder.JSONDecodeError:
            return v

    def matches(self, target: dict) -> bool:
        value = safe_dict_drill(target, self.field.split("."))

        if self.comparator in [Comparator.NotExists, Comparator.IsNull]:
            return value is None

        if self.comparator in [Comparator.Exists, Comparator.IsNotNull]:
            return value is not None

        # We need the value for everything else
        if value is None:
            return False

        if isinstance(value, str) and not isinstance(self.value, str):
            if isinstance(self.value, int):
                value = int(value)
            elif isinstance(self.value, float):
                value = float(value)
            elif isinstance(self.value, bool):
                value = value.lower() == "true"
            elif isinstance(self.value, decimal.Decimal):
                value = decimal.Decimal.from_float(float(value))

        if self.comparator is Comparator.Equals:
            return value == self.value

        if self.comparator is Comparator.NotEquals:
            return value != self.value

        if self.comparator is Comparator.GreaterThan:
            return value > self.value

        if self.comparator is Comparator.GreaterThanOrEqual:
            return value >= self.value

        if self.comparator is Comparator.LessThan:
            return value < self.value

        if self.comparator is Comparator.LessThanOrEqual:
            return value <= self.value

        if self.comparator is Comparator.Contains:
            return isinstance(value, list) and self.value in value

        if self.comparator is Comparator.NotContains:
            return isinstance(value, list) and self.value not in value

        if self.comparator is Comparator.BeginsWith:
            if not isinstance(value, str) or not isinstance(self.value, str):
                return False

            return value.startswith(self.value)

        return False

    def __str__(self):
        return self.json()

    def __repr__(self):
        return self.json()


class ConditionOperator(str, enum.Enum):
    """The operator to use when combining multiple conditions."""

    And = "AND"
    Or = "OR"
    Not = "NOT"


class ConditionGroup(pydantic.BaseModel):
    """A group of conditions that are combined together."""

    operator: ConditionOperator
    conditions: collections.abc.Sequence[typing.Union[Condition, "ConditionGroup"]]

    def matches(self, target: dict):
        inner_matches = map(lambda x: x.matches(target), self.conditions)

        if self.operator is ConditionOperator.And:
            return all(inner_matches)

        if self.operator is ConditionOperator.Or:
            return any(inner_matches)

        if self.operator is ConditionOperator.Not:
            return not any(inner_matches)

        return False

    @pydantic.validator("conditions")
    def validate_conditions(
        cls, v: collections.abc.Sequence[typing.Union[Condition, "ConditionGroup"]]
    ):
        if len(v) == 0:
            raise ValueError(
                "At least one condition must be provided to a ConditionGroup, got 0!"
            )

        return v

    def __str__(self):
        return self.json()

    def __repr__(self):
        return self.json()


ConditionType = typing.Union[Condition, ConditionGroup]
