# Repository details

Product: `Archive Scout 3.0`

Release: `3.0.0-beta.2.2`

Database schema: `5`

Supported build targets:

- Windows x64
- Linux x64
- macOS Universal 2 for Intel and Apple Silicon

Primary release files:

```text
ArchiveScout-Windows-x64.zip
ArchiveScout-Linux-x64.tar.gz
ArchiveScout-macOS-Universal.zip
```

Each package has a corresponding `.sha256` file.

## Beta 2.2 performance-engine release

Archive Scout 3.0 Beta 2.2 is the current source release. It keeps Python package metadata `3.0.0b1.post8`, schema version 5, and the existing project format for compatibility with the established build and test workflows. Beta 2.2 adds compiled literal prefiltering, bounded parallel rescanning, streamed media transfers, size-aware work queues, no-op persistence for unchanged data, expanded offline benchmarks, and the earlier Beta 2 hardening and Beta 2.1 startup safeguards.

## Beta 1.6 scope

Beta 1.6 is a whole-repository reliability and large-project optimization pass. The existing request-rate limit, project schema, visible workflows, media behavior, live Dashboard, icon, date handling, external-media operation, and signing workflow remain in place.

Release-blocker fixes:

- compact and bounded handling of 50,000-row CDX responses
- immediate release of completed numbered pages
- safe reduction/subdivision after oversized responses or parser memory pressure
- bounded connection-setup retries followed by a clean saved pause
- operation-wide no-progress protection
- complete paged connection failures routed into the same connection circuit

Repository-wide audit work:

- streaming/bounded database, download, rescan, reporting, analysis, repair, integrity, merge, migration, and retry paths
- temporary tables for large explicit ID selections
- deterministic duplicate candidate de-duplication without a global pair set
- resource cleanup on client/database/operation failures
- bounded GUI event/log retention

## Preserved Wayback speed envelope

- fixed 0.75-second request-start interval
- 50,000 rows per resume-key request
- nine CDX blocks per numbered page
- ten configured workers for small pages
- four effective resident workers for nine-block pages
- coordinated HTTP 429 backpressure

## External embedded-media workflow

The dedicated operation completes the normal text index, downloads and scans selected pages, then reads saved documents' extracted link lists. It looks up matching external media URLs and downloads them after discovery is complete using the existing media filters, size limit, snapshot strategy, retries, database tables, and reports.

## macOS bundle integrity

The macOS build verifies `Contents/Resources/base_library.zip`, the executable, and every symbolic link before signing. It packages the signed application with `ditto`, extracts the completed ZIP into a clean temporary directory, and verifies the extracted bundle and code signature again.

## Repository update

Apply the Beta 2.2 changed-file payload with the supplied browser-only `apply-beta2-2-performance-engine.yml` workflow. The payload deliberately does not replace either established GitHub workflow. It removes generated build products before validation and explicitly commits only the documented source, tests, packaging metadata, and documentation paths.
