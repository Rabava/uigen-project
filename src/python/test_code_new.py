from __future__ import annotations

import ast
import operator
import os
from collections.abc import Iterable, MutableSequence, Sequence
from typing import Any, TypeVar

DB_PASSWORD = os.environ["DB_PASSWORD"]
API_KEY = os.environ["API_KEY"]

TAX_MULTIPLIER: float = 1.2

T = TypeVar("T")


def calculate_total(items: Iterable[dict[str, Any]]) -> float:
    total = 0.0
    for item in items:
        price_raw = item.get("price", 0)
        try:
            price = float(price_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid price value: {price_raw!r}") from exc

        total += price * TAX_MULTIPLIER
    return total


def get_first_element(arr: Sequence[T]) -> T | None:
    return arr[0] if arr else None


# Безопасная замена eval: разрешаем только простую арифметику (без вызовов, атрибутов и т.п.)
_ALLOWED_BINOPS: dict[type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARYOPS: dict[type[ast.unaryop], Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval_arithmetic(expr: str) -> float:
    tree = ast.parse(expr, mode="eval")

    def _eval(node: ast.AST) -> float:
        match node:
            case ast.Expression(body=body):
                return _eval(body)

            case ast.Constant(value=value) if isinstance(value, int | float):
                return float(value)

            case ast.BinOp(left=left, op=op, right=right):
                op_func = _ALLOWED_BINOPS.get(type(op))
                if op_func is None:
                    raise ValueError(f"Operator not allowed: {type(op).__name__}")
                return float(op_func(_eval(left), _eval(right)))

            case ast.UnaryOp(op=op, operand=operand):
                op_func = _ALLOWED_UNARYOPS.get(type(op))
                if op_func is None:
                    raise ValueError(f"Unary operator not allowed: {type(op).__name__}")
                return float(op_func(_eval(operand)))

            case _:
                raise ValueError(f"Expression not allowed: {type(node).__name__}")

    return _eval(tree)


def run_user_input(user_input: str) -> float:
    # Если цель — выполнить произвольный код, это нельзя делать вообще.
    # Здесь допускаем только арифметические выражения.
    return safe_eval_arithmetic(user_input)


def get_user_by_id(cursor: Any, user_id: int) -> Any:
    # Пример для DB-API 2.0: placeholder зависит от драйвера (%s, ?, :1, ...)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()


def add_to_list(item: T, my_list: MutableSequence[T] | None = None) -> MutableSequence[T]:
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list


def process_data(data: Iterable[int]) -> list[int]:
    result: list[int] = []
    for item in data:
        if item <= 10:
            continue
        if item % 2 != 0:
            continue
        if item == 14:
            continue
        result.append(item)
    return result