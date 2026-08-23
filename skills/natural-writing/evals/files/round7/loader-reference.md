# hostmap loader

The loader reads `hosts.yaml` at startup and answers lookups from memory. It does
not touch the file again while the process is alive.

## Lookups

`resolve()` was added in the 1.4 rewrite to replace the old linear scan. It takes a
hostname and returns the first matching entry, or `None`. The map is built once at
startup, so a lookup is a dictionary hit and costs nothing worth measuring; the old
scan walked every entry.

The cache is rebuilt whenever the manifest changes, which in practice means on
deploy and after `hostmap sync`.

## Timeouts

We changed the default connect timeout from 5 seconds to 30 seconds in 2.2, after
the Frankfurt region kept tripping it. Per-host overrides go in the `timeout` key
and beat the default.

Config files written before 2.0 use `timeout_ms` and give the value in
milliseconds. The loader still accepts that key, converts it, and logs a warning
once per process. Support for it goes away in 3.0.

## Failure modes

This page was reorganized in March so that the failure modes come before the API
reference, because that is the order people read it in at 3am.

A malformed entry does not stop startup. The loader skips it, counts it, and
exposes the count as `hostmap_skipped_entries`. A file that fails to parse at all
does stop startup, on purpose: half a host map is worse than no process.

## Changelog

- 2.6 `reload()` deprecated; it logs a warning and returns immediately.
- 2.2 Default connect timeout raised to 30 seconds.
- 2.0 `timeout_ms` replaced by `timeout`, given in seconds.
- 1.4 `resolve()` replaces the linear scan.
