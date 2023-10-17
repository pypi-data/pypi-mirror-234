from typing import Dict
from typing import List

from src.domain import Rules


def logic_ingestion(
        lines: List[str],
        rules: Rules,
) -> List[Dict[str, str | int]]:
    result = []
    current_position_hierarchy = 0
    for line in lines:
        object = dict((a.strip(), b.strip()) for a, b in (element.split('=') for element in line.split(',')))

        if not object.get("type") or not object["type"] in rules.hierarchy[current_position_hierarchy:]:
            continue

        try:
            object["id"] = int(object["id"])
        except:  # noqa: E722
            continue

        if all([object.get(key) and isinstance(object[key], value) for key, value in rules.important_keys.items()]):
            result.append(object)
        current_position_hierarchy = rules.hierarchy.index(object["type"])

    return result
