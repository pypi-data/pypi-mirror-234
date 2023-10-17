import pathlib
import typing as ty
from maplocal.env import MapLocalEnv
from maplocal.maplocal import _remove_root, openlocal, maplocal

MAPENV = MapLocalEnv()
PATH_TEST = pathlib.Path(__file__)
DIR_REPO = PATH_TEST.parents[1]


class TestMAPENV:
    def test_MAPENV(self):
        assert MAPENV.MAPLOCAL_FROM == pathlib.PurePosixPath("/home")
        assert MAPENV.MAPLOCAL_TO == pathlib.PureWindowsPath('//wsl.localhost/ubuntu_2004_jovyan/home')


class TestRemoveRoot:
    def test__remove_root(self):
        rootfound, newpath = _remove_root(PATH_TEST, DIR_REPO)
        assert rootfound == True
        assert newpath == pathlib.Path("tests/test_maplocal.py")


class TestMapLocal:
    def test_map_local(self):
        path = maplocal(PATH_TEST, oldroot=MAPENV.MAPLOCAL_FROM, newroot=MAPENV.MAPLOCAL_TO)
        assert (
            str(path)
            == "\\\\wsl.localhost\\ubuntu_2004_jovyan" + str(PATH_TEST).replace("/", "\\")
        )


class TestWslExample:
    def test_map_local(self):
        """This will open the file in windows explorer"""
        openlocal(PATH_TEST, mapenv=MAPENV)
        assert isinstance(MAPENV.openpath, ty.Callable)

