
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-git/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my Scrangourou friend](./scrippy-git.png "Scrippy, my Scrangourou friend")

# `scrippy_git`

Git client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python Modules

#### List of Required Modules

The modules listed below will be automatically installed.

- GitPython

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-git.git
cd scrippy-git
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-git
```

### Usage

The `scrippy_git.git` module provides the `Repo` object for easy manipulation of a _Git_ repository.

```python
import os
from scrippy_git import git

username = "git"
host = "gitlab.monty.py"
port = 2242
reponame = "luiggi.vercotti/monty_python.git"
branch = "master"

repo = git.Repo(username, host, port, reponame)
local_path = os.path.join(workspace_path, "monty_python")
repo.clone(branch=branch, path=local_path)

test_fname = os.path.join(local_path, "dead_parrot.txt")
with open(test_fname, mode="w") as test_file:
  test_file.write("Nobody expects the Spanish inquisition !")
  commit_message = "Inquisition shall not be expected"
  repo.commit_push(commit_message)
```
