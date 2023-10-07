# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inspect

import click

import no_vtf_desktop
import no_vtf_desktop.installation


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf-desktop - Desktop integration for no_vtf
    Copyright (C) b5327157

    https://git.sr.ht/~b5327157/no_vtf-desktop/
    https://pypi.org/project/no-vtf-desktop/

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    click.echo(inspect.cleandoc(credits))
    ctx.exit()


def _show_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    click.echo(no_vtf_desktop.__version__)
    ctx.exit()


@click.command(name="no_vtf-desktop")
@click.option(
    "--force",
    help="Repeat integration even if it appears up-to-date",
    type=bool,
    is_flag=True,
)
@click.option(
    "--no-elevate",
    hidden=True,
    help="Disallow privilege elevation",
    type=bool,
    is_flag=True,
)
@click.help_option("--help", "-h")
@click.option(
    "--version",
    help="Show the version and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_version,
)
@click.option(
    "--credits",
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main_command(
    *,
    no_elevate: bool,
    force: bool,
) -> None:
    """
    Integrate no_vtf into the desktop environment.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    """

    no_vtf_desktop.installation.integrate(
        elevate=not no_elevate,
        force=force,
        verbose=True,
    )


@click.command(name="no_vtf-desktop-uninstall")
@click.confirmation_option(
    help="Do not ask for confirmation before uninstallation.",
    prompt="Do you want to uninstall no_vtf-desktop?",
    default=True,
    flag_value=True,
)
@click.option(
    "--no-elevate",
    hidden=True,
    help="Disallow privilege elevation",
    type=bool,
    is_flag=True,
)
@click.help_option("--help", "-h")
@click.option(
    "--version",
    help="Show the version and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_version,
)
@click.option(
    "--credits",
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def uninstall_command(
    *,
    no_elevate: bool,
) -> None:
    """
    Uninstall no_vtf-desktop and clean-up the desktop environment integration.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    """

    no_vtf_desktop.installation.uninstall(
        elevate=not no_elevate,
    )
