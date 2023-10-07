from typing import cast

import daiquiri
from more_itertools import first
from pptx.chart.chart import Chart
from pptx.enum.chart import XL_CHART_TYPE
from pptx.shapes.graphfrm import GraphicFrame
from pptx.slide import Slide

from dbnomics_pptx_tools.metadata import ChartSpec
from dbnomics_pptx_tools.repo import SeriesRepo

from .time_series_chart import update_time_series_chart
from .xy_chart import update_xy_scatter_lines_chart

logger = daiquiri.getLogger(__name__)


def update_chart(chart_shape: GraphicFrame, *, chart_spec: ChartSpec, repo: SeriesRepo, slide: Slide) -> None:
    chart = cast(Chart, chart_shape.chart)
    if chart.chart_type in {XL_CHART_TYPE.LINE, XL_CHART_TYPE.LINE_MARKERS}:
        update_time_series_chart(chart_shape, chart_spec=chart_spec, repo=repo, slide=slide)
    elif chart.chart_type == XL_CHART_TYPE.XY_SCATTER_LINES:
        update_xy_scatter_lines_chart(chart_shape, chart_spec=chart_spec, repo=repo, slide=slide)
    else:
        chart_type_name = first(m.name for m in XL_CHART_TYPE.__members__ if m.value == chart.chart_type)
        raise NotImplementedError(chart_type_name)
