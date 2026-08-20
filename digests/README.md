# Closed-Period Digests

This directory indexes immutable digests created by the scheduled Daily Agent after a period has fully closed.

## Stable identities

- ISO week: `digests/weeks/YYYY-Www.md`
- Calendar month: `digests/months/YYYY-MM.md`

The first successful Daily Agent run after a boundary creates the prior period once, following [`COMPACTION.md`](../COMPACTION.md). The current week and month are still open, so this migration intentionally creates no empty or speculative digest files.

Future entries appear here only after their source periods close. Rolling 7/30-day views remain on the README pair and are not archived as evidence.
