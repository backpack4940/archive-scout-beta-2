# Beta 2.2 performance engine

Beta 2.2 is an internal execution-engine refactor. It was informed by a comparative review of another Wayback Machine downloader's use of persistent queues, resume keys, keyset pagination, bounded concurrency, bulk SQLite writes, size-aware scheduling, compiled multi-pattern search, and streamed output. Archive Scout adapts those sound fundamentals to its existing architecture rather than copying the other application's process-global state, destructive table resets, subprocess-driven interface, unbounded task groups, or whole-file buffering.

## Preserved contracts

- Database schema version 5 and existing projects
- The current desktop interface and operation pages
- Keyword rule types, weights, required and excluded logic, regex rules, whole-word rules, snippets, proximity scoring, and multiple keyword sets
- CDX page and resume recovery, shared rate-limit handling, retry queues, and fixed user-selected pacing
- Review statuses, notes, tags, reports, comparisons, extraction, forum reconstruction, provenance, diagnostics, merge, backup, repair, and migration behavior
- Existing text and media path conventions

## Compiled literal prefilter

Ordinary normalized literal rules are compiled into one Aho-Corasick trie. Each title, URL, visible-text, raw-text, and link field can be rejected or accepted in one pass, independent of the number of literal rules. Case-sensitive, whole-word, exact, and regular-expression rules remain on the existing regex path. Full scoring still evaluates the original compiled rules, so the automaton changes only the fast gate and not result semantics. Excluded-only sets retain the former positive-match behavior for URL-scoped downloads and extracted-link discovery; exclusions are never treated as positive candidates.

## Parallel local rescanning

Saved files are read and parsed by a bounded thread pool. The number of resident futures is capped at three times the worker count. Workers never touch SQLite. Completed result groups return to the owning thread, which writes their documents, matches, errors, and resolution state in one transaction. This preserves SQLite safety and project consistency while allowing file I/O, HTML parsing, normalization, hashing, and scoring to overlap.

## Size-aware download scheduling

Text and media work queues order known-size captures from smallest to largest and place unknown-size captures last. This does not drop or change any capture. It improves time-to-first-results and reduces the chance that every worker simultaneously holds a large response. Queue state changes are submitted with `executemany` in bounded groups rather than one transaction per future.

## Direct-to-disk media transfer

Every built-in network backend now supports a streamed file response. HTTPX and urllib3 write decoded chunks directly to a `.part` file. The curl backend writes directly to the same destination and then hashes the file incrementally. All paths enforce the configured byte ceiling, honor cancellation, retain the shared Wayback retry and rate-limit policy, collect only a 20,000-byte validation preview, and remove partial files after failure. A successful transfer is atomically moved to its final location.

## Write avoidance

Capture and media upserts update an existing row only when indexed metadata actually changed. Existing documents skip full body and FTS replacement when path, title, links, content hashes, and size are unchanged. Existing matches skip replacement and keyword-hit rebuilding when their analysis payload is unchanged. This sharply reduces WAL growth, SSD writes, and rescan time without altering state when something did change.

## Validation

The Beta 2.2 regression suite covers:

- 5,000-pattern Aho-Corasick matching
- unchanged CDX rows producing zero database writes
- unchanged documents and matches producing zero database writes
- known small files being scheduled before large and unknown files
- bounded four-worker rescanning preserving all results
- media download completion through the streamed-file API without a whole-body `get`
- all pre-existing integration, migration, recovery, packaging, media, analysis, and interface tests

The offline benchmark now measures a 5,000-pattern literal prefilter and repeats the 100,000-row CDX insert. The repeated pass must report `unchanged_cdx_writes: 0`.
