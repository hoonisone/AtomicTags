from __future__ import annotations

TAG_COLUMNS = (
    "is_stylized",
    "is_size_inconsistent",
    "is_incomplete",
    "is_low_visibility",
    "is_noisy_background",
    "is_distracted",
    "is_perspective_distorted",
    "is_multiline",
    "is_nonstraight",
    "is_rotated",
)


def is_true(value: object) -> bool:
    return str(value or "").strip().lower() in {"true", "1", "yes", "t"}


def is_false(value: object) -> bool:
    return str(value or "").strip().lower() in {"false", "0", "no", "f"}


def value_matches(actual: object, expected: object) -> bool:
    if isinstance(expected, bool):
        if str(actual or "").strip() == "":
            return False
        return is_true(actual) if expected else is_false(actual)
    return str(actual or "").strip() == str(expected).strip()


def row_matches(row: dict[str, str], filters: dict[str, object] | None) -> bool:
    if not filters:
        return True
    return all(value_matches(row.get(column), expected) for column, expected in filters.items())


def tag_name(column: str) -> str:
    return column.removeprefix("is_")
