from pathlib import Path
from typing import Any, Iterable

from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from .config import ConfigWrapper

GODOT_URL = "https://downloads.tuxfamily.org/godotengine"

COMBO_PATH = Path(".combo")

COMBO_CACHE_PATH = COMBO_PATH.joinpath("cache")
COMBO_BIN_PATH = COMBO_PATH.joinpath("bin")
COMBO_BUILD_PATH = COMBO_PATH.joinpath("build")

String = str | Path


def cmd(c: Context, command: String, *arguments: String) -> Any:
    builder = CmdBuilder(c)
    if command == "godot":
        builder = builder.godot()
    else:
        builder = builder.cmd(command)
    builder = builder.args(*arguments)
    return builder.run()


class CmdBuilder:

    def __init__(self, c: Context) -> None:
        self.c = c
        self._args: Iterable[str] = []
        self._cmd: str = ''

    def run(self) -> Any:
        return self.c.run(' '.join([self._cmd, *self._args]))

    def cmd(self, cmd: String) -> 'CmdBuilder':
        self._cmd = str(cmd)
        return self

    def godot(self) -> 'CmdBuilder':
        return self.cmd(COMBO_BIN_PATH / ConfigWrapper.godot_filename(self.c))

    def args(self, *args: String) -> 'CmdBuilder':
        self._args = [str(arg) for arg in args]
        return self


@task()
def makedirs(c: Context) -> None:
    for dir_path in (COMBO_PATH, COMBO_CACHE_PATH, COMBO_BIN_PATH, COMBO_BUILD_PATH):
        cmd(c, "mkdir", "-p", dir_path)

    cmd(c, "touch", COMBO_PATH / ".gitignore")
    cmd(c, "echo", "'*'", ">>", COMBO_PATH / ".gitignore")
    cmd(c, "touch", COMBO_PATH / ".gdignore")


@task()
def install_godot(c: Context) -> None:
    cmd(
        c,
        "curl",
        "-X GET",
        f"'{GODOT_URL}/{ConfigWrapper.godot_version(c)}{ConfigWrapper.godot_subdir(c)}/{ConfigWrapper.godot_filename(c)}.zip'",
        "--output",
        COMBO_CACHE_PATH / f"{ConfigWrapper.godot_filename(c)}.zip",
    )
    cmd(
        c, "unzip", COMBO_CACHE_PATH / f"{ConfigWrapper.godot_filename(c)}.zip", "-d",
        COMBO_CACHE_PATH
    )
    cmd(
        c,
        "cp",
        COMBO_CACHE_PATH / ConfigWrapper.godot_filename(c),
        COMBO_BIN_PATH / ConfigWrapper.godot_filename(c),
    )


@task()
def install_templates(c: Context) -> None:
    cmd(
        c,
        "curl",
        "-X GET",
        "'{GODOT_URL}/{ConfigWrapper.godot_version(c)}{ConfigWrapper.godot_subdir(c)}/{ConfigWrapper.godot_template(c)}'",
        "--output",
        COMBO_CACHE_PATH / ConfigWrapper.godot_template(c),
    )
    cmd(
        c, "unzip", COMBO_CACHE_PATH / ConfigWrapper.godot_template(c), "-d",
        COMBO_CACHE_PATH
    )
    cmd(
        c, "mkdir", "--parents",
        f"~/.local/share/godot/export_templates/{ConfigWrapper.godot_version(c)}.{ConfigWrapper.godot_release(c)}"
    )
    cmd(
        c, "cp", COMBO_CACHE_PATH / "templates/*",
        f"~/.local/share/godot/export_templates/{ConfigWrapper.godot_version(c)}.{ConfigWrapper.godot_release(c)}"
    )


@task(pre=[makedirs])
def install_addons(c: Context) -> None:
    cmd(
        c,
        "godot",
        "--headless",
        "--script",
        "plug.gd",
        "install",
        "||",
        "true",
    )


@task(pre=[makedirs])
def import_resources(c: Context) -> None:
    cmd(
        c,
        "godot",
        "--headless",
        "--export-pack",
        "null",
        "/dev/null",
    )


@task()
def export_release_linux(c: Context) -> None:
    export_dir = COMBO_BUILD_PATH / "linux"
    cmd(c, "mkdir", "--parents", export_dir)
    cmd(
        c,
        "godot",
        "--export-release 'Linux/X11'",
        "--headless",
        export_dir / f"{ConfigWrapper.game_name(c)}.x86_64",
    )
    zip_filename = "%s-linux-v%s.zip" % (
        ConfigWrapper.game_name(c), ConfigWrapper.game_version(c)
    )
    cmd(
        c,
        "cd",
        export_dir,
        "&&",
        "zip",
        zip_filename,
        "-r",
        ".",
        "&&",
        "cd",
        "-",
    )
    cmd(c, "mv", (export_dir / zip_filename), (COMBO_BUILD_PATH / zip_filename))


@task()
def export_release_windows(c: Context) -> None:
    export_dir = COMBO_BUILD_PATH / "windows"
    cmd(c, "mkdir", "--parents", export_dir)
    cmd(
        c, "godot", "--export-release 'Windows Desktop'"
        "--headless", export_dir / f"{ConfigWrapper.game_name(c)}.exe"
    )

    zip_filename = "%s-windows-v%s.zip" % (
        ConfigWrapper.game_name(c), ConfigWrapper.game_version(c)
    )
    cmd(
        c,
        "cd",
        export_dir,
        "&&",
        "zip",
        zip_filename,
        "-r",
        ".",
        "&&",
        "cd",
        "-",
    )
    cmd(c, "mv", export_dir / zip_filename, COMBO_BUILD_PATH / zip_filename)


@task()
def export_release_mac(c: Context) -> None:
    cmd(
        c, "godot", "--export-release 'macOS'"
        "--headless", (
            COMBO_BUILD_PATH /
            f"{ConfigWrapper.game_name(c)}-mac-v{ConfigWrapper.game_version(c)}.zip"
        )
    )


@task()
def editor(c: Context) -> None:
    cmd(c, "godot", "--editor")


@task()
def godot(c: Context) -> None:
    cmd(c, "godot")


@task()
def run_release(c: Context) -> None:
    cmd(c, COMBO_BUILD_PATH / "linux" / f"{ConfigWrapper.game_name(c)}.x86_64")


@task()
def clean_combo(c: Context) -> None:
    c.run("rm -rf .combo")


@task()
def clean_godot(c: Context) -> None:
    c.run("rm -rf .godot")


@task()
def clean_plug(c: Context) -> None:
    c.run("rm -rf .plugged")
    cmd(
        c,
        "find",
        "addons/",
        "-type d",
        "-not -name 'addons'",
        "-not -name 'gd-plug'",
        "-exec rm -rf {} \; || true",
    )


task_ns = Collection('task')
task_ns.add_task(clean_godot)
task_ns.add_task(clean_combo)
task_ns.add_task(clean_plug)
task_ns.add_task(godot)
task_ns.add_task(editor)
task_ns.add_task(export_release_linux)
task_ns.add_task(export_release_mac)
task_ns.add_task(export_release_windows)
task_ns.add_task(import_resources)
task_ns.add_task(install_addons)
task_ns.add_task(install_godot)
task_ns.add_task(install_templates)
task_ns.add_task(run_release)
task_ns.add_task(makedirs)
