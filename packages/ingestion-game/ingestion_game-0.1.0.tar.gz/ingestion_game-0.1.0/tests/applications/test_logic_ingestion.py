from src.application import logic_ingestion
from src.domain import Rules


def test_logic_ingestion(
        new_rules: Rules,
) -> None:
    lines = [
        "name=levy,type=A,id=3,food=pizza",
        "type=B,name=lima,noise=hello,more_noise=bye,id=?,food=fish",
        "type=B,name=lima,noise=hello,more_noise=bye,id=1,food=fish",
        "name=name,noise=hello,more_noise=bye,id=1,food=vegetables,type=A",
        "type=C,name=my_name,food=sushi,id=10000",
        "name=lemon,type=A,random_key=random_value,food=lemonade,id=10",
        "name=guido,noisy=noise,food=snakes,id=3",
    ]
    expected = [
        {"food": "pizza", "id": 3, "name": "levy", "type": "A"},
        {"food": "fish", "id": 1, "more_noise": "bye", "name": "lima", "noise": "hello", "type": "B"},
        {"food": "sushi", "id": 10000, "name": "my_name", "type": "C"}
    ]
    assert logic_ingestion(lines=lines, rules=new_rules) == expected
