from __future__ import annotations

import ast
import math
import operator
from collections.abc import Iterable, MutableSequence, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any, TypeVar

TAX_MULTIPLIER = Decimal("1.2")

T = TypeVar("T")


def calculate_total(items: Iterable[dict[str, Any]]) -> Decimal:
    total = Decimal("0")
    for item in items:
        if "price" not in item:
            raise ValueError(f"Item has no 'price': {item!r}")
        price_raw = item["price"]
        if isinstance(price_raw, bool):
            raise ValueError(f"Invalid price value: {price_raw!r}")
        try:
            price = Decimal(str(price_raw))
        except InvalidOperation as exc:
            raise ValueError(f"Invalid price value: {price_raw!r}") from exc
        if not price.is_finite():
            raise ValueError(f"Invalid price value: {price_raw!r}")

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
    """Evaluate a plain arithmetic expression; raises ValueError on any failure."""
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval(tree)
    except (SyntaxError, ArithmeticError, TypeError, RecursionError, MemoryError) as exc:
        raise ValueError(f"Cannot evaluate expression: {expr!r}") from exc
    if not math.isfinite(result):
        raise ValueError(f"Expression result is not finite: {expr!r}")
    return result


def _eval(node: ast.AST) -> float:
    match node:
        case ast.Expression(body=body):
            return _eval(body)

        case ast.Constant(value=value) if isinstance(value, int | float) and not isinstance(value, bool):
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


def run_user_input(user_input: str) -> float:
    return safe_eval_arithmetic(user_input)


def get_user_by_id(cursor: Any, user_id: int, placeholder: str = "%s") -> Any:
    # placeholder must be the driver's paramstyle (%s, ?, :1, ...) and never user input
    cursor.execute(f"SELECT * FROM users WHERE id = {placeholder}", (user_id,))
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