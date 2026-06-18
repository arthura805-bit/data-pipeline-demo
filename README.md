# data-pipeline-demo

A minimal, runnable **extract → transform → validate → load** pipeline in Python.

- **extract** rows from a CSV file
- **transform** records (type coercion, normalization) with pure functions
- **validate** records into valid / invalid sets
- **export** valid records to JSON
- **report** a simple run summary (`PipelineReport` dataclass)

Standard library at runtime. Synthetic data only. No proprietary code or data.

## Project layout

```
pipeline.py               # extract_csv / transform / validate / export / run_pipeline
examples/input.csv        # sample data
examples/run_pipeline.py  # run the full pipeline + print report
tests/test_pipeline.py    # pytest / standalone tests
requirements.txt          # dev-only: pytest
```

## Run

```bash
python examples/run_pipeline.py
python -m pytest                # or: python tests/test_pipeline.py
```

Expected: `extracted=6 transformed=6 valid=3 invalid=3` (rows with bad id, an
out-of-range score, and a missing name are rejected).

## License

MIT — see [LICENSE](LICENSE).
