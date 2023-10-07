import click

from chinaski.henry import core


@click.command()
@click.argument("path_to_file_or_dir")
def cli(
    path_to_file_or_dir: str,
) -> None:
    """Detect email addresses in files.

    PATH_TO_FILE_OR_DIR: Path to single file or directory to scan.
    """

    for result in core(path_to_file_or_dir=path_to_file_or_dir):
        print(result)
