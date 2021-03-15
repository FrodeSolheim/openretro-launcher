import os
import tempfile

from fsgamesys.FSGSDirectories import FSGSDirectories

"""
Data/Firmware/Amiga
Data/Firmware/CDTV
Data/Firmware/CD32

Data/Saves/Amiga

"""


def saves_directory():
    return FSGSDirectories.saves_dir()


_temp_directory = None
_temp_directory_t = None
_temp_counter = 0


def temp_directory():
    global _temp_directory
    global _temp_directory_t
    if _temp_directory is None:
        _temp_directory = tempfile.mkdtemp(prefix="fsgamesys-", suffix="")
        print("FSGS TEMP directory is", _temp_directory)
    if _temp_directory_t is None:
        _temp_directory_t = os.path.join(_temp_directory, "T")
        os.mkdir(_temp_directory_t)
    return _temp_directory_t


def temp_directory_for_config(config):
    global _temp_counter
    _temp_counter += 1
    path = os.path.join(temp_directory, str(_temp_counter))
    print("FSGS new temp directory", path)
    # If the directory already exists, an exception is raised, and we want
    # that.
    os.mkdir(path)
    return path
