import sys

from invoke.collection import Collection
from invoke.config import Config
from invoke.program import Program

from .playbooks import playbook_ns
from .scripts import script_ns
from .tasks import task_ns


class ComboConfig(Config):
    prefix = 'combo'


def main() -> None:
    ns = Collection(playbook_ns, task_ns, script_ns)
    ns.configure({
        'godot': {
            'version': '4.1.1',
            'version_file': None,
            'release': 'stable',
            'subdir': '',
            'platform': 'linux.x86_64',
        },
        'game': {
            # 'name': None,
            'version': '0.1.0',
            'version_file': None,
        },
    })

    program = Program(version='0.2.0', namespace=ns, config_class=ComboConfig)
    program.run()
    sys.exit(1)


main()
