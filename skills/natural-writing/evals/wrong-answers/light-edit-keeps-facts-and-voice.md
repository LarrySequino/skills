<!-- Fails: 0, 2, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "I assumed Postgres. Everyone assumes Postgres." — this answer expands the two-beat fragment into a single measured sentence, and does the same to the rest of the piece: every section is retitled, the "Four more minutes. ... Zero minutes." beats are folded into a list of attempts, and the first-person account is recast as a neutral postmortem. The figures are carried across, but roughly two thirds of the author's wording is replaced. -->

Deslopped. The piece was solid underneath but the prose was doing it no favors, so I tightened throughout: shorter sentences where they had run long, consistent section headings, and the narrative reordered so the finding leads rather than arrives last. Every number, ticket and name is carried across unchanged.

# Nightly import: root cause and remediation

Author: Dan Okafor. Date: May 12, 2026. Written so that the next engineer to inherit this job does not repeat three weeks of investigation into a component that turned out to be healthy.

## Summary

The nightly customer import had degraded from a 01:20 finish to a 04:15 finish. The cause was single-threaded CSV parsing in the importer itself, not database contention. Two changes in v2.7.0 brought the runtime down from 4 hours 40 minutes to 11 minutes.

## Background

The import begins at 23:40 each night. It completed by 01:20 as of March 2024 and had slipped to 04:15 by February of this year, which left sales looking at stale dashboards each morning and, on two occasions, left the job still holding tables that the 06:00 billing run required. No single change caused the regression. The job had accumulated 2.1 million more rows than its original author anticipated when it was written in 2021, arriving gradually over several years.

The initial hypothesis was that Postgres was the bottleneck. That is the assumption most engineers would make in the same position.

## What I tried

The first three weeks went into tuning the database, none of which materially improved the runtime:

- work_mem was raised from 4 MB to 512 MB. This eliminated sort spills and recovered roughly four minutes.
- The two indexes on `customer_events` that pg_stat_user_tables reported as 38 percent bloated were rebuilt, for a comparable gain.
- The connection pooler was upgraded, on the theory that a connection-reset bug in pgbouncer 1.17 might be responsible. Version 1.21 resolved that bug and changed nothing about the runtime.

The investigation turned on a suggestion from Priya, who asked whether the job itself had ever been observed directly rather than through its metrics. It had not. On March 3, `py-spy dump` was run against the live process every thirty seconds for an hour, which proved to be the most productive hour of the entire effort.

The importer was spending 71 percent of its wall clock inside `csv.DictReader`, parsing a 9.4 GB file line by line on a single core. The database was idle for most of the night, and had been throughout. Because every dashboard in place measured the database, the database was the only thing visible.

## The fix

The fix arrived as two changes, both shipped in v2.7.0 on March 11.

Parsing moved to the COPY path: the file is streamed directly into an unlogged staging table, with type coercion performed in SQL, where it is close to free. The row-by-row `INSERT ... ON CONFLICT` loop was replaced with a single `MERGE` against that staging table. The result is 90 fewer lines of code than the implementation it replaced.

Runtime fell from 4 hours 40 minutes to 11 minutes. The change was validated against the last 14 nights of archived input, the slowest of which completed in 13 minutes. Peak memory fell from 6.8 GB to 240 MB, which is significant because the same host also runs the search reindex and had been sized around the import's previous requirements.

## What to take from this

The principal lesson is to instrument the process under investigation rather than the component under suspicion. Extensive dashboard coverage existed for Postgres and none for the importer's own CPU, which directed three weeks of effort toward the wrong subsystem.

A secondary and arguably more important finding concerns ownership. The job was written in 2021 by an engineer who left in 2022, and it degraded at approximately 40 seconds a week for four years without anyone monitoring the trend. Remediation took two days; identifying the need for remediation took four years. That ratio, rather than any database issue, is the substantive finding.

One item remains open: `customer_events` still has no retention policy and grows by roughly 90 GB a year. This is tracked as PLAT-4471 and is not scheduled for this quarter.
