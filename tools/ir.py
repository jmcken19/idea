#!/usr/bin/env python3
"""ir.py: Idea Research CLI. Standard library only.

Subcommands
  note <slug> "<idea in the founder's words>"    save a brainstorm note ideas/<slug>.md (Mode A, only when asked)
  new <slug> "<idea in the submitter's words>"   start a deep validation record validations/<slug>/ (Mode B)
  searched <terms...>                            check the search log and the research index before searching
  log <tool> "<query>" <idea|-> "<result>"       record a search you ran (WebSearch, web-fetch, manual)
  fetch <source> <arg> [--max-age DAYS] [--chars N]  cached GET (logged); prints 3,000 chars by default
  score <slug>                                   compute the score and verdict ceiling from scorecard.md
  lint [slug]                                    check that an idea record follows the framework
  npm-grep <pkg>[@version] <regex>               download an npm package (cached) and grep its files: primary-source SDK evidence
  spend <slug>                                   research spend for an idea from the search log, against the budget
  rpc <method> ['<json params>']                 Solana JSON-RPC call (SOLANA_RPC_URL or the public endpoint), cached
  check-sources [--pages]                        call every data source with a known query and validate the response body
  budget start <slug> <validate|discover> [--research N] [--agents N] --reason "<founder's request>"
  budget status | budget extend <research|agents> <n> --reason "<why>" | budget end
                                                 hard caps enforced by tools/budget_hook.py (see system/usage-budget.md)
  packet-check <slug>                            check validations/<slug>/evidence-packet.md (size cap, sections)

Set IR_IDEA=<slug> in the environment so fetch / npm-grep / rpc calls are attributed
to that idea in the search log and counted by `spend` (export IR_IDEA=salary).

Cached responses live in research/.cache/ (git-ignored). Every fetch and log
entry is appended to research/search-log.md, so later sessions can see what
was already asked and reuse it instead of paying for it again.
"""
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research", ".cache")
SEARCH_LOG = os.path.join(ROOT, "research", "search-log.md")
RESEARCH_INDEX = os.path.join(ROOT, "research", "INDEX.md")
IDEAS = os.path.join(ROOT, "validations")  # Mode B records; brainstorm notes live in ideas/
NOTES = os.path.join(ROOT, "ideas")
IDEA_INDEX = os.path.join(IDEAS, "INDEX.md")
TEMPLATE = os.path.join(ROOT, "templates", "validation")
TODAY = dt.date.today().isoformat()

VERDICTS = ["REJECTED", "NEEDS MORE RESEARCH", "CONDITIONAL OPPORTUNITY", "VALIDATED OPPORTUNITY"]
REQUIRED_FILES = [
    "README.md", "initial-hypothesis.md", "existing-solutions.md", "competitor-analysis.md",
    "market-research.md", "commercial-analysis.md", "technical-feasibility.md",
    "adversarial-review.md", "scorecard.md", "sources.md", "final-verdict.md",
]

# Free endpoints. {q} is URL-encoded. Hosts must be allowed by the environment's network policy.
SOURCES = {
    "defillama-protocol": "https://api.llama.fi/protocol/{q}",
    "defillama-fees": "https://api.llama.fi/summary/fees/{q}?dataType=dailyFees",
    "defillama-revenue": "https://api.llama.fi/summary/fees/{q}?dataType=dailyRevenue",
    "defillama-fees-overview": "https://api.llama.fi/overview/fees/{q}?excludeTotalDataChart=true",
    "coingecko-search": "https://api.coingecko.com/api/v3/search?query={q}",
    "coingecko-coin": "https://api.coingecko.com/api/v3/coins/{q}?localization=false&tickers=false&community_data=false",
    "dexscreener-search": "https://api.dexscreener.com/latest/dex/search?q={q}",
    "dexscreener-token": "https://api.dexscreener.com/latest/dex/tokens/{q}",
    "geckoterminal-pools": "https://api.geckoterminal.com/api/v2/search/pools?query={q}&network=solana",
    "jup-search": "https://lite-api.jup.ag/tokens/v2/search?query={q}",
    "rugcheck": "https://api.rugcheck.xyz/v1/tokens/{q}/report/summary",
    "github-repos": "https://api.github.com/search/repositories?q={q}&per_page=20&sort=updated",
    "github-code": "https://api.github.com/search/code?q={q}&per_page=20",
    "npm": "https://registry.npmjs.org/{q}",
    "npm-search": "https://registry.npmjs.org/-/v1/search?text={q}&size=20",
    "reddit": "https://www.reddit.com/search.json?q={q}&sort=relevance&limit=25",
    "hn": "https://hn.algolia.com/api/v1/search?query={q}",
    "wayback": "https://web.archive.org/cdx/search/cdx?url={q}&output=json&limit=5&fl=timestamp,original",
    "github-raw": "https://raw.githubusercontent.com/{raw}",
    "pypi": "https://pypi.org/pypi/{q}/json",
    "url": "{raw}",
}
# Note (2026-11-24): api.github.com/repos/* is refused for repos not attached to the session,
# but search and raw.githubusercontent.com work. github-raw takes owner/repo/HEAD/path.


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def append_log(tool, query, idea, result):
    if idea in ("-", "", None):
        idea = os.environ.get("IR_IDEA", "-")  # attribute fetches to the idea being researched
    new = not os.path.exists(SEARCH_LOG)
    with open(SEARCH_LOG, "a", encoding="utf-8") as f:
        if new:
            f.write("# Search log\n\nAppend-only. One line per search or fetch. Check with `python3 tools/ir.py searched <terms>` before searching.\n\n| Date | Tool | Query | Idea | Result |\n|---|---|---|---|---|\n")
        clean = lambda s: str(s).replace("|", "/").replace("\n", " ").strip()
        f.write(f"| {TODAY} | {clean(tool)} | {clean(query)} | {clean(idea)} | {clean(result)[:300]} |\n")


