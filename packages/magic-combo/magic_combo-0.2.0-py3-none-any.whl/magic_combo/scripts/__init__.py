from pathlib import Path
from typing import Optional

import packaging
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from .bump_version import read_version_file, replace_version
from .generate_credits import generate_credits_file, parse_dep5_file


@task(
    name="bump_version",
    help={
        "version_file": "A path to a version file. (default: .version)",
        "cfg_file": "A path to a presets file. (default: export_presets.cfg)",
        "version": "Override the version-file, if it's pass. (default: None)",
    },
    optional=['version', 'version_file', 'cfg_file']
)
def bump_version_(
    c: Context,
    version: Optional[str] = None,
    version_file: Path = Path(".version"),
    cfg_file: Path = Path("export_presets.cfg")
) -> None:
    """
    Updates the game version for export.
    """
    game_version = packaging.version.parse(
        read_version_file(version_file) if version is None else version
    )

    replace_version(game_version, cfg_file)


@task(
    name="generate_credits",
    help={
        "dep5_file": "A path to a dep5 file. (default: .reuse/dep5)",
        "output": "A path for the output credit file. (default: CREDITS.md)",
    },
    optional=['dep5_file', 'output']
)
def generate_credits_(
    c: Context,
    dep5_file: Path = Path(".reuse/dep5"),
    output: Path = Path("CREDITS.md")
) -> None:
    """
    Generate a CREDITS.md file.
    """
    deps = parse_dep5_file(dep5_file)
    generate_credits_file(deps, output)


script_ns = Collection('script')
script_ns.add_task(bump_version_)
script_ns.add_task(generate_credits_)
