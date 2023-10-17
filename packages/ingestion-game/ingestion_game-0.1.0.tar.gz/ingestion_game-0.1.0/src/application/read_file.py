from typing import List


def read_file(
        path: str,
) -> List[str]:
    """
    Read external file with path.
    Delete the final \n

    :param str path: path
    :return: text
    """
    with open(path, "r") as file:
        lines = file.readlines()
    return [line[:-1] for line in lines]
