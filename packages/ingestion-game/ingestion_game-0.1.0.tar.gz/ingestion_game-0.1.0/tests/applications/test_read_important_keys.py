from src.application import read_important_keys


def test_read_important_keys(
        new_important_keys: str,
) -> None:
    expected = dict(
        id=int,
        name=str,
        food=str,
        type=str,
    )
    assert read_important_keys(new_important_keys) == expected
