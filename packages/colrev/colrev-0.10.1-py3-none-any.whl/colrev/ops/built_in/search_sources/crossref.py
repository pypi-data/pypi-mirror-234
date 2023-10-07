#! /usr/bin/env python
"""SearchSource: Crossref"""
from __future__ import annotations

import json
import re
import typing
import urllib
from copy import deepcopy
from dataclasses import dataclass
from importlib.metadata import version
from multiprocessing import Lock
from pathlib import Path
from sqlite3 import OperationalError
from typing import Optional
from typing import TYPE_CHECKING

import requests
import zope.interface
from crossref.restful import Etiquette
from crossref.restful import Journals
from crossref.restful import Works
from dacite import from_dict
from dataclasses_jsonschema import JsonSchemaMixin
from thefuzz import fuzz

import colrev.env.package_manager
import colrev.exceptions as colrev_exceptions
import colrev.ops.built_in.search_sources.doi_org as doi_connector
import colrev.ops.built_in.search_sources.utils as connector_utils
import colrev.record
import colrev.ui_cli.cli_colors as colors

if TYPE_CHECKING:
    import colrev.ops.search
    import colrev.ops.prep

# pylint: disable=unused-argument
# pylint: disable=duplicate-code
# pylint: disable=too-many-lines


@zope.interface.implementer(
    colrev.env.package_manager.SearchSourcePackageEndpointInterface
)
@dataclass
class CrossrefSearchSource(JsonSchemaMixin):
    """Crossref API"""

    __ISSN_REGEX = r"^\d{4}-?\d{3}[\dxX]$"
    __YEAR_SCOPE_REGEX = r"^\d{4}-\d{4}$"

    # https://github.com/CrossRef/rest-api-doc
    __api_url = "https://api.crossref.org/works?"

    settings_class = colrev.env.package_manager.DefaultSourceSettings
    endpoint = "colrev.crossref"
    source_identifier = "doi"
    # "https://api.crossref.org/works/{{doi}}"
    search_types = [
        colrev.settings.SearchType.API,
        colrev.settings.SearchType.MD,
        colrev.settings.SearchType.TOC,
    ]

    ci_supported: bool = True
    heuristic_status = colrev.env.package_manager.SearchSourceHeuristicStatus.oni
    docs_link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/"
        + "colrev/ops/built_in/search_sources/crossref.md"
    )
    short_name = "Crossref"
    __crossref_md_filename = Path("data/search/md_crossref.bib")

    __availability_exception_message = (
        f"Crossref ({colors.ORANGE}check https://status.crossref.org/{colors.END})"
    )

    def __init__(
        self,
        *,
        source_operation: colrev.operation.Operation,
        settings: Optional[dict] = None,
    ) -> None:
        if settings:
            # Crossref as a search_source
            self.search_source = from_dict(
                data_class=self.settings_class, data=settings
            )
        else:
            # Crossref as an md-prep source
            crossref_md_source_l = [
                s
                for s in source_operation.review_manager.settings.sources
                if s.filename == self.__crossref_md_filename
            ]
            if crossref_md_source_l:
                self.search_source = crossref_md_source_l[0]
            else:
                self.search_source = colrev.settings.SearchSource(
                    endpoint="colrev.crossref",
                    filename=self.__crossref_md_filename,
                    search_type=colrev.settings.SearchType.MD,
                    search_parameters={},
                    comment="",
                )

            self.crossref_lock = Lock()

        self.language_service = colrev.env.language_service.LanguageService()

        self.review_manager = source_operation.review_manager
        self.etiquette = self.get_etiquette(review_manager=self.review_manager)
        self.email = self.review_manager.get_committer()

    @classmethod
    def get_etiquette(
        cls, *, review_manager: colrev.review_manager.ReviewManager
    ) -> Etiquette:
        """Get the etiquette for the crossref api"""
        _, email = review_manager.get_committer()
        return Etiquette(
            "CoLRev",
            version("colrev"),
            "https://github.com/CoLRev-Environment/colrev",
            email,
        )

    def check_availability(
        self, *, source_operation: colrev.operation.Operation
    ) -> None:
        """Check status (availability) of the Crossref API"""

        try:
            # pylint: disable=duplicate-code
            test_rec = {
                "doi": "10.17705/1cais.04607",
                "author": "Schryen, Guido and Wagner, Gerit and Benlian, Alexander "
                "and Paré, Guy",
                "title": "A Knowledge Development Perspective on Literature Reviews: "
                "Validation of a new Typology in the IS Field",
                "ID": "SchryenEtAl2021",
                "journal": "Communications of the Association for Information Systems",
                "ENTRYTYPE": "article",
            }
            returned_record = self.crossref_query(
                record_input=colrev.record.PrepRecord(data=test_rec),
                jour_vol_iss_list=False,
                timeout=20,
            )[0]

            if 0 != len(returned_record.data):
                assert returned_record.data["title"] == test_rec["title"]
                assert returned_record.data["author"] == test_rec["author"]
            else:
                if not source_operation.force_mode:
                    raise colrev_exceptions.ServiceNotAvailableException(
                        self.__availability_exception_message
                    )
        except (requests.exceptions.RequestException, IndexError) as exc:
            print(exc)
            if not source_operation.force_mode:
                raise colrev_exceptions.ServiceNotAvailableException(
                    self.__availability_exception_message
                ) from exc

    def __query(self, **kwargs) -> typing.Iterator[dict]:  # type: ignore
        """Get records from Crossref based on a bibliographic query"""

        works = Works(etiquette=self.etiquette)
        # use facets:
        # https://api.crossref.org/swagger-ui/index.html#/Works/get_works

        crossref_query_return = works.query(**kwargs).sort("deposited").order("desc")
        yield from crossref_query_return

    @classmethod
    def query_doi(cls, *, doi: str, etiquette: Etiquette) -> colrev.record.PrepRecord:
        """Get records from Crossref based on a doi query"""

        try:
            works = Works(etiquette=etiquette)
            crossref_query_return = works.doi(doi)
            if crossref_query_return is None:
                raise colrev_exceptions.RecordNotFoundInPrepSourceException(
                    msg="Record not found in crossref (based on doi)"
                )

            retrieved_record_dict = connector_utils.json_to_record(
                item=crossref_query_return
            )
            retrieved_record = colrev.record.PrepRecord(data=retrieved_record_dict)
            return retrieved_record

        except (requests.exceptions.RequestException,) as exc:
            raise colrev_exceptions.RecordNotFoundInPrepSourceException(
                msg="Record not found in crossref (based on doi)"
            ) from exc

    def __query_journal(self, *, issn: str, rerun: bool) -> typing.Iterator[dict]:
        """Get records of a selected journal from Crossref"""

        assert re.match(self.__ISSN_REGEX, issn)

        journals = Journals(etiquette=self.etiquette)
        if rerun:
            # Note : the "deposited" field is not always provided.
            # only the general query will return all records.
            crossref_query_return = journals.works(issn).query()
        else:
            crossref_query_return = (
                journals.works(issn).query().sort("deposited").order("desc")
            )

        yield from crossref_query_return

    def __create_query_url(
        self, *, record: colrev.record.Record, jour_vol_iss_list: bool
    ) -> str:
        if jour_vol_iss_list:
            if not all(x in record.data for x in ["journal", "volume", "number"]):
                raise colrev_exceptions.NotEnoughDataToIdentifyException
            params = {"rows": "50"}
            container_title = re.sub(r"[\W]+", " ", record.data["journal"])
            params["query.container-title"] = container_title.replace("_", " ")

            query_field = ""
            if "volume" in record.data:
                query_field = record.data["volume"]
            if "number" in record.data:
                query_field = query_field + "+" + record.data["number"]
            params["query"] = query_field

        else:
            if "title" not in record.data:
                raise colrev_exceptions.NotEnoughDataToIdentifyException()

            params = {"rows": "15"}
            if not isinstance(record.data.get("year", ""), str) or not isinstance(
                record.data.get("title", ""), str
            ):
                print("year or title field not a string")
                print(record.data)
                raise AssertionError

            bibl = (
                record.data["title"].replace("-", "_")
                + " "
                + record.data.get("year", "")
            )
            bibl = re.sub(r"[\W]+", "", bibl.replace(" ", "_"))
            params["query.bibliographic"] = bibl.replace("_", " ")

            container_title = record.get_container_title()
            if "." not in container_title:
                container_title = container_title.replace(" ", "_")
                container_title = re.sub(r"[\W]+", "", container_title)
                params["query.container-title"] = container_title.replace("_", " ")

            author_last_names = [
                x.split(",")[0] for x in record.data.get("author", "").split(" and ")
            ]
            author_string = " ".join(author_last_names)
            author_string = re.sub(r"[\W]+", "", author_string.replace(" ", "_"))
            params["query.author"] = author_string.replace("_", " ")

        url = self.__api_url + urllib.parse.urlencode(params)
        return url

    def __get_similarity(
        self, *, record: colrev.record.Record, retrieved_record_dict: dict
    ) -> float:
        title_similarity = fuzz.partial_ratio(
            retrieved_record_dict.get("title", "NA").lower(),
            record.data.get("title", "").lower(),
        )
        container_similarity = fuzz.partial_ratio(
            colrev.record.PrepRecord(data=retrieved_record_dict)
            .get_container_title()
            .lower(),
            record.get_container_title().lower(),
        )
        weights = [0.6, 0.4]
        similarities = [title_similarity, container_similarity]

        similarity = sum(similarities[g] * weights[g] for g in range(len(similarities)))
        # logger.debug(f'record: {pp.pformat(record)}')
        # logger.debug(f'similarities: {similarities}')
        # logger.debug(f'similarity: {similarity}')
        # pp.pprint(retrieved_record_dict)
        return similarity

    def __prep_crossref_record(
        self,
        *,
        record: colrev.record.Record,
        prep_main_record: bool = True,
        crossref_source: str = "",
    ) -> None:
        if "language" in record.data:
            try:
                self.language_service.unify_to_iso_639_3_language_codes(record=record)
            except colrev_exceptions.InvalidLanguageCodeException:
                del record.data["language"]

        doi_connector.DOIConnector.get_link_from_doi(
            review_manager=self.review_manager,
            record=record,
        )

        if (
            self.review_manager.settings.is_curated_masterdata_repo()
        ) and "cited_by" in record.data:
            del record.data["cited_by"]

        if not prep_main_record:
            # Skip steps for feed records
            return

        if "retracted" in record.data.get(
            "warning", ""
        ) or "retracted" in record.data.get("prescreen_exclusion", ""):
            record.prescreen_exclude(reason="retracted")
            record.remove_field(key="warning")
        else:
            assert "" != crossref_source
            record.set_masterdata_complete(
                source=crossref_source,
                masterdata_repository=self.review_manager.settings.is_curated_repo(),
            )
            record.set_status(target_state=colrev.record.RecordState.md_prepared)

    def __get_crossref_query_items(
        self, *, record: colrev.record.Record, jour_vol_iss_list: bool, timeout: int
    ) -> list:
        # Note : only returning a multiple-item list for jour_vol_iss_list
        try:
            url = self.__create_query_url(
                record=record, jour_vol_iss_list=jour_vol_iss_list
            )
            headers = {"user-agent": f"{__name__} (mailto:{self.email})"}
            session = self.review_manager.get_cached_session()

            # review_manager.logger.debug(url)
            ret = session.request("GET", url, headers=headers, timeout=timeout)
            ret.raise_for_status()
            if ret.status_code != 200:
                # review_manager.logger.debug(
                #     f"crossref_query failed with status {ret.status_code}"
                # )
                return []

            data = json.loads(ret.text)

        # pylint: disable=duplicate-code
        except OperationalError as exc:
            raise colrev_exceptions.ServiceNotAvailableException(
                "sqlite, required for requests CachedSession "
                "(possibly caused by concurrent operations)"
            ) from exc
        except (
            colrev_exceptions.NotEnoughDataToIdentifyException,
            json.decoder.JSONDecodeError,
            requests.exceptions.RequestException,
        ):
            return []

        return data["message"].get("items", [])

    def crossref_query(
        self,
        *,
        record_input: colrev.record.Record,
        jour_vol_iss_list: bool = False,
        timeout: int = 40,
    ) -> list:
        """Retrieve records from Crossref based on a query"""

        record = record_input.copy_prep_rec()
        record_list, most_similar, most_similar_record = [], 0.0, {}
        for item in self.__get_crossref_query_items(
            record=record, jour_vol_iss_list=jour_vol_iss_list, timeout=timeout
        ):
            try:
                retrieved_record_dict = connector_utils.json_to_record(item=item)
                similarity = self.__get_similarity(
                    record=record, retrieved_record_dict=retrieved_record_dict
                )
                retrieved_record = colrev.record.PrepRecord(data=retrieved_record_dict)

                # source = (
                #     f'https://api.crossref.org/works/{retrieved_record.data["doi"]}'
                # )
                # retrieved_record.add_provenance_all(source=source)

                # record.set_masterdata_complete(source=source)

                if jour_vol_iss_list:
                    record_list.append(retrieved_record)
                elif most_similar < similarity:
                    most_similar = similarity
                    most_similar_record = retrieved_record.get_data()
            except colrev_exceptions.RecordNotParsableException:
                pass

        if not jour_vol_iss_list:
            if most_similar_record:
                record_list = [colrev.record.PrepRecord(data=most_similar_record)]

        return record_list

    # def __check_journal(
    #     self,
    #     prep_operation: colrev.ops.prep.Prep,
    #     record: colrev.record.Record,
    #     timeout: int,
    #     save_feed: bool,
    # ) -> colrev.record.Record:
    #     """When there is no doi, journal names can be checked against crossref"""

    #     if record.data["ENTRYTYPE"] == "article":
    #         # If type article and doi not in record and
    #         # journal name not found in journal-query: notify
    #         journals = Journals(etiquette=self.etiquette)
    #         # record.data["journal"] = "Information Systems Research"
    #         found = False
    #         ret = journals.query(record.data["journal"])
    #         for rets in ret:
    #             if rets["title"]:
    #                 found = True
    #                 break
    #         if not found:
    #             record.add_masterdata_provenance_note(
    #                 key="journal", note="quality_defect:journal not in crossref"
    #             )

    #     return record

    def __get_masterdata_record(
        self,
        prep_operation: colrev.ops.prep.Prep,
        record: colrev.record.Record,
        timeout: int,
        save_feed: bool,
    ) -> colrev.record.Record:
        try:
            if "doi" in record.data:
                retrieved_record = self.query_doi(
                    doi=record.data["doi"], etiquette=self.etiquette
                )
            else:
                retrieved_records = self.crossref_query(
                    record_input=record,
                    jour_vol_iss_list=False,
                    timeout=timeout,
                )
                retrieved_record = retrieved_records.pop()

                retries = 0
                while (
                    not retrieved_record
                    and retries < prep_operation.max_retries_on_error
                ):
                    retries += 1

                    retrieved_records = self.crossref_query(
                        record_input=record,
                        jour_vol_iss_list=False,
                        timeout=timeout,
                    )
                    retrieved_record = retrieved_records.pop()

            if 0 == len(retrieved_record.data) or "doi" not in retrieved_record.data:
                raise colrev_exceptions.RecordNotFoundInPrepSourceException(
                    msg="Record not found in crossref"
                )

            similarity = colrev.record.PrepRecord.get_retrieval_similarity(
                record_original=record, retrieved_record_original=retrieved_record
            )
            # prep_operation.review_manager.logger.debug("Found matching record")
            # prep_operation.review_manager.logger.debug(
            #     f"crossref similarity: {similarity} "
            #     f"(>{prep_operation.retrieval_similarity})"
            # )
            self.review_manager.logger.debug(
                f"crossref similarity: {similarity} "
                f"(<{prep_operation.retrieval_similarity})"
            )
            if similarity < prep_operation.retrieval_similarity:
                return record

            try:
                self.crossref_lock.acquire(timeout=120)

                # Note : need to reload file because the object is not shared between processes
                crossref_feed = self.search_source.get_feed(
                    review_manager=self.review_manager,
                    source_identifier=self.source_identifier,
                    update_only=False,
                )

                crossref_feed.set_id(record_dict=retrieved_record.data)
                crossref_feed.add_record(record=retrieved_record)

                record.merge(
                    merging_record=retrieved_record,
                    default_source=retrieved_record.data["colrev_origin"][0],
                )

                self.__prep_crossref_record(
                    record=record,
                    crossref_source=retrieved_record.data["colrev_origin"][0],
                )

                if save_feed:
                    crossref_feed.save_feed_file()

            except (
                colrev_exceptions.InvalidMerge,
                colrev_exceptions.NotFeedIdentifiableException,
            ):
                pass
            finally:
                try:
                    self.crossref_lock.release()
                except ValueError:
                    pass

            return record

        except (
            requests.exceptions.RequestException,
            OSError,
            IndexError,
            colrev_exceptions.RecordNotFoundInPrepSourceException,
            colrev_exceptions.RecordNotParsableException,
        ) as exc:
            if prep_operation.review_manager.verbose_mode:
                print(exc)

        return record

    def __check_doi_masterdata(
        self, record: colrev.record.Record
    ) -> colrev.record.Record:
        try:
            retrieved_record = self.query_doi(
                doi=record.data["doi"], etiquette=self.etiquette
            )
            similarity = colrev.record.PrepRecord.get_retrieval_similarity(
                record_original=record,
                retrieved_record_original=retrieved_record,
                same_record_type_required=False,
            )
            if similarity < 0.7:
                # self.review_manager.logger.error(
                #     f" mismatching metadata (record/doi-record): {record.data['doi']} "
                #     + f"(similarity: {similarity})"
                # )
                record.remove_field(key="doi")
                # record.print_citation_format()
                # retrieved_record.print_citation_format()

        except (
            requests.exceptions.RequestException,
            OSError,
            IndexError,
            colrev_exceptions.RecordNotFoundInPrepSourceException,
            colrev_exceptions.RecordNotParsableException,
        ):
            pass

        return record

    def get_masterdata(
        self,
        prep_operation: colrev.ops.prep.Prep,
        record: colrev.record.Record,
        save_feed: bool = True,
        timeout: int = 30,
    ) -> colrev.record.Record:
        """Retrieve masterdata from Crossref based on similarity with the record provided"""

        # To test the metadata provided for a particular DOI use:
        # https://api.crossref.org/works/DOI

        # https://github.com/OpenAPC/openapc-de/blob/master/python/import_dois.py
        if len(record.data.get("title", "")) < 35 and "doi" not in record.data:
            return record

        if "doi" in record.data:
            record = self.__check_doi_masterdata(record=record)

        record = self.__get_masterdata_record(
            prep_operation=prep_operation,
            record=record,
            timeout=timeout,
            save_feed=save_feed,
        )

        # Note: this should be optional
        # if "doi" not in record.data:
        #     record = self.__check_journal(
        #         prep_operation=prep_operation,
        #         record=record,
        #         timeout=timeout,
        #         save_feed=save_feed,
        #     )

        return record

    def __validate_source(self) -> None:
        """Validate the SearchSource (parameters etc.)"""
        source = self.search_source
        self.review_manager.logger.debug(f"Validate SearchSource {source.filename}")

        if source.filename.name != self.__crossref_md_filename.name:
            if not any(x in source.search_parameters for x in ["query", "scope"]):
                raise colrev_exceptions.InvalidQueryException(
                    "Crossref search_parameters requires a query or issn field"
                )

            if "scope" in source.search_parameters:
                if "issn" in source.search_parameters["scope"]:
                    assert isinstance(source.search_parameters["scope"]["issn"], list)
                    for issn_field in source.search_parameters["scope"]["issn"]:
                        if not re.match(self.__ISSN_REGEX, issn_field):
                            raise colrev_exceptions.InvalidQueryException(
                                f"Crossref journal issn ({issn_field}) not matching required format"
                            )
                elif "years" in source.search_parameters["scope"]:
                    years_field = source.search_parameters["scope"]["years"]
                    if not re.match(self.__YEAR_SCOPE_REGEX, years_field):
                        raise colrev_exceptions.InvalidQueryException(
                            f"Scope (years) ({years_field}) not matching required format"
                        )
                else:
                    raise colrev_exceptions.InvalidQueryException(
                        "Query missing valid parameters"
                    )

            elif "query" in source.search_parameters:
                # Note: not yet implemented/supported
                if " AND " in source.search_parameters["query"]:
                    raise colrev_exceptions.InvalidQueryException(
                        "AND not supported in CROSSREF query"
                    )

            else:
                raise colrev_exceptions.InvalidQueryException(
                    "Query missing valid parameters"
                )

            if source.search_type not in [
                colrev.settings.SearchType.DB,
                colrev.settings.SearchType.TOC,
            ]:
                raise colrev_exceptions.InvalidQueryException(
                    "Crossref search_type should be in [DB,TOC]"
                )

        self.review_manager.logger.debug(f"SearchSource {source.filename} validated")

    def __get_crossref_query_return(self, *, rerun: bool) -> typing.Iterator[dict]:
        params = self.search_source.search_parameters

        if "query" in params and "mode" not in params:
            crossref_query = {"bibliographic": params["query"].replace(" ", "+")}
            # potential extension : add the container_title:
            # crossref_query_return = works.query(
            #     container_title=
            #       "Journal of the Association for Information Systems"
            # )
            yield from self.__query(**crossref_query)
        elif "scope" in params and "issn" in params["scope"]:
            if "issn" in params["scope"]:
                for issn in params["scope"]["issn"]:
                    yield from self.__query_journal(issn=issn, rerun=rerun)

    def __restore_url(
        self,
        *,
        record: colrev.record.Record,
        feed: colrev.ops.search_feed.GeneralOriginFeed,
    ) -> None:
        """Restore the url from the feed if it exists
        (url-resolution is not always available)"""
        if record.data["ID"] not in feed.feed_records:
            return
        prev_url = feed.feed_records[record.data["ID"]].get("url", None)
        if prev_url is None:
            return
        record.data["url"] = prev_url

    def __run_md_search(
        self,
        *,
        crossref_feed: colrev.ops.search_feed.GeneralOriginFeed,
        rerun: bool,
    ) -> None:
        records = self.review_manager.dataset.load_records_dict()

        for feed_record_dict in crossref_feed.feed_records.values():
            feed_record = colrev.record.Record(data=feed_record_dict)

            try:
                retrieved_record = self.query_doi(
                    doi=feed_record_dict["doi"], etiquette=self.etiquette
                )

                if retrieved_record.data["doi"] != feed_record.data["doi"]:
                    continue

                crossref_feed.set_id(record_dict=retrieved_record.data)
            except (
                colrev_exceptions.RecordNotFoundInPrepSourceException,
                colrev_exceptions.NotFeedIdentifiableException,
            ):
                continue

            self.__prep_crossref_record(record=retrieved_record, prep_main_record=False)

            prev_record_dict_version = {}
            if retrieved_record.data["ID"] in crossref_feed.feed_records:
                prev_record_dict_version = crossref_feed.feed_records[
                    retrieved_record.data["ID"]
                ]

            self.__restore_url(record=retrieved_record, feed=crossref_feed)
            crossref_feed.add_record(record=retrieved_record)

            crossref_feed.update_existing_record(
                records=records,
                record_dict=retrieved_record.data,
                prev_record_dict_version=prev_record_dict_version,
                source=self.search_source,
                update_time_variant_fields=rerun,
            )

        crossref_feed.print_post_run_search_infos(records=records)
        crossref_feed.save_feed_file()
        self.review_manager.dataset.save_records_dict(records=records)
        self.review_manager.dataset.add_record_changes()

    def __scope_excluded(self, *, retrieved_record_dict: dict) -> bool:
        if (
            "scope" not in self.search_source.search_parameters
            or "years" not in self.search_source.search_parameters["scope"]
        ):
            return False
        year_from, year_to = self.search_source.search_parameters["scope"][
            "years"
        ].split("-")
        if not retrieved_record_dict.get("year", -1000).isdigit():
            return True
        if (
            int(year_from)
            <= int(retrieved_record_dict.get("year", -1000))
            <= int(year_to)
        ):
            return False
        return True

    def __run_keyword_exploration_search(
        self,
        crossref_feed: colrev.ops.search_feed.GeneralOriginFeed,
    ) -> None:
        works = Works(etiquette=self.etiquette)

        def retrieve_exploratory_papers(keyword: str) -> typing.Iterator[dict]:
            crossref_query_return = works.query(bibliographic=keyword.replace(" ", "+"))
            yield from crossref_query_return

        records = self.review_manager.dataset.load_records_dict()
        available_dois = [x["doi"] for x in records.values() if "doi" in x]

        covered_keywords = [
            x["explored_keyword"] for x in crossref_feed.feed_records.values()
        ]

        for keyword in self.search_source.search_parameters["query"].split(" OR "):
            self.review_manager.logger.info(f"Explore '{keyword}'")
            # Skip keywords that were already explored
            if keyword in covered_keywords:
                continue
            nr_added = 0
            for item in retrieve_exploratory_papers(keyword=keyword):
                try:
                    retrieved_record_dict = connector_utils.json_to_record(item=item)

                    # Skip papers that do not have the keyword in the title
                    if keyword not in retrieved_record_dict.get(
                        "title", ""
                    ).lower().replace("-", " "):
                        continue

                    # Skip papers that were already retrieved
                    if retrieved_record_dict["doi"] in available_dois:
                        continue
                    retrieved_record_dict["explored_keyword"] = keyword
                    crossref_feed.set_id(record_dict=retrieved_record_dict)
                    retrieved_record = colrev.record.Record(data=retrieved_record_dict)
                    self.__prep_crossref_record(
                        record=retrieved_record, prep_main_record=False
                    )

                    self.__restore_url(record=retrieved_record, feed=crossref_feed)

                    added = crossref_feed.add_record(record=retrieved_record)

                    if added:
                        nr_added += 1
                        self.review_manager.logger.info(
                            " retrieve " + retrieved_record.data["doi"]
                        )
                    if nr_added >= 10:
                        break

                except (
                    colrev_exceptions.RecordNotParsableException,
                    colrev_exceptions.NotFeedIdentifiableException,
                    KeyError  # error in crossref package:
                    # if len(result['message']['items']) == 0:
                    # KeyError: 'items'
                ):
                    pass
                if nr_added < 10:
                    self.review_manager.logger.info(
                        f"Only {nr_added} papers found to resample keyword '{keyword}'"
                    )

        crossref_feed.print_post_run_search_infos(records=records)

        crossref_feed.save_feed_file()
        self.review_manager.dataset.save_records_dict(records=records)
        self.review_manager.dataset.add_record_changes()

        self.review_manager.dataset.format_records_file()
        self.review_manager.dataset.add_record_changes()
        self.review_manager.dataset.add_changes(path=self.search_source.filename)
        self.review_manager.create_commit(msg="Run search")

    def __run_api_search(
        self,
        *,
        crossref_feed: colrev.ops.search_feed.GeneralOriginFeed,
        rerun: bool,
    ) -> None:
        if rerun:
            self.review_manager.logger.info(
                "Performing a search of the full history (may take time)"
            )

        if self.search_source.search_parameters.get("mode", "") == "resample_keywords":
            self.__run_keyword_exploration_search(crossref_feed=crossref_feed)
            return

        records = self.review_manager.dataset.load_records_dict()
        for item in self.__get_crossref_query_return(rerun=rerun):
            try:
                retrieved_record_dict = connector_utils.json_to_record(item=item)
                crossref_feed.set_id(record_dict=retrieved_record_dict)
                prev_record_dict_version = {}
                if retrieved_record_dict["ID"] in crossref_feed.feed_records:
                    prev_record_dict_version = deepcopy(
                        crossref_feed.feed_records[retrieved_record_dict["ID"]]
                    )

                if self.__scope_excluded(retrieved_record_dict=retrieved_record_dict):
                    continue
                retrieved_record = colrev.record.Record(data=retrieved_record_dict)
                self.__prep_crossref_record(
                    record=retrieved_record, prep_main_record=False
                )

                self.__restore_url(record=retrieved_record, feed=crossref_feed)

                added = crossref_feed.add_record(record=retrieved_record)

                if added:
                    self.review_manager.logger.info(
                        " retrieve " + retrieved_record.data["doi"]
                    )
                else:
                    crossref_feed.update_existing_record(
                        records=records,
                        record_dict=retrieved_record.data,
                        prev_record_dict_version=prev_record_dict_version,
                        source=self.search_source,
                        update_time_variant_fields=rerun,
                    )

                # Note : only retrieve/update the latest deposits (unless in rerun mode)
                if not added and not rerun:
                    # problem: some publishers don't necessarily
                    # deposit papers chronologically
                    break
            except (
                colrev_exceptions.RecordNotParsableException,
                colrev_exceptions.NotFeedIdentifiableException,
                KeyError  # error in crossref package:
                # if len(result['message']['items']) == 0:
                # KeyError: 'items'
            ):
                pass

        crossref_feed.print_post_run_search_infos(records=records)

        crossref_feed.save_feed_file()
        self.review_manager.dataset.save_records_dict(records=records)
        self.review_manager.dataset.add_record_changes()

    def run_search(self, rerun: bool) -> None:
        """Run a search of Crossref"""

        self.__validate_source()

        crossref_feed = self.search_source.get_feed(
            review_manager=self.review_manager,
            source_identifier=self.source_identifier,
            update_only=(not rerun),
        )

        try:
            if self.search_source.search_type in [
                colrev.settings.SearchType.API,
                colrev.settings.SearchType.TOC,
            ]:
                self.__run_api_search(
                    crossref_feed=crossref_feed,
                    rerun=rerun,
                )
            elif self.search_source.search_type == colrev.settings.SearchType.MD:
                self.__run_md_search(
                    crossref_feed=crossref_feed,
                    rerun=rerun,
                )
            else:
                raise NotImplementedError

        except (requests.exceptions.RequestException,) as exc:
            # watch github issue:
            # https://github.com/fabiobatalha/crossrefapi/issues/46
            if "504 Gateway Time-out" in str(exc):
                raise colrev_exceptions.ServiceNotAvailableException(
                    self.__availability_exception_message
                )
            raise colrev_exceptions.ServiceNotAvailableException(
                self.__availability_exception_message
            )

    @classmethod
    def heuristic(cls, filename: Path, data: str) -> dict:
        """Source heuristic for Crossref"""

        result = {"confidence": 0.0}

        return result

    @classmethod
    def add_endpoint(
        cls,
        operation: colrev.ops.search.Search,
        params: str,
        filename: typing.Optional[Path],
    ) -> colrev.settings.SearchSource:
        """Add SearchSource as an endpoint"""

        if params and "https://search.crossref.org/?q=" in params:
            params = (
                params.replace("https://search.crossref.org/?q=", "")
                .replace("&from_ui=yes", "")
                .lstrip("+")
            )

            filename = operation.get_unique_filename(
                file_path_string=f"crossref_{params}"
            )
            add_source = colrev.settings.SearchSource(
                endpoint="colrev.crossref",
                filename=filename,
                search_type=colrev.settings.SearchType.DB,
                search_parameters={"query": params},
                comment="",
            )
            return add_source

        if params is not None:
            params_dict: typing.Dict[str, typing.Any] = {"scope": {}}
            for item in params.split(";"):
                key, value = item.split("=")
                if key in ["issn", "years"]:
                    params_dict["scope"][key] = value
                else:
                    params_dict[key] = value
            if not params_dict["scope"]:
                del params_dict["scope"]

            if "scope" not in params_dict and "query" not in params_dict:
                raise colrev_exceptions.InvalidQueryException(
                    "Query parameters must contain query or scope (such as issn)"
                )

            filename = operation.get_unique_filename(
                file_path_string=f"crossref_{params}"
            )
            add_source = colrev.settings.SearchSource(
                endpoint="colrev.crossref",
                filename=filename,
                search_type=colrev.settings.SearchType.DB,
                search_parameters=params_dict,
                comment="",
            )
            return add_source
        source = cls.__add_interactively(operation=operation)
        return source

    @classmethod
    def __add_interactively(
        cls, *, operation: colrev.ops.search.Search
    ) -> colrev.settings.SearchSource:
        print("Interactively add Crossref as a SearchSource")
        print()
        print("Documentation:")
        print(
            "https://github.com/CoLRev-Environment/colrev/blob/"
            + "main/colrev/ops/built_in/search_sources/crossref.md"
        )
        print()
        query_type = ""
        while query_type not in ["j", "k"]:
            query_type = input("Create a query based on [k]eywords or [j]ournal?")
        if query_type == "j":
            print("Get ISSN from https://portal.issn.org/issn/search")

            issn = ""
            while True:
                issn = input("Enter the ISSN (or journal name to lookup the ISSN):")
                if re.match(cls.__ISSN_REGEX, issn):
                    break

                journals = Journals()
                ret = journals.query(issn)
                for jour in ret:
                    print(f"{jour['title']}: {','.join(jour['ISSN'])}")

            filename = operation.get_unique_filename(
                file_path_string=f"crossref_issn_{issn}"
            )
            add_source = colrev.settings.SearchSource(
                endpoint="colrev.crossref",
                filename=filename,
                search_type=colrev.settings.SearchType.DB,
                search_parameters={"scope": {"issn": [issn]}},
                comment="",
            )
            return add_source

        # if query_type == "k":
        keywords = input("Enter the keywords:")

        filename = operation.get_unique_filename(
            file_path_string=f"crossref_{keywords}"
        )
        add_source = colrev.settings.SearchSource(
            endpoint="colrev.crossref",
            filename=filename,
            search_type=colrev.settings.SearchType.DB,
            search_parameters={"query": keywords},
            comment="",
        )
        return add_source

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
        """Source-specific preparation for Crossref"""

        source_item = [
            x
            for x in record.data["colrev_origin"]
            if str(source.filename).replace("data/search/", "") in x
        ]
        if source_item:
            record.set_masterdata_complete(
                source=source_item[0],
                masterdata_repository=self.review_manager.settings.is_curated_repo(),
            )

        return record
