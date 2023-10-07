#! /usr/bin/env python
"""SearchSource: Web of Science"""
from __future__ import annotations

import typing
from dataclasses import dataclass
from pathlib import Path

import zope.interface
from dacite import from_dict
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.ops.load_utils_bib
import colrev.ops.search
import colrev.record

# pylint: disable=unused-argument
# pylint: disable=duplicate-code


@zope.interface.implementer(
    colrev.env.package_manager.SearchSourcePackageEndpointInterface
)
@dataclass
class WebOfScienceSearchSource(JsonSchemaMixin):
    """Web of Science"""

    settings_class = colrev.env.package_manager.DefaultSourceSettings
    endpoint = "colrev.web_of_science"
    source_identifier = (
        "https://www.webofscience.com/wos/woscc/full-record/" + "{{unique-id}}"
    )
    search_types = [colrev.settings.SearchType.DB]

    ci_supported: bool = False
    heuristic_status = colrev.env.package_manager.SearchSourceHeuristicStatus.supported
    short_name = "Web of Science"
    docs_link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/"
        + "colrev/ops/built_in/search_sources/web_of_science.md"
    )

    def __init__(
        self, *, source_operation: colrev.operation.Operation, settings: dict
    ) -> None:
        self.search_source = from_dict(data_class=self.settings_class, data=settings)

    @classmethod
    def heuristic(cls, filename: Path, data: str) -> dict:
        """Source heuristic for Web of Science"""

        result = {"confidence": 0.0}

        if data.count("UT WOS:") > 0.4 * data.count("TI "):
            result["confidence"] = 0.7
            return result

        if "Unique-ID = {WOS:" in data:
            result["confidence"] = 0.7
            return result
        if "UT_(Unique_WOS_ID) = {WOS:" in data:
            result["confidence"] = 0.7
            return result
        if "@article{ WOS:" in data or "@article{WOS:" in data:
            if data.count("{WOS:") > data.count("\n@"):
                result["confidence"] = 1.0
            elif data.count("{ WOS:") > data.count("\n@"):
                result["confidence"] = 1.0
            else:
                result["confidence"] = 0.7

            return result

        return result

    @classmethod
    def add_endpoint(
        cls,
        operation: colrev.ops.search.Search,
        params: str,
        filename: typing.Optional[Path],
    ) -> colrev.settings.SearchSource:
        """Add SearchSource as an endpoint (based on query provided to colrev search -a )"""
        raise NotImplementedError

    def run_search(self, rerun: bool) -> None:
        """Run a search of WebOfScience"""

        # if self.search_source.search_type == colrev.settings.SearchSource.DB:
        #     if self.review_manager.in_ci_environment():
        #         raise colrev_exceptions.SearchNotAutomated(
        #             "DB search for WebOfScience not automated."
        #         )

    def get_masterdata(
        self,
        prep_operation: colrev.ops.prep.Prep,
        record: colrev.record.Record,
        save_feed: bool = True,
        timeout: int = 10,
    ) -> colrev.record.Record:
        """Not implemented"""
        return record

    def load(self, load_operation: colrev.ops.load.Load) -> dict:
        """Load the records from the SearchSource file"""

        if self.search_source.filename.suffix == ".bib":
            records = colrev.ops.load_utils_bib.load_bib_file(
                load_operation=load_operation, source=self.search_source
            )
            return records

        raise NotImplementedError

    def prepare(
        self, record: colrev.record.PrepRecord, source: colrev.settings.SearchSource
    ) -> colrev.record.Record:
        """Source-specific preparation for Web of Science"""

        record.format_if_mostly_upper(key="title", case="sentence")
        record.format_if_mostly_upper(key="journal", case="title")
        record.format_if_mostly_upper(key="booktitle", case="title")
        record.format_if_mostly_upper(key="author", case="title")

        record.remove_field(key="colrev.web_of_science.researcherid-numbers")
        record.remove_field(key="colrev.web_of_science.orcid-numbers")

        return record
