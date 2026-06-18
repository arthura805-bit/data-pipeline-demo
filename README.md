# data-pipeline-demo

A minimal **extract → transform → validate → load** pipeline in Python.

## What this demonstrates
- **Extract** rows from a CSV file.
- **Transform** records (type coercion, normalization) with pure functions.
- **Validate** records into valid / invalid sets.
- **Export** valid records to JSON.
- **Report** a simple run summary (`PipelineReport` dataclass).

## Run
```bash
python examples/run_pipeline.py
```

## Run tests
```bash
python -m pytest                # if pytest is installed
python tests/test_pipeline.py   # standalone, no dependencies
```

## How it works
`run_pipeline` chains `extract_csv` → `transform` → `validate` → `export_json`
and returns a `PipelineReport`. Records with a bad id, an out-of-range score, or
a missing name are rejected; valid records are written to JSON.

## Scope
A focused demonstration of a small, honest ETL flow with validation and
reporting. Standard library at runtime, synthetic data only. Not a product, not a
benchmark.

## License
MIT — see [LICENSE](LICENSE).
