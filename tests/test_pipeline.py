"""Tests for data-pipeline-demo. Runs under pytest or standalone."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import extract_csv, run_pipeline, transform, validate  # noqa: E402

SAMPLE = "id,name,score\n1,alice,88\n0,bob,60\n5,erin,150\n6,,40\n"


def _write(tmp_path: Path) -> Path:
    p = tmp_path / "in.csv"
    p.write_text(SAMPLE, encoding="utf-8")
    return p


def test_extract_reads_rows(tmp_path):
    rows = extract_csv(_write(tmp_path))
    assert len(rows) == 4
    assert rows[0]["name"] == "alice"


def test_transform_coerces_types(tmp_path):
    recs = transform(extract_csv(_write(tmp_path)))
    assert recs[0]["id"] == 1 and isinstance(recs[0]["id"], int)
    assert recs[0]["name"] == "Alice"  # title-cased


def test_validate_splits_valid_invalid(tmp_path):
    valid, invalid = validate(transform(extract_csv(_write(tmp_path))))
    # only the first row (id=1, alice, 88) is valid
    assert len(valid) == 1
    assert len(invalid) == 3


def test_run_pipeline_report(tmp_path):
    report = run_pipeline(_write(tmp_path), tmp_path / "out.json")
    assert report.extracted == 4
    assert report.valid == 1
    assert report.invalid == 3
    assert Path(report.output_path).exists()


def _run_standalone() -> int:
    import tempfile

    failures = 0
    with tempfile.TemporaryDirectory() as d:
        for fn in (
            test_extract_reads_rows,
            test_transform_coerces_types,
            test_validate_splits_valid_invalid,
            test_run_pipeline_report,
        ):
            try:
                fn(Path(d))
            except AssertionError as exc:  # pragma: no cover
                failures += 1
                print("FAIL:", fn.__name__, exc)
    print("PASS" if failures == 0 else f"{failures} FAILED")
    return failures


if __name__ == "__main__":
    raise SystemExit(_run_standalone())
