"""data-pipeline-demo — a minimal extract -> transform -> validate -> load pipeline.

Demonstrates a classic small ETL flow: read CSV, transform records, validate
them, export valid records to JSON, and produce a simple run report.

Standard library only. Synthetic data only. No proprietary code or data.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def extract_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of string-valued dict rows."""
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def transform(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Coerce types and normalize fields (pure: returns new records)."""
    out: list[dict[str, Any]] = []
    for row in rows:
        rec: dict[str, Any] = dict(row)
        # numeric coercion where sensible; leave as-is if it fails
        for key in ("id", "score"):
            if key in rec:
                try:
                    rec[key] = int(rec[key])
                except (ValueError, TypeError):
                    pass
        if "name" in rec:
            rec["name"] = rec["name"].strip().title()
        out.append(rec)
    return out


def validate(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split records into (valid, invalid). Rules: int id>=1, name, 0<=score<=100."""
    valid, invalid = [], []
    for rec in records:
        ok = (
            isinstance(rec.get("id"), int)
            and rec["id"] >= 1
            and bool(rec.get("name"))
            and isinstance(rec.get("score"), int)
            and 0 <= rec["score"] <= 100
        )
        (valid if ok else invalid).append(rec)
    return valid, invalid


def export_json(records: list[dict[str, Any]], path: str | Path) -> Path:
    p = Path(path)
    p.write_text(json.dumps(records, sort_keys=True, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


@dataclass
class PipelineReport:
    extracted: int = 0
    transformed: int = 0
    valid: int = 0
    invalid: int = 0
    output_path: str = ""

    def __str__(self) -> str:
        return (
            f"extracted={self.extracted} transformed={self.transformed} "
            f"valid={self.valid} invalid={self.invalid} -> {self.output_path}"
        )


def run_pipeline(csv_path: str | Path, json_out: str | Path) -> PipelineReport:
    rows = extract_csv(csv_path)
    records = transform(rows)
    valid, invalid = validate(records)
    out = export_json(valid, json_out)
    return PipelineReport(
        extracted=len(rows),
        transformed=len(records),
        valid=len(valid),
        invalid=len(invalid),
        output_path=str(out),
    )
