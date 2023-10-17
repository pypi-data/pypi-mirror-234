# maplocal

[![PyPI - Version](https://img.shields.io/pypi/v/maplocal.svg)](https://pypi.org/project/maplocal)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/maplocal.svg)](https://pypi.org/project/maplocal)

-----

**Table of Contents**

- [maplocal](#maplocal)
  - [Installation](#installation)
  - [Use Case](#use-case)
    - [Examples](#examples)
  - [License](#license)

## Installation

```console
pip install maplocal
```

## Configuration

to configure `maplocal` the following env vars must be set:  
```
MAPLOCAL_OS_FROM: str = "linux"  #  TODO make enum
MAPLOCAL_OS_TO: str = "windows"  #  TODO make enum
MAPLOCAL_FROM: ty.Optional[pathlib.PurePath] = None  # the rootdir to be removed from path
MAPLOCAL_TO: ty.Optional[pathlib.PurePath] = None  # the rootdir to be added to path
MAPLOCAL_SCRIPT_PATH: ty.Optional[pathlib.Path] = None  # script with `openpath` and `runcmd` functions
```
in the `MAPLOCAL_SCRIPT_PATH` dir is a python file that must contain functions named `openpath` and `runcmd`. 

## Use Case

You manage a cloud-hosted service that is attached to file-server storing user data.
Users have access to your service, but also separately have access to file-directory through their computers.
The way that the file-server is mounted is different for the user and for the cloud hosted service.
This provides a way to map the root directory of the users machine and the file server.
It also provides a **hacky, potentially unsafe**[1][1] hook that allows a locally saved script file to
inject the functions `openfile` and `runcmd` that are intended to provide ways for the server
to open a file from the users machine and run a shell command on the users machine.

[1]: a script file placed in a known directory allows users to inject code into the program.
Not inherently unsafe but could be used as a way to inject malicious code by bad-actors.

### Examples

1. running WSL, Ubuntu. Opening files saved in the Ubuntu file system with Windows Programs.
2. running WSL, Ubuntu. Opening files on the windows files system (mounted C:\drive).

## License

`maplocal` is distributed under the terms of the [0BSD](https://spdx.org/licenses/0BSD.html) license.
