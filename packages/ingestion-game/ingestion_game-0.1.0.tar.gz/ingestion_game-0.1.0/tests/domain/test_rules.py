from typing import Any
from typing import Dict

import pytest
from pydantic import ValidationError

from src.domain import Rules


def test_rules_ok(
        new_rules_data: Dict,
) -> None:
    assert Rules(**Rules.Config.json_schema_extra.get("example"))


@pytest.mark.parametrize(
    "attr",
    [
        "important_keys",
        "hierarchy",
    ]
)
def test_rules_pop(
        new_rules_data: Dict,
        attr: str,
) -> None:
    new_rules_data.pop(attr)
    with pytest.raises(ValidationError) as exception:
        Rules(**new_rules_data)
    assert attr in str(exception.value)


@pytest.mark.parametrize(
    "attr",
    [
        "important_keys",
        "hierarchy",
    ]
)
def test_rules_none(
        new_rules_data: Dict,
        attr: str,
) -> None:
    new_rules_data[attr] = None
    with pytest.raises(ValidationError) as exception:
        Rules(**new_rules_data)
    assert attr in str(exception.value)


@pytest.mark.parametrize(
    "attr, value",
    [
        ("important_keys", "hola"),
        ("important_keys", 17),
        ("important_keys", dict(hola=17.0)),
        ("hierarchy", dict(hola=17)),
        ("hierarchy", []),
    ]
)
def test_rules_wrong(
        new_rules_data: Dict,
        attr: str,
        value: Any,
) -> None:
    new_rules_data[attr] = value
    with pytest.raises(ValidationError) as exception:
        Rules(**new_rules_data)
    assert attr in str(exception.value)
