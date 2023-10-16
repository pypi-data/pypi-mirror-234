import os
from pathlib import Path
from string import Template
from typing import Dict, List, Optional


def parse_dep5_file(source: Path) -> Dict[str, List[Dict[str, str]]]:
    deps: Dict[str, List[Dict[str, str]]] = {}
    section: Optional[str] = None

    with open(source, "r") as file:
        for line in file:
            if line.startswith('# '):
                section = line[len("# "):-1].lower()

            if section is None:
                continue

            if line.startswith("Files: "):
                if section not in deps:
                    deps[section] = []

                deps[section].append({"files": line[len("Files: "):-1]})

            elif line.startswith("Copyright: "):
                if section not in deps:
                    deps[section] = []

                date_author = line[len("Copyright: "):-1].split(" ")
                date_author.pop(0)
                deps[section][-1]["author"] = " ".join(date_author)

            elif line.startswith("License: "):
                if section not in deps:
                    deps[section] = []

                deps[section][-1]["license"] = line[len("License: "):-1]

            elif line.startswith("Source: "):
                if section not in deps:
                    deps[section] = []

                deps[section][-1]["source"] = line[len("Source: "):-1]

    return deps


def generate_credits_file(deps: Dict[str, List[Dict[str, str]]], output: Path) -> None:
    if deps:
        template = Template((
            '- "[$files]($source)" by **$author** licensed'
            ' under [$license](https://spdx.org/licenses/$license.html)\n'
        ))

        with open(output, "w+") as file:
            file.writelines("# Credits\n\n")

            for key, value in deps.items():
                file.writelines(f"## {key.title()}\n")
                for dep in value:
                    file.writelines(template.substitute(**dep))
    else:
        if os.path.exists(output):
            os.remove(output)
