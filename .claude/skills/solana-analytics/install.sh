#!/usr/bin/env bash
# install.sh — install the solana-analytics skill into ~/.claude/skills/solana-analytics
# Usage: ./install.sh [-y|--yes] [-h|--help]
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills/solana-analytics"
ASSUME_YES=0

for arg in "$@"; do
  case "$arg" in
    -y|--yes) ASSUME_YES=1 ;;
    -h|--help)
      echo "Install the solana-analytics skill."
      echo "  -y, --yes   non-interactive (install to ${DEST})"
      echo "  -h, --help  show this help"
      exit 0 ;;
    *) echo "Unknown arg: $arg (try --help)"; exit 1 ;;
  esac
done

echo -e "${BLUE}solana-analytics-skill installer${NC}"
echo -e "  source: ${SRC_DIR}"
echo -e "  target: ${DEST}"

if [ "$ASSUME_YES" -ne 1 ]; then
  printf "Proceed? [y/N] "
  read -r reply
  case "$reply" in [Yy]*) ;; *) echo "Aborted."; exit 0 ;; esac
fi

if [ -d "$DEST" ]; then
  backup="${DEST}.bak.$(date +%Y%m%d%H%M%S)"
  echo -e "${YELLOW}Existing install found — backing up to ${backup}${NC}"
  mv "$DEST" "$backup"
fi

mkdir -p "$DEST"
for item in SKILL.md CLAUDE.md README.md LICENSE .mcp.json references assets scripts agents commands rules; do
  if [ -e "${SRC_DIR}/${item}" ]; then
    cp -R "${SRC_DIR}/${item}" "${DEST}/"
  fi
done

echo -e "${GREEN}✓ Installed to ${DEST}${NC}"
echo "Next:"
echo "  • Optional execution: export DUNE_API_KEY=...  (and HELIUS_API_KEY for live state)"
echo "  • The skill auto-routes from SKILL.md. Ask: \"which DEX is winning on Solana?\""
