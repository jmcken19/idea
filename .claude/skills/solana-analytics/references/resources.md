# Resources & Table Cheat-Sheet

Links and quick references the skill leans on. Confirm table/column names in the platform's schema
sidebar before shipping — Spellbook evolves.

## Platforms & docs

- **Dune** — docs.dune.com · DuneSQL (Trino) reference · the Spellbook repo (open-source curated
  models): github.com/duneanalytics/spellbook · the Dune decoder (submit an IDL to get decoded
  tables).
- **Flipside** — flipsidecrypto.xyz · Snowflake SQL · `solana.core` / `solana.defi` schemas.
- **Helius** — docs.helius.dev · Digital Asset Standard (DAS) API · Enhanced Transactions ·
  webhooks / LaserStream.
- **DefiLlama** — defillama.com · the market's trust metric for TVL (use it to sanity-check on-chain
  reconstructions).
- **Solana docs** — Anchor (anchor-lang.com) for IDL/discriminator conventions · SPL Token & Token-2022.

## Dune Solana table cheat-sheet

| Need | Table | Key columns |
| --- | --- | --- |
| Activity / DAU / fees | `solana.transactions` | `signer`, `block_time`, `success`, `fee` |
| Scope to a program | `solana.instructions` | `program_id` / `executing_account`, `data` |
| DEX swaps (USD) | `dex_solana.trades` | `amount_usd`, `project`, `trader_id`, `token_*_mint_address`, `token_pair`, `block_date` |
| Cross-chain DEX | `dex.trades` | `blockchain`, `amount_usd`, `taker` |
| SPL transfers | `tokens_solana.transfers` | `token_mint_address`, `from_owner`, `to_owner`, `amount` |
| Pricing | `prices.usd` | `blockchain`, `contract_address`, `minute`, `price` |
| Staking rewards | `solana.rewards` (+ staking models) | epoch, reward, validator |
| Decoded program calls | `<project>_solana.<Program>_call_<Ix>` / `_evt_<Event>` | per-IDL args |

## Flipside quick map

`solana.core.fact_transactions` · `solana.core.fact_events` · `solana.defi.fact_swaps` ·
`solana.core.fact_transfers` · `solana.core.fact_decoded_instructions` ·
`solana.price.ez_prices_hourly` · `solana.gov.fact_staking`.

## Anchor discriminators (for `02` decoding)

- instruction: `sha256("global:<snake_ix_name>")[..8]`
- account:     `sha256("account:<AccountName>")[..8]`
- event:       `sha256("event:<EventName>")[..8]`

`emit!` events ride in `Program data:` log lines as base64 `[discriminator(8) ‖ Borsh(fields)]`.

## Known-account labels (maintain & exclude in `05`/`06`)

Keep a project-local list of CEX hot/deposit wallets, bridge contracts (Wormhole, deBridge,
Allbridge), and a token's own mint authority / program PDAs / LP pools. These dominate balance and
funding-graph queries and must be excluded or labeled before reporting concentration, whales, or
sybil clusters.

## The 8 source dashboards (lineage of the query library)

Reverse-engineered from professional Dune work by **dune**, **cryptokoryo**, **21sharesresearch**,
and **web3precious** (DEX Metrics, BTC Pairs/Narratives, Crypto Buy Signal, Bitcoin Key Metrics,
Pump.fun vs LetsBonk, xStocks Traders, SolFi, Monad MON). The 22 templates in
`assets/dune-query-library.sql` generalize the patterns those dashboards are built from.

## House voice

Institutional but sharp. *"The blockchain never lies. Stop guessing. Start querying."* — @Ghostieemoh.
