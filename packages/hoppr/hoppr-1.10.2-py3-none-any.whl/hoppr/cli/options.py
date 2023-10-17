"""
Common options for typer commands
"""
import os

from typer import CallbackParam, Context, Option


def set_global_option(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """
    Add option value to shared Click context. Allows interspersed CLI options/arguments

    Args:
        ctx (Context): Click context to update
        param (CallbackParam): Typer metadata for the parameter
        value (bool): The parameter value

    Returns:
        bool: The flag that was passed, unmodified
    """
    if param.name:
        ctx.params[param.name] = value

        if param.envvar and value:
            os.environ[str(param.envvar)] = "1"

    return value


basic_term_option: bool = Option(
    False,
    "-b",
    "--basic-term",
    callback=set_global_option,
    help="Use simplified output for non-TTY or legacy terminal emulators",
    is_eager=True,
    envvar="HOPPR_BASIC_TERM",
    rich_help_panel="Global options",
    show_default=False,
)

experimental_option: bool = Option(
    False,
    "-x",
    "--experimental",
    callback=set_global_option,
    help="Enable experimental features",
    is_eager=True,
    envvar="HOPPR_EXPERIMENTAL",
    rich_help_panel="Global options",
    show_default=False,
)

strict_repos_option: bool = Option(
    True,
    "--strict/--no-strict",
    callback=set_global_option,
    help="Utilize only manifest repositories for package collection",
    is_eager=True,
    envvar="HOPPR_STRICT_REPOS",
    rich_help_panel="Global options",
    show_default=False,
)

verbose_option: bool = Option(
    False,
    "-v",
    "--debug",
    "--verbose",
    callback=set_global_option,
    help="Enable debug output",
    is_eager=True,
    rich_help_panel="Global options",
    show_default=False,
)
