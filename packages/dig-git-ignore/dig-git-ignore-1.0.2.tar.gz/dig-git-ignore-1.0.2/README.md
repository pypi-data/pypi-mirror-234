# DIG git-ignore
[![Build Status](https://img.shields.io/appveyor/build/DIG-/python-git-ignore/master?logo=appveyor&logoColor=dddddd)](https://ci.appveyor.com/project/DIG-/python-git-ignore/branch/master)
[![Build tests](https://img.shields.io/appveyor/tests/DIG-/python-git-ignore/master?logo=appveyor&logoColor=dddddd)](https://ci.appveyor.com/project/DIG-/python-git-ignore/branch/master)
[![PyPI - License](https://img.shields.io/pypi/l/dig-git-ignore?color=blue)](https://creativecommons.org/licenses/by-nd/4.0/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dig-git-ignore)](https://pypi.org/project/dig-git-ignore/)
[![PyPI - Version](https://img.shields.io/pypi/v/dig-git-ignore)](https://pypi.org/project/dig-git-ignore/)

[![Windows - Supported](https://img.shields.io/badge/windows-supported-success?logo=windows&logoColor=dddddd)](#)
[![Linux - Supported](https://img.shields.io/badge/linux-supported-success?logo=linux&logoColor=dddddd)](#)
[![MacOS - Supported](https://img.shields.io/badge/macos-supported-success?logo=apple&logoColor=dddddd)](#)

Generate and/or Update gitignore files using [gitignore.io](https://gitignore.io/) templates

## Usage
```sh
python -m dig_git_ignore ACTION
```
or
```sh
git-ignore ACTION
```

`ACTION` must be one of:

### • `create`
```sh
git-ignore create template [template ...]
```
Create a new .gitignore only with selected templates. It will erease any existing rule.

### • `add`
```sh
git-ignore add template [template ...]
```
Update .gitignore, append selected templates to the existing ones. Only affect the rules inside the generated block.

### • `remove`
```sh
git-ignore remove template [template ...]
```
Update .gitignore, remove selected templates from the existing ones. Only affect the rules inside the generated block.

### • `update`
```sh
git-ignore update
```
Update .gitignore with most recent rules. Only affect the rules inside the generated block.

### • `list`
```sh
git-ignore list
```
List templates used in current .gitignore.

### • `list-all`
```sh
git-ignore list-all
```
List all supported templates.

### • `find`
```sh
git-ignore find term
```
Return supported templates who contains the searched term.

## Installation
### From PyPI (preferred):
``` sh
python -m pip install dig-git-ignore
```
### From github release:
``` sh
python -m pip install "https://github.com/DIG-/python-git-ignore/releases/download/1.0.2/dig_git_ignore-1.0.2-py3-none-any.whl"
```
or
``` sh
python -m pip install "https://github.com/DIG-/python-git-ignore/releases/download/1.0.2/dig_git_ignore.tar.gz"
```

### From github main branch:
``` sh
python -m pip install "git+https://github.com/DIG-/python-git-ignore.git@master#egg=dig_git_ignore"
```

## License
[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)

- You can use and redist freely.
- You can also modify, but only for yourself.
- You can use it as a part of your project, but without modifications in this project.