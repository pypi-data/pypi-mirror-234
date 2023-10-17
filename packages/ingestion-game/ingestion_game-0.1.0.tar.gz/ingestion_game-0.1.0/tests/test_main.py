from click.testing import CliRunner

from src.main import main


def test_main(
        new_important_keys: str,
        new_hierarchy: str,
        path_input_txt: str,
) -> None:
    runner = CliRunner()
    result = runner.invoke(main, args=[new_important_keys, new_hierarchy, path_input_txt])
    assert result.exit_code == 0
    expected = """id,name,food,type
3,levy,pizza,A
1,lima,fish,B
10000,my_name,sushi,C
"""
    assert result.output == expected
