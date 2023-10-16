<div align="center">

# `🌟 magic_combo`

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-0a7bbc?logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-green?logo=open-source-initiative&logoColor=white)
[![standard-readme compliant](https://img.shields.io/badge/readme-standard-brightgreen.svg?logo=readme&logoColor=white)](https://github.com/RichardLitt/standard-readme)
<!--
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
-->

![PyPI - Package Version](https://img.shields.io/pypi/v/magic_combo?logo=pypi&logoColor=white)

[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![format - yapf](https://img.shields.io/badge/format-yapf-000000.svg)](https://github.com/google/yapf)
[![types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy)

A collection of Python utilities for seamless
 management of my personal games project in
 Godot Engine.

</div>

## About

This project is used to **develop, contribute**
 **and manage** my game projects, but it's also
 completely **optional**.

### Develop, contribute and manage

The package is split into 3 parts:
- **tasks**, that is a wrapper around the Godot
 binary. It's allow to automatically download
 the version of Godot used by your game...
- **playbooks**, that is a suite of tasks. It's
 useful to build your game from scratch, like
 in CI.
- **scripts**, that is more random stuff, like
 generate credits from a dep5 file, or bump
 your game version in the Godot export preset
 file.

And the second goal of this package is to pin
 dependencies use in my `.pre-commit-config.yml`
 files.

### Optional

I attach importance to being able  to do
 things without extra tools, so my personal
 game projects used this package
 to simplify some tasks, but if you know
 how to use Godot you can do anything
 with Godot.

This project was born to localize
 my scripts in one place rather than having
 them duplicated in each project.

## Install

This project uses [python](https://www.python.org/)
 and [pip](https://pip.pypa.io/en/stable/).
 Go check them out if you don't have them
 locally installed.

```
$ pip install magic_combo
```

## Usage

To list all sucommands, run:
```
$ magic_combo --list
Subcommands:

  playbook.build
  playbook.ci-build
  playbook.clean
  playbook.export-release-all
  playbook.run
  script.bump-version           Updates the game
                                version for export.
  script.generate-credits       Generate a
                                CREDITS.md file.
  task.clean-combo
  task.clean-godot
  task.clean-plug
  task.editor
  task.export-release-linux
  task.export-release-mac
  task.export-release-windows
  task.godot
  task.import-resources
  task.install-addons
  task.install-godot
  task.install-templates
  task.makedirs
  task.run-release
```

And to run any subcommands, run:

```
$ magic_combo <sucommand>
```
