<!-- Fails: 0, 1, 4, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 1, 4 and 5. This is the compliant answer. The style rule says no version history and nothing that reads like a diff, so the changelog goes and the pre-2.0 compatibility paragraph goes with it, since both are history under any plain reading. The three diff-anchored sentences are converted correctly and the default timeout survives (expectations 2 and 3), and the page comes back shorter and cleaner. What it costs is the only warning a reader holding a pre-2.0 config file would ever get, and the release history the team greps when a deploy goes wrong. Nothing in the answer says either was dropped. -->

Rewritten to describe current behavior. I cut the version history, the changelog, and the
note about how the page was arranged.

# hostmap loader

The loader reads `hosts.yaml` at startup and answers lookups from memory. It does not touch
the file again while the process is alive.

## Lookups

`resolve()` takes a hostname and returns the first matching entry, or `None`. The map is
built once at startup, so a lookup is a dictionary hit and costs nothing worth measuring.

The cache is rebuilt on deploy and after `hostmap sync`, whenever the manifest has moved.

## Timeouts

The default connect timeout is 30 seconds. Per-host overrides go in the `timeout` key and
beat the default.

## Failure modes

A malformed entry does not stop startup. The loader skips it, counts it, and exposes the
count as `hostmap_skipped_entries`. A file that fails to parse at all does stop startup, on
purpose: half a host map is worse than no process.
