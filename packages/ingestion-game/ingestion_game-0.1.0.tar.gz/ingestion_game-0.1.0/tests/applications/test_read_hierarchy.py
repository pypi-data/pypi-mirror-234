from src.application import read_hierarchy


def test_read_hierarchy(
        new_hierarchy: str,
) -> None:
    assert read_hierarchy(new_hierarchy) == ["A", "B", "C"]
