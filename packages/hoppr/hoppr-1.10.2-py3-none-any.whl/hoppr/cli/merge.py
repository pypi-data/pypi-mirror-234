"""
`merge` subcommand for `hoptctl`
"""
from __future__ import annotations

import time

from pathlib import Path
from typing import TYPE_CHECKING

import typer

from pydantic import ValidationError
from rich.console import Group
from rich.live import Live
from rich.progress import Progress
from rich.table import Table
from typer import BadParameter, Option, Typer

import hoppr.utils

from hoppr.cli.layout import HopprBasePanel, HopprJobsPanel, HopprLayout, HopprSpinnerColumn, console
from hoppr.cli.options import basic_term_option, verbose_option
from hoppr.models.base import CycloneDXBaseModel
from hoppr.models.manifest import Manifest
from hoppr.models.sbom import Sbom

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Merge all properties of two or more SBOM files",
    invoke_without_command=True,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="markdown",
    subcommand_metavar="",
)


class HopprMergeJobsPanel(HopprJobsPanel):
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress(
        "{task.description}",
        HopprSpinnerColumn(),
        expand=True,
    )


class HopprMergeLayout(HopprLayout):
    """
    Layout of the `hopctl merge` console application
    """

    name: str = "root"
    jobs_panel = HopprMergeJobsPanel()


class HopprMergeSummary(HopprBasePanel):  # pylint: disable=too-few-public-methods
    """
    `hopctl merge` results summary
    """

    stage_results_map: dict[str, Table] = {}

    def __init__(self, *args, title: str | None = "Summary", **kwargs) -> None:
        self.total_components = 0
        self.merged_components = 0

        self.summary_table = Table(
            "File Name",
            "# Components",
            "Elapsed Time",
            box=None,
            pad_edge=False,
            show_edge=False,
        )

        self.before_after_table = Table.grid(padding=(0, 1))

        self.summary_group = Group(self.summary_table, self.before_after_table)

        super().__init__(self.summary_group, title, *args, **kwargs)

    def __rich_console__(self, console_: Console, options: ConsoleOptions) -> RenderResult:
        # pylint: disable=arguments-renamed
        self.before_after_table.add_row()
        self.before_after_table.add_row("Total components before merge:", str(self.total_components))
        self.before_after_table.add_row("Total components after merge:", str(self.merged_components))

        if hoppr.utils.is_basic_terminal():
            console_.line()
            console_.rule(title="Summary", characters="=", style="[bold]rule.line")
            console_.print(self.summary_table)
            console_.print(self.before_after_table)
            return []

        return super().__rich_console__(console_, options)


def manifest_callback(manifest_file: Path | None) -> Path | None:
    """
    Extract and return SBOM refs from manifest files
    """
    if manifest_file is None:
        return None

    # Load manifest file to populate `Sbom.loaded_sboms`
    Manifest.load(manifest_file)

    return manifest_file


def output_file_callback(output_file: Path | None) -> Path:
    """
    Auto-generate an output file name if not provided
    """
    return output_file or Path.cwd() / f"hopctl-merge-{time.strftime('%Y%m%d-%H%M%S')}.json"


def sbom_callback(sbom_sources: list[str | Path]) -> list[str | Path]:
    """
    Load SBOM input files
    """
    # Combine SBOM files from all CLI input file arguments
    _load_sbom_files(sbom_sources)

    return sbom_sources


def sbom_dir_callback(sbom_dirs: list[Path]) -> list[Path]:
    """
    Load SBOM files from input directories
    """
    for sbom_dir in sbom_dirs:
        sbom_files = sbom_dir.glob("*.json")

        _load_sbom_files(list(sbom_files))

    return sbom_dirs


def _load_sbom_files(sbom_files: list[str | Path]) -> None:
    """
    Load SBOM input files
    """
    for sbom_file in sbom_files:
        try:
            Sbom.load(sbom_file)
        except ValidationError as ex:
            raise BadParameter(f"'{sbom_file}' is not a valid SBOM file") from ex


