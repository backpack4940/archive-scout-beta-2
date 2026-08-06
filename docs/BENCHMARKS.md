# Offline benchmarks

Archive Scout includes a deterministic benchmark runner that does not contact the Wayback Machine. It generates compact CDX rows, a temporary schema-version-5 project, paginated review results, notes, tags, and export data.

Run the standard 100,000-row profile:

```bash
python scripts/benchmark_offline.py --output benchmark-results.json
```

Run the required million-row CDX profile while keeping the review fixture smaller:

```bash
python scripts/benchmark_offline.py --cdx-rows 1000000 --cdx-chunk-rows 50000 --skip-cdx-upsert --result-rows 1000 --body-bytes 1024 --output benchmark-million.json
```

The standard profile parses and inserts 100,000 CDX rows, then measures review browsing and export. The million-row command measures the parser in realistic 50,000-row response chunks and explicitly records that the million-row SQLite upsert phase was skipped; this keeps the profile practical on low-resource machines while the standard profile covers database insertion. The report records elapsed time, Python peak memory, database size, transaction count, inserted rows, HTTP attempts, and duplicate work. HTTP attempts remain zero by design. Run benchmarks on an otherwise idle machine and compare results produced by the same Python version, operating system, storage device, and arguments.

## Beta 2 hardening measurement

The result-browser and JSON-export comparison used 10,000 generated review rows with an approximately 8 KiB document body per row. Measurements were taken in the same Linux runtime with Python 3.13.5 solely to compare the old and new implementations; supported release validation remains Python 3.11 and 3.12.

| Operation | Before time | After time | Before peak memory | After peak memory |
| --- | ---: | ---: | ---: | ---: |
| Load 500 result rows | 0.1431 s | 0.0109 s | 4,712,286 B | 593,125 B |
| Export 10,000 rows to JSON | 3.2895 s | 0.6091 s | 110,874,891 B | 2,365,561 B |

The browser improvement comes from no longer loading full document bodies into each table row. The exporter now reads one SQLite cursor in bounded batches and writes incrementally through an atomic temporary file.

## Reproducible fixture results

The final local validation used Python 3.13.5 in the same Linux container as the before/after comparison. These figures are recorded for reproducibility and are not substituted for supported-platform CI.

### Standard database profile

Command:

```bash
python scripts/benchmark_offline.py --cdx-rows 100000 --cdx-chunk-rows 50000 --result-rows 10000 --body-bytes 8192 --output benchmark-100k.json
```

- Parsed 100,000 CDX rows in 2.217146 seconds with 23,847,113 bytes traced peak memory.
- Parsed and inserted 100,000 rows in 4.595365 seconds with 44,263,739 bytes traced peak memory.
- Loaded 500 review rows in 0.009891 seconds with 618,181 bytes traced peak memory.
- Exported 10,000 JSON rows in 0.656362 seconds with 2,472,468 bytes traced peak memory.
- Final database size: 135,901,184 bytes.
- Benchmark-managed transactions: 4.
- HTTP attempts: 0.
- Duplicate work: 0.

### Million-row parser profile

Command:

```bash
python scripts/benchmark_offline.py --cdx-rows 1000000 --cdx-chunk-rows 50000 --skip-cdx-upsert --result-rows 1000 --body-bytes 1024 --output benchmark-million.json
```

- Parsed all 1,000,000 CDX rows in twenty 50,000-row chunks in 21.317409 seconds.
- Traced parser peak memory: 24,047,119 bytes.
- HTTP attempts: 0.
- Duplicate work: 0.
- The report explicitly records `cdx_upsert_skipped: true` and `cdx_rows_inserted: 0`; the standard profile supplies the SQLite insertion measurement.
