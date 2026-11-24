#!/usr/bin/env python3
"""PreToolUse hook: hard research budgets (standard library only).

Claude Code runs this before matching tool calls (see .claude/settings.json) and passes
the call as JSON on stdin. Exit 0 allows the call; exit 2 blocks it and shows stderr to Claude.

What it counts
  research : WebSearch, WebFetch, the web-fetch agent, and Bash calls to
             tools/ir.py fetch|npm-grep|rpc|check-sources
  agents   : every other Agent/Task launch, plus SendMessage resumes during a workflow
  prompt   : the size of any agent prompt (a cap on the context handed to an agent)

Budgets
  No active workflow (brainstorming, default): research 3 per session, agents 0.
  Active workflow (started only on the founder's explicit request with
  `python3 tools/ir.py budget start ...`): the caps written in research/.budget/active.json.

Limits of enforcement (documented in system/usage-budget.md): only calls that pass
through these tools are counted. A deliberate bypass (e.g. raw curl) is not caught. Failed
calls count too, so retries cost budget. If the ledger can't be read, the hook allows the call
(fail-open) and prints a warning.
"""
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUDGET_DIR = os.environ.get("IR_BUDGET_DIR", os.path.join(ROOT, "research", ".budget"))
ACTIVE = os.path.join(BUDGET_DIR, "active.json")
DEFAULT_CAPS = {"research": 3, "agents": 0}
MAX_PROMPT_CHARS = 16000
SPECIALISTS = {"market-researcher", "technical-researcher", "commercial-analyst", "adversarial-reviewer", "extractor"}
IR_RESEARCH = re.compile(r"tools/ir\.py\s+(fetch|npm-grep|rpc|check-sources)\b")

STOP = ("BUDGET EXHAUSTED ({what}: {used}/{cap}). Do not retry or work around this. "
        "Summarize the evidence collected so far, list the unanswered questions, and stop. "
        "Only the founder can approve more: `python3 tools/ir.py budget extend <kind> <n> --reason \"...\"`.")


def classify(tool, inp):
    if tool in ("WebSearch", "WebFetch"):
        return "research"
    if tool in ("Agent", "Task"):
        return "research" if inp.get("subagent_type") == "web-fetch" else "agents"
    if tool == "SendMessage":
        return "resume"
    if tool == "Bash" and IR_RESEARCH.search(inp.get("command", "")):
        return "research"
    return None


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    tool, inp = event.get("tool_name", ""), event.get("tool_input") or {}
    kind = classify(tool, inp)
    if kind is None:
        return 0
    if kind == "agents" and len(inp.get("prompt", "")) > MAX_PROMPT_CHARS:
        print(f"BLOCKED: agent prompt is {len(inp['prompt'])} chars (cap {MAX_PROMPT_CHARS}). "
              "Pass the evidence packet path and the specific sections instead of pasting files.", file=sys.stderr)
        return 2
    try:
        os.makedirs(BUDGET_DIR, exist_ok=True)
        ledger = load(ACTIVE, None)
        if ledger and ledger.get("expires", "") < dt.datetime.now().isoformat():
            ledger = None
        if ledger:
            path = ACTIVE
        else:
            sid = re.sub(r"[^A-Za-z0-9_-]", "", str(event.get("session_id", "unknown")))[:64]
            path = os.path.join(BUDGET_DIR, f"session-{sid}.json")
            ledger = load(path, {"workflow": "brainstorm (default)", "caps": dict(DEFAULT_CAPS), "used": {}})
        if kind == "resume":
            if ledger.get("workflow", "").startswith("brainstorm"):
                return 0  # messages outside a workflow are not research
            kind = "agents"
        cap = ledger["caps"].get(kind, 0)
        used = ledger["used"].get(kind, 0)
        if used >= cap:
            what = f"{ledger.get('workflow')} / {kind}"
            if ledger.get("workflow", "").startswith("brainstorm") and kind == "agents":
                print("BLOCKED: brainstorming uses the main session only (0 agents). Agents run only in a deep "
                      "validation or discovery scan the founder explicitly asked for (`python3 tools/ir.py budget start`).",
                      file=sys.stderr)
            else:
                print(STOP.format(what=what, used=used, cap=cap), file=sys.stderr)
            return 2
        ledger["used"][kind] = used + 1
        ledger.setdefault("log", []).append([dt.datetime.now().isoformat(timespec="seconds"), tool, kind])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=1)
        left = cap - used - 1
        if left <= 1:
            print(f"budget note: {kind} {used + 1}/{cap} used in '{ledger.get('workflow')}'", file=sys.stderr)
        return 0
    except Exception as e:  # fail-open: never break the session over a ledger problem
        print(f"budget hook warning (call allowed): {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
