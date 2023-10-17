from typing import Dict
from typing import List

from src.domain import Rules


def get_output(
        rules: Rules,
        results: List[Dict[str, str | int]],
) -> str:
    result = ",".join([key for key in rules.important_keys.keys()]) + "\n"
    for object in results:
        result += ",".join([str(object[key]) for key in rules.important_keys.keys()]) + "\n"

    return result
