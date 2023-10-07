# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import filelock

import no_vtf_desktop.installation


def pre_main() -> None:
    try:
        no_vtf_desktop.installation.integrate(
            lock_timeout=0,
        )
    except filelock.Timeout:
        pass
