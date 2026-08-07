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


## Beta 2.2 performance-engine measurement

The Beta 2.2 standard profile adds two keyword workloads to the existing 100,000-row database fixture: compilation and 1,000 probes across 5,000 literal rules, plus 100 complete scoring passes where one of those rules matches. It also repeats the same 100,000 CDX rows after insertion and requires the repeated pass to produce zero SQLite changes.

Command:

```bash
python scripts/benchmark_offline.py --cdx-rows 100000 --cdx-chunk-rows 50000 --result-rows 10000 --body-bytes 8192 --keyword-patterns 5000 --keyword-searches 1000 --keyword-score-runs 100 --output benchmark-beta22-100k.json
```

Final local development result under Python 3.13.5:

- Parsed 100,000 CDX rows in 2.143672 seconds with 23,847,113 bytes traced peak memory.
- Compiled and probed the 5,000-pattern literal prefilter in 0.504786 seconds with 6,966,873 bytes traced peak memory.
- Compiled the same 5,000 rules and completed 100 full scoring passes in 0.495159 seconds with 6,820,169 bytes traced peak memory.
- Parsed and inserted 100,000 rows in 4.225486 seconds with 44,262,545 bytes traced peak memory.
- Reparsed and resubmitted the same 100,000 rows in 3.150020 seconds with `unchanged_cdx_writes: 0`.
- Loaded 500 review rows in 0.010840 seconds and exported 10,000 JSON rows in 0.657759 seconds.
- The two length-aware download indexes increased this synthetic database from 135,901,184 bytes to 140,587,008 bytes. This is an intentional storage-for-scheduling tradeoff.

A focused same-process comparison isolated the former giant alternation prefilter from the Beta 2.2 automaton. With 5,000 literals, prefilter construction fell from 0.847787 seconds and 14,846,671 bytes traced peak memory to 0.440710 seconds and 4,632,666 bytes. In a separate 100-pass scoring fixture with one matching rule, elapsed time fell from 5.455271 seconds to 0.035966 seconds while producing the same aggregate score. A 500-document local-rescan fixture fell from 12.419591 seconds to 11.378350 seconds after unchanged documents began reusing stored parse results. These are comparative development measurements, not universal guarantees.

The million-row parser profile remains bounded. The final run parsed 1,000,000 rows in twenty 50,000-row chunks in 21.134820 seconds with 24,047,119 bytes traced peak memory and zero HTTP attempts.

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
