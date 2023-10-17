from src.application import get_output
from src.domain import Rules


def test_get_output(
        new_rules: Rules,
) -> None:
    results = [
        {"food": "pizza", "id": 3, "name": "levy", "type": "A"},
        {"food": "fish", "id": 1, "more_noise": "bye", "name": "lima", "noise": "hello", "type": "B"},
        {"food": "sushi", "id": 10000, "name": "my_name", "type": "C"}
    ]
    expected = """id,name,food,type
3,levy,pizza,A
1,lima,fish,B
10000,my_name,sushi,C
"""
    assert get_output(rules=new_rules, results=results) == expected
