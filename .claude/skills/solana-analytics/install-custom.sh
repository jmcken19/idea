#!/usr/bin/env bash
# install-custom.sh — install solana-analytics with control over location.
# Usage: ./install-custom.sh [--personal | --project DIR] [--name NAME] [-y]
#   --personal       install to ~/.claude/skills/<name>   (default)
#   --project DIR     install to DIR/.claude/skills/<name>
#   --name NAME       skill folder name (default: solana-analytics)
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="personal"; PROJECT_DIR=""; NAME="solana-analytics"; ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    --personal) MODE="personal" ;;
    --project) MODE="project"; PROJECT_DIR="${2:-}"; shift ;;
    --name) NAME="${2:-solana-analytics}"; shift ;;
    -y|--yes) ASSUME_YES=1 ;;
    -h|--help)
      sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1 (try --help)"; exit 1 ;;
  esac
  shift
done

if [ "$MODE" = "project" ]; then
  [ -n "$PROJECT_DIR" ] || { echo "--project needs a DIR"; exit 1; }
  DEST="${PROJECT_DIR%/}/.claude/skills/${NAME}"
else
  DEST="${HOME}/.claude/skills/${NAME}"
fi

echo -e "${BLUE}solana-analytics-skill custom installer${NC}"
echo -e "  mode:   ${MODE}"
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
echo "Set DUNE_API_KEY (and HELIUS_API_KEY) to enable live query execution."
