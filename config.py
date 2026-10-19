"""Pipeline config for atomic multi-tag label files and tag statistics."""
from __future__ import annotations

from pathlib import Path

from taxonomy.step import Pipeline
from taxonomy.steps.analyze_tag_statistics import AnalyzeTagStatisticsStep
from taxonomy.steps.make_tag_labels import MakeTagLabelFilesStep

DATASET_DIR = Path(r"S:\02 Datasets\3_Atomic_Multi_Tag_Taxonomy_huggingface")

SPLITS = (
    ("K_STR_Bench", "text.v1.0.csv", {"is_only_korean": True, "is_illegible": False}),
    ("Union14M_Benchmark", "text.v1.0.csv", {}),
    ("Union14M_General", "text_v.1.0.csv", {}),
)

make_tag_labels_steps = [
    MakeTagLabelFilesStep(
        name=split_name,
        csv_path=str(DATASET_DIR / split_name / csv_name),
        labels_dir=str(DATASET_DIR / split_name / "labels"),
        column_value_filters=column_value_filters,
    )
    for split_name, csv_name, column_value_filters in SPLITS
]

analyze_tag_statistics_steps = [
    AnalyzeTagStatisticsStep(
        name=split_name,
        csv_path=str(DATASET_DIR / split_name / csv_name),
        output_dir=str(DATASET_DIR / split_name / "analysis"),
        column_value_filters=column_value_filters,
    )
    for split_name, csv_name, column_value_filters in SPLITS
]

pipelines = {
    "make_tag_labels": Pipeline(name="make_tag_labels", steps=make_tag_labels_steps),
    "analyze_tag_statistics": Pipeline(
        name="analyze_tag_statistics",
        steps=analyze_tag_statistics_steps,
    ),
}


def main() -> None:
    pipelines["make_tag_labels"].run()
    pipelines["analyze_tag_statistics"].run()


if __name__ == "__main__":
    main()
