#!/usr/bin/env python3
"""Static Magic Image boot bridge.

This tiny starter remains on the FAT32 Debian partition. The actual program
and all mutable state live on the NTFS image partition so interrupted updates
or an unexpected USB removal cannot damage the boot-side application files.
"""

from __future__ import annotations
import os
import pathlib
import subprocess
import sys

BOOT_ROOT = pathlib.Path(__file__).resolve().parent
RUNTIME_DIR_NAME = "HardwareCheck-Runtime"
RUNTIME_LABEL = "MISOLOIMAGES"
MOUNT_POINT = pathlib.Path("/run/hardwarecheck-runtime-media")

def _valid_runtime(path: pathlib.Path) -> bool:
    return (path / "hardwarecheck_fast_gui.py").is_file() and (path / "hardwarecheck_v5_gui.py").is_file()

def _mounted_candidates() -> list[pathlib.Path]:
    candidates: list[pathlib.Path] = []
    configured = os.environ.get("HC_RUNTIME_DIR", "").strip()
    if configured:
        candidates.append(pathlib.Path(configured))
    for base in (pathlib.Path("/media"), pathlib.Path("/mnt"), pathlib.Path("/run/media"), MOUNT_POINT):
        if base.is_dir():
            candidates.append(base / RUNTIME_DIR_NAME)
            try:
                candidates.extend(item / RUNTIME_DIR_NAME for item in base.iterdir() if item.is_dir())
            except OSError:
                pass
    return candidates

def _mount_runtime_media() -> pathlib.Path | None:
    device = pathlib.Path("/dev/disk/by-label") / RUNTIME_LABEL
    if not device.exists():
        return None
    try:
        MOUNT_POINT.mkdir(parents=True, exist_ok=True)
        if not os.path.ismount(MOUNT_POINT):
            completed = subprocess.run(
                ["mount", "-o", "rw,nosuid,nodev", str(device), str(MOUNT_POINT)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=12, check=False)
            if completed.returncode:
                return None
        candidate = MOUNT_POINT / RUNTIME_DIR_NAME
        return candidate if _valid_runtime(candidate) else None
    except (OSError, subprocess.SubprocessError):
        return None

def _start(path: pathlib.Path) -> None:
    os.environ["HC_RUNTIME_DIR"] = str(path)
    os.environ["HC_DATA_DIR"] = str(path)
    os.execv(sys.executable, [sys.executable, str(path / "hardwarecheck_fast_gui.py")])

def main() -> int:
    for candidate in _mounted_candidates():
        if _valid_runtime(candidate):
            _start(candidate)
    candidate = _mount_runtime_media()
    if candidate:
        _start(candidate)
    # The recovery copy is deliberately static and has no updater path. It
    # allows technicians to start the medium if the NTFS partition is unavailable.
    recovery = BOOT_ROOT / "hardwarecheck_fast_gui.recovery.py"
    if recovery.is_file():
        os.execv(sys.executable, [sys.executable, str(recovery)])
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
