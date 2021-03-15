import os

from fsbc.paths import Paths
from fsgamesys.amiga.amiga import Amiga
from fsgamesys.archive import Archive
from fsgamesys.checksumtool import ChecksumTool
from fsgamesys.FSGSDirectories import FSGSDirectories
from launcher.i18n import gettext
from launcher.ui.LauncherFilePicker import LauncherFilePicker


class FloppyManager(object):
    @classmethod
    def clear_all(cls, *, config):
        for i in range(4):
            cls.eject(i, config=config)
        cls.clear_floppy_list(config=config)

    @classmethod
    def eject(cls, drive, *, config):
        # values = []
        # values.append(("floppy_drive_{0}".format(drive), ""))
        # values.append(("x_floppy_drive_{0}_sha1".format(drive), ""))
        # Config.set_multiple(values)
        # fsgs.amiga.eject_floppy(drive, config=config)
        values = [
            ("floppy_drive_{0}".format(drive), ""),
            ("x_floppy_drive_{0}_sha1".format(drive), ""),
        ]
        config.set_multiple(values)

    @classmethod
    def clear_floppy_list(cls, *, config):
        values = []
        for i in range(Amiga.MAX_FLOPPY_IMAGES):
            values.append(("floppy_image_{0}".format(i), ""))
            values.append(("x_floppy_image_{0}_sha1".format(i), ""))
        config.set_multiple(values)

    @classmethod
    def multi_select(cls, parent=None, *, config):
        default_dir = FSGSDirectories.get_floppies_dir()
        dialog = LauncherFilePicker(
            parent,
            gettext("Select multiple floppies"),
            "floppy",
            multiple=True,
        )
        if not dialog.show_modal():
            return
        original_paths = dialog.get_paths()
        original_paths.sort()
        paths = []
        for path in original_paths:
            path = Paths.get_real_case(path)
            embedded_files = []
            if path.endswith(".zip"):
                archive = Archive(path)
                files = archive.list_files()
                for file in files:
                    _name, ext = os.path.splitext(file)
                    # FIXME: get list of floppy extensions from a central
                    # place
                    if ext in [".adf", ".ipf"]:
                        embedded_files.append(file)
            if len(embedded_files) > 0:
                embedded_files.sort()
                print("found embedded floppy images:")
                print(embedded_files)
                for file in embedded_files:
                    paths.append(file)
            else:
                paths.append(path)

        checksum_tool = ChecksumTool(parent)
        for i, path in enumerate(paths):
            sha1 = checksum_tool.checksum(path)
            path = Paths.contract_path(
                path, default_dir, force_real_case=False
            )

            if i < 4:
                config.set_multiple(
                    [
                        ("floppy_drive_{0}".format(i), path),
                        ("x_floppy_drive_{0}_sha1".format(i), sha1),
                    ]
                )
            config.set_multiple(
                [
                    ("floppy_image_{0}".format(i), path),
                    ("x_floppy_image_{0}_sha1".format(i), sha1),
                ]
            )

        # blank the rest of the drives
        for i in range(len(paths), 4):
            config.set_multiple(
                [
                    ("floppy_drive_{0}".format(i), ""),
                    ("x_floppy_drive_{0}_sha1".format(i), ""),
                ]
            )
        # blank the rest of the image list
        for i in range(len(paths), 20):
            config.set_multiple(
                [
                    ("floppy_image_{0}".format(i), ""),
                    ("x_floppy_image_{0}_sha1".format(i), ""),
                ]
            )
            # dialog.destroy()
