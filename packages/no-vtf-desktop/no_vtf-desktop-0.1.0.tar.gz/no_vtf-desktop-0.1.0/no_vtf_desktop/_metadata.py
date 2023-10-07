# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.metadata
import pathlib
import site
import sys
import sysconfig

from typing import Literal, TypeAlias

import xdg.BaseDirectory  # pyright: ignore [reportMissingTypeStubs]

InstallationType: TypeAlias = Literal["system", "user", "venv"]


def get_xdg_data_path(distribution_name: str) -> pathlib.Path:
    if sys.platform != "linux":
        raise RuntimeError("Only the Linux platform is supported")

    installation_type = get_installation_type(distribution_name)
    if installation_type == "venv":
        return pathlib.Path(xdg.BaseDirectory.xdg_data_home)

    data_path = get_path(distribution_name, "data")
    xdg_data_path = data_path / "share"
    xdg_data_path = xdg_data_path.resolve()

    xdg_data_dirs = [
        pathlib.Path(xdg_data_dir).resolve() for xdg_data_dir in xdg.BaseDirectory.xdg_data_dirs
    ]

    if xdg_data_path not in xdg_data_dirs:
        raise RuntimeError("Detected path is not a known XDG base directory for data files")

    return xdg_data_path


def get_installation_type(distribution_name: str) -> InstallationType:
    distribution_location = get_distribution_location(distribution_name).resolve()
    preferred_prefix_purelib = pathlib.Path(
        sysconfig.get_paths(_get_preferred_prefix_scheme())["purelib"]
    ).resolve()
    usersitepackages = pathlib.Path(site.getusersitepackages()).resolve()

    if distribution_location == preferred_prefix_purelib:
        if sys.prefix == sys.base_prefix:
            return "system"
        else:
            return "venv"
    elif distribution_location == usersitepackages:
        return "user"

    raise RuntimeError("Unsupported installation type")


def get_path(distribution_name: str, path_name: str) -> pathlib.Path:
    distribution_location = get_distribution_location(distribution_name)

    installation_paths = get_installation_paths(
        _get_preferred_prefix_scheme(), _get_preferred_user_scheme(), purelib=distribution_location
    )
    if not installation_paths:
        raise RuntimeError("Cannot get installation paths matching distribution location")

    data_path = next(iter(installation_paths.values()))[path_name]
    return data_path


def get_distribution_location(distribution_name: str) -> pathlib.Path:
    try:
        return pathlib.Path(importlib.metadata.distribution(distribution_name).locate_file("."))
    except importlib.metadata.PackageNotFoundError:
        raise


def get_installation_paths(
    *schemes: str, **paths_match: pathlib.Path
) -> dict[str, dict[str, pathlib.Path]]:
    installation_paths: dict[str, dict[str, pathlib.Path]] = {}

    for scheme in schemes:
        paths = sysconfig.get_paths(scheme)
        if all(
            path.resolve() == pathlib.Path(paths[path_name]).resolve()
            for path_name, path in paths_match.items()
        ):
            installation_paths[scheme] = {
                path_name: pathlib.Path(path) for path_name, path in paths.items()
            }

    return installation_paths


def _get_preferred_prefix_scheme() -> str:
    return sysconfig.get_preferred_scheme("prefix")


def _get_preferred_user_scheme() -> str:
    return sysconfig.get_preferred_scheme("user")
