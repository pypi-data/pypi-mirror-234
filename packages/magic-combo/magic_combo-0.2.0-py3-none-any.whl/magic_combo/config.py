from pathlib import Path

from invoke.context import Context

from .scripts.bump_version import read_version_file


class ConfigWrapper:

    @staticmethod
    def godot_version(c: Context) -> str:
        if c['godot']['version_file'] is not None:
            return read_version_file(Path(c['godot']['version_file']))
        return str(c['godot']['version'])

    @staticmethod
    def godot_release(c: Context) -> str:
        return str(c['godot']['release'])

    @staticmethod
    def godot_subdir(c: Context) -> str:
        return str(c['godot']['subdir'])

    @staticmethod
    def godot_platform(c: Context) -> str:
        return str(c['godot']['platform'])

    @staticmethod
    def godot_filename(c: Context) -> str:
        return (
            f"Godot_v{ConfigWrapper.godot_version(c)}"
            f"-{ConfigWrapper.godot_release(c)}_{ConfigWrapper.godot_platform(c)}"
        )

    @staticmethod
    def godot_template(c: Context) -> str:
        return (
            f"Godot_v{ConfigWrapper.godot_version(c)}"
            f"-{ConfigWrapper.godot_release(c)}_export_templates.tpz"
        )

    @staticmethod
    def game_name(c: Context) -> str:
        return str(c['game']['name'])

    @staticmethod
    def game_version(c: Context) -> str:
        if c['game']['version_file'] is not None:
            return read_version_file(Path(c['game']['version_file']))
        return str(c['game']['version'])
