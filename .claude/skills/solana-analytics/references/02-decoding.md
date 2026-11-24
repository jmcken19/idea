# 02 — Decoding Programs: Logs & IDL → Analytics Tables

This is the part nobody documents, and it's where most "there's no data for this protocol" walls
fall down. Solana instruction data and program logs are opaque bytes until you decode them. This
reference shows the three decoding paths, in order of preference, so you can analyze *any* program —
not only the ones the Spellbook already covers.

## How Solana encodes the thing you want to count

- **Instructions are Borsh-encoded bytes.** A program's instruction is `[discriminator ‖ args]`,
  serialized with Borsh. To read it you need the layout, which lives in the program's **IDL**
  (Anchor) or its documented schema (native programs).
- **Anchor discriminators are deterministic.** Anchor prepends an 8-byte tag:
  - instruction discriminator = `sha256("global:<snake_case_ix_name>")[..8]`
  - account discriminator     = `sha256("account:<AccountName>")[..8]`
  - event discriminator       = `sha256("event:<EventName>")[..8]`
  This is why you can recognize an instruction without the full IDL: match the first 8 bytes.
- **Logs are a transcript, not a schema.** A transaction's log messages look like:
  ```
  Program <programId> invoke [1]
  Program log: Instruction: Swap
  Program data: <base64>          # Anchor emit! event, base64 Borsh, prefixed by event discriminator
  Program <programId> consumed 12345 of 200000 compute units
  Program <programId> success
  ```
  `Program log:` lines are free-text the program chose to print. `Program data:` lines are the gold:
  base64-encoded Borsh event payloads (`emit!`) you can decode with the IDL's event layout.

## Path A (preferred): use an already-decoded table

Before decoding anything yourself, check whether the work is done.

- **Dune decoded namespace.** When a program's IDL is uploaded to Dune's decoder, instructions and
  events appear as curated tables (e.g. `<project>_solana.<Program>_call_<Instruction>` and
  `..._evt_<Event>`). Search the Dune schema sidebar for the project name. If the protocol you need
  isn't decoded, **you (or anyone) can submit its IDL to Dune's decoder** — then everyone gets the
  table. That is often the highest-leverage move in a research task.
- **Flipside decoded.** `solana.core.fact_decoded_instructions` exposes decoded program calls with
  `program_id`, `event_type`, and a parsed `decoded_instruction` object — query the args directly.
- **Helius enhanced/parsed transactions** decode many common programs into human-readable types
  (`SWAP`, `NFT_SALE`, `TRANSFER`, …) — good for labeling, not for heavy aggregation.

If a decoded table exists, **use it** and skip the rest of this file. Decoding by hand is a last
resort, not a flex.

## Path B: recognize instructions by discriminator on raw tables

When no decoded table exists, you can still segment activity by instruction type off
`solana.instructions` by matching the leading discriminator bytes.

```sql
-- Q: How many times per day is a specific Anchor instruction called on a program?
-- Compute the 8-byte discriminator once (offline): sha256("global:swap")[..8] -> hex,
-- e.g. 0xf8c69e91e17587c8. Match it against the instruction data prefix.
SELECT
    date_trunc('day', block_time)            AS day,
    count(*)                                 AS swap_calls
FROM solana.instructions
WHERE executing_account = '{{program_id}}'           -- the program being invoked
  AND bytearray_starts_with(data, 0x{{ix_discriminator_hex}})
  AND block_time >= now() - interval '{{days}}' day
GROUP BY 1
ORDER BY 1;
```

Notes:
- Compute the discriminator outside SQL (any sha256 tool, or `anchor idl` tooling). The skill's
  agents can derive it from an instruction name; confirm against one known transaction.
- Column names for raw instruction data vary by table version (`data`, `account_arguments`,
  `executing_account`/`program_id`). **Confirm in the schema sidebar** before shipping — never guess.
- This gives you *counts and timing* of an instruction without full arg decoding — often enough for
  "how busy is this instruction" and adoption curves.

## Path C: decode `Program data:` events from logs

For numbers carried inside events (amounts, fees, prices a program emits via `emit!`), parse the
`Program data:` base64 payload. The event payload is `[event_discriminator(8) ‖ Borsh(fields)]`.

Workflow:
1. From the IDL, take the event's field layout and compute its discriminator
   (`sha256("event:<Event>")[..8]`).
2. Pull candidate log lines (Dune `solana.transactions` carries `log_messages`; or use the
   decoded-events table if present).
3. Base64-decode, strip the 8-byte discriminator, Borsh-decode the remaining bytes per the layout.
4. For repeatable work, **push this into a decoded model** (submit the IDL to Dune, or build a
   Flipside/dbt model) rather than decoding inline every time.

Because inline Borsh decoding in pure SQL is painful, the practical pattern is: use
`scripts/dune_run.py` to pull the raw rows, decode in a small Python step (Borsh layout from the
IDL), and write the result back as a Dune query/table or a Flipside model. The skill prefers
*promoting a program to a decoded table* over one-off inline hacks — it's reusable and auditable.

## Building your own decoded model (when it matters)

If a protocol is central to the analysis and undecoded:
1. **Get the IDL** — from the program's repo, `anchor idl fetch <programId>` (if published on-chain),
   or the project's docs. Confirm it matches the deployed program (version drift is real).
2. **Submit it to Dune's decoder** (fastest path to shareable tables) or model it on Flipside.
3. **Verify** the new table against a handful of known transactions on a block explorer — match
   amounts and counts before you trust it for aggregates.
4. **Document** the discriminators and field meanings in the dashboard so the next analyst doesn't
   re-derive them.

## Pitfalls specific to decoding

- **IDL ≠ deployed program.** A repo IDL can be ahead of or behind mainnet. Always validate against
  a real transaction.
- **Inner instructions (CPI).** A swap may execute as an inner instruction of an aggregator. If you
  only scan top-level instructions you'll undercount; include inner instructions where the table
  exposes them.
- **Native (non-Anchor) programs** don't use Anchor discriminators — their instruction tag is the
  first byte(s) per the program's own enum. Read the program's docs, not the Anchor convention.
- **Versioned transactions & address lookup tables** can change how accounts are referenced; the
  curated tables resolve this, raw scans may not.
- **Don't over-decode.** If `dex_solana.trades` already gives you `amount_usd`, do not hand-decode
  the swap event to recompute it. Decode only the fields no curated table provides.
