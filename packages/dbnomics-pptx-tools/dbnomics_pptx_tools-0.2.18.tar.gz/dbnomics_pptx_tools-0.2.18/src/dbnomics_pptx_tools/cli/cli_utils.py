from pathlib import Path

import daiquiri
import typer
import yaml
from pptx import Presentation as _open_presentation  # noqa: N813
from pptx.presentation import Presentation
from typer import FileBinaryRead

from dbnomics_pptx_tools.cli.slide_expr import parse_slide_expr, parse_slides_expr, slide_to_number
from dbnomics_pptx_tools.metadata import PresentationMetadata

logger = daiquiri.getLogger(__name__)


def load_presentation_metadata(metadata_file: Path) -> PresentationMetadata:
    logger.debug("Loading presentation metadata from %r...", str(metadata_file))
    presentation_metadata_data = yaml.safe_load(metadata_file.read_text())
    return PresentationMetadata.parse_obj(presentation_metadata_data)


def open_presentation(input_pptx_file: FileBinaryRead) -> Presentation:
    logger.debug("Loading presentation from %r...", str(input_pptx_file.name))
    prs: Presentation = _open_presentation(input_pptx_file)
    return prs


def parse_slide_option(expr: str, *, slide_ids: list[str | None]) -> int:
    try:
        slide = parse_slide_expr(expr)
    except Exception as exc:
        msg = f"Could not parse {expr!r}"
        raise typer.BadParameter(msg) from exc

    try:
        return slide_to_number(slide, slide_ids=slide_ids)
    except ValueError as exc:
        msg = f"Invalid slide expression {expr!r}: {exc}"
        raise typer.BadParameter(msg) from exc


def parse_slides_option(expr: str, *, slide_ids: list[str | None]) -> list[int]:
    try:
        slides = list(parse_slides_expr(expr))
    except Exception as exc:
        msg = f"Could not parse {expr!r}"
        raise typer.BadParameter(msg) from exc

    return [slide_to_number(slide, slide_ids=slide_ids) for slide in slides]
