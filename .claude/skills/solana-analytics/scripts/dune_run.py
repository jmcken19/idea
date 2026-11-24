#!/usr/bin/env python3
"""
dune_run.py - minimal, dependency-free Dune Analytics client for the solana-analytics-skill.
By Muhammad Auwal Abdul Aziz (@Ghostieemoh).

Lets the skill actually DO things on Dune: create a query, execute it, poll, and fetch results
(so a query is validated before it is handed over or wired into a dashboard). Also derives Anchor
instruction/account/event discriminators for the decoding workflow (references/02-decoding.md).

Auth: set the DUNE_API_KEY environment variable. Creating/updating queries needs an Analyst plan or
higher; reading results works on lower tiers. Dashboards are assembled in the Dune UI from the query
IDs this script creates - there is no public create-dashboard endpoint.

Usage:
  python dune_run.py validate path/to/query.sql --params params.json   # create+run+preview, then trash
  python dune_run.py create   path/to/query.sql --name "DAU - Solana"  # create a saved query -> prints id
  python dune_run.py run      <query_id> --params params.json          # execute saved query -> results
  python dune_run.py results  <query_id>                               # latest cached results
  python dune_run.py discriminator global swap                         # Anchor discriminator (hex)

params.json is a flat object of Dune parameter values, e.g. {"days": "30", "project": "raydium"}.
Exit code is non-zero on failure so callers can branch.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.dune.com/api/v1"
DISCRIMINATOR_NAMESPACES = ("global", "account", "event")


# --------------------------------------------------------------------------------------
# Pure helpers (no network, no env) - covered by scripts/test_dune_run.py
# --------------------------------------------------------------------------------------
def anchor_discriminator(namespace: str, name: str) -> str:
    """Return the 8-byte Anchor discriminator (hex) for an instruction/account/event.

    Anchor hashes the preimage "<namespace>:<name>" with sha256 and takes the first 8 bytes:
      instruction -> namespace "global"  account -> "account"  event -> "event".
    See references/02-decoding.md.
    """
    if namespace not in DISCRIMINATOR_NAMESPACES:
        raise ValueError(f"namespace must be one of {DISCRIMINATOR_NAMESPACES}, got {namespace!r}")
    preimage = f"{namespace}:{name}".encode("utf-8")
    return hashlib.sha256(preimage).hexdigest()[:16]  # 8 bytes = 16 hex chars


def build_create_payload(sql: str, name: str, params: dict, private: bool) -> dict:
    """Build the POST /query body. Pure so it can be unit-tested without an API key."""
    payload = {"name": name, "query_sql": sql, "is_private": private}
    if params:
        payload["parameters"] = [
            {"key": k, "type": "text", "value": str(v)} for k, v in params.items()
        ]
    return payload


def load_params(path: str | None) -> dict:
    """Load a flat params.json, or {} when no path is given."""
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("params file must be a flat JSON object of key -> value")
    return data


# --------------------------------------------------------------------------------------
# Network layer (needs DUNE_API_KEY)
# --------------------------------------------------------------------------------------
def _key() -> str:
    k = os.environ.get("DUNE_API_KEY")
    if not k:
        sys.exit("ERROR: DUNE_API_KEY is not set. Export it, then retry. "
                 "Get a key at dune.com -> Settings -> API.")
    return k


def _req(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("X-DUNE-API-KEY", _key())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"ERROR {e.code} on {method} {path}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: network failure on {method} {path}: {e.reason}")


def create_query(sql_path: str, name: str, params: dict, private: bool) -> int:
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    res = _req("POST", "/query", build_create_payload(sql, name, params, private))
    return res["query_id"]


def execute_and_wait(query_id: int, params: dict, poll_s: float = 2.0, timeout_s: float = 300) -> dict:
    body = {"query_parameters": params} if params else None
    ex = _req("POST", f"/query/{query_id}/execute", body)
    execution_id = ex["execution_id"]
    waited = 0.0
    while waited < timeout_s:
        st = _req("GET", f"/execution/{execution_id}/status")
        state = st.get("state")
        if state == "QUERY_STATE_COMPLETED":
            return _req("GET", f"/execution/{execution_id}/results")
        if state in ("QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED", "QUERY_STATE_EXPIRED"):
            sys.exit(f"ERROR: execution ended in state {state}. "
                     f"Likely a SQL error, timeout, or bad parameters.")
        time.sleep(poll_s)
        waited += poll_s
    sys.exit(f"ERROR: query {query_id} did not complete within {timeout_s}s. "
             f"Optimize it (bound block_time, pre-aggregate) - see references/09-execution-playbook.md.")


def latest_results(query_id: int) -> dict:
    return _req("GET", f"/query/{query_id}/results")


def _preview(results: dict, limit: int = 10) -> None:
    rows = results.get("result", {}).get("rows", [])
    meta = results.get("result", {}).get("metadata", {})
    print(f"rows_returned: {len(rows)}  (total reported: {meta.get('total_row_count', 'n/a')})")
    if not rows:
        print("WARNING: zero rows. Check filters/params before trusting this query.")
        return
    cols = list(rows[0].keys())
    print("columns: " + ", ".join(cols))
    print("--- sample ---")
    for r in rows[:limit]:
        print(json.dumps(r, default=str))


def main() -> None:
    p = argparse.ArgumentParser(description="Minimal Dune API client for the solana-analytics-skill.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("validate", help="create a private query, run it, preview rows, then delete it")
    pv.add_argument("sql_path")
    pv.add_argument("--params")
    pv.add_argument("--name", default="[validate] solana-analytics-skill")

    pc = sub.add_parser("create", help="create a saved query and print its id")
    pc.add_argument("sql_path")
    pc.add_argument("--params")
    pc.add_argument("--name", required=True)
    pc.add_argument("--private", action="store_true")

    pr = sub.add_parser("run", help="execute a saved query by id and print results")
    pr.add_argument("query_id", type=int)
    pr.add_argument("--params")

    pg = sub.add_parser("results", help="fetch latest cached results for a query id")
    pg.add_argument("query_id", type=int)

    pd = sub.add_parser("discriminator", help="derive an Anchor discriminator (hex) - no network")
    pd.add_argument("namespace", choices=DISCRIMINATOR_NAMESPACES)
    pd.add_argument("name")

    args = p.parse_args()

    if args.cmd == "validate":
        params = load_params(args.params)
        qid = create_query(args.sql_path, args.name, params, private=True)
        print(f"created temp query {qid}; executing...")
        res = execute_and_wait(qid, params)
        _preview(res)
        _req("DELETE", f"/query/{qid}")  # best-effort cleanup
        print(f"deleted temp query {qid}.")
    elif args.cmd == "create":
        params = load_params(args.params)
        qid = create_query(args.sql_path, args.name, params, private=args.private)
        print(f"query_id: {qid}")
        print(f"url: https://dune.com/queries/{qid}")
    elif args.cmd == "run":
        res = execute_and_wait(args.query_id, load_params(args.params))
        _preview(res, limit=25)
    elif args.cmd == "results":
        _preview(latest_results(args.query_id), limit=25)
    elif args.cmd == "discriminator":
        print(f"0x{anchor_discriminator(args.namespace, args.name)}")


if __name__ == "__main__":
    main()
