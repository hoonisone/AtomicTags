"""Pipeline config for atomic multi-tag label files and tag statistics."""
from __future__ import annotations

import argparse
from pathlib import Path

from taxonomy.step import Pipeline
from taxonomy.steps.analyze_tag_statistics import AnalyzeTagStatisticsStep
from taxonomy.steps.make_tag_labels import MakeTagLabelFilesStep

SPLITS = (
    ("K_STR_Bench", "text.v1.0.csv", {"is_only_korean": True, "is_illegible": False}),
    ("Union14M_Benchmark", "text.v1.0.csv", {}),
    ("Union14M_General", "text_v.1.0.csv", {}),
)

PIPELINE_NAMES = ("make_tag_labels", "analyze_tag_statistics")


def build_pipelines(dataset_dir: Path) -> dict[str, Pipeline]:
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
    return {
        "make_tag_labels": Pipeline(name="make_tag_labels", steps=make_tag_labels_steps),
        "analyze_tag_statistics": Pipeline(
            name="analyze_tag_statistics",
            steps=analyze_tag_statistics_steps,
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build atomic multi-tag label files or tag statistics."
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_dir = Path(args.dataset_dir)
    build_pipelines(dataset_dir)[args.pipeline].run()


if __name__ == "__main__":
    main()
