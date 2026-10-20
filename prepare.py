"""Pipeline config for label files, tag statistics, and the Hugging Face release."""
from __future__ import annotations

import argparse
import tarfile
from pathlib import Path

from taxonomy.step import Pipeline
from taxonomy.steps.analyze_tag_statistics import AnalyzeTagStatisticsStep
from taxonomy.steps.make_tag_labels import MakeTagLabelFilesStep
from taxonomy.steps.upload_huggingface import (
    PackTextImagesStep,
    UploadHuggingFaceStep,
    ensure_huggingface_login,
    release_files,
    require_metadata_files,
)

SPLITS = (
    ("K_STR_Bench", "text.v1.0.csv", {}),
    ("Union14M_Benchmark", "text.v1.0.csv", {}),
    ("Union14M_General", "text_v.1.0.csv", {}),
)

PIPELINE_NAMES = ("make_tag_labels", "analyze_tag_statistics", "upload_huggingface")

HUGGINGFACE_REPO_ID = "hoonisone/AtomicTags"

IMAGE_ARCHIVES = (
    ("K_STR_Bench", "GIST_Signboard/text_images.tar"),
    ("K_STR_Bench", "KAIST_Corrected/text_images.tar"),
    ("Union14M_Benchmark", "text_images.tar"),
    ("Union14M_General", "text_images.tar"),
)


def _archive_has_text_images_dir(names: list[str]) -> bool:
    for name in names:
        relative = name.replace("\\", "/").lstrip("./")
        if relative == "text_images" or relative.startswith("text_images/"):
            return True
    return False


def extract_text_images(archive: Path) -> None:
    """Extract text_images.tar next to the text_images folder it recreates."""
    folder = archive.parent / "text_images"
    if folder.is_dir():
        print(f"images already extracted: {folder}")
        return
    print(f"extract: {archive}")
    with tarfile.open(archive, "r") as handle:
        names = [member.name for member in handle.getmembers()]
        if _archive_has_text_images_dir(names):
            handle.extractall(archive.parent, filter="data")
            return
        folder.mkdir(parents=True, exist_ok=True)
        handle.extractall(folder, filter="data")


def extract_image_archives(dataset_dir: Path) -> None:
    for split_name, relative_archive in IMAGE_ARCHIVES:
        archive = dataset_dir / split_name / relative_archive
        if archive.is_file():
            extract_text_images(archive)


def build_pipelines(dataset_dir: Path, repo_id: str) -> dict[str, Pipeline]:
    make_tag_labels_steps = [
        MakeTagLabelFilesStep(
            name=split_name,
            csv_path=str(dataset_dir / split_name / csv_name),
            labels_dir=str(dataset_dir / split_name / "labels"),
            column_value_filters=column_value_filters,
        )
        for split_name, csv_name, column_value_filters in SPLITS
    ]
    analyze_tag_statistics_steps = [
        AnalyzeTagStatisticsStep(
            name=split_name,
            csv_path=str(dataset_dir / split_name / csv_name),
            output_dir=str(dataset_dir / split_name / "analysis"),
            column_value_filters=column_value_filters,
        )
        for split_name, csv_name, column_value_filters in SPLITS
    ]
    upload_paths = release_files(SPLITS, IMAGE_ARCHIVES)
    return {
        "make_tag_labels": Pipeline(name="make_tag_labels", steps=make_tag_labels_steps),
        "analyze_tag_statistics": Pipeline(
            name="analyze_tag_statistics",
            steps=analyze_tag_statistics_steps,
        ),
        "upload_huggingface": Pipeline(
            name="upload_huggingface",
            steps=[
                PackTextImagesStep(
                    name="pack_text_images",
                    dataset_dir=str(dataset_dir),
                    archives=IMAGE_ARCHIVES,
                ),
                UploadHuggingFaceStep(
                    name="upload_files",
                    dataset_dir=str(dataset_dir),
                    repo_id=repo_id,
                    paths=upload_paths,
                ),
            ],
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build label files, tag statistics, or upload the Hugging Face release."
    )
    parser.add_argument(
        "--dataset-dir",
        required=True,
        help="Folder that contains K_STR_Bench, Union14M_Benchmark, and Union14M_General.",
    )
    parser.add_argument(
        "--pipeline",
        required=True,
        choices=PIPELINE_NAMES,
        help="Pipeline to run.",
    )
    parser.add_argument(
        "--repo-id",
        default=HUGGINGFACE_REPO_ID,
        help="Hugging Face dataset repo. Used by upload_huggingface.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_dir = Path(args.dataset_dir)
    if args.pipeline == "upload_huggingface":
        ensure_huggingface_login()
        require_metadata_files(dataset_dir, SPLITS)
    else:
        extract_image_archives(dataset_dir)
    build_pipelines(dataset_dir, args.repo_id)[args.pipeline].run()


if __name__ == "__main__":
    main()
