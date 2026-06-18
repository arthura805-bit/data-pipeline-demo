"""Run the ETL pipeline on the sample CSV and print the report.

    python examples/run_pipeline.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import run_pipeline  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        report = run_pipeline(HERE / "input.csv", Path(d) / "output.json")
        print("pipeline run:")
        print(f"  {report}")
        print(f"\n{report.valid} valid records written, {report.invalid} rejected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
