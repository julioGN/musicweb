# Matching recall fixes

The user authorized fixes for the defects reproduced during diagnosis.

## Contract

- The active library/playlist matcher recovers punctuation and accent variants of artist names without lowering acceptance thresholds.
- Artist credit cleanup preserves names such as Daft Punk and still recognizes collaboration separators.
- Candidate ordering and reuse across target libraries cannot hide a valid candidate or return a track outside the current library.
- Ordinary music titles containing Rain, Talk, or Explicit remain eligible; explicit podcast/tutorial indicators still filter non-music.
- Parentheses and square brackets preserve recording and part distinctions. Live/studio and different parts must not be automatically conflated; remaster metadata may differ.
- Existing ISRC precedence and public result interfaces remain intact.

## Implementation brief

Repair the active matcher and normalizer in `core/models.py`, adjust comparison/audit shortcuts as needed, and add focused regression tests. Preserve the user's existing `web/app.py` edits. Do not rewrite the separate `core/matching.py` API or change YouTube search queries.

## Verification

Exercise real comparator paths, candidate permutations, reuse/mutation, normalization, negative version/artist cases, and playlist scoring/audit paths. Run existing core tests and distinguish baseline failures from regressions. Check the diff and formatting. Real-library recall/precision remains unmeasured without labeled paired exports; do not claim a percentage improvement.
