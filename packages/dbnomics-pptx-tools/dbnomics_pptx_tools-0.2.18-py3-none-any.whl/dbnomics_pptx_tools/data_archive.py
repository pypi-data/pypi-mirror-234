import zipfile
from pathlib import Path

from dbnomics_pptx_tools.metadata import PresentationMetadata
from dbnomics_pptx_tools.repo import SeriesRepo


def save_data_archive_file(*, output_file: Path, presentation_metadata: PresentationMetadata, repo: SeriesRepo) -> None:
    fetchable_series_ids = presentation_metadata.find_fetchable_series_ids()
    with zipfile.ZipFile(output_file, mode="w") as zf:
        for series_id in fetchable_series_ids:
            csv_relative_path, csv_text = repo.fetch_csv(series_id)
            zf.writestr(str(csv_relative_path), csv_text)