def cmd_searched(args):
    if not args:
        die("usage: searched <terms...>")
    terms = [t.lower() for t in args]
    hits = 0
    for path in (SEARCH_LOG, RESEARCH_INDEX, IDEA_INDEX):
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            low = line.lower()
            if all(t in low for t in terms):
                hits += 1
                if hits <= 25:
                    print(f"{os.path.relpath(path, ROOT)}: {line.rstrip()[:240]}")
    for dirpath, _, files in os.walk(os.path.join(ROOT, "research")):
        if ".cache" in dirpath:
            continue
        for fn in files:
            if fn.endswith(".md") and fn not in ("search-log.md", "INDEX.md"):
                p = os.path.join(dirpath, fn)
                text = open(p, encoding="utf-8").read().lower()
                if all(t in text for t in terms):
                    hits += 1
                    if hits <= 25:
                        print(f"mentioned in: {os.path.relpath(p, ROOT)}")
    if hits > 25:
        print(f"-- output capped at 25 lines; add terms to narrow")
    print(f"-- {hits} prior hit(s). Reuse them if they are within their freshness window (system/usage-budget.md).")


def cmd_log(args):
    if len(args) != 4:
        die('usage: log <tool> "<query>" <idea|-> "<one-line result>"')
    append_log(*args)
    print("logged")


