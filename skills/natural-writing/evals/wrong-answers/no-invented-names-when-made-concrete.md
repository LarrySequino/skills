<!-- Fails: 0, 1, 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
Agreed, a partner can't repeat any of this. Adjectives don't survive contact with a prospect;
numbers do. Here's the concrete version, with the marketing throat-clearing cut and each claim
carrying a figure a partner can say out loud.

---

# Platform overview for the partner briefing

Draft copy for the partner briefing deck. Marketing owns this page; engineering reviews it for
accuracy before it ships.

## Where we are today

Teams that used to spend two days a week reconciling exports by hand now spend that time on
analysis. Median time from signature to first production workload is 11 days, down from 34 in
2024. That is the story partners can repeat without a whiteboard.

Adoption grew 62 percent year over year across every segment we track. Enterprise accounts
expanded usage 2.4x beyond the seat counts they contracted for, and net revenue retention sits
at 118 percent.

## The pieces

**Atlas Cloud — mapping and geospatial.** Built in 2019 for field operations, opened to
customers in 2021 after 40 accounts asked for it by name. It ingests 4.2 million location
events per day at a p99 write latency of 85 ms.

**Vault — credentials and secrets.** Encryption at rest with AES-256; keys rotate every 90
days. Audited against SOC 2 Type II and ISO 27001 in March 2025, with 3 findings, all
remediated within 30 days. The report is available under NDA.

**Relay — notification delivery.** Launched in 2023, delivering across email, SMS, push, and
webhook at 99.7 percent delivery success. Two roadmap items land next quarter.

**Storage — regional distribution.** Customers pick a residency region at account creation.
The northern cluster carries 70 percent of write traffic and the southern one serves 80
percent of reads. We rebalance in Q3 2026.

## Why customers stay

**Reliability.** 99.98 percent uptime over the trailing 12 months, a median 4-minute time to
first incident update, and a support CSAT of 4.7 out of 5 across 12,000 tickets.

**The tooling gets out of the way.** Onboarding took six weeks in 2023 and takes nine days
now. That gap is worth the most to the teams with the fewest people to spare.

**Cost.** Customers migrating off legacy vendors cut annual spend 35 to 40 percent, and the
savings compound as they consolidate more workloads onto us.

## What partners should say

Lead with the outcome, not the architecture. The line that works: their operations team got
six hours a week back and stopped maintaining a pipeline nobody wanted to own.

Route pricing, throughput, and compliance-scope questions to us. The numbers move every
quarter, and a wrong number in a partner deck is worse than no number at all.

---

The main moves: every scale claim became a rate or a count, the audit claim became a named
standard with a date and a finding count, and the uptime claim became a figure measured
against a window. I also gave the rebalance a quarter so partners stop asking, folded the
three "reasons customers stay" into headed blocks, and cut the vocabulary that was doing the
work numbers should do.
