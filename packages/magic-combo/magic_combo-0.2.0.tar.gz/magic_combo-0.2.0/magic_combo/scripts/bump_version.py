import re
from datetime import datetime
from pathlib import Path

from packaging import version


def get_today() -> datetime:
    return datetime.today()


def sed(
    pattern: str | re.Pattern[str],
    replace: str,
    source: Path,
    output: Path | None = None
) -> None:
    """
    Read a source file, and for each line, replaces the pattern inplace.

    :param pattern: pattern to match
    :param replace: replacement str
    :param source: input filename
    :param output: output filename, if it's None replace the source in-place
    """
    lines = []
    with open(source, 'r') as fin:

        for line in fin:
            out = re.sub(pattern, replace, line)
            lines.append(out)

    if output is None:
        output = source

    with open(output, 'w') as fout:

        for line in lines:
            fout.write(line)


def read_version_file(source: Path) -> str:
    """
    Read a source file, and return it's first line.

    :param source: input filename
    :raises ValueError: raises an exception when the source is empty
    """
    with open(source, 'r') as fin:
        for line in fin:
            return line

    raise ValueError(f'{source} is an empty file')


def replace_version(
    game_version: version.Version,
    input_cfg_file: Path,
    output_cfg_file: Path | None = None
) -> None:
    today = get_today().strftime('%Y%m%d')

    if output_cfg_file is None:
        output_cfg_file = input_cfg_file

    short_version = f"{game_version.major}.{game_version.minor}"
    release_version = f"{short_version}.{game_version.micro}"

    sed(
        'application/file_version=.*$',
        f'application/file_version="{release_version}.{today}"', input_cfg_file,
        output_cfg_file
    )
    sed(
        'application/product_version=.*$',
        f'application/product_version="{release_version}.{today}"', output_cfg_file
    )
    sed(
        'application/version=.*$', f'application/version="{release_version}"',
        output_cfg_file
    )
    sed(
        'application/short_version=.*$', f'application/short_version="{short_version}"',
        output_cfg_file
    )
