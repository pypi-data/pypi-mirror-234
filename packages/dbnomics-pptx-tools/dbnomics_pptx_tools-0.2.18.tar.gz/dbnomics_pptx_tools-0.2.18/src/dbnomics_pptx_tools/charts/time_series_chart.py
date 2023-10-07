from datetime import datetime
from typing import cast

import daiquiri
import numpy as np
from pandas import DataFrame, DatetimeIndex
from pptx.chart.chart import Chart
from pptx.chart.data import CategoryChartData
from pptx.shapes.graphfrm import GraphicFrame
from pptx.slide import Slide

from dbnomics_pptx_tools.data_loader import ShapeDataLoader
from dbnomics_pptx_tools.metadata import ChartSpec
from dbnomics_pptx_tools.repo import SeriesRepo

from .chart_data import replace_chart_data_or_recreate
from .data_labels import update_data_labels
from .series import update_series

logger = daiquiri.getLogger(__name__)


def build_category_chart_data(chart_spec: ChartSpec, *, pivoted_df: DataFrame) -> CategoryChartData:
    chart_data = CategoryChartData()

    index = pivoted_df.index
    chart_data.categories = index.to_pydatetime() if isinstance(index, DatetimeIndex) else index

    for series_spec in chart_spec.series:
        series_id = series_spec.id
        if series_id not in pivoted_df:
            logger.warning("Could not find series %r among downloaded DBnomics series, ignoring", series_id)
            continue
        series = pivoted_df[series_id]
        series = series.replace({np.NaN: None})
        series_attrs = pivoted_df.attrs.get(series_id, {})
        series_name = series_spec.name.format(**series_attrs)
        chart_data.add_series(series_name, series.values)

    return chart_data


def filter_df_to_domain(df: DataFrame, *, max_datetime: datetime | None, min_datetime: datetime | None) -> DataFrame:
    if min_datetime is not None:
        df = df.query("period >= @min_datetime")
    if max_datetime is not None:
        df = df.query("period <= @max_datetime")
    return df


def update_time_series_chart(
    chart_shape: GraphicFrame, *, chart_spec: ChartSpec, repo: SeriesRepo, slide: Slide
) -> None:
    chart = cast(Chart, chart_shape.chart)
    chart_series_df = ShapeDataLoader(repo).load_shape_df(chart_spec)
    pivoted_df = chart_series_df.pivot(index="period", columns="series_id", values="value")
    pivoted_df.attrs = chart_series_df.attrs
    chart_data = build_category_chart_data(chart_spec, pivoted_df=pivoted_df)
    replace_chart_data_or_recreate(chart_shape, chart_data=chart_data, slide=slide)
    update_data_labels(chart, chart_spec=chart_spec, pivoted_df=pivoted_df)
    update_series(chart, chart_series_attrs=chart_series_df.attrs, chart_spec=chart_spec)
