# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import pathlib
import shutil
import subprocess
import sys

from collections.abc import Sequence
from typing import Final


class Desktop:
    def __init__(
        self,
        *,
        dist_data_path: pathlib.Path,
        xdg_data_path: pathlib.Path,
        generic_subpaths: Sequence[pathlib.Path],
        desktop_entry_subpath: pathlib.Path,
        thumbnailer_subpath: pathlib.Path,
    ) -> None:
        self.dist_data_path: Final = dist_data_path
        self.xdg_data_path: Final = xdg_data_path
        self.generic_subpaths: Final = generic_subpaths
        self.desktop_entry_subpath: Final = desktop_entry_subpath
        self.thumbnailer_subpath: Final = thumbnailer_subpath

    def integrate(self) -> None:
        self._install()
        self._update()

    def uninstall(self) -> None:
        if not self.xdg_data_path.resolve() == self._get_dist_share_path().resolve():
            for subpath in self._get_subpaths():
                path = self.xdg_data_path / subpath
                path.unlink(missing_ok=True)

        self._update()

    def _install(self) -> None:
        if self.xdg_data_path.resolve() == self._get_dist_share_path().resolve():
            return

        for subpath in self._get_subpaths():
            src = self._get_dist_share_path() / subpath
            dst = self.xdg_data_path / subpath

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        desktop_entry_path = self.xdg_data_path / self.desktop_entry_subpath
        thumbnailer_path = self.xdg_data_path / self.thumbnailer_subpath

        escaped_executable_path = self._escape(str(pathlib.Path(sys.executable).absolute()))
        self._replace(desktop_entry_path, "python3", escaped_executable_path)
        self._replace(thumbnailer_path, "python3", escaped_executable_path)

    def _get_dist_share_path(self) -> pathlib.Path:
        return self.dist_data_path / "share"

    def _get_subpaths(self) -> Sequence[pathlib.Path]:
        return list(self.generic_subpaths) + [
            self.desktop_entry_subpath,
            self.thumbnailer_subpath,
        ]

    def _escape(self, string: str) -> str:
        string = string.replace("\\", r"""\\\\""")

        string = string.replace("\n", r"\n")
        string = string.replace("\t", r"\t")
        string = string.replace("\r", r"\r")

        string = string.replace("%", "%%")

        for char in r'$`"':
            string = string.replace(char, r"\\" + char)

        return f'"{string}"'

    def _replace(self, path: pathlib.Path, old: str, new: str) -> None:
        old_content = path.read_text()
        new_content = old_content.replace(old, new)
        assert new_content != old_content
        path.write_text(new_content)

    def _update(self) -> None:
        update_methods = [
            self._update_icon_cache,
            self._update_desktop_database,
            self._update_mime_database,
        ]
        for update_method in update_methods:
            with contextlib.suppress(FileNotFoundError):
                update_method()

    def _update_icon_cache(self) -> None:
        hicolor_path = self.xdg_data_path / "icons/hicolor"
        hicolor_index_path = hicolor_path / "index.theme"

        if not hicolor_index_path.exists():
            return

        subprocess.run(
            [
                "gtk-update-icon-cache",
                "--force",
                "--quiet",
                "--",
                hicolor_path,
            ],
            check=True,
        )

    def _update_desktop_database(self) -> None:
        applications_path = self.xdg_data_path / "applications"

        if not applications_path.exists():
            return

        subprocess.run(
            [
                "update-desktop-database",
                "--quiet",
                "--",
                applications_path,
            ],
            check=True,
        )

    def _update_mime_database(self) -> None:
        mime_path = self.xdg_data_path / "mime"
        mime_packages_path = mime_path / "packages"

        if not mime_packages_path.exists():
            return

        subprocess.run(
            [
                "update-mime-database",
                "--",
                mime_path,
            ],
            check=True,
        )
