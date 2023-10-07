from collections.abc import Iterator
from typing import Any

import daiquiri
from pptx.chart.chart import Chart
from pptx.chart.series import _BaseCategorySeries

from dbnomics_pptx_tools.metadata import ChartSpec, SeriesSpec

logger = daiquiri.getLogger(__name__)


def iter_chart_series_with_spec(
    chart: Chart,
    *,
    chart_series_attrs: dict[str, dict[str, Any]],
    chart_spec: ChartSpec,
) -> Iterator[tuple[_BaseCategorySeries, SeriesSpec]]:
    chart_series_by_name = {chart_series.name: chart_series for chart_series in chart.series}
    for series_spec in chart_spec.series:
        series_attrs = chart_series_attrs.get(series_spec.id, {})
        series_name = series_spec.name.format(**series_attrs)
        chart_series = chart_series_by_name.get(series_name)
        if chart_series is None:
            logger.warning("Could not find the chart series corresponding to the series name %r, ignoring", series_name)
            continue
        yield chart_series, series_spec
