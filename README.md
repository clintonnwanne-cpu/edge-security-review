# Edge Security Configuration Review

Review fictional edge-rule metadata and proposed changes without applying them.

**Status:** independent local prototype, developed with AI assistance, using original code and synthetic fixtures. No production integration or employer implementation is included. Python 3.10+; standard library only.

## Two-minute demo

From this repository directory:

```sh
python3 edge_review.py examples/before.json examples/proposed.json --now 2026-10-08T12:00:00Z
python3 -m unittest discover -v
```

The sample proposes an owner, a specific path and a future metadata expiry. Its output remains REVIEW_REQUIRED. New or remaining findings, rule removal and environment changes block the proposal. Output includes a readable diff and proposed resolutions.

See `examples/report.json` for the recorded local output and `test-results.txt` for the local test run. There are 12 focused regression tests. A GitHub workflow is included but has not run remotely before publication.

## Design

Fictional before and proposed rules → checks and comparison → blocked or human review required.

The code is intentionally small enough to inspect. CLI inputs are local JSON files, and stdout is a JSON report. Only the ticket simulator writes a database explicitly chosen by the caller. No tool connects to employer systems or makes a network call.

## Verification boundaries

This is a deliberately strict fictional format, not an Akamai configuration parser. It cannot evaluate actual WAF behavior, bot protection, DDoS capacity, traffic or token cryptography. Wildcards and encoded paths are flagged rather than interpreted. No secret token values belong in the input. A changed expiry field does not issue or rotate a real token. Environment-change checks compare the same rule across versions, not complete cross-environment deployments.

This is a bounded control-validation demonstration, not a production security product. Tests exercise the included synthetic cases; passing tests do not establish comprehensive correctness or production readiness. Malformed top-level schemas may reject the input; they must never be treated as an all-clear report.

## Operational walkthrough

1. Run the checked-in fixture and inspect the report.
2. Change one synthetic input to trigger a failure; run the tests to see the expected behavior.
3. Review any proposed resolution manually. For real adoption, independently validate schema, identity, ownership, freshness and API semantics before developing a separately reviewed adapter.

No deployment takes place, so there is no production rollback. Keep the original input for comparison. For a disposable simulator run, choose a new temporary database path rather than overwriting an existing run. Do not put credentials, employer exports or sensitive identifiers in fixtures or reports.

## Contributing

Add a minimal synthetic failing fixture and a regression test with each behavior change. Keep evidence states explicit and avoid claims stronger than the input supports. See SECURITY.md for safe issue reporting.

## Provenance and license

Inspired by general security-engineering patterns from Kubernetes sensor validation, event-driven workflow automation and edge-control review. This is independent demonstration code, not code used by or endorsed by any employer. No historical workplace metric is presented as a measurement of this demo. AI assisted implementation and documentation; local tests and sample outputs are retained for inspection.

MIT license. Copyright 2026 Clinton Nwanne.
