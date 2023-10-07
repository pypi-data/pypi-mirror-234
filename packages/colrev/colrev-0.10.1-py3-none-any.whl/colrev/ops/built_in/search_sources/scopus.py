#! /usr/bin/env python
"""SearchSource: Scopus"""
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
class ScopusSearchSource(JsonSchemaMixin):
    """Scopus"""

    settings_class = colrev.env.package_manager.DefaultSourceSettings
    endpoint = "colrev.scopus"
    source_identifier = "url"
    search_types = [colrev.settings.SearchType.DB]

    ci_supported: bool = False
    heuristic_status = colrev.env.package_manager.SearchSourceHeuristicStatus.supported
    short_name = "Scopus"
    docs_link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/"
        + "colrev/ops/built_in/search_sources/scopus.md"
    )

    def __init__(
        self, *, source_operation: colrev.operation.Operation, settings: dict
    ) -> None:
        self.search_source = from_dict(data_class=self.settings_class, data=settings)
        self.quality_model = source_operation.review_manager.get_qm()

    @classmethod
    def heuristic(cls, filename: Path, data: str) -> dict:
        """Source heuristic for Scopus"""

        result = {"confidence": 0.0}
        if "source={Scopus}," in data:
            result["confidence"] = 1.0
            return result

        if "www.scopus.com" in data:
            if data.count("www.scopus.com") >= data.count("\n@"):
                result["confidence"] = 1.0

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
        """Run a search of Scopus"""

        # if self.search_source.search_type == colrev.settings.SearchSource.DB:
        #     if self.review_manager.in_ci_environment():
        #         raise colrev_exceptions.SearchNotAutomated(
        #             "DB search for Scopus not automated."
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
        self, record: colrev.record.Record, source: colrev.settings.SearchSource
    ) -> colrev.record.Record:
        """Source-specific preparation for Scopus"""

        if "conference" == record.data["ENTRYTYPE"]:
            record.data["ENTRYTYPE"] = "inproceedings"

        if "book" == record.data["ENTRYTYPE"]:
            if "journal" in record.data and "booktitle" not in record.data:
                record.rename_field(key="title", new_key="booktitle")
                record.rename_field(key="journal", new_key="title")

        if "colrev.scopus.document_type" in record.data:
            if record.data["colrev.scopus.document_type"] == "Conference Paper":
                record.change_entrytype(
                    new_entrytype="inproceedings", qm=self.quality_model
                )

            elif record.data["colrev.scopus.document_type"] == "Conference Review":
                record.change_entrytype(
                    new_entrytype="proceedings", qm=self.quality_model
                )

            elif record.data["colrev.scopus.document_type"] == "Article":
                record.change_entrytype(new_entrytype="article", qm=self.quality_model)

            record.remove_field(key="colrev.scopus.document_type")

        if (
            "colrev.scopus.Start_Page" in record.data
            and "colrev.scopus.End_Page" in record.data
        ):
            if (
                record.data["colrev.scopus.Start_Page"] != "nan"
                and record.data["colrev.scopus.End_Page"] != "nan"
            ):
                record.data["pages"] = (
                    record.data["colrev.scopus.Start_Page"]
                    + "--"
                    + record.data["colrev.scopus.End_Page"]
                )
                record.data["pages"] = record.data["pages"].replace(".0", "")
                record.remove_field(key="colrev.scopus.Start_Page")
                record.remove_field(key="colrev.scopus.End_Page")

        if "colrev.scopus.note" in record.data:
            if "cited By " in record.data["colrev.scopus.note"]:
                record.rename_field(key="colrev.scopus.note", new_key="cited_by")
                record.data["cited_by"] = record.data["cited_by"].replace(
                    "cited By ", ""
                )

        if "author" in record.data:
            record.data["author"] = record.data["author"].replace("; ", " and ")

        record.remove_field(key="colrev.scopus.source")

        return record
