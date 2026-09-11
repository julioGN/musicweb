# Matching fix verification and contract review

## Decision

The authorized matching fixes are implemented and verified at the comparator and helper level. End-to-end playlist/UI operation and real-library recall/precision are not verified.

## Evidence

- Python 3.10 temporary environment with project-compatible dependencies, including RapidFuzz 3.14.5, pandas 2.3.3, and NumPy 1.26.4.
- New `tests/unit/test_core/test_matching_regressions.py`: **39 passed**. Running the same tests against an untouched `git archive HEAD` checkout produced **27 failed, 12 passed**.
- Full existing-plus-new core suite: **47 passed, 16 failed**. Original core suite in the baseline checkout: **7 passed, 17 failed**. No new failures in the existing suite; the title-normalization test now passes.
- Black check and scoped `git diff --check`: pass. Changed Python files also parse with Python 3.8 syntax.
- Local synthetic timing: 1,000 exact matches in 0.023 seconds; 300 fuzzy matches against 300 targets in 0.876 seconds. These are smoke measurements, not a production benchmark.
- Final review added a 10,000-entry limit on similarity memoization because exhaustive candidate retrieval can encounter many distinct artist pairs. The 39 regression checks and static checks passed again afterward.

## Contract coverage

- Artist punctuation, accent, spelling, collaborator separators, and Daft Punk cleanup: verified.
- Short-name matches beyond position 50, word-overlap exclusions, reused comparators, in-place candidate replacement, and music eligibility changes: verified.
- Ordinary Rain/Talk/Explicit titles and retained podcast/tutorial filtering: verified.
- Equivalent bracket annotations and remasters match; studio/live, acoustic, instrumental, remix, radio edit, and distinct parts remain separate in tested examples.
- ISRC precedence, whitespace cleanup, and rejection of blank identifiers: verified.
- Playlist audit spelling variants and playlist search scoring: verified using isolated helpers and mocked search results; no external API calls or playlist writes.
- The user's unrelated app, README, ignore-file, and editor configuration changes were preserved.

## Remaining limitations

- The pre-existing `musicweb.integrations.__init__` import of nonexistent `DeduplicationService` blocks normal playlist package imports. Tests load helper modules directly to isolate matching behavior. This unrelated packaging defect remains open.
- Existing core failures include obsolete comparator/result APIs, normalization expectations, artist-count behavior, and duration parsing. They remain outside this fix.
- The separate `core/matching.py` implementation is unchanged; library comparison and playlist scoring use `core/models.py`.
- Exhaustive fuzzy fallback favors recall and can take longer for large libraries with few exact/ISRC matches. Version detection is conservative and limited to recognized annotations/part markers; it is not a comprehensive recording-identity model.
- A measured real-library improvement requires labeled source/target exports and negative examples. No percentage improvement is claimed.

## Reproduce

With project dependencies and pytest installed:

```sh
PYTHONPATH=src python -m pytest tests/unit/test_core/test_matching_regressions.py
PYTHONPATH=src python -m pytest tests/unit/test_core
```
