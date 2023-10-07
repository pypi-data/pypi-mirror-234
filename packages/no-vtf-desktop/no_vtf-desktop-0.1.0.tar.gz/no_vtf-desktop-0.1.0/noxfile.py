# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import pathlib
import shutil

import nox
import nox.command

nox.needs_version = ">= 2023.4.22"

nox.options.default_venv_backend = "venv"
nox.options.error_on_external_run = True
nox.options.error_on_missing_interpreters = True
nox.options.sessions = ["lint"]


@nox.session(python="3.10")
def lint(session: nox.Session) -> None:
    session.install("black[colorama] >= 23.7.0, < 24")
    session.install("flake8 >= 6.1.0, < 7")
    session.install("flake8-builtins >= 2.1.0, < 3")
    session.install("flake8-deprecated >= 2.0.1, < 3")
    session.install("flake8-pep585 >= 0.1.7, < 1")
    session.install("isort[colors] >= 5.12.0, < 6")
    session.install("mypy >= 1.5.1, < 2")
    session.install("nox >= 2023.4.22, < 2024")
    session.install("pep8-naming >= 0.13.3, < 1")
    session.install("pyright >= 1.1.325, < 2")
    session.install("reuse >= 2.1.0, < 3")

    session.install(".")

    posargs_paths = session.posargs
    fix = False
    if posargs_paths and posargs_paths[0] == "--fix":
        posargs_paths = posargs_paths[1:]
        fix = True

    paths = ["no_vtf_desktop", "noxfile.py"]
    if posargs_paths:
        paths = posargs_paths

    if not fix:
        session.run("mypy", "--pretty", "--show-error-context", "--", *paths)
        session.run("pyright", "--warnings", *paths, silent=True)
        session.run("flake8", "--", *paths)
        session.run("isort", "--check", "--diff", "--", *paths)
        session.run("black", "--check", "--diff", "--", *paths)
        session.run("reuse", "lint", silent=True)
    else:
        session.run("isort", "--", *paths)
        session.run("black", "--", *paths)


@nox.session(python="3.10")
def package(session: nox.Session) -> None:
    path_dist = pathlib.Path("dist")
    if path_dist.is_dir():
        dist_files = [path for path in path_dist.iterdir() if path.is_file()]
        for dist_file in dist_files:
            dist_file.unlink()

    session.install("build >= 1.0.0, < 2")

    session.run("python", "-m", "build", silent=True)

    path_sdist = next(path_dist.glob("*.tar.gz"))
    path_wheel = next(path_dist.glob("*.whl"))

    # run even with the --no-install flag
    session.run("pip", "install", "--force-reinstall", str(path_wheel), silent=True)

    executable = ["python", "-I", "-m", "no_vtf_desktop"]
    session.run(*executable, "--version")

    if len(session.posargs) >= 1:
        shutil.copy2(path_sdist, session.posargs[0])

    if len(session.posargs) >= 2:
        shutil.copy2(path_wheel, session.posargs[1])


@nox.session(python="3.10")
def publish(session: nox.Session) -> None:
    if not session.posargs:
        session.error("Path to API token file was not provided")

    session.install("twine >= 4.0.2, < 5")

    dist = pathlib.Path("dist")
    dist_files = [path for path in dist.iterdir() if path.is_file()]
    dist_args = [str(path) for path in dist_files]

    session.run("twine", "check", "--strict", *dist_args)

    upload_args: list[str] = []
    upload_args.append("--non-interactive")
    upload_args.append("--disable-progress-bar")
    upload_args.extend(dist_args)

    env = session.env.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = pathlib.Path(session.posargs[0]).read_text().strip()

    nox.command.run(
        ["twine", "upload", *upload_args],
        env=env,
        paths=session.bin_paths,
        external=True,
    )
