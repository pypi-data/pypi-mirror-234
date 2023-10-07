from collections.abc import Iterable, Iterator

import daiquiri
import pandas as pd
from more_itertools import partition
from pandas import DataFrame, Series

from dbnomics_pptx_tools.metadata import SeriesId, SeriesSpec, ShapeSpec
from dbnomics_pptx_tools.repo import SeriesRepo

logger = daiquiri.getLogger(__name__)


class ShapeDataLoader:
    def __init__(self, repo: SeriesRepo) -> None:
        self._repo = repo

    def load_dbnomics_series_spec_df(self, series_spec: SeriesSpec) -> DataFrame:
        series_id = series_spec.id
        df = self.load_series_df(series_id)
        self._apply_transformers(df, series_spec=series_spec)
        df["__display_name"] = series_spec.name
        return df

    def load_factory_series_spec_df(self, series_spec: SeriesSpec, *, series_so_far_df: DataFrame) -> DataFrame:
        series_id = series_spec.id
        factory_spec = series_spec.factory
        assert factory_spec is not None

        factory_spec_function = factory_spec._function  # noqa: SLF001

        result = factory_spec_function(series_so_far_df.copy(), **factory_spec.parameters)
        if not isinstance(result, DataFrame | Series):
            msg = f"Factory function {factory_spec_function.__qualname__!r} for series ID {series_id!r} must return a DataFrame or a Series, got {result!r}"  # noqa: E501
            raise TypeError(msg)

        logger.debug(
            "Factory function %r with parameters %r for series ID %r returned:\n%r",
            factory_spec_function.__qualname__,
            factory_spec.parameters,
            series_id,
            result,
        )
        df = self._post_process_factory_function_series(result) if isinstance(result, Series) else result
        df["series_id"] = series_id
        self._apply_transformers(df, series_spec=series_spec)

        display_name = series_spec.name.format(**df.attrs)
        df["__display_name"] = display_name
        return df

    def load_series_df(self, series_id: SeriesId) -> DataFrame:
        df = self._repo.load_df(series_id)
        if df.empty:
            msg = f"Series {series_id!r} is empty"
            raise ValueError(msg)
        return df

    def load_shape_df(self, shape_spec: ShapeSpec) -> DataFrame:
        factory_series_specs, dbnomics_series_specs = partition(
            lambda series_spec: series_spec.factory is None, shape_spec.series
        )

        data_source_series_dfs = list(self._iter_data_source_dfs(shape_spec.data_sources))
        dbnomics_series_dfs = list(self._iter_dbnomics_dfs(dbnomics_series_specs))

        loaded_series_dfs = data_source_series_dfs + dbnomics_series_dfs
        loaded_series_df = pd.concat(loaded_series_dfs) if loaded_series_dfs else DataFrame()
        factory_series_dfs = list(self._iter_factory_dfs(factory_series_specs, loaded_series_df))

        shape_series_dfs = dbnomics_series_dfs + factory_series_dfs

        if not shape_series_dfs:
            return DataFrame()

        shape_series_df = pd.concat(shape_series_dfs)
        shape_series_df.attrs = {df["series_id"].values[0]: df.attrs for df in shape_series_dfs}
        return shape_series_df

    def _apply_transformers(self, df: pd.DataFrame, *, series_spec: SeriesSpec) -> None:
        transformers = series_spec._transformers  # noqa: SLF001
        if not transformers:
            return

        series_id = series_spec.id
        series = df["value"]
        df["__value_before_transformers"] = series
        for transformer in transformers:
            logger.debug("Applying transformer %r to series %r", transformer.__qualname__, series_id)
            series = transformer(series)
            if not isinstance(series, Series):
                msg = f"Transformer function {transformer.__qualname__!r} did not return a Series, got {series!r}"
                raise TypeError(msg)

        df["value"] = series

    def _iter_data_source_dfs(self, series_ids_to_load: Iterable[SeriesId]) -> Iterator[DataFrame]:
        for series_id in series_ids_to_load:
            try:
                yield self.load_series_df(series_id)
            except ValueError as exc:
                logger.warning("Could not load DataFrame for data source series ID %r: %s", series_id, exc)

    def _iter_dbnomics_dfs(self, dbnomics_series_specs: Iterable[SeriesSpec]) -> Iterator[DataFrame]:
        for dbnomics_series_spec in dbnomics_series_specs:
            try:
                yield self.load_dbnomics_series_spec_df(dbnomics_series_spec)
            except ValueError as exc:
                logger.warning("Could not load DataFrame for DBnomics series ID %r: %s", dbnomics_series_spec.id, exc)

    def _iter_factory_dfs(
        self, factory_series_specs: Iterable[SeriesSpec], loaded_series_df: DataFrame
    ) -> Iterator[DataFrame]:
        series_so_far_df = loaded_series_df
        for factory_series_spec in factory_series_specs:
            factory = factory_series_spec.factory
            assert factory is not None
            try:
                factory_df = self.load_factory_series_spec_df(factory_series_spec, series_so_far_df=series_so_far_df)
            except Exception:
                logger.exception(
                    "Could not load series from factory function %r with parameters %r, ignoring",
                    factory._function.__qualname__,  # noqa: SLF001
                    factory.parameters,
                )
            else:
                yield factory_df
                if "period" in factory_df.columns:
                    series_so_far_df = pd.concat([series_so_far_df, factory_df])

    def _post_process_factory_function_series(self, series: Series) -> DataFrame:
        df: DataFrame = series.rename("value").reset_index()
        return df
