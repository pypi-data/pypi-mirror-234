# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import functools
import os
import pathlib
import shutil
import subprocess
import sys

from collections.abc import Callable
from typing import Final, Optional

import click
import filelock
import imageio.core.util
import imageio.plugins.freeimage
import xdg.BaseDirectory  # pyright: ignore [reportMissingTypeStubs]

import no_vtf_desktop._admin
import no_vtf_desktop._desktop
import no_vtf_desktop._lock
import no_vtf_desktop._metadata

_DISTRIBUTION_NAME: Final = "no_vtf-desktop"


def integrate(
    *,
    lock_timeout: Optional[float] = None,
    elevate: bool = True,
    force: bool = False,
    verbose: bool = False,
) -> None:
    config = _Config()
    if not force and config.is_version_current() and config.does_installation_mtime_match():
        if verbose:
            _echo("Integration is up-to-date, nothing to do")

        return

    fn = _integrate_with_lock

    scripts_path = no_vtf_desktop._metadata.get_path(_DISTRIBUTION_NAME, "scripts")
    elevate_fn = functools.partial(
        no_vtf_desktop._admin.elevate,
        scripts_path / "no_vtf-desktop",
        "--force",
    )

    _do_with_lock(
        fn=fn,
        elevate_fn=elevate_fn,
        lock_timeout=lock_timeout,
        elevate=elevate,
    )


def uninstall(
    *,
    elevate: bool = True,
) -> None:
    fn = _uninstall_with_lock

    scripts_path = no_vtf_desktop._metadata.get_path(_DISTRIBUTION_NAME, "scripts")
    elevate_fn = functools.partial(
        no_vtf_desktop._admin.elevate,
        scripts_path / "no_vtf-desktop-uninstall",
        "--yes",
    )

    _do_with_lock(
        fn=fn,
        elevate_fn=elevate_fn,
        lock_timeout=None,
        elevate=elevate,
    )


def _do_with_lock(
    *,
    fn: Callable[[], None],
    elevate_fn: Callable[[], None],
    lock_timeout: Optional[float],
    elevate: bool,
) -> None:
    if sys.platform != "linux":
        raise RuntimeError("Only the Linux platform is supported")

    installation_type = no_vtf_desktop._metadata.get_installation_type(_DISTRIBUTION_NAME)
    if installation_type != "system" and no_vtf_desktop._admin.is_admin():
        raise RuntimeError("Superuser can only manage system installation")

    lock = no_vtf_desktop._lock.get_lock(f"{_DISTRIBUTION_NAME}.{installation_type}.lock")
    try:
        with lock.acquire(timeout=lock_timeout):
            if installation_type == "system" and not no_vtf_desktop._admin.is_admin():
                if not elevate:
                    raise RuntimeError(
                        "Privilege elevation is required to manage system installation"
                    )

                elevate_fn()
                return

            fn()
    except filelock.Timeout:
        raise


def _integrate_with_lock() -> None:
    desktop = _get_desktop()
    desktop.integrate()

    imageio_package_dir = imageio.core.util.resource_package_dir()  # type: ignore[no-untyped-call]
    imageio.plugins.freeimage.download(imageio_package_dir)  # type: ignore[no-untyped-call]

    config = _Config()
    config.set_version_current()
    config.set_installation_mtime()

    _echo("Integrated successfully")


def _uninstall_with_lock() -> None:
    desktop = _get_desktop()
    config = _Config()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "uninstall",
            "--yes",
            _DISTRIBUTION_NAME,
        ],
        check=True,
        env={
            **os.environ,
            "PIP_BREAK_SYSTEM_PACKAGES": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_INPUT": "1",
            "PIP_ROOT_USER_ACTION": "ignore",
        },
    )
    desktop.uninstall()
    config.remove()

    _echo("Uninstalled successfully")


def _get_desktop() -> no_vtf_desktop._desktop.Desktop:
    dist_data_path = no_vtf_desktop._metadata.get_path(_DISTRIBUTION_NAME, "data")
    xdg_data_path = no_vtf_desktop._metadata.get_xdg_data_path(_DISTRIBUTION_NAME)

    generic_subpaths = [
        *[
            pathlib.Path(f"icons/hicolor/{size}x{size}/mimetypes/no_vtf-application-x-vtf.png")
            for size in [16, 22, 24, 32, 48, 64, 128, 256]
        ],
        pathlib.Path("icons/hicolor/scalable/mimetypes/no_vtf-application-x-vtf.svg"),
        pathlib.Path("mime/packages/no_vtf.xml"),
    ]

    desktop_entry_subpath = pathlib.Path("applications/no_vtf.desktop")
    thumbnailer_subpath = pathlib.Path("thumbnailers/no_vtf.thumbnailer")

    return no_vtf_desktop._desktop.Desktop(
        dist_data_path=dist_data_path,
        xdg_data_path=xdg_data_path,
        generic_subpaths=generic_subpaths,
        desktop_entry_subpath=desktop_entry_subpath,
        thumbnailer_subpath=thumbnailer_subpath,
    )


class _Config:
    def __init__(self) -> None:
        xdg_config_dirs = [
            pathlib.Path(xdg_config_dir) for xdg_config_dir in xdg.BaseDirectory.xdg_config_dirs
        ]

        installation_type = no_vtf_desktop._metadata.get_installation_type(_DISTRIBUTION_NAME)
        match installation_type:
            case "user" | "venv":
                xdg_config_dir = xdg_config_dirs[0]
            case "system":
                xdg_config_dir = xdg_config_dirs[-1]

        self._config_dir: Final = xdg_config_dir / _DISTRIBUTION_NAME
        self._installation_mtime_file: Final = self._config_dir / "installation_mtime"
        self._version_file: Final = self._config_dir / "version"

    def is_version_current(self) -> bool:
        with contextlib.suppress(FileNotFoundError):
            version = self._version_file.read_text().strip()
            return version == no_vtf_desktop.__version__

        return False

    def set_version_current(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._version_file.write_text(f"{no_vtf_desktop.__version__}\n")

    def remove(self) -> None:
        shutil.rmtree(self._config_dir, ignore_errors=True)

    def does_installation_mtime_match(self) -> bool:
        try:
            installation_mtime = self._get_installation_mtime()
            config_mtime = int(self._installation_mtime_file.read_text().strip())
            return config_mtime == installation_mtime
        except Exception:
            return not self._installation_mtime_file.exists()

    def set_installation_mtime(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)

        try:
            installation_mtime = self._get_installation_mtime()
            self._installation_mtime_file.write_text(f"{installation_mtime}\n")
        except Exception:
            self._installation_mtime_file.unlink(missing_ok=True)

    def _get_installation_mtime(self) -> int:
        return int(os.path.getmtime(__file__))


def _echo(message: str) -> None:
    click.echo(click.style(_DISTRIBUTION_NAME, fg=127, bold=True) + ": " + message)
