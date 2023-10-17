from typing import Dict


def read_important_keys(
        important_keys: str,
) -> Dict[str, type(str) | type(int)]:
    """
    Convert the string with important keys to domain
    Example: id:int,name:str,food:str,type:str

    :param str important_keys: important keys with types
    :return: object with important keys
    """
    pars = important_keys.split(",")
    result = {}
    for par in pars:
        key, type_name = par.split(":")
        result[key] = int if type_name == "int" else str

    return result
