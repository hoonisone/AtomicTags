"""Build inclusive and exclusive tag label files from an annotation CSV."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from taxonomy.step import Step
from taxonomy.tags import TAG_COLUMNS, is_true, row_matches, tag_name

CSV_ENCODING = "utf-8-sig"
TXT_ENCODING = "utf-8"
TEXT_IMAGES_MARKER = "text_images/"


def norm_path(path_text: str) -> str:
    return str(path_text or "").strip().replace("\\", "/")


def crop_filename(image_path: str) -> str:
    rel = norm_path(image_path).lstrip("/")
    index = rel.find(TEXT_IMAGES_MARKER)
    if index >= 0:
        return rel[index + len(TEXT_IMAGES_MARKER) :]
    return rel


def clean_text(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def positive_tags(row: dict[str, str], tag_columns: list[str]) -> list[str]:
    return [column for column in tag_columns if is_true(row.get(column))]


def parse_positive_int(value: object) -> int | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        number = int(float(text))
    except ValueError:
        return None
    if number <= 0:
        return None
    return number


def jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            prefix = handle.read(1)
            if prefix != b"\xff":
                if not prefix:
                    return None
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9", b""}:
                if not marker:
                    return None
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) < 2:
                return None
            length = int.from_bytes(length_bytes, "big")
            if length < 2:
                return None
            if marker in {b"\xc0", b"\xc1", b"\xc2"}:
                segment = handle.read(5)
                if len(segment) < 5:
                    return None
                height = int.from_bytes(segment[1:3], "big")
                width = int.from_bytes(segment[3:5], "big")
                if width <= 0 or height <= 0:
                    return None
                return width, height
            handle.seek(length - 2, 1)


def sample_size(row: dict[str, str], image_file: Path) -> tuple[int, int] | None:
    width = parse_positive_int(row.get("width"))
    height = parse_positive_int(row.get("height"))
    if width and height:
        return width, height
    if image_file.is_file():
        return jpeg_size(image_file)
    return None


def format_txt(filename: str, text: str) -> str:
    return f"{filename}\t{text}\n"


def format_jsonl(filename: str, text: str, width: int, height: int) -> str:
    payload = {
        "filename": filename,
        "text": text,
        "width": width,
        "height": height,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def write_lines(path: Path, lines: list[str]) -> int:
    if not lines:
        print(f"{path}: skip (empty)")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding=TXT_ENCODING)
    print(f"{path}: {len(lines)}")
    return len(lines)


def execute(
    csv_path: Path,
    labels_dir: Path,
    column_value_filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    filters = dict(column_value_filters or {})
    split_dir = csv_path.parent
    with csv_path.open("r", encoding=CSV_ENCODING, newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {csv_path}")
        tag_columns = [column for column in TAG_COLUMNS if column in reader.fieldnames]
        if not tag_columns:
            raise ValueError(f"CSV has no tag columns: {csv_path}")
        missing = [column for column in ("image_path", "label", *filters) if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing columns {missing}: {csv_path}")
        rows = list(reader)

    grouped: dict[str, dict[str, list[str]]] = {
        "inclusive": {column: [] for column in tag_columns},
        "exclusive": {column: [] for column in tag_columns},
    }
    grouped_jsonl: dict[str, dict[str, list[str]]] = {
        "inclusive": {column: [] for column in tag_columns},
        "exclusive": {column: [] for column in tag_columns},
    }
    skipped = 0
    filtered_out = 0

    for row in rows:
        if not row_matches(row, filters):
            filtered_out += 1
            continue
        text = clean_text(row.get("label"))
        image_path = norm_path(row.get("image_path") or "")
        if not text or not image_path:
            skipped += 1
            continue
        filename = crop_filename(image_path)
        size = sample_size(row, split_dir / image_path)
        if size is None:
            skipped += 1
            continue
        tags = positive_tags(row, tag_columns)
        if not tags:
            continue
        txt_line = format_txt(filename, text)
        jsonl_line = format_jsonl(filename, text, size[0], size[1])
        for column in tags:
            grouped["inclusive"][column].append(txt_line)
            grouped_jsonl["inclusive"][column].append(jsonl_line)
        if len(tags) == 1:
            column = tags[0]
            grouped["exclusive"][column].append(txt_line)
            grouped_jsonl["exclusive"][column].append(jsonl_line)

    written: dict[str, dict[str, int]] = {"inclusive": {}, "exclusive": {}}
    for mode in ("inclusive", "exclusive"):
        for column in tag_columns:
            stem = tag_name(column)
            folder = labels_dir / mode
            written[mode][stem] = write_lines(folder / f"{stem}.txt", grouped[mode][column])
            write_lines(folder / f"{stem}.jsonl", grouped_jsonl[mode][column])

    return {
        "csv_path": str(csv_path),
        "labels_dir": str(labels_dir),
        "rows": len(rows),
        "column_value_filters": filters,
        "filtered_out": filtered_out,
        "skipped": skipped,
        "tags": [tag_name(column) for column in tag_columns],
        "inclusive": written["inclusive"],
        "exclusive": written["exclusive"],
    }


@dataclass(kw_only=True)
class MakeTagLabelFilesStep(Step):
    csv_path: str
    labels_dir: str
    column_value_filters: dict[str, Any] = field(default_factory=dict)

    def run(self) -> dict[str, Any]:
        return execute(
            Path(self.csv_path),
            Path(self.labels_dir),
            column_value_filters=self.column_value_filters,
        )
