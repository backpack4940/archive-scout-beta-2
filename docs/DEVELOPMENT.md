# Development

## Requirements

- Python 3.11 or newer
- Tkinter
- `truststore`
- `httpx`
- `urllib3`

Install runtime requirements:

```bash
python -m pip install -r requirements-runtime.txt
```

Run the interface:

```bash
python run_app.py
```

Run all tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the visual theme test under Linux without a physical display:

```bash
xvfb-run -a python -m unittest tests.unit.test_v3_ui_theme -v
```

Compile-check the package:

```bash
python -m compileall -q archive_scout tests scripts/benchmark_offline.py
```

The pull-request test workflow runs on Windows, Linux, Intel macOS, and Apple Silicon macOS using Python 3.11 and 3.12. The build workflow creates Windows x64, Linux x64, and universal macOS packages.

Run the deterministic offline benchmark without contacting the Wayback Machine:

```bash
python scripts/benchmark_offline.py --output benchmark-results.json
```

Use `--cdx-rows 1000000 --skip-cdx-upsert` for the million-row parser profile; the JSON report explicitly records the skipped insertion phase. See `docs/BENCHMARKS.md` for methodology and comparison rules.

## Release version

The current source release is:

```text
3.0.0-beta.1.6
```

The Python package version uses the PEP 440 form `3.0.0b1.post8` in `pyproject.toml`.

Unreleased Beta 2 hardening work does not change either version identifier or schema version 5.
