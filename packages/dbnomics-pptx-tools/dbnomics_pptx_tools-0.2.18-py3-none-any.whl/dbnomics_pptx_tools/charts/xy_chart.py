from typing import cast

import daiquiri
from pandas import DataFrame
from pptx.chart.chart import Chart
from pptx.chart.data import XyChartData
from pptx.shapes.graphfrm import GraphicFrame
from pptx.slide import Slide

from dbnomics_pptx_tools.charts.data_labels import update_data_labels
from dbnomics_pptx_tools.data_loader import ShapeDataLoader
from dbnomics_pptx_tools.metadata import ChartSpec
from dbnomics_pptx_tools.repo import SeriesRepo

from .chart_data import replace_chart_data_or_recreate
from .series import update_series

logger = daiquiri.getLogger(__name__)


def build_xy_chart_data(chart_spec: ChartSpec, *, chart_series_df: DataFrame) -> XyChartData:
    chart_data = XyChartData()
    for series_spec in chart_spec.series:
        series = chart_data.add_series(series_spec.name)
        series_df = chart_series_df[chart_series_df["series_id"] == series_spec.id]
        for _, row in series_df.iterrows():
            series.add_data_point(row["X"], row["Y"])
    return chart_data


def update_xy_scatter_lines_chart(
    chart_shape: GraphicFrame, *, chart_spec: ChartSpec, repo: SeriesRepo, slide: Slide
) -> None:
    chart = cast(Chart, chart_shape.chart)
    chart_series_df = ShapeDataLoader(repo).load_shape_df(chart_spec)
    chart_series_df = chart_series_df.dropna()
    chart_data = build_xy_chart_data(chart_spec, chart_series_df=chart_series_df)
    replace_chart_data_or_recreate(chart_shape, chart_data=chart_data, slide=slide)
    update_data_labels(chart, chart_spec=chart_spec, pivoted_df=chart_series_df)
    update_series(chart, chart_series_attrs=chart_series_df.attrs, chart_spec=chart_spec)
