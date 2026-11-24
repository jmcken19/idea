# Changelog

All notable changes to **solana-analytics-skill** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/).

## [0.1.0] — 2026-06-29

Initial release — the missing on-chain **analytics** layer for the Solana AI Kit.

### Added
- `SKILL.md` router with progressive, intent-based loading into focused `references/`.
- 10 reference modules: data sources, IDL/log decoding, protocol KPIs, DeFi-by-vertical,
  holder/wallet, forensics, growth & grant reporting, dashboard build, execution playbook, resources.
- `assets/dune-query-library.sql` — 22 parameterized DuneSQL templates (Solana-first, EVM-aware).
- `scripts/dune_run.py` — dependency-free Dune client (`validate`/`create`/`run`/`results`) plus an
  Anchor discriminator deriver; `scripts/test_dune_run.py` with 12 offline unit tests.
- Executable layer: `.mcp.json` wiring the **Dune** and **Helius** MCP servers, env-keyed.
- 3 agents (analytics-architect, sql-engineer, forensics-analyst), 5 commands, and SQL-convention rules.
- Installers (`install.sh`, `install-custom.sh`, `install.ps1`) and a CI workflow (tests + SQL slop gate).

### Notes
- MCP endpoints verified against official sources: Dune `https://api.dune.com/mcp/v1`
  (header `x-dune-api-key`) and the `helius-mcp` npm package.
- MIT licensed. Methodology reverse-engineered from 8 professional Dune dashboards.

[0.1.0]: https://github.com/Ghostiemoh/solana-analytics-skill/releases/tag/v0.1.0