def cmd_fetch(args):
    max_age = 7.0
    limit = 3000  # printed characters; the full body is always in the cache file
    if "--chars" in args:
        i = args.index("--chars")
        limit = int(args[i + 1])
        del args[i:i + 2]
    if "--max-age" in args:
        i = args.index("--max-age")
        max_age = float(args[i + 1])
        del args[i:i + 2]
    if len(args) < 2 or args[0] not in SOURCES:
        die("usage: fetch <source> <arg> [--max-age DAYS]\nsources: " + ", ".join(SOURCES))
    src, raw = args[0], " ".join(args[1:])
    url = SOURCES[src].format(q=urllib.parse.quote(raw, safe=":/"), raw=raw)
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    path = os.path.join(CACHE, f"{src}-{key}.json")
    os.makedirs(CACHE, exist_ok=True)
    if os.path.exists(path):
        meta = json.load(open(path, encoding="utf-8"))
        age = (dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.datetime.fromisoformat(meta["fetched_at"])).total_seconds() / 86400
        if age <= max_age:
            print(f"# cache hit ({age:.1f} days old) {url}", file=sys.stderr)
            print((json.dumps(meta["body"], indent=1) if not isinstance(meta["body"], str) else meta["body"])[:limit])
            print(f"# printed {limit} chars; full body in {os.path.relpath(path, ROOT)} (use --chars N or grep it)", file=sys.stderr)
            return
    headers = {"User-Agent": "idea-research-cli/1.0", "Accept": "application/json"}
    if src.startswith("github") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    if src.startswith("coingecko") and os.environ.get("COINGECKO_DEMO_API_KEY"):
        headers["x-cg-demo-api-key"] = os.environ["COINGECKO_DEMO_API_KEY"]
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code} from {url}")
    except (urllib.error.URLError, OSError) as e:
        host = urllib.parse.urlparse(url).hostname
        append_log(f"fetch:{src}", raw, "-", f"FAILED: {host} unreachable ({e})")
        die(f"Could not reach {host}: {e}\nIf this is a proxy 403, the host is not in the environment's allowed hosts. See system/tooling.md.")
    try:
        body = json.loads(data)
    except json.JSONDecodeError:
        body = data
    json.dump({"url": url, "fetched_at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(), "body": body}, open(path, "w", encoding="utf-8"))
    append_log(f"fetch:{src}", raw, "-", f"cached {os.path.relpath(path, ROOT)}")
    print(f"# fetched {url} -> {os.path.relpath(path, ROOT)}", file=sys.stderr)
    print((json.dumps(body, indent=1) if not isinstance(body, str) else body)[:limit])
    print(f"# printed {limit} chars; full body in {os.path.relpath(path, ROOT)} (use --chars N or grep it)", file=sys.stderr)


def cmd_npm_grep(args):
    import io, tarfile
    if len(args) < 2:
        die("usage: npm-grep <pkg>[@version] <regex>")
    spec, rx = args[0], re.compile(" ".join(args[1:]), re.I)
    name, _, ver = spec[1:].partition("@") if spec.startswith("@") else spec.partition("@")
    name = ("@" + name) if spec.startswith("@") else name
    os.makedirs(CACHE, exist_ok=True)
    meta_url = "https://registry.npmjs.org/" + urllib.parse.quote(name, safe="@")
    meta = json.loads(urllib.request.urlopen(urllib.request.Request(meta_url, headers={"User-Agent": "idea-research-cli/1.0"}), timeout=30).read())
    ver = ver or meta["dist-tags"]["latest"]
    if ver not in meta["versions"]:
        die(f"{name}@{ver} not found")
    tar_url = meta["versions"][ver]["dist"]["tarball"]
    path = os.path.join(CACHE, "npm-" + hashlib.sha256(tar_url.encode()).hexdigest()[:20] + ".tgz")
    if not os.path.exists(path):
        data = urllib.request.urlopen(urllib.request.Request(tar_url, headers={"User-Agent": "idea-research-cli/1.0"}), timeout=60).read()
        open(path, "wb").write(data)
        cached = "downloaded"
    else:
        cached = "cache hit"
    published = meta.get("time", {}).get(ver, "?")[:10]
    hits = 0
    with tarfile.open(path) as t:
        for m in t.getmembers():
            if not m.isfile() or m.size > 5_000_000:
                continue
            text = t.extractfile(m).read().decode("utf-8", "replace")
            for i, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    hits += 1
                    if hits <= 40:
                        print(f"{m.name}:{i}: {line.strip()[:200]}")
    print(f"-- {hits} match(es) in {name}@{ver} (published {published}, {cached})")
    append_log("npm-grep", f"{name}@{ver} /{rx.pattern}/", "-", f"{hits} matches; published {published}")


BUDGET = {"WebSearch": 50, "fetch": 60, "page": 30}


def cmd_spend(args):
    if len(args) != 1:
        die("usage: spend <slug>")
    counts = {}
    if os.path.exists(SEARCH_LOG):
        for line in open(SEARCH_LOG, encoding="utf-8"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 5 and cells[3] == args[0]:
                tool = cells[1]
                kind = "WebSearch" if tool.startswith("WebSearch") else "page" if tool in ("web-fetch", "github-raw-read") else "fetch"
                counts[kind] = counts.get(kind, 0) + 1
    for k, cap in BUDGET.items():
        n = counts.get(k, 0)
        flag = "  OVER BUDGET" if n > cap else ""
        print(f"{k:10s} {n:3d} / {cap} (full-pipeline cap){flag}")
    print("Per-stage limits: system/usage-budget.md. Untagged fetches (idea '-') are not counted here.")


def http_get(url, data=None, timeout=25):
    headers = {"User-Agent": "idea-research-cli/1.0", "Accept": "application/json, text/plain, */*"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def cmd_rpc(args):
    if not args:
        die("usage: rpc <method> ['<json params>']")
    url = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    params = json.loads(args[1]) if len(args) > 1 else []
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": args[0], "params": params}).encode()
    key = hashlib.sha256(payload).hexdigest()[:20]
    path = os.path.join(CACHE, f"rpc-{key}.json")
    os.makedirs(CACHE, exist_ok=True)
    try:
        _, body = http_get(url, payload)
    except (urllib.error.URLError, OSError) as e:
        append_log("rpc", args[0], "-", f"FAILED: {e}")
        die(f"RPC unreachable: {e}")
    json.dump({"url": url, "fetched_at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(), "body": json.loads(body)}, open(path, "w"))
    append_log("rpc", f"{args[0]} {args[1] if len(args) > 1 else ''}", "-", f"cached {os.path.relpath(path, ROOT)}")
    print(body[:3000])


# (source, argument, validator) – the validator must confirm real content, not just a 200
CHECKS = [
    ("defillama-fees", "pump.fun", lambda b: isinstance(b, dict) and "total24h" in b),
    ("defillama-protocol", "pump.fun", lambda b: isinstance(b, dict) and b.get("name")),
    ("coingecko-search", "solana", lambda b: isinstance(b, dict) and len(b.get("coins", [])) > 0),
    ("dexscreener-search", "bonk", lambda b: isinstance(b, dict) and len(b.get("pairs") or []) > 0),
    ("geckoterminal-pools", "bonk", lambda b: isinstance(b, dict) and len(b.get("data", [])) > 0),
    ("jup-search", "SOL", lambda b: isinstance(b, list) and len(b) > 0),
    ("rugcheck", "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", lambda b: isinstance(b, dict) and ("score" in b or "risks" in b)),
    ("github-repos", "solana payroll", lambda b: isinstance(b, dict) and b.get("total_count", 0) > 0),
    ("github-raw", "Squads-Protocol/v4/HEAD/README.md", lambda b: isinstance(b, str) and "Squads" in b),
    ("npm", "@pump-fun/pump-sdk", lambda b: isinstance(b, dict) and "dist-tags" in b),
    ("npm-search", "solana payroll", lambda b: isinstance(b, dict) and "objects" in b),
    ("pypi", "solana", lambda b: isinstance(b, dict) and "info" in b),
    ("reddit", "solana fee split", lambda b: isinstance(b, dict) and "data" in b),
    ("hn", "solana", lambda b: isinstance(b, dict) and len(b.get("hits", [])) > 0),
    ("wayback", "bags.fm", lambda b: isinstance(b, list) and len(b) > 1),
]
PAGES = [
    "https://pump.fun/docs/fees", "https://docs.bags.fm/llms.txt", "https://pumpdev.io/claim-distribute",
    "https://streamflow.finance/blog/web3-payroll", "https://docs.squads.so/main/development/reference/spending-limits",
    "https://madeonsol.com/deployer-hunter", "https://docs.mobula.io/llms.txt", "https://gmgn.ai/",
    "https://clanker.gitbook.io/clanker-documentation", "https://docs.dexscreener.com/api/reference",
    "https://www.theblock.co/", "https://cointelegraph.com/",
]


def cmd_check_sources(args):
    rows = []
    for src, arg, ok in CHECKS:
        raw = arg
        url = SOURCES[src].format(q=urllib.parse.quote(raw, safe=":/"), raw=raw)
        try:
            status, text = http_get(url)
            try:
                body = json.loads(text)
            except json.JSONDecodeError:
                body = text
            verdict = "OK (content validated)" if ok(body) else f"RESPONDED {status} but content check FAILED"
        except urllib.error.HTTPError as e:
            verdict = f"HTTP {e.code}"
        except (urllib.error.URLError, OSError) as e:
            verdict = "BLOCKED/UNREACHABLE: " + str(getattr(e, "reason", e))[:90]
        rows.append((src, urllib.parse.urlparse(url).hostname, verdict))
    try:
        _, text = http_get("https://api.mainnet-beta.solana.com", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getSlot"}).encode())
        rows.append(("rpc", "api.mainnet-beta.solana.com", "OK (content validated)" if '"result"' in text else "content check FAILED"))
    except (urllib.error.URLError, OSError) as e:
        rows.append(("rpc", "api.mainnet-beta.solana.com", "BLOCKED/UNREACHABLE: " + str(getattr(e, "reason", e))[:90]))
    if "--pages" in args:
        for u in PAGES:
            try:
                status, text = http_get(u)
                rows.append(("page", u, f"OK {status}, {len(text)} chars" if len(text) > 500 else f"{status} but only {len(text)} chars"))
            except urllib.error.HTTPError as e:
                rows.append(("page", u, f"HTTP {e.code}"))
            except (urllib.error.URLError, OSError) as e:
                rows.append(("page", u, "BLOCKED/UNREACHABLE: " + str(getattr(e, "reason", e))[:90]))
    print(f"Source check {dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec='minutes')}Z\n")
    print("| Source | Host / URL | Result |\n|---|---|---|")
    for r in rows:
        print(f"| {r[0]} | {r[1]} | {r[2]} |")
    ok_n = sum(r[2].startswith("OK") for r in rows)
    print(f"\n{ok_n}/{len(rows)} working.")


def cmd_note(args):
    if len(args) != 2:
        die('usage: note <slug> "<idea in the founder\'s words>"')
    slug, idea = args
    p = os.path.join(NOTES, slug + ".md")
    if os.path.exists(p):
        die(f"{p} exists: update it instead")
    t = open(os.path.join(ROOT, "templates", "idea-note.md"), encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(t.replace("{{SLUG}}", slug).replace("{{DATE}}", TODAY).replace("{{IDEA}}", idea))
    print(f"saved ideas/{slug}.md")


BUDGET_DIR = os.environ.get("IR_BUDGET_DIR", os.path.join(ROOT, "research", ".budget"))
ACTIVE_BUDGET = os.path.join(BUDGET_DIR, "active.json")
PRESETS = {"validate": {"research": 45, "agents": 5}, "discover": {"research": 12, "agents": 1}}
PACKET_MAX_CHARS = 12000
PACKET_SECTIONS = ["## Idea under test", "## Claims and evidence", "## Sources", "## Already searched",
                   "## Open questions", "## Assignments"]


def _flag(args, name, cast=str, default=None):
    if name in args:
        i = args.index(name)
        v = cast(args[i + 1])
        del args[i:i + 2]
        return v
    return default


def cmd_budget(args):
    if not args:
        die("usage: budget start|status|extend|end ...")
    sub, args = args[0], args[1:]
    os.makedirs(BUDGET_DIR, exist_ok=True)
    active = json.load(open(ACTIVE_BUDGET)) if os.path.exists(ACTIVE_BUDGET) else None
    if sub == "start":
        reason = _flag(args, "--reason")
        research = _flag(args, "--research", int)
        agents = _flag(args, "--agents", int)
        if len(args) != 2 or args[1] not in PRESETS or not reason:
            die('usage: budget start <slug> <validate|discover> [--research N] [--agents N] --reason "<founder request>"')
        if active:
            die(f"a workflow is already active ({active['workflow']}). End it first: budget end")
        caps = dict(PRESETS[args[1]])
        caps["research"] = research if research is not None else caps["research"]
        caps["agents"] = agents if agents is not None else caps["agents"]
        expires = (dt.datetime.now() + dt.timedelta(hours=24)).isoformat()
        ledger = {"workflow": f"{args[1]}:{args[0]}", "caps": caps, "used": {}, "reason": reason,
                  "started": dt.datetime.now().isoformat(timespec="seconds"), "expires": expires, "extensions": []}
        json.dump(ledger, open(ACTIVE_BUDGET, "w"), indent=1)
        append_log("budget-start", ledger["workflow"], args[0], f"caps {caps}; reason: {reason}")
        print(f"started {ledger['workflow']} with caps {caps} (expires in 24h)")
    elif sub == "status":
        if not active:
            print("no active workflow: brainstorm defaults apply (research 3 per session, agents 0)")
            return
        for k, cap in active["caps"].items():
            print(f"{k:9s} {active['used'].get(k, 0)}/{cap}")
        print(f"workflow {active['workflow']}; extensions: {len(active['extensions'])}")
    elif sub == "extend":
        reason = _flag(args, "--reason")
        if not active or len(args) != 2 or args[0] not in ("research", "agents") or not reason:
            die('usage: budget extend <research|agents> <n> --reason "<specific justification>" (needs an active workflow)')
        active["caps"][args[0]] += int(args[1])
        active["extensions"].append([dt.datetime.now().isoformat(timespec="seconds"), args[0], int(args[1]), reason])
        json.dump(active, open(ACTIVE_BUDGET, "w"), indent=1)
        append_log("budget-extend", f"{args[0]} +{args[1]}", active["workflow"].split(":", 1)[1], reason)
        print(f"{args[0]} cap now {active['caps'][args[0]]}. Report this extension and its reason to the founder.")
    elif sub == "end":
        if not active:
            die("no active workflow")
        hist = os.path.join(BUDGET_DIR, "history")
        os.makedirs(hist, exist_ok=True)
        os.replace(ACTIVE_BUDGET, os.path.join(hist, active["workflow"].replace(":", "-") + "-" + TODAY + ".json"))
        append_log("budget-end", active["workflow"], active["workflow"].split(":", 1)[1], f"used {active['used']} of {active['caps']}")
        print(f"ended {active['workflow']}: used {active['used']} of {active['caps']}")
    else:
        die("usage: budget start|status|extend|end")


def cmd_packet_check(args):
    if len(args) != 1:
        die("usage: packet-check <slug>")
    p = os.path.join(IDEAS, args[0], "evidence-packet.md")
    if not os.path.exists(p):
        die(f"missing {p} (copy templates/validation/evidence-packet.md)")
    text = open(p, encoding="utf-8").read()
    problems = [f"missing section '{h}'" for h in PACKET_SECTIONS if h not in text]
    if len(text) > PACKET_MAX_CHARS:
        problems.append(f"{len(text)} chars exceeds the {PACKET_MAX_CHARS}-char cap: compress claims, cite S-IDs instead of quoting")
    if re.search(r"^##\s*(Lead'?s (view|conclusion)|Verdict|Recommendation)", text, re.M | re.I):
        problems.append("packet contains the lead's conclusions; keep them out so specialists and the reviewer judge independently")
    for prob in problems:
        print(" - " + prob)
    print(f"packet {len(text)}/{PACKET_MAX_CHARS} chars: {'OK' if not problems else 'FIX BEFORE HANDOFF'}")
    sys.exit(1 if problems else 0)


def cmd_new(args):
    if len(args) != 2:
        die('usage: new <slug> "<idea in the submitter\'s own words>"')
    slug, idea = args
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", slug):
        die("slug: lowercase letters, digits and hyphens")
    dest = os.path.join(IDEAS, slug)
    if os.path.exists(dest):
        die(f"{dest} exists. Reuse and update it instead of starting again.")
    shutil.copytree(TEMPLATE, dest)
    for fn in os.listdir(dest):
        p = os.path.join(dest, fn)
        s = open(p, encoding="utf-8").read().replace("{{SLUG}}", slug).replace("{{DATE}}", TODAY).replace("{{IDEA}}", idea)
        open(p, "w", encoding="utf-8").write(s)
    with open(IDEA_INDEX, "a", encoding="utf-8") as f:
        f.write(f"| [{slug}]({slug}/) | {TODAY} | Stage 1 | NOT YET DECIDED | {idea[:120]} |\n")
    print(f"created validations/{slug}/. Next: fill initial-hypothesis.md, then the existence check (Stage 2).")


def parse_scorecard(slug):
    p = os.path.join(IDEAS, slug, "scorecard.md")
    if not os.path.exists(p):
        die(f"missing {p}")
    rows = []
    for line in open(p, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and re.fullmatch(r"\d+", cells[0] or ""):
            # | # | Criterion | Weight | Score (0-5 or ?) | Fatal (yes/no) | Evidence IDs | Rationale |
            num, crit, weight, score, fatal = cells[:5]
            evidence = cells[5] if len(cells) > 5 else ""
            rows.append({"n": int(num), "criterion": crit, "weight": float(weight or 0),
                         "score": None if score in ("?", "", "-") else float(score),
                         "fatal": fatal.lower().startswith("y"), "evidence": evidence})
    return rows


def evaluate(rows):
    """Return (weighted score 0-100 or None, verdict ceiling, reasons)."""
    reasons, ceiling = [], 3
    by = {r["n"]: r for r in rows}
    for r in rows:
        if r["score"] is not None and r["score"] > 0 and not re.search(r"S\d+", r["evidence"]):
            reasons.append(f"#{r['n']} {r['criterion']}: score {r['score']} has no source IDs, treated as unverified (?)")
            r["score"] = None
    if any(r["fatal"] for r in rows):
        ceiling = 0
        reasons += [f"FATAL: #{r['n']} {r['criterion']}" for r in rows if r["fatal"]]
    orig, comp = by.get(1, {}).get("score"), by.get(2, {}).get("score")
    if orig is not None and comp is not None and orig <= 1 and comp <= 1:
        ceiling = 0
        reasons.append("GATE: an equivalent exists (#2 <= 1) and differentiation is not meaningful (#1 <= 1)")
    dem = by.get(3, {}).get("score")
    if dem is None or dem <= 1:
        ceiling = min(ceiling, 1)
        reasons.append("CAP: verified demand unknown or <= 1: at most NEEDS MORE RESEARCH")
    elif dem < 3:
        ceiling = min(ceiling, 2)
        reasons.append("CAP: verified demand < 3: at most CONDITIONAL OPPORTUNITY")
    for r in rows:
        if r["score"] is not None and r["score"] <= 1 and ceiling > 2:
            ceiling = 2
            reasons.append(f"CAP: #{r['n']} {r['criterion']} scored <= 1: at most CONDITIONAL OPPORTUNITY")
    unknown = [r for r in rows if r["score"] is None]
    if unknown and ceiling >= 2:
        ceiling = min(ceiling, 2 if len(unknown) <= 2 else 1)
        reasons.append(f"CAP: {len(unknown)} criterion/criteria unverified")
    scored = [r for r in rows if r["score"] is not None]
    total_w = sum(r["weight"] for r in rows) or 1
    pts = sum(r["score"] / 5 * r["weight"] for r in scored)
    return round(100 * pts / total_w, 1), ceiling, reasons


def cmd_score(args):
    if len(args) != 1:
        die("usage: score <slug>")
    rows = parse_scorecard(args[0])
    if len(rows) != 10:
        die(f"scorecard.md must have 10 scored criteria, found {len(rows)}")
    score, ceiling, reasons = evaluate(rows)
    print(f"weighted score: {score}/100 (unverified criteria count as 0)")
    print(f"verdict ceiling: {VERDICTS[ceiling]}")
    for r in reasons:
        print(" - " + r)
    print("The ceiling is a maximum, not a target. The verdict follows the evidence, and can be lower.")


def declared_verdict(slug):
    p = os.path.join(IDEAS, slug, "final-verdict.md")
    if not os.path.exists(p):
        return None
    m = re.search(r"^\*\*Verdict:\*\*\s*(.+)$", open(p, encoding="utf-8").read(), re.M)
    if not m:
        return None
    v = m.group(1).strip().upper().replace("*", "")
    return next((x for x in VERDICTS if v.startswith(x)), v)



# ---- Demand classification: engagement is never demand (system/research-standards.md §8) ----
DEMAND_KINDS = {
    # kind: highest demand level it can ever support
    "engagement": 1, "likes": 1, "followers": 1, "views": 1, "upvotes": 1, "comments": 1, "stars": 1,
    "forks": 1, "community-members": 1, "waitlist": 1, "survey-interest": 1, "kol-mention": 1,
    "token-price": 1, "token-volume": 1, "press-coverage": 1, "discussion": 1, "complaint": 1,
    "request": 2, "bounty-posted": 2, "rfp": 2, "search-for-tool": 2, "feature-request": 2,
    "downloads": 3, "onchain-usage": 3, "active-users": 3, "integration": 3, "workaround-built": 3,
    "native-feature-usage": 3,
    "paid-product": 4, "revenue": 4, "fees-paid": 4, "price-paid": 4, "paid-preorder": 4, "contract": 4,
}


def demand_rows(d):
    """Rows of the 'Demand evidence' table in market-research.md:
    | Evidence | Kind | Level | Direction | Tag + source |"""
    p = os.path.join(d, "market-research.md")
    if not os.path.exists(p):
        return None
    text = open(p, encoding="utf-8").read()
    if "## Demand evidence" not in text:
        return None
    sect = text.split("## Demand evidence", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in sect.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0] not in ("Evidence", "") and not set(cells[0]) <= set("-: "):
            rows.append({"evidence": cells[0], "kind": cells[1].lower(), "level": cells[2], "dir": cells[3], "tag": cells[4]})
    return rows


def check_demand(d):
    problems, rows = [], demand_rows(d)
    if rows is None:
        return problems, 0
    best = 0
    for r in rows:
        if r["kind"] not in DEMAND_KINDS:
            problems.append(f"demand row '{r['evidence'][:40]}': unknown kind '{r['kind']}' (see DEMAND_KINDS)")
            continue
        try:
            lvl = int(r["level"])
        except ValueError:
            problems.append(f"demand row '{r['evidence'][:40]}': level must be 1-4")
            continue
        cap = DEMAND_KINDS[r["kind"]]
        if lvl > cap:
            problems.append(f"demand row '{r['evidence'][:40]}': kind '{r['kind']}' can support at most level {cap}, not {lvl} (engagement is not demand)")
        strong = re.search(r"\[(V|C)\b", r["tag"])
        if lvl >= 3 and strong and r["dir"].strip().startswith("+"):
            best = max(best, min(lvl, cap))
    return problems, best


def safeguard_checks(d):
    """Permanent safeguards added 2026-11-24 (system/research-standards.md §8)."""
    problems = []
    read = lambda fn: open(os.path.join(d, fn), encoding="utf-8").read() if os.path.exists(os.path.join(d, fn)) else ""
    es, fv, src = read("existing-solutions.md"), read("final-verdict.md"), read("sources.md")
    types = {}
    for line in src.splitlines():
        m = re.match(r"\|\s*(S\d+)\s*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            types[m.group(1)] = cells[3].lower() if len(cells) > 3 else ""
    direct = lambda ids: [i for i in ids if types.get(i, "").startswith(("primary", "onchain", "repo"))]
    # SG1: fatal competitor findings rest on direct evidence where available
    rows = parse_scorecard(d) if os.path.exists(os.path.join(d, "scorecard.md")) else []
    by = {r["n"]: r for r in rows}
    gate = by.get(2, {}).get("score") is not None and by.get(1, {}).get("score") is not None and by[2]["score"] <= 1 and by[1]["score"] <= 1
    for r in rows:
        if (r["fatal"] or (gate and r["n"] in (1, 2))):
            ids = re.findall(r"S\d+", r["evidence"])
            if not direct(ids) and "Direct evidence unavailable:" not in fv:
                problems.append(f"SG1: #{r['n']} is fatal/gating but cites no primary/onchain/repo source; add one or explain under 'Direct evidence unavailable:' in final-verdict.md")
    # SG3/SG4: replicators, recent launches and discontinued projects are covered
    if es and "## Easy replicators" not in es:
        problems.append("SG3: existing-solutions.md lacks '## Easy replicators' (who could copy this quickly)")
    elif es:
        rep = es.split("## Easy replicators", 1)[1].split("\n## ", 1)[0]
        if not re.search(r"^\|(?!\s*-)(?!\s*Product)(?!\s*Who).+\|", rep, re.M):
            problems.append("SG3: '## Easy replicators' has no rows")
    for label in ("Recent launches", "Discontinued"):
        m = re.search(r"^\|\s*" + label + r"[^|]*\|\s*([^|]*)\|", es, re.M)
        if not m:
            problems.append(f"SG4: coverage table lacks a '{label} …' row")
        elif not re.match(r"(yes|blocked)", m.group(1).strip(), re.I):
            problems.append(f"SG4: '{label}' coverage is '{m.group(1).strip()}': must be Yes or 'Blocked: <reason>'")
    # SG5: absence of evidence is never scored as opportunity
    incomplete = re.findall(r"^\|[^|]+\|\s*(no|partly|blocked)[^|]*\|", es, re.M | re.I)
    for n in (1, 2):
        sc = by.get(n, {}).get("score")
        if incomplete and sc is not None and sc >= 4:
            problems.append(f"SG5: #{n} scored {sc} while {len(incomplete)} coverage channel(s) are incomplete: lack of evidence is not evidence of opportunity")
    # SG2: sample statistics state n and representativeness
    for fn in REQUIRED_FILES + ["postmortem.md"]:
        for i, line in enumerate(read(fn).splitlines(), 1):
            if re.search(r"\b(sample|sampled|study)\b", line, re.I) and re.search(r"\d+\s*(%|/\s*\d+|of\s+\d+)", line):
                if not re.search(r"n\s*=\s*[\d,]+", line):
                    problems.append(f"SG2: {fn}:{i} quotes a sample statistic without 'n=' and its representativeness")
    # SG6: every final verdict names unresolved uncertainties
    v = declared_verdict(d)
    if v in VERDICTS:
        if "## Unresolved uncertainties" not in fv:
            problems.append("SG6: final-verdict.md lacks '## Unresolved uncertainties'")
        else:
            body = fv.split("## Unresolved uncertainties", 1)[1].split("\n## ", 1)[0].strip()
            if len(body) < 20:
                problems.append("SG6: '## Unresolved uncertainties' is empty")
    # Demand: engagement cannot be counted as demand; demand score needs matching evidence
    dp, best = check_demand(d)
    problems += dp
    dem = by.get(3, {}).get("score")
    if dem is not None and dem >= 3 and best < 3:
        problems.append(f"DEMAND: #3 verified demand scored {dem} but market-research.md has no (+) level-3/4 row with V/C evidence")
    return problems


def lint_one(slug):
    problems = []
    d = os.path.join(IDEAS, slug)
    for fn in REQUIRED_FILES:
        if not os.path.exists(os.path.join(d, fn)):
            problems.append(f"missing {fn}")
    src = os.path.join(d, "sources.md")
    ids = set()
    if os.path.exists(src):
        for line in open(src, encoding="utf-8"):
            m = re.match(r"\|\s*(S\d+)\s*\|", line)
            if m:
                ids.add(m.group(1))
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 7 or not cells[2].startswith(("http", "repo:", "chain:", "file:", "npm:", "github:")):
                    problems.append(f"sources.md {m.group(1)}: needs a URL / repo: / npm: / github: / chain: / file: locator")
                elif not re.match(r"\d{4}-\d{2}-\d{2}", cells[5]):
                    problems.append(f"sources.md {m.group(1)}: accessed date missing")
    for fn in REQUIRED_FILES:
        p = os.path.join(d, fn)
        if os.path.exists(p) and fn != "sources.md":
            for ref in set(re.findall(r"\bS\d+\b", open(p, encoding="utf-8").read())):
                if ids and ref not in ids:
                    problems.append(f"{fn} cites {ref}, which is not in sources.md")
    v = declared_verdict(slug)
    if v is None:
        problems.append("final-verdict.md has no '**Verdict:** ...' line (use NOT YET DECIDED while in progress)")
    elif v in VERDICTS and os.path.exists(os.path.join(d, "scorecard.md")):
        rows = parse_scorecard(slug)
        if len(rows) == 10:
            _, ceiling, _ = evaluate(rows)
            if VERDICTS.index(v) > ceiling:
                problems.append(f"verdict {v} exceeds the scorecard ceiling {VERDICTS[ceiling]}")
        if VERDICTS.index(v) >= 2:
            adv = open(os.path.join(d, "adversarial-review.md"), encoding="utf-8").read()
            if "Reviewer:" not in adv or "TODO" in adv:
                problems.append("CONDITIONAL/VALIDATED needs a completed independent adversarial review")
    problems += safeguard_checks(d)
    return problems


def cmd_lint(args):
    slugs = args or sorted(x for x in os.listdir(IDEAS) if os.path.isdir(os.path.join(IDEAS, x)))
    if not slugs:
        print("no validation records yet (lessons/ holds frozen historical records and is not linted)")
    bad = 0
    for s in slugs:
        probs = lint_one(s)
        print(f"{s}: {'OK' if not probs else str(len(probs)) + ' problem(s)'}")
        for p in probs:
            print("  - " + p)
        bad += bool(probs)
    sys.exit(1 if bad else 0)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, args = sys.argv[1], sys.argv[2:]
    {"new": cmd_new, "note": cmd_note, "searched": cmd_searched, "log": cmd_log, "fetch": cmd_fetch,
     "score": cmd_score, "lint": cmd_lint, "npm-grep": cmd_npm_grep, "spend": cmd_spend,
     "rpc": cmd_rpc, "check-sources": cmd_check_sources,
     "budget": cmd_budget, "packet-check": cmd_packet_check}.get(cmd, lambda a: die(f"unknown command {cmd}"))(args)


if __name__ == "__main__":
    main()
