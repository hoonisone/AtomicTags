"""Pack text_images folders and upload the release file list to Hugging Face."""
from __future__ import annotations

import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from taxonomy.step import Step

REPO_TYPE = "dataset"
COMMIT_MESSAGE = "Upload CSV files and text_images archives"


def require_metadata_files(
    dataset_dir: Path,
    splits: tuple[tuple[str, str, dict[str, Any]], ...],
) -> None:
    required = ["README.md", *[f"{split_name}/{csv_name}" for split_name, csv_name, _filters in splits]]
    missing = [relative for relative in required if not (dataset_dir / relative).is_file()]
    if missing:
        raise FileNotFoundError("Release files missing: " + ", ".join(missing))


def release_files(
    splits: tuple[tuple[str, str, dict[str, Any]], ...],
    archives: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    """CSV files, image archives, and the dataset card. Nothing else."""
    files = ["README.md"]
    files.extend(f"{split_name}/{csv_name}" for split_name, csv_name, _filters in splits)
    files.extend(
        f"{split_name}/{relative.replace(chr(92), '/')}"
        for split_name, relative in archives
    )
    return tuple(files)


def _folder_files(folder: Path) -> tuple[int, float]:
    count = 0
    newest = 0.0
    for path in folder.rglob("*"):
        if not path.is_file():
            continue
        count += 1
        newest = max(newest, path.stat().st_mtime)
    return count, newest


def archive_is_current(folder: Path, archive: Path) -> bool:
    if not archive.is_file():
        return False
    count, newest = _folder_files(folder)
    if count == 0:
        return False
    try:
        with tarfile.open(archive, "r") as handle:
            archived = sum(1 for member in handle.getmembers() if member.isfile())
    except (tarfile.TarError, OSError):
        return False
    if archived != count:
        return False
    return newest <= archive.stat().st_mtime + 1


def pack_text_images(folder: Path, archive: Path) -> str:
    """Write text_images.tar whose members start with text_images/."""
    if not folder.is_dir():
        if archive.is_file():
            print(f"archive already packed: {archive}")
            return "skipped"
        raise FileNotFoundError(f"Image folder not found: {folder}")
    count, _newest = _folder_files(folder)
    if count == 0:
        raise FileNotFoundError(f"Image folder is empty: {folder}")
    if archive_is_current(folder, archive):
        print(f"archive is current: {archive}")
        return "skipped"

    archive.parent.mkdir(parents=True, exist_ok=True)
    partial = archive.with_name(archive.name + ".partial")
    if partial.exists():
        partial.unlink()
    action = "updated" if archive.is_file() else "created"
    print(f"pack {count} files: {folder} -> {archive}")
    added = 0

    def _posix(member: tarfile.TarInfo) -> tarfile.TarInfo:
        nonlocal added
        member.name = member.name.replace("\\", "/")
        if member.isfile():
            added += 1
            if added % 2000 == 0:
                print(f"  {added} files")
        return member

    try:
        with tarfile.open(partial, "w") as handle:
            handle.add(folder, arcname="text_images", filter=_posix)
        partial.replace(archive)
    except Exception:
        if partial.exists():
            partial.unlink()
        raise
    print(f"{action}: {archive} ({archive.stat().st_size} bytes, {added} files)")
    return action


def pack_archives(
    dataset_dir: Path,
    archives: tuple[tuple[str, str], ...],
) -> dict[str, Any]:
    actions: dict[str, str] = {}
    for split_name, relative in archives:
        relative_posix = relative.replace("\\", "/")
        archive = dataset_dir / split_name / relative_posix
        folder = archive.parent / "text_images"
        actions[f"{split_name}/{relative_posix}"] = pack_text_images(folder, archive)
    return {"archives": actions}


def ensure_huggingface_login() -> str:
    try:
        from huggingface_hub import HfApi
    except ImportError as exc:
        raise RuntimeError(
            "huggingface_hub is required. Install it with: pip install -U huggingface_hub"
        ) from exc
    try:
        user = HfApi().whoami()
    except Exception as exc:
        raise RuntimeError("Hugging Face login is required. Run: hf auth login") from exc
    name = str(user.get("name") or user.get("fullname") or "")
    if not name:
        raise RuntimeError("Hugging Face login is required. Run: hf auth login")
    print(f"huggingface user: {name}")
    return name


def upload_files(dataset_dir: Path, repo_id: str, paths: tuple[str, ...]) -> dict[str, Any]:
    from huggingface_hub import CommitOperationAdd, HfApi

    missing = [relative for relative in paths if not (dataset_dir / relative).is_file()]
    if missing:
        listed = ", ".join(missing)
        raise FileNotFoundError(f"Release files missing: {listed}")

    total = sum((dataset_dir / relative).stat().st_size for relative in paths)
    print(f"upload {len(paths)} files ({total} bytes) to {repo_id}")
    for relative in paths:
        print(f"  {relative}")

    api = HfApi()
    api.create_repo(repo_id, repo_type=REPO_TYPE, exist_ok=True)
    operations = [
        CommitOperationAdd(
            path_in_repo=relative,
            path_or_fileobj=str(dataset_dir / relative),
        )
        for relative in paths
    ]
    commit = api.create_commit(
        repo_id=repo_id,
        repo_type=REPO_TYPE,
        operations=operations,
        commit_message=COMMIT_MESSAGE,
    )
    commit_url = getattr(commit, "commit_url", None) or str(commit)
    print(f"commit: {commit_url}")
    return {
        "repo_id": repo_id,
        "commit_url": commit_url,
        "files": list(paths),
        "bytes": total,
    }


@dataclass(kw_only=True)
class PackTextImagesStep(Step):
    dataset_dir: str
    archives: tuple[tuple[str, str], ...]

    def run(self) -> dict[str, Any]:
        return pack_archives(Path(self.dataset_dir), self.archives)


@dataclass(kw_only=True)
class UploadHuggingFaceStep(Step):
    dataset_dir: str
    repo_id: str
    paths: tuple[str, ...]

    def run(self) -> dict[str, Any]:
        return upload_files(Path(self.dataset_dir), self.repo_id, self.paths)
