"""
Report Generating Plugin
"""

import shutil

from pathlib import Path
from typing import Any, Optional
from uuid import UUID

import typer

from jinja2 import Environment, FileSystemLoader

from hoppr import __version__
from hoppr.base_plugins.hoppr import HopprPlugin
from hoppr.models.manifest import SearchSequence
from hoppr.models.sbom import Component
from hoppr.result import ResultStatus


class Report:  # pylint: disable=too-few-public-methods
    """
    A report of a plugin's execution stage result.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        unique_id: UUID,
        plugin: str,
        stage: str,
        result: ResultStatus,
        details: Any,
        method: str,
        component: Optional[Component] = None,
    ):
        self.unique_id = unique_id
        self.plugin = plugin
        self.stage = stage
        self.result = result
        self.details = details
        self.method = method
        self.component = component


class ReportGenerator(HopprPlugin):
    """
    A class for generating a report based on a list of `Report` objects.
    """

    report_gen_list: list[Report] = []

    def get_version(self) -> str:
        return __version__

    def generate_report(self) -> None:  # pylint: disable=too-many-locals
        """
        Generate a report based on the given list of `Report` objects.
        """

        # Count the number of reports and errors
        report_count = len(self.report_gen_list)
        error_count = len([report for report in self.report_gen_list if report.result.numerator == ResultStatus.FAIL])

        # Sort reports
        reports_with_components = [report for report in self.report_gen_list if report.component is not None]
        sorted_reports = sorted(reports_with_components, key=lambda report: (-report.result.numerator, report.plugin))

        # Organize reports by plugin and stage
        reports_by_plugin = self._get_reports_by("plugin", sorted_reports)
        reports_by_stage = self._get_reports_by("stage", sorted_reports)

        # Generate report HTML file
        environment = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))
        index_template = environment.get_template("index.jinja2")

        report_dir = Path.cwd() / "report"
        report_dir.mkdir(exist_ok=True)

        results_file_name = report_dir / "index.html"

        for dir_name in ("assets", "scripts", "styles"):
            source_dir = Path(__file__).parent / dir_name
            dest_dir = report_dir / dir_name
            shutil.copytree(src=source_dir, dst=dest_dir, dirs_exist_ok=True)

        context = {
            "report_count": report_count,
            "error_count": error_count,
            "reports_by_stage": reports_by_stage,
            "reports_by_plugin": reports_by_plugin,
            "ResultStatus": ResultStatus,
            "get_type": type,
            "get_length": len,
            "parse_search_sequence": SearchSequence.parse_raw,
            "get_successful_report_total": self._get_successful_report_total,
            "get_overall_status_button_class": self._get_overall_status_button_class,
        }

        results_file_name.write_text(index_template.render(context), encoding="utf-8")
        typer.echo(f"HTML report generated: {results_file_name}")

    def _get_successful_report_total(self, reports: list[Report]) -> int:
        """
        Return the number of successful reports for a given list of reports.
        """

        successful_reports = [report for report in reports if report.result.numerator == ResultStatus.SUCCESS]
        return len(successful_reports)

    def _get_overall_status_button_class(self, reports: list[Report]) -> str:
        """
        Determine the overall status of a list of reports and returns the appropriate css class.
        """

        num_successful_reports = sum(report.result.numerator == ResultStatus.SUCCESS for report in reports)

        if num_successful_reports == 0:
            return "btn-danger"

        if num_successful_reports == len(reports):
            return "btn-success"

        return "btn-warning"

    def _get_reports_by(self, sort_by: str, reports: list[Report]) -> dict:
        """
        Organize report data by plugin or stage.
        """

        sorted_reports: dict = {}

        for report in reports:
            if report.__dict__[sort_by] in sorted_reports:
                sorted_reports[report.__dict__[sort_by]].append(report)
            else:
                sorted_reports[report.__dict__[sort_by]] = [report]

        return sorted_reports
