#!/usr/bin/env python3
"""Validate the shared ModelSuite release files in modelfinder-db."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any


REQUIRED_LATEST_FIELDS = [
    "manifest_version",
    "app",
    "version",
    "platform",
    "package_type",
    "download_url",
    "sha256",
    "size_bytes",
    "filename",
    "repo_path",
    "created_at",
    "notes",
]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def canonical_rows_sha256(rows: list[dict[str, Any]]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(payload)


def download_bytes(url: str, timeout: int = 20) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ModelSuite-Release-Verify/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def norm_sha(value: Any) -> str:
    return str(value or "").strip().lower()


def add_error(errors: list[str], message: str) -> None:
    errors.append(f"ERROR: {message}")


def add_warning(warnings: list[str], message: str) -> None:
    warnings.append(f"WARN: {message}")


def validate_latest_manifest(repo: Path, filename: str, errors: list[str], warnings: list[str], remote: bool) -> None:
    path = repo / filename
    if not path.exists():
        add_error(errors, f"{filename} fehlt.")
        return
    try:
        manifest = read_json(path)
    except Exception as exc:
        add_error(errors, f"{filename} ist kein gueltiges JSON: {exc}")
        return
    if not isinstance(manifest, dict):
        add_error(errors, f"{filename} muss ein JSON-Objekt enthalten.")
        return

    for field in REQUIRED_LATEST_FIELDS:
        if field not in manifest or str(manifest.get(field, "")).strip() == "":
            add_error(errors, f"{filename}: Feld {field} fehlt oder ist leer.")

    repo_path = repo / str(manifest.get("repo_path", ""))
    if repo_path.exists():
        actual_size = repo_path.stat().st_size
        expected_size = int(manifest.get("size_bytes", -1) or -1)
        if actual_size != expected_size:
            add_error(errors, f"{filename}: size_bytes={expected_size}, Datei hat {actual_size} Bytes.")
        actual_sha = sha256_file(repo_path)
        if norm_sha(manifest.get("sha256")) and actual_sha != norm_sha(manifest.get("sha256")):
            add_error(errors, f"{filename}: sha256 passt nicht zu {manifest.get('repo_path')}.")
    else:
        add_error(errors, f"{filename}: repo_path existiert nicht: {manifest.get('repo_path')}")

    if remote and manifest.get("download_url"):
        try:
            payload = download_bytes(str(manifest["download_url"]))
            expected_size = int(manifest.get("size_bytes", -1) or -1)
            if len(payload) != expected_size:
                add_error(errors, f"{filename}: Remote-Groesse passt nicht ({len(payload)} statt {expected_size}).")
            if sha256_bytes(payload) != norm_sha(manifest.get("sha256")):
                add_error(errors, f"{filename}: Remote-sha256 passt nicht.")
        except Exception as exc:
            add_error(errors, f"{filename}: Remote-Download fehlgeschlagen: {exc}")

    if repo_path.exists() and repo_path.stat().st_size > 50 * 1024 * 1024:
        add_warning(warnings, f"{manifest.get('filename', filename)} ist groesser als 50 MB.")


def validate_model_manifest(repo: Path, errors: list[str], warnings: list[str], remote: bool) -> None:
    model_path = repo / "model.json"
    manifest_path = repo / "model_manifest.json"
    if not model_path.exists():
        add_error(errors, "model.json fehlt.")
        return
    if not manifest_path.exists():
        add_error(errors, "model_manifest.json fehlt.")
        return

    try:
        rows_raw = read_json(model_path)
        manifest = read_json(manifest_path)
    except Exception as exc:
        add_error(errors, f"model.json/model_manifest.json ist nicht lesbar: {exc}")
        return

    if not isinstance(rows_raw, list):
        add_error(errors, "model.json muss eine JSON-Liste sein.")
        return
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows_raw, start=1):
        if not isinstance(row, dict):
            add_error(errors, f"model.json Eintrag {index} ist kein Objekt.")
        else:
            rows.append(row)
    if not isinstance(manifest, dict):
        add_error(errors, "model_manifest.json muss ein JSON-Objekt sein.")
        return

    expected_count = int(manifest.get("models_count", -1) or -1)
    if expected_count != len(rows_raw):
        add_error(errors, f"model_manifest.json: models_count={expected_count}, model.json enthaelt {len(rows_raw)}.")

    local_file_sha = sha256_file(model_path)
    stored_local_file_sha = norm_sha(manifest.get("local_file_sha256"))
    if stored_local_file_sha and local_file_sha != stored_local_file_sha:
        add_error(errors, "model_manifest.json: local_file_sha256 passt nicht zur lokalen model.json.")

    canonical_sha = canonical_rows_sha256(rows)
    stored_canonical_sha = norm_sha(manifest.get("canonical_sha256"))
    if stored_canonical_sha and canonical_sha != stored_canonical_sha:
        add_error(errors, "model_manifest.json: canonical_sha256 passt nicht zur normalisierten model.json.")

    for field in ["version", "sha256", "updated_at", "database_url"]:
        if not str(manifest.get(field, "")).strip():
            add_error(errors, f"model_manifest.json: Feld {field} fehlt oder ist leer.")

    if remote and manifest.get("database_url"):
        try:
            payload = download_bytes(str(manifest["database_url"]))
            remote_sha = sha256_bytes(payload)
            if remote_sha != norm_sha(manifest.get("sha256")):
                add_error(errors, "model_manifest.json: Remote-sha256 passt nicht.")
            remote_rows = json.loads(payload.decode("utf-8-sig"))
            if not isinstance(remote_rows, list):
                add_error(errors, "Remote-model.json ist keine JSON-Liste.")
            elif len(remote_rows) != expected_count:
                add_error(errors, f"Remote-model.json enthaelt {len(remote_rows)} statt {expected_count} Eintraege.")
        except Exception as exc:
            add_error(errors, f"model_manifest.json: Remote-Download fehlgeschlagen: {exc}")

    if len(rows_raw) == 0:
        add_warning(warnings, "model.json ist leer.")


def validate_zip_footprint(repo: Path, warnings: list[str]) -> None:
    zips = list((repo / "updates").rglob("*.zip")) if (repo / "updates").exists() else []
    total = sum(path.stat().st_size for path in zips)
    large = [path for path in zips if path.stat().st_size > 50 * 1024 * 1024]
    if len(zips) > 50:
        add_warning(warnings, f"{len(zips)} ZIP-Updatepakete im Repo.")
    if total > 1024 * 1024 * 1024:
        add_warning(warnings, f"ZIP-Updatepakete belegen zusammen {total / (1024 * 1024 * 1024):.2f} GB.")
    if large:
        names = ", ".join(path.name for path in sorted(large, key=lambda item: item.stat().st_size, reverse=True)[:5])
        add_warning(warnings, f"{len(large)} ZIPs sind groesser als 50 MB: {names}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate modelfinder-db release files.")
    parser.add_argument("--remote", action="store_true", help="Also verify raw GitHub downloads.")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    warnings: list[str] = []

    validate_model_manifest(repo, errors, warnings, args.remote)
    validate_latest_manifest(repo, "latest_modelfinder.json", errors, warnings, args.remote)
    validate_latest_manifest(repo, "latest_hardwarecheck.json", errors, warnings, args.remote)
    validate_zip_footprint(repo, warnings)

    for line in warnings + errors:
        print(line)
    if errors:
        print("Release state: FAILED")
        return 1
    print("Release state: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
