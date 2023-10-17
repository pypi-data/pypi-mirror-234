import pathlib
import importlib.util
import sys
import typing as ty
import os
import logging
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


MAPOS = {"windows": pathlib.PureWindowsPath, "linux": pathlib.PurePosixPath}
PLATFORM = sys.platform

def load(path, fn_name: str):
    if isinstance(path, str):
        path = pathlib.Path(path)
    if not path.is_file():
        raise ValueError(f"{str(path)} must be a file")
    try:
        spec = importlib.util.spec_from_file_location("maplocal", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        fn = getattr(foo, fn_name)
    except:
        raise ValueError(f"could not find `{fn_name}` from {str(path)}")

    return fn

def get_maplocal_dir():
    if PLATFORM == "linux":
        return pathlib.Path(os.environ['HOME']) / '.maplocal'
    elif PLATFORM == "windows":
        return pathlib.Path(os.environ['USERPROFILE']) / '.maplocal'
    else:
        raise ValueError('platform not windows or linux')

def get_maplocal_path():
    return get_maplocal_dir() / 'maplocal.py'

class MapLocalEnv(BaseSettings):
    MAPLOCAL_OS_FROM: str = "linux"  #  TODO make enum
    MAPLOCAL_OS_TO: str = "windows"
    MAPLOCAL_FROM: ty.Optional[pathlib.PurePath] = Field(None)
    MAPLOCAL_TO: ty.Optional[pathlib.PurePath] = Field(None)
    MAPLOCAL_SCRIPT_PATH: ty.Optional[pathlib.Path] = Field(None)
    openpath: ty.Optional[ty.Callable[[pathlib.Path], bool]] = Field(None)
    runcmd: ty.Optional[ty.Callable[[str], None]] = Field(None)

    @model_validator(mode="after")
    @classmethod
    def _set_values(cls, data: ty.Any):
        if data.MAPLOCAL_FROM is None:
            data.MAPLOCAL_FROM = MAPOS[data.MAPLOCAL_OS_FROM]("/home")
        else:
            data.MAPLOCAL_FROM = MAPOS[data.MAPLOCAL_OS_FROM](data.MAPLOCAL_FROM)
        
        if data.MAPLOCAL_TO is None:
            data.MAPLOCAL_TO = MAPOS[data.MAPLOCAL_OS_TO](f"\\\\wsl.localhost\\{os.environ['WSL_DISTRO_NAME']}\\home")
        else:
            data.MAPLOCAL_TO = MAPOS[data.MAPLOCAL_OS_TO](data.MAPLOCAL_TO)

        if data.MAPLOCAL_SCRIPT_PATH is None:
            p = get_maplocal_path()
            if p.is_file():
                data.MAPLOCAL_SCRIPT_PATH = p
            else:
                data.MAPLOCAL_SCRIPT_PATH = pathlib.Path(__file__).parent / "maplocal_wsl.py"
        else:
            p = pathlib.Path(data.MAPLOCAL_SCRIPT_PATH)
            if p.is_file():
                data.MAPLOCAL_SCRIPT_PATH = p
            else:
                logger.warning(f"for maplocal to load openpath and runcmd callable, {str(p)} must exist with functions `openpath` and `runcmd`")
        
        if "MAPLOCAL_SCRIPT_PATH" not in data.model_fields:
            data.openpath = None
        p = data.MAPLOCAL_SCRIPT_PATH
        if p is not None:
            data.openpath = load(p, "openpath")
        else:
            data.openpath = None

        if "MAPLOCAL_SCRIPT_PATH" not in data.model_fields:
            data.runcmd = None
        else:
            p = data.MAPLOCAL_SCRIPT_PATH
            if p is not None:
                data.runcmd = load(p, "runcmd")
            else:
                data.runcmd = None

        return data

    model_config = SettingsConfigDict(env_file_encoding="utf-8", arbitrary_types_allowed=True)

