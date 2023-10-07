# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pathlib

import filelock
import xdg.BaseDirectory  # pyright: ignore [reportMissingTypeStubs]

import no_vtf_desktop._admin


def get_lock(file_name: str) -> filelock.FileLock:
    file_path = _get_lock_dir() / file_name
    return filelock.FileLock(file_path)


def _get_lock_dir() -> pathlib.Path:
    if no_vtf_desktop._admin.is_admin():
        return pathlib.Path("/run/lock")
    else:
        return pathlib.Path(xdg.BaseDirectory.get_runtime_dir())
