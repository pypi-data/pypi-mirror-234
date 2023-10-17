import click

from src.application import get_output
from src.application import logic_ingestion
from src.application import read_file
from src.application import read_hierarchy
from src.application import read_important_keys
from src.domain import Rules


@click.command()
@click.argument("important_keys")
@click.argument("hierarchy")
@click.argument("path")
def main(
        important_keys: str,
        hierarchy: str,
        path: str,
):
    """
    The ingestion game.

    You need to add some required arguments, the rules: important keys and hierarchy, and the path with the input file

    Arguments:

        - IMPORTANT_KEYS: [required] important keys, separate by commas without spaces

            example: id:int,name:str,food:str,type:str

        - HIERARCHY: [required] hierarchy, separate by commas without spaces

            example: A,B,C

        - PATH: [required] path of the input file

            example: /files/input.txt

    Example:

    python main.py id:int,name:str,type:str A,B,C /file/input.txt
    """
    rules = Rules(
        important_keys=read_important_keys(important_keys=important_keys),
        hierarchy=read_hierarchy(hierarchy=hierarchy),
    )

    lines = read_file(path=path)

    ingestion = logic_ingestion(lines=lines, rules=rules)

    print(get_output(rules=rules, results=ingestion), end="")


if __name__ == '__main__':
    main()
