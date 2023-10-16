from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from .tasks import (
    clean_combo,
    clean_godot,
    clean_plug,
    export_release_linux,
    export_release_mac,
    export_release_windows,
    import_resources,
    install_addons,
    install_godot,
    install_templates,
    run_release,
)


@task(pre=[clean_combo, clean_godot, clean_plug])
def clean(c: Context) -> None:
    pass


@task(
    pre=[
        clean_godot, clean_plug, install_addons, import_resources, export_release_linux
    ]
)
def build(c: Context) -> None:
    pass


@task(pre=[build, run_release])
def run(c: Context) -> None:
    pass


@task(pre=[export_release_linux, export_release_mac, export_release_windows])
def export_release_all(c: Context) -> None:
    pass


@task(
    pre=[
        clean, install_godot, install_templates, install_addons, import_resources,
        export_release_all
    ]
)
def ci_build(c: Context) -> None:
    pass


playbook_ns = Collection('playbook')
playbook_ns.add_task(clean)
playbook_ns.add_task(build)
playbook_ns.add_task(run)
playbook_ns.add_task(export_release_all)
playbook_ns.add_task(ci_build)
