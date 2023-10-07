from typing import TYPE_CHECKING, Any

from pptx.chart.chart import Chart
from pptx.chart.series import _BaseCategorySeries
from pptx.dml.color import RGBColor
from pptx.util import Pt

from dbnomics_pptx_tools.charts.utils import iter_chart_series_with_spec
from dbnomics_pptx_tools.metadata import ChartSpec, SeriesFormatSpec

if TYPE_CHECKING:
    from pptx.dml.line import LineFormat


def update_series(chart: Chart, *, chart_series_attrs: dict[str, dict[str, Any]], chart_spec: ChartSpec) -> None:
    for chart_series, series_spec in iter_chart_series_with_spec(
        chart, chart_series_attrs=chart_series_attrs, chart_spec=chart_spec
    ):
        format_spec = series_spec.format
        if format_spec is not None:
            update_series_format(chart_series, format_spec=format_spec)


def update_series_format(chart_series: _BaseCategorySeries, *, format_spec: SeriesFormatSpec) -> None:
    line_format: LineFormat = chart_series.format.line

    color = format_spec._color  # noqa: SLF001
    if color is not None:
        line_format.fill.fore_color.rgb = RGBColor(*color)

    dash_style = format_spec._dash_style  # noqa: SLF001
    if dash_style is not None:
        line_format.dash_style = dash_style

    width = format_spec.width
    if width is not None:
        line_format.width = Pt(width)
