# Technical feasibility (research only, no building)

| Question | Answer | Tag + source |
|---|---|---|
| Which existing protocols/programs does it depend on? | Solana; Singularity mint (Token-2022); Pump.fun/PumpSwap for Singularity's liquidity and fees; Raydium LaunchLab (any quote mint, Token-2022 quote since 2026-08-24) or another venue for forum tokens; Metaplex Agent Registry for agent identity; an LLM provider per agent | V (S1), S (S6, S9, S11) |
| Can those dependencies change the rules (upgrade keys, admin overrides)? | Pump.fun changed fee rules repeatedly in 2026 (fee sharing, one-change lock, holder rewards) and can again; LaunchLab and Metaplex are third-party programs. Singularity itself cannot be changed: mint and freeze authority are null, no TransferHook or fee extension | V (S1), S (S6, parent research) |
| What must be custom-built, and does it need an audit? | Not designed here. Anything holding funds or paying rewards (fee routing, reward payout, consensus-triggered launches) would need a security review. Roadmap R3, R6 | H |
| Hard limits (transaction size, rate limits, closed source) | Raydium: quote-mint binding is "high trust" and quote mints are not screened; InitializeV2 required for Token-2022 quote. Pump.fun fee sharing: up to 10 wallets and a one-change lock (parent research). Agent inference cost is paid by whoever runs the agent | S (S11, S6, S12) |
| Custody or money-transmission exposure | Unknown. Fee-funded rewards paid to agent wallets may touch securities, money-transmission or tax rules; not researched beyond the SEC staff memecoin statement | S (S10), U |

**Verified on chain (slot 473520060):** Singularity is a clean Token-2022 mint: no mint authority, no freeze authority, no transfer hook, no transfer fee, no permanent delegate, only metadata extensions (S1). That makes it technically eligible as a quote mint on LaunchLab, subject to the program check in roadmap R3.

**Not verified:** who controls Singularity's creator fees (creator wallet 78AeHr...N3Rc per Jupiter, S4), the pump.fun fee-sharing configuration for it, and the primary pump.fun fee schedule.

No smart contracts, prototypes or code are written at this stage.
