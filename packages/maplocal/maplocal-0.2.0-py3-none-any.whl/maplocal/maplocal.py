import pathlib
import typing as ty
import logging
from maplocal.env import MapLocalEnv

logger = logging.getLogger(__name__)
MAPENV = MapLocalEnv()

def _remove_root(
    path: pathlib.PurePath, root: ty.Optional[pathlib.PurePath]
) -> ty.Tuple[bool, pathlib.PurePath]:
    """removes root from path
    Args:
        path (pathlib.PurePath): path
        pathlib (pathlib.PurePath): root to remove from path
    Returns:
        bool, path:
            bool-> if root successfully removed: True, else: False
            path-> if bool: newpath, else: oldpath
    """
    assert isinstance(
        path, pathlib.PurePath
    ), f"path ({path}) passed to _remove_root fn not a valid pathlib.PurePath"
    assert isinstance(
        root, pathlib.PurePath
    ), f"root ({root}) passed to _remove_root fn not a valid pathlib.PurePath"
    path = pathlib.Path(path).absolute()
    if root in path.parents:
        rootfound = True
        parts = pathlib.Path(path).parts
        n = len(root.parts)
        newpath = pathlib.PurePath(*parts[n:])
    else:
        rootfound = False
        newpath = path
    return rootfound, newpath

def roots_found(oldroot, newroot):
    if oldroot is None:
        logger.warning("oldroot is None. set this by setting the env var: MAPLOCAL_OLDROOT")
        if newroot is None:
            logger.warning("newroot is None. set this by setting the env var: MAPLOCAL_NEWROOT")
            return False
        return False
    return True

def maplocal(
    path: pathlib.PurePath,
    oldroot: ty.Optional[pathlib.PurePath] = None,
    newroot: ty.Optional[pathlib.PurePath] = None,
):
    if oldroot is None:
        oldroot = MAPENV.MAPLOCAL_FROM
    if newroot is None:
        newroot = MAPENV.MAPLOCAL_TO
    if not roots_found(oldroot, newroot):
        return path
    path = pathlib.PurePath(path)
    rootfound, newpath = _remove_root(path, oldroot)
    if not rootfound:
        raise ValueError(f"root: {str(oldroot)}. not found in path: {str(path)}")
    return newroot / newpath


def mapremote(path: pathlib.PurePath,
    oldroot: ty.Optional[pathlib.PurePath] = None,
    newroot: ty.Optional[pathlib.PurePath] = None,
):
    if oldroot is None:
        oldroot = MAPENV.MAPLOCAL_TO
    if newroot is None:
        newroot = MAPENV.MAPLOCAL_FROM
    if not roots_found(oldroot, newroot):
        return path
    path = pathlib.PurePath(path)
    rootfound, newpath = _remove_root(path, oldroot)
    if not rootfound:
        raise ValueError(f"root: {str(oldroot)}. not found in path: {str(path)}")
    return newroot / newpath


def openlocal(path, mapenv=MAPENV):
    path = maplocal(path, oldroot=mapenv.MAPLOCAL_FROM, newroot=mapenv.MAPLOCAL_TO)

    return mapenv.openpath(path)


def runlocal(cmd, mapenv=MAPENV):
    return mapenv.runcmd(cmd)

def maplocal_openlocal_exists():
    if isinstance(MAPENV.openpath, ty.Callable):
        return True
    else:
        return False
    
def maplocal_runlocal_exists():
    if isinstance(MAPENV.runcmd, ty.Callable):
        return True
    else:
        return False
    
