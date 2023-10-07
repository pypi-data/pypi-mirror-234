# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import pathlib
import subprocess


def is_admin() -> bool:
    return os.geteuid() == 0


def elevate(program: pathlib.Path, *args: str) -> None:
    subprocess.run(
        [
            "pkexec",
            program.absolute(),
            "--no-elevate",
            *args,
        ],
        check=True,
    )
