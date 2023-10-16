import enum
import typing

import pydantic

from .conditions import (
    Comparator,
    Condition,
    ConditionGroup,
    ConditionOperator,
)


class SortDirection(str, enum.Enum):
    """The direction to sort the results of a query."""

    Ascending = "ASC"
    Descending = "DESC"


class QuerySpecification(pydantic.BaseModel):
    """
    Model for specifying a query to the Roboto Platform.

    Examples:
        Specify a query with a single condition:
            >>> from roboto import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.Condition(
            ...         field="name",
            ...         comparator=query.Comparator.Equals,
            ...         value="Roboto"
            ...     )
            ... )

        Specify a query with multiple conditions:
            >>> from roboto import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.ConditionGroup(
            ...         operator=query.ConditionOperator.And,
            ...         conditions=[
            ...             query.Condition(
            ...                 field="name",
            ...                 comparator=query.Comparator.Equals,
            ...                 value="Roboto"
            ...             ),
            ...             query.Condition(
            ...                 field="age",
            ...                 comparator=query.Comparator.GreaterThan,
            ...                 value=18
            ...             )
            ...         ]
            ...     )
            ... )

        Arbitrarily nest condition groups:
            >>> from roboto import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.ConditionGroup(
            ...         operator=query.ConditionOperator.And,
            ...         conditions=[
            ...             query.Condition(
            ...                 field="name",
            ...                 comparator=query.Comparator.Equals,
            ...                 value="Roboto"
            ...             ),
            ...             query.ConditionGroup(
            ...                 operator=query.ConditionOperator.Or,
            ...                 conditions=[
            ...                     query.Condition(
            ...                         field="age",
            ...                         comparator=query.Comparator.GreaterThan,
            ...                         value=18
            ...                     ),
            ...                     query.Condition(
            ...                         field="age",
            ...                         comparator=query.Comparator.LessThan,
            ...                         value=30
            ...                     )
            ...                 ]
            ...             )
            ...         ]
            ...     )
            ... )
    """

    condition: typing.Optional[typing.Union[Condition, ConditionGroup]] = None
    limit: int = 1000
    after: typing.Optional[str] = None  # An encoded PaginationToken
    sort_by: typing.Optional[str] = None
    sort_direction: typing.Optional[SortDirection] = None

    class Config:
        extra = "forbid"

    @classmethod
    def protected_from_oldstyle_request(
        cls, filters: dict, page_token: typing.Optional[str] = None
    ) -> "QuerySpecification":
        """
        Convert deprecated query format to new format.

        Not for public use.

        :meta private:
        """
        conditions: list[typing.Union[Condition, ConditionGroup]] = []

        def _iterconditions(field: str, value: typing.Any):
            if isinstance(value, list):
                conditions.append(
                    ConditionGroup(
                        operator=ConditionOperator.Or,
                        conditions=[
                            Condition(
                                field=field, comparator=Comparator.Equals, value=v
                            )
                            for v in value
                        ],
                    )
                )

            elif isinstance(value, dict):
                for k, v in value.items():
                    _iterconditions(f"{field}.{k}", v)

            else:
                conditions.append(
                    Condition(field=field, comparator=Comparator.Equals, value=value)
                )

        for field, value in filters.items():
            _iterconditions(field, value)

        condition: typing.Optional[ConditionGroup] = None
        if len(conditions) > 0:
            condition = ConditionGroup(
                operator=ConditionOperator.And, conditions=conditions
            )

        return cls(
            condition=condition,
            after=page_token,
        )

    def fields(self) -> set[str]:
        """Return a set of all fields referenced in the query."""
        fields = set()

        def _iterconditions(
            condition: typing.Optional[typing.Union[Condition, ConditionGroup]]
        ):
            if condition is None:
                return

            if isinstance(condition, Condition):
                fields.add(condition.field)
            else:
                for cond in condition.conditions:
                    _iterconditions(cond)

        _iterconditions(self.condition)
        return fields
