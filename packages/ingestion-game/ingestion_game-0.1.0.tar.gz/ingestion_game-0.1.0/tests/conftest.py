import os
from copy import deepcopy
from typing import Dict

import pytest

from src.application import read_hierarchy
from src.application import read_important_keys
from src.domain import Rules


@pytest.fixture
def new_rules_data() -> Dict:
    return deepcopy(Rules.Config.json_schema_extra.get("example"))


@pytest.fixture
def new_important_keys() -> str:
    return "id:int,name:str,food:str,type:str"


@pytest.fixture
def new_hierarchy() -> str:
    return "A,B,C"


@pytest.fixture
def new_rules(
        new_important_keys: str,
        new_hierarchy: str,
) -> Rules:
    return Rules(
        important_keys=read_important_keys(important_keys=new_important_keys),
        hierarchy=read_hierarchy(hierarchy=new_hierarchy),
    )


@pytest.fixture
def path_input_txt() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
