from typing import List


def read_hierarchy(
        hierarchy: str,
) -> List[str]:
    """
    Convert the string with hierarchy to domain
    Example: A, B, C

    :param str hierarchy: hierarchy
    :return: list with hierarchy
    """
    return hierarchy.split(",")
