# Solana fee-routing and payment primitives

Imported 2026-11-24 from `jmcken19/salary` (`docs/research.md`, `docs/AUDIT.md`, `docs/design-existing-programs.md`, research-v2/04). Those findings were verified on Nov 23, 2026 against SDK source (`@pump-fun/pump-sdk` 4.3.1, `@streamflow/stream` 13.4.0), IDLs and live mainnet reads, unless marked otherwise. Freshness: 90 days, or on an SDK major version.

## Pump.fun creator fees [V unless noted]
- Creator fees build up in the creator vault PDA (`["creator-vault", creator]`) on the bonding curve; after graduation (PumpSwap) they build up in WSOL in the creator vault ATA.
- Fee sharing: up to 10 shareholders by percentage. Editable rule (`isSharingConfigEditable`): v1 → not editable; v2 + `admin_revoked` → not editable; anything else → editable. One change allowed since Mar 25, 2026 [C].
- The distribute instruction can be called by anyone.
- Override: `admin_cto` (signed by `Global.admin_set_creator_authority`) can rewrite a locked split to one new creator, or end it in favour of holder rewards. The program is closed source; behaviour is taken from the SDK docs and Pump's announcement.
- Holder Rewards sends the whole creator fee to holders; it cannot be combined with a split, and converting is gated and permanent [C].
- Pump, Pump fees, Streamflow and Jupiter Lock can each be upgraded by a single key (ProgramData read live, Nov 23 2026).

## Chain census, Nov 23 2026 (slot ≈473.0M) [V]
- 903,612 SharingConfig accounts. In a random sample of 3,000: 95.4% had one shareholder; 4.6% (≈42k coins) had 2–5. 96.3% locked.
- Of 139 multi-wallet coins checked: 1 Streamflow lock to a paid wallet (already closed), 0 Jupiter Locks. Blind study of 20: 20/20 splits locked, 0/20 team locks.
- Jupiter Lock, all 420,580 escrows: 89.7% cancellable/updatable by either party; 5.8% fully irreversible.
- Streamflow, all 80,332 contracts: 41,097 fully fixed.

## Other primitives
- **Streamflow:** locks 0.16 SOL + 0.5% of tokens; streams/payroll; `partner` fee schedule field [V for layout; fees from docs].
- **Jupiter Lock:** no protocol fees; permissions set once [V].
- **Squads v4:** multisig, time lock, spending limits; 0.1 SOL creation fee [C from docs].
- **Bags:** up to 100 claimers; admin can change claimers and bps; no lock product [C].
- **Meteora DBC / Jupiter Studio:** partner-configurable fees, anti-sniper fees, vesting at launch (research-v2/04, S-grade).
- **Raydium LaunchLab:** platform-set splits, team vesting; the platform admin can change fees (research-v2/04, S-grade).

## Limits worth remembering
- A team-pay transaction (collect, unwrap, N transfers, memo) fits about 5–8 people. This is an estimate that was never measured (salary AUDIT, E).
- Nothing in these programs can stop a holder selling tokens they already hold.
