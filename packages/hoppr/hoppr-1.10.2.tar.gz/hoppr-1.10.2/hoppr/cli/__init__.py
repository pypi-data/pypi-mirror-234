"""
Top-level CLI application
"""
from __future__ import annotations

import ctypes
import sys

from pathlib import Path
from platform import python_version

import rich

from rich.ansi import AnsiDecoder
from typer import Option, Typer

import hoppr.main
import hoppr.utils

from hoppr.cli import bundle, generate, merge
from hoppr.cli.options import basic_term_option, experimental_option, strict_repos_option, verbose_option

# Windows flags and types
NT_ENABLE_ECHO_INPUT = 0b0100
NT_ENABLE_LINE_INPUT = 0b0010
NT_ENABLE_PROCESSED_INPUT = 0b0001
NT_CONSOLE_FLAGS = NT_ENABLE_ECHO_INPUT | NT_ENABLE_LINE_INPUT | NT_ENABLE_PROCESSED_INPUT
NT_STD_OUTPUT_HANDLE = ctypes.c_uint(-11)

# Enable ANSI processing on Windows systems
if sys.platform == "win32":  # pragma: no cover
    nt_kernel = ctypes.WinDLL(name="kernel32.dll")

    nt_kernel.SetConsoleMode(nt_kernel.GetStdHandle(NT_STD_OUTPUT_HANDLE), NT_CONSOLE_FLAGS)


app = Typer(
    name="hopctl",
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="markdown",
)

app.add_typer(typer_instance=bundle.app, name="bundle")
app.add_typer(typer_instance=generate.app, name="generate")
app.add_typer(typer_instance=merge.app, name="merge")


# Aliases for deprecated commands to preserve backward compatibility
generate_layout = app.command(
    name="generate-layout",
    deprecated=True,
    rich_help_panel="Deprecated",
    help="See `hopctl generate layout` subcommand",
)(generate.layout)


generate_schemas = app.command(
    name="generate-schemas",
    deprecated=True,
    rich_help_panel="Deprecated",
    help="See `hopctl generate schemas` subcommand",
)(generate.schemas)


@app.callback()
def hopctl(  # pylint: disable=unused-argument
    basic_term: bool = basic_term_option,
    experimental: bool = experimental_option,
    strict_repos: bool = strict_repos_option,
    verbose: bool = verbose_option,
):
    """
    Collect, process, & bundle your software supply chain
    """


@app.command()
def validate(
    input_files: list[Path],
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
):  # pragma: no cover
    """
    Validate multiple manifest files for schema errors
    """
    hoppr.main.validate(input_files, credentials_file, transfer_file)


@app.command()
def version():
    """
    Print version information for `hoppr`
    """
    # Non-TTY terminals and MacOS Terminal.app don't support ANSI multibyte characters. Print low-resolution art instead
    suffix = ".ascii" if hoppr.utils.is_basic_terminal() else ".ansi"
    hippo_file = (Path(hoppr.main.__file__).parent / "resources" / "hoppr-hippo").with_suffix(suffix)

    decoder = AnsiDecoder()
    hippo = decoder.decode(hippo_file.read_text(encoding="utf-8"))

    rich.print(*hippo, sep="\n")
    rich.print(f"[green]Hoppr Framework Version[/] : {hoppr.__version__}")
    rich.print(f"[green]Python Version         [/] : {python_version()}")


__all__ = ["app"]
