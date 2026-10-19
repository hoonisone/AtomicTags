"""Count inclusive and exclusive tag coverage for an annotation CSV."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from taxonomy.step import Step
from taxonomy.tags import TAG_COLUMNS, is_true, row_matches, tag_name

CSV_ENCODING = "utf-8-sig"


def execute(
    csv_path: Path,
    output_dir: Path,
    column_value_filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    filters = dict(column_value_filters or {})
    with csv_path.open("r", encoding=CSV_ENCODING, newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {csv_path}")
        tag_columns = [column for column in TAG_COLUMNS if column in reader.fieldnames]
        if not tag_columns:
            raise ValueError(f"CSV has no tag columns: {csv_path}")
        missing = [column for column in filters if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing columns {missing}: {csv_path}")
        rows = [row for row in reader if row_matches(row, filters)]

    positive = {column: 0 for column in tag_columns}
    exclusive = {column: 0 for column in tag_columns}
    tag_count_hist: dict[int, int] = {}
    n_rows = len(rows)

    for row in rows:
        tags = [column for column in tag_columns if is_true(row.get(column))]
        tag_count_hist[len(tags)] = tag_count_hist.get(len(tags), 0) + 1
        for column in tags:
            positive[column] += 1
        if len(tags) == 1:
            exclusive[tags[0]] += 1

    output_dir.mkdir(parents=True, exist_ok=True)
    stats_path = output_dir / "tag_statistics.csv"
    with stats_path.open("w", encoding=CSV_ENCODING, newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "tag",
                "rows",
                "positive",
                "exclusive",
                "positive_ratio",
                "exclusive_among_positive",
            ],
        )
        writer.writeheader()
        for column in tag_columns:
            pos = positive[column]
            exc = exclusive[column]
            writer.writerow(
                {
                    "tag": tag_name(column),
                    "rows": n_rows,
                    "positive": pos,
                    "exclusive": exc,
                    "positive_ratio": f"{(pos / n_rows) if n_rows else 0:.6f}",
                    "exclusive_among_positive": f"{(exc / pos) if pos else 0:.6f}",
                }
            )

    count_path = output_dir / "tag_count.csv"
    with count_path.open("w", encoding=CSV_ENCODING, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["n_tags", "samples"])
        writer.writeheader()
        for n_tags in range(0, len(tag_columns) + 1):
            writer.writerow({"n_tags": n_tags, "samples": tag_count_hist.get(n_tags, 0)})

    print(f"{stats_path}: {len(tag_columns)} tags, rows={n_rows}")
    print(f"{count_path}: {sum(tag_count_hist.values())} samples")
    return {
        "csv_path": str(csv_path),
        "output_dir": str(output_dir),
        "column_value_filters": filters,
        "rows": n_rows,
        "tag_statistics": str(stats_path),
        "tag_count": str(count_path),
        "positive": {tag_name(column): positive[column] for column in tag_columns},
        "exclusive": {tag_name(column): exclusive[column] for column in tag_columns},
    }


@dataclass(kw_only=True)
class AnalyzeTagStatisticsStep(Step):
    csv_path: str
    output_dir: str
    column_value_filters: dict[str, Any] = field(default_factory=dict)

    def run(self) -> dict[str, Any]:
        return execute(
            Path(self.csv_path),
            Path(self.output_dir),
            column_value_filters=self.column_value_filters,
        )
