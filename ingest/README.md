# Ingestion adapters

This directory is the compatibility boundary between maintained public data
sources and LegisGraph's historical parser-facing file layout.

Adapters should:

1. fetch one source family;
2. store the unmodified response;
3. emit a provenance receipt conforming to
   `source-manifest.schema.json`;
4. normalize into the existing `data/` layout;
5. fail on missing required identifiers instead of silently inventing them.

Adapters must not directly write Neo4j. Existing parse/import scripts remain
the graph boundary during the migration.

Planned adapters:

- `congress_legislators`
- `congress_gov_bills`
- `congress_gov_house_votes`
- `senate_rollcall`
- `govinfo_validation`
