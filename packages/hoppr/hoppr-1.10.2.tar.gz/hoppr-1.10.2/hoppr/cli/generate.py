"""
`generate` subcommand for `hoptctl`
"""
from __future__ import annotations

import os

from pathlib import Path
from runpy import run_module

import typer

from typer import Option, Typer

from hoppr import main

app = Typer(
    name="generate",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Generate `in-toto` keys/layout or schemas for Hoppr input files",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="markdown",
)


@app.command()
def layout(
    # pylint: disable=unused-argument
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        envvar="HOPPR_TRANSFER_CONFIG",
        help="Specify transfer config",
    ),
    project_owner_key_path: Path = Option(
        ...,
        "-pk",
        "--project-owner-key",
        envvar="HOPPR_PROJECT_OWNER_KEY",
        help="Path to key used to sign in-toto layout",
    ),
    functionary_key_path: Path = Option(
        ...,
        "-fk",
        "--functionary-key",
        envvar="HOPPR_FUNCTIONARY_KEY",
        help="Path to key used to sign in-toto layout",
    ),
    project_owner_key_prompt: bool = Option(
        False,
        "-p",
        "--prompt",
        envvar="HOPPR_PROJECT_OWNER_KEY_PROMPT",
        help="Prompt user for project owner key's password",
    ),
    project_owner_key_password: str = Option(
        None,
        "-pk-pass",
        "--project-owner-key-password",
        envvar="HOPPR_PROJECT_OWNER_KEY_PASSWORD",
        help="Password for project owner key",
    ),
):  # pragma: no cover
    """
    Create in-toto layout based on transfer file
    """
    main.generate_layout(**locals())


@app.command(hidden=True)
def schemas(
    output_dir: Path = Option(
        Path(),
        "-o",
        "--output-dir",
        exists=True,
        file_okay=False,
        help=f"Output directory for schema files {typer.style(text='[default: current directory]', dim=True)}",
        resolve_path=True,
        show_default=False,
    )
):  # pragma: no cover
    """
    Generate JSON/YAML schemas for Hoppr manifest, credential, and transfer files
    """
    os.chdir(output_dir)
    run_module(mod_name="hoppr.models")
