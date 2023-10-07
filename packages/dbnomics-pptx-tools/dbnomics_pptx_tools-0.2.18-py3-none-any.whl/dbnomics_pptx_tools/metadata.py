from collections.abc import Callable
from enum import Enum
from itertools import chain
from typing import Any, Literal, TypeAlias, cast

import daiquiri
import isodate
import pandas as pd
import webcolors
from isodate import Duration
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pydantic import BaseModel, Field, PrivateAttr, StrictStr, validator
from webcolors import IntegerRGB

from dbnomics_pptx_tools.module_utils import parse_callable

logger = daiquiri.getLogger(__name__)


ChartName: TypeAlias = str
Frequency: TypeAlias = Literal["annual", "monthly", "quarterly"]
SeriesId: TypeAlias = str
SeriesFactory: TypeAlias = Callable[..., pd.DataFrame | pd.Series]
SeriesTransformer: TypeAlias = Callable[[pd.Series], pd.Series]
TableLocation: TypeAlias = str


def parse_dash_style(value: str) -> int:
    try:
        return cast(int, getattr(MSO_LINE_DASH_STYLE, value))
    except AttributeError as exc:
        available = [member.name for member in MSO_LINE_DASH_STYLE.__members__]
        msg = f"Invalid dash_style: {value!r}. Available values: {available!r}"
        raise ValueError(msg) from exc


def parse_entry_point(value: str) -> Callable[..., Any]:
    if not isinstance(value, str):
        msg = f"str expected, got {type(value)}"
        raise TypeError(msg)
    function = parse_callable(value)
    if function is None:
        msg = f"The function referenced by {value!r} does not exist"
        raise ValueError(msg)
    return function


class FactorySpec(BaseModel):
    function: str
    parameters: dict[str, str] = Field(default_factory=dict)

    _function: SeriesFactory = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._function = staticmethod(parse_entry_point(self.function))


class SeriesFormatSpec(BaseModel):
    color: str | None = None
    dash_style: str | None = None
    width: int | None = None

    _color: IntegerRGB | None = PrivateAttr()
    _dash_style: int | None = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._color = None if self.color is None else webcolors.name_to_rgb(self.color)
        self._dash_style = None if self.dash_style is None else parse_dash_style(self.dash_style)


class SeriesSpec(BaseModel):
    id: str  # noqa: A003
    name: str

    format: SeriesFormatSpec | None = None  # noqa: A003
    factory: FactorySpec | None = None
    transformers: list[str] = Field(default_factory=list)

    _transformers: list[SeriesTransformer] = PrivateAttr(default_factory=list)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._transformers = [parse_entry_point(transformer_str) for transformer_str in self.transformers]

    def is_fetchable(self) -> bool:
        return self.factory is None


class ShapeSpec(BaseModel):
    data_sources: list[SeriesId] = Field(default_factory=list)
    series: list[SeriesSpec]

    def find_fetchable_series_ids(self) -> list[SeriesId]:
        return sorted(
            set(chain((series_spec.id for series_spec in self.series if series_spec.is_fetchable()), self.data_sources))
        )

    @validator("series")
    def validate_series_name_is_unique(cls, value: list[SeriesSpec]) -> list[SeriesSpec]:
        series_names = {series_spec.name for series_spec in value}
        if len(series_names) != len(value):
            msg = "Series names must be unique"
            raise ValueError(msg)
        return value


class DataLabelPosition(Enum):
    ALL_POINTS = "all_points"
    FIRST_AND_LAST_POINTS = "first_and_last_points"
    LAST_POINT = "last_point"
    NONE = "none"


class DataLabelShow(Enum):
    PERIOD = "period"
    VALUE = "value"


class DataLabelSpec(BaseModel):
    position: DataLabelPosition
    number_format: StrictStr = "0.0"
    show: DataLabelShow = DataLabelShow.VALUE


class ChartSpec(ShapeSpec):
    data_labels: DataLabelPosition | DataLabelSpec = DataLabelPosition.NONE

    def get_data_label_spec(self) -> DataLabelSpec:
        data_labels = self.data_labels
        if isinstance(data_labels, DataLabelPosition):
            return DataLabelSpec(position=data_labels)
        return data_labels


class ColumnsSpec(BaseModel):
    end_period_offset: str | None
    frequency: Frequency
    period_format: str

    _end_period_offset: Duration | None = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._end_period_offset = (
            None if self.end_period_offset is None else isodate.parse_duration(self.end_period_offset)
        )


class TableSpec(ShapeSpec):
    columns: ColumnsSpec | None
    header_first_cell: str = "Country"


class SlideMetadata(BaseModel):
    charts: dict[ChartName, ChartSpec] = Field(default_factory=dict)
    tables: dict[TableLocation, TableSpec] = Field(default_factory=dict)

    def find_fetchable_series_ids(self) -> set[SeriesId]:
        series_ids = set()
        for chart_spec in self.charts.values():
            series_ids |= set(chart_spec.find_fetchable_series_ids())
        for table_spec in self.tables.values():
            series_ids |= set(table_spec.find_fetchable_series_ids())
        return series_ids


class PresentationMetadata(BaseModel):
    slides: dict[str, SlideMetadata]

    def find_fetchable_series_ids(self) -> set[SeriesId]:
        result = set()
        for slide in self.slides.values():
            result |= slide.find_fetchable_series_ids()
        return result
