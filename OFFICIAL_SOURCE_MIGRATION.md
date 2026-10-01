# Official-source ingestion migration

The current `sync.sh` depends on GovTrack's retired rsync service. The safest
migration is to preserve the existing parser-facing data layout first and
replace only the acquisition layer.

## Existing local contract

### Legislators and committees

Existing parsers consume:

- `data/congress-legislators/legislators-current.yaml`
- `data/congress-legislators/legislators-historical.yaml`
- `data/congress-legislators/committees-current.yaml`

Source replacement: the maintained
[`unitedstates/congress-legislators`](https://github.com/unitedstates/congress-legislators)
dataset.

### Bills

`parse_bills.py` expects:

```
data/congress/<congress>/bills/<type>/<number>/data.json
```

The adapter must normalize current source records to the fields already
consumed by the parser:

- `bill_id`
- `history.active`
- `history.enacted`
- `history.vetoed`
- `official_title`
- `popular_title`
- `sponsor.bioguide_id`
- `cosponsors[].bioguide_id`
- `committees[].committee_id`
- `committees[].activity`
- `subjects[]`

Primary source: [Congress.gov API](https://api.congress.gov/).

Validation/cache source: [GovInfo bulk data](https://www.govinfo.gov/bulkdata/)
BILLSTATUS/BILLS collections.

### Votes

`parse_votes.py` expects:

```
data/congress/<congress>/votes/<year>/<rollcall>/data.json
```

with:

- `category`
- `bill.type`
- `bill.number`
- `bill.congress`
- grouped member votes with stable member identifiers

House source: Congress.gov House vote endpoints.

Senate source: Senate roll-call XML
([roll-call archive](https://www.senate.gov/legislative/votes_new.htm)).

The adapter owns chamber-specific identifier normalization. The graph parser
should not need to know which upstream source produced a normalized vote.

## Provenance receipt

Every downloaded source artifact should have a sidecar receipt validated by
`ingest/source-manifest.schema.json`.

Required evidence:

- source family
- exact source URL
- fetch timestamp
- SHA-256 of downloaded bytes
- Congress/session when applicable
- adapter name/version

Derived records should retain the receipt ID that produced them. This makes
source changes and parser regressions distinguishable.

## Migration phases

1. **P0 — contract fixtures**
   - freeze representative bill, House vote, Senate vote, member and committee
     fixtures
   - add manifest validation
2. **P1 — people/committee adapter**
   - replace the old GovTrack mirror with `congress-legislators`
3. **P2 — bill adapter**
   - normalize Congress.gov bill records to the existing `data.json` shape
   - compare a fixture set against GovInfo BILLSTATUS
4. **P3 — vote adapters**
   - House: Congress.gov
   - Senate: Senate roll-call XML
   - normalize stable member IDs before writing parser-facing JSON
5. **P4 — parity gate**
   - run the existing parse/import pipeline
   - compare counts, missing identifiers and relationship coverage against
     fixtures
6. **P5 — retire `sync.sh`**
   - only after current-Congress rebuilds are reproducible from a clean checkout

## Stop conditions

Do not remove the old parser contract until:

- bills, legislators, committees and passage votes can all be rebuilt
- every fetched artifact has a valid provenance receipt
- fixture/parity checks pass
- missing identifiers are surfaced rather than silently dropped

This migration deliberately separates **retrieval**, **normalization** and
**graph import** so source changes do not require rewriting the graph model.
