"""Import explicitly selected observations; never execute their recorded command text."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("meta", type=Path, help="本次要追加的一条 meta.json")
    parser.add_argument("--runtime-dir", default=".runtime/course/L01-workbench")
    parser.add_argument("--task-id", default="CASE-WB-L01-001")
    args = parser.parse_args()
    entry = json.loads(args.meta.read_text(encoding="utf-8-sig"))
    output = Path(entry["output_file"])
    if hashlib.sha256(output.read_bytes()).hexdigest() != entry["sha256"]:
        raise ValueError("输出与采集时的摘要不一致，请核对原记录，不要修改元数据凑通过")
    return subprocess.run([sys.executable, "-X", "utf8", "-m", "workbench.cli", "workbench-evidence-add",
                           "--runtime-dir", args.runtime_dir, "--task-id", args.task_id,
                           "--phase", entry["phase"], "--command-text", entry["command"],
                           "--output-file", str(output), "--returncode", str(entry["returncode"]),
                           "--observed-at", entry["observed_at"]], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
