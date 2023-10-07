from pathlib import Path

import daiquiri
import requests
from dbnomics import fetch_series
from pandas import DataFrame

from dbnomics_pptx_tools.cache import SeriesCache
from dbnomics_pptx_tools.metadata import SeriesId

logger = daiquiri.getLogger(__name__)


class SeriesRepo:
    def __init__(self, *, auto_fetch: bool = True, cache: SeriesCache, resume: bool = False, timeout: int) -> None:
        self._auto_fetch = auto_fetch
        self._cache = cache
        self._resume = resume
        self._timeout = timeout

        self._api_base_url = "https://api.db.nomics.world/v22"

    def fetch_csv(self, series_id: str) -> tuple[Path, str]:
        if self._resume:
            csv_result = self._cache.get_csv(series_id)
            if csv_result is not None:
                return csv_result

        if not self._auto_fetch:
            msg = f"The series {series_id!r} CSV is not in cache and auto_load is disabled"
            raise SeriesRepoError(msg, repo=self)

        csv_url = f"{self._api_base_url}/series/{series_id}.csv"
        response = requests.get(csv_url, timeout=self._timeout)
        response.raise_for_status()
        csv_text = response.content.decode("utf-8")  # response.encoding detects ISO-8859-1
        csv_relative_path = self._cache.set_csv(series_id, csv_text)
        return csv_relative_path, csv_text

    def load_df(self, series_id: str) -> DataFrame:
        if self._resume:
            series_df = self._cache.get_df(series_id)
            if series_df is not None:
                return series_df

        if not self._auto_fetch:
            msg = f"The series {series_id!r} DataFrame is not in cache and auto_load is disabled"
            raise SeriesRepoError(msg, repo=self)

        logger.debug("Fetching the series %r from DBnomics API...", series_id)
        df = self._fetch_series_df([series_id])
        self._cache.set_df(series_id, df)
        logger.debug("Series %r was fetched from DBnomics API and added to the cache", series_id)
        return df

    def _add_series_id_column(self, df: DataFrame) -> DataFrame:
        return df.assign(series_id=lambda row: row.provider_code + "/" + row.dataset_code + "/" + row.series_code)

    def _fetch_series_df(self, series_ids: list[SeriesId]) -> DataFrame:
        df: DataFrame = fetch_series(series_ids=series_ids, timeout=self._timeout)
        if df.empty:
            return df
        return self._add_series_id_column(df)


class SeriesRepoError(Exception):
    def __init__(self, message: str, *, repo: SeriesRepo) -> None:
        super().__init__(message)
        self.repo = repo
