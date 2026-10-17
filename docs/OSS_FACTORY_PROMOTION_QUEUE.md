<!-- oss-factory:v1
{"id":"20261017-civic-legis-graph-queue","kind":"state","project":"legis-graph","from":"chatgpt","to":["factory"],"status":"working","dedupe_key":"promotion-queue:legis-graph/legis-graph","civ":{"city_id":"oss:legis-graph"}}
-->

# Canonical upstream promotion queue — legis-graph/legis-graph

Tracked via registry PR https://github.com/kvnloo/oss-factory/pull/191 (provisional until merged). Fork Issues are disabled; this fork-local document is the **one canonical queue**. Original implementation PRs, issue threads, and author credit stay where they originated.

- Origin: https://github.com/legis-graph/legis-graph
- Coordination fork: https://github.com/kvnloo/legis-graph
- Last evidence audit: 2026-10-17
- State: **CHECK / LOCAL_ONLY** for the full source migration; **READY_FOR_HUMAN_REVIEW** for the separate loader fix (not origin-action authorization)

## Existing upstream review / source work

- Retired fork draft: https://github.com/kvnloo/legis-graph/pull/1 (`closed`, not merged).
- Planning branch: `civic/official-source-migration` @ `423f8419b360af761b2d79ad8206929fccbdd882`.
- Existing `sync.sh` relies on retired GovTrack rsync; replacement candidates: Congress.gov, GovInfo, Senate roll-call XML and congress-legislators.
- Official-source migration is **documentation/schema only**; no API adapter, fixture parity, or importer tests yet.
- **Independent tested leaf — READY_FOR_HUMAN_REVIEW:** `civic/legislators-safe-yaml-20261017` @ `93efb13780ec6ae6fbbd5bdcf9186099d17b3b61` fixes `yaml.load(f)` incompatibility with unpinned PyYAML 6+ by using `yaml.safe_load(f)`.
- **RED:** PyYAML 6.0.3 raises `TypeError` for `yaml.load(f)` without `Loader`.
- **GREEN:** 2 native stdlib `unittest` subprocess checks PASSED on Python 3.13.5 + PyYAML 6.0.3, checking current/historical CSV and rejection of Python-specific YAML tags. Exact tested file Git blob IDs match remote: parser `652e5fb889e228ab060e434b84dda00bef162d6b`, test `c12059588a20d9a51ece3a91e436317f7a6f7080`.
- Test command: `python -m unittest discover -s tests -v`. No external API or Neo4j required. Origin repo last pushed in 2020; request maintainer review before proposing publication.
- Next: map maintained official sources onto legacy bill/vote/legislator parser contracts; implement smallest fixture-backed adapter; keep origin publication blocked until reproducible evidence.

## Release gates

- Record original author/reporter/maintainer provenance and exact source head SHA.
- Follow project contribution policy, current upstream reviews, conflicts, and CI checks.
- Require native targeted tests; separate static reasoning from exercised runtime evidence.
- Do not publish an overlapping origin PR or claim a fork draft is landed.
- Only a bounded human authorization under factory/HITL.md permits additional origin actions; upstream merges are for maintainers.

## Results

- **Ready for new origin publication:** none independently verified.
- **Origin writes from this coordination update:** none.
- **Next update:** when CI/reviews/test results or upstream ownership changes materially.
