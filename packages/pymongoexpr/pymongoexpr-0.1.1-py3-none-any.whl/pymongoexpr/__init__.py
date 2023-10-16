""":mod:`pymongoexpr` --- MongoDB query expression parser."""


from typing import Any, Dict, Union

from typing_extensions import TypeAlias

from ._version import __version__ as __version__


class OperatorCondition:
    """Represents the OperatorCondition filter of MongoDB query expression."""

    operators = ["$eq", "$gt", "$lt", "$ne", "$gte", "$lte"]

    def __init__(self, field, operator, value) -> None:
        """Construct the Operator condition with given arguments.

        Args:
            field (str): The field name.
            operator (str): The operator.
                One of "$eq", "$gt", "$lt", "$ne", "$gte", "$lte".
            value (object): The value to compare.

        Raises:
            ValueError: If the operator is invalid.
        """
        if operator not in self.operators:
            raise ValueError(f"Invalid operator: {operator}")
        self.field = field
        self.operator = operator
        self.value = value

    def evaluate(self, record: Dict[str, Any]) -> bool:
        """Return the predicate for applying the Operator condition."""
        if self.operator == "$eq":
            return record[self.field] == self.value
        elif self.operator == "$gt":
            return record[self.field] > self.value
        elif self.operator == "$lt":
            return record[self.field] < self.value
        elif self.operator == "$ne":
            return record[self.field] != self.value
        elif self.operator == "$gte":
            return record[self.field] >= self.value
        elif self.operator == "$lte":
            return record[self.field] <= self.value
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Operator condition as a dict."""
        return {self.field: {self.operator: self.value}}


class LogicalCondition:
    """Represents the LogicalCondition filter of MongoDB query expression."""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Logical condition as a dict."""
        raise NotImplementedError("Subclasses must implement this method")


class And(LogicalCondition):
    """Represents the And LogicalCondition filter of MongoDB query expression."""

    def __init__(self, conditions) -> None:
        """Construct the And condition with given arguments."""
        self.conditions = conditions

    def evaluate(self, record) -> bool:
        """Return the predicate for applying the And condition."""
        return all(condition.evaluate(record) for condition in self.conditions)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the And condition as a dict."""
        return {"$and": [condition.to_dict() for condition in self.conditions]}


class Or(LogicalCondition):
    """Represents the Or LogicalCondition filter of MongoDB query expression."""

    def __init__(self, conditions) -> None:
        """Construct the Or condition with given arguments."""
        self.conditions = conditions

    def evaluate(self, record) -> bool:
        """Return the predicate for applying the filter Or condition."""
        return any(condition.evaluate(record) for condition in self.conditions)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Or condition as a dict."""
        return {"$or": [condition.to_dict() for condition in self.conditions]}


class Nor(LogicalCondition):
    """Represents the Nor LogicalCondition filter of MongoDB query expression."""

    def __init__(self, conditions) -> None:
        """Construct the Nor condition with given arguments."""
        self.conditions = conditions

    def evaluate(self, record) -> bool:
        """Return the predicate for applying the filter Nor condition."""
        return not any(condition.evaluate(record) for condition in self.conditions)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Nor condition as a dict."""
        return {"$nor": [condition.to_dict() for condition in self.conditions]}


Condition: TypeAlias = Union[Or, And, Nor, OperatorCondition]


class Filter:
    """Represents the MongoDB query expression."""

    def __init__(self, filter_expr):
        """Construct a Filter with given arguments.

        Args:
            filter_expr (dict): The MongoDB query expression as dict.
        """
        self.parsed_expr = self._parse(filter_expr)

    @staticmethod
    def from_dict(filter_dict) -> "Filter":
        """Construct a Filter from a dict."""
        return Filter(filter_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Filter as a dict."""
        return self.parsed_expr.to_dict()

    def _parse(self, condition) -> Condition:
        if "$and" in condition:
            return And(
                [self._parse(sub_condition) for sub_condition in condition["$and"]]
            )
        elif "$or" in condition:
            return Or(
                [self._parse(sub_condition) for sub_condition in condition["$or"]]
            )
        elif "$nor" in condition:
            return Nor(
                [self._parse(sub_condition) for sub_condition in condition["$nor"]]
            )
        for field, value in condition.items():
            if isinstance(value, dict):
                for op, op_value in value.items():
                    return OperatorCondition(field, op, op_value)
            else:
                return OperatorCondition(field, "$eq", value)
        raise ValueError(f"Invalid condition: {condition}")

    def evaluate(self, record) -> bool:
        """Return the predicate for applying the filter condition."""
        return self.parsed_expr.evaluate(record)