def _merge_sboms() -> Sbom:
    """
    Merge SBOMs into single object
    """
    merged_sbom = Sbom()
    layout = HopprMergeLayout()
    live_display = Live(layout, console=console, refresh_per_second=10)
    merged_sbom.subscribe(observer=layout, callback=layout.print)
    summary_panel = HopprMergeSummary()

    for sbom_ref, sbom in Sbom.loaded_sboms.items():
        summary_panel.total_components += len(sbom.components)
        layout.add_job(description=Path(str(sbom_ref)).name, sbom=sbom)

    if not hoppr.utils.is_basic_terminal():
        live_display.start(refresh=True)

    for task in layout.jobs_panel.progress_bar.tasks:
        layout.print(f"Merging {task.description}...")
        layout.start_job(task.description)

        merged_sbom.merge(task.fields["sbom"])

        layout.stop_job(task.description)
        layout.advance_job(task.description)

        summary_panel.summary_table.add_row(
            task.description, str(len(task.fields["sbom"].components)), f"{task.elapsed:.3f}"
        )

    layout.print("Writing merged SBOM...")

    layout.overall_progress.progress_bar.stop_task(layout.progress_task.id)

    summary_panel.merged_components = len(merged_sbom.components)

    if not hoppr.utils.is_basic_terminal():
        live_display.stop()

    console.print("\n", summary_panel)

    merged_sbom.unsubscribe(observer=layout)
    return merged_sbom


@app.callback()
def merge(  # pylint: disable=too-many-arguments, unused-argument
    manifest_file: Path = Option(
        None,
        "-m",
        "--manifest",
        callback=manifest_callback,
        dir_okay=False,
        exists=True,
        help="Manifest file containing SBOMs to merge",
        resolve_path=True,
        show_default=False,
    ),
    sbom_files: list[Path] = Option(
        [],
        "-s",
        "--sbom",
        callback=sbom_callback,
        dir_okay=False,
        exists=True,
        help="SBOM file to merge (can be specified multiple times)",
        resolve_path=True,
        show_default=False,
    ),
    sbom_dirs: list[Path] = Option(
        [],
        "-d",
        "--sbom-dir",
        callback=sbom_dir_callback,
        exists=True,
        file_okay=False,
        help="Directory containing SBOM files to merge (can be specified multiple times)",
        resolve_path=True,
        show_default=False,
    ),
    sbom_urls: list[str] = Option(
        [],
        "-u",
        "--sbom-url",
        callback=sbom_callback,
        help="URL of SBOM to merge (can be specified multiple times)",
        metavar="URL",
        show_default=False,
    ),
    output_file: Path = Option(
        None,
        "-o",
        "--output-file",
        callback=output_file_callback,
        dir_okay=False,
        exists=False,
        help=f"Path to output file {typer.style(text='[default: hopctl-merge-YYMMDD-HHMMSS.json]', dim=True)}",
        resolve_path=True,
        show_default=False,
    ),
    deep_merge: bool = Option(
        False,
        "--deep-merge",
        help="Resolve and expand `externalReferences` in-place",
        show_default=False,
    ),
    flatten: bool = Option(
        False,
        "--flatten",
        help="Flatten nested `components` into single unified list",
        show_default=False,
    ),
    basic_term: bool = basic_term_option,
    verbose: bool = verbose_option,
):
    """
    Merge SBOM files
    """
    if not any([manifest_file, *sbom_dirs, *sbom_files, *sbom_urls]) or len(Sbom.loaded_sboms) < 2:
        raise BadParameter(
            "A minimum of two SBOM files must be provided via the "
            "--sbom, --sbom-dir, --sbom-url, and --manifest arguments."
        )

    CycloneDXBaseModel.deep_merge = deep_merge
    CycloneDXBaseModel.flatten = flatten

    merged_sbom = _merge_sboms()

    output_file.write_text(
        data=merged_sbom.json(exclude_none=True, exclude_unset=True, by_alias=True, indent=2),
        encoding="utf-8",
    )
