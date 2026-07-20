#!/usr/bin/env python3
"""End-to-end smoke test for the Enterprise AI Platform.

Exercises every service in the deployed stack and verifies the cross-service
LLM integration through the NVIDIA NIM Gateway. Uses only the Python standard
library so it runs in CI without extra dependencies.

Configuration (all optional, sensible defaults for the docker-compose stack):
  GATEWAY_PORT            (default 8100)
  FINANCIAL_PORT           (default 8101)
  KNOWLEDGE_PORT           (default 8102)
  AGENT_PORT               (default 8103)
  PROMPT_PORT              (default 8104)
  OBSERVABILITY_PORT       (default 8105)
  SMOKE_TIMEOUT            per-request timeout seconds (default 10)
  SMOKE_RETRIES            health-check retry count (default 30)
  SMOKE_RETRY_DELAY        seconds between health retries (default 2)

Exit code is non-zero if any check fails, so it can gate CI / deploys.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

# ── Config ──────────────────────────────────────────────────────────────
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "8100"))
FINANCIAL_PORT = int(os.getenv("FINANCIAL_PORT", "8101"))
KNOWLEDGE_PORT = int(os.getenv("KNOWLEDGE_PORT", "8102"))
AGENT_PORT = int(os.getenv("AGENT_PORT", "8103"))
PROMPT_PORT = int(os.getenv("PROMPT_PORT", "8104"))
OBSERVABILITY_PORT = int(os.getenv("OBSERVABILITY_PORT", "8105"))

TIMEOUT = int(os.getenv("SMOKE_TIMEOUT", "10"))
RETRIES = int(os.getenv("SMOKE_RETRIES", "30"))
RETRY_DELAY = float(os.getenv("SMOKE_RETRY_DELAY", "2"))

SERVICES = {
    "nvidia-nim-gateway": GATEWAY_PORT,
    "financial-ai-copilot": FINANCIAL_PORT,
    "enterprise-knowledge-assistant": KNOWLEDGE_PORT,
    "enterprise-agent-platform": AGENT_PORT,
    "prompt-evaluation-platform": PROMPT_PORT,
    "ai-observability-platform": OBSERVABILITY_PORT,
}


@dataclass
class Result:
    name: str
    ok: bool
    detail: str


def _get(url: str, data: bytes | None = None, headers: dict | None = None,
         method: str = "GET") -> tuple[int, str]:
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:  # type: ignore[attr-defined]
        body = exc.read().decode("utf-8", "replace") if exc.fp else ""
        return exc.code, body
    except Exception as exc:  # noqa: BLE001 - surface as connection failure
        return 0, f"{type(exc).__name__}: {exc}"


def _post_json(port: int, path: str, payload: dict, query: str = "") -> tuple[int, str]:
    url = f"http://localhost:{port}{path}{query}"
    data = json.dumps(payload).encode() if payload else None
    return _get(url, data=data, headers={"Content-Type": "application/json"}, method="POST")


# ── Individual checks ─────────────────────────────────────────────────────
def check_health(name: str, port: int) -> Result:
    for _ in range(RETRIES):
        code, _ = _get(f"http://localhost:{port}/health")
        if code == 200:
            return Result(name, True, "health OK")
        time.sleep(RETRY_DELAY)
    return Result(name, False, f"/health returned {code}")


def check_gateway_mock() -> Result:
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": "ping"}],
        "stream": False,
    }
    code, body = _post_json(GATEWAY_PORT, "/v1/chat/completions", payload)
    ok = code == 200 and "[MOCK]" in body
    return Result("gateway → mock completion", ok, f"HTTP {code}" + ("" if ok else f" | {body[:120]}"))


def check_financial_stream() -> Result:
    payload = {"messages": [{"role": "user", "content": "ping"}]}
    code, body = _post_json(FINANCIAL_PORT, "/api/v1/chat/stream", payload)
    ok = code == 200 and "[MOCK]" in body
    return Result("financial → gateway (stream)", ok, f"HTTP {code}" + ("" if ok else f" | {body[:120]}"))


def check_agent_orchestration() -> Result:
    # Create an agent (query-param endpoint, no JSON body), then run
    # orchestrator chat through the gateway.
    code, _ = _post_json(
        AGENT_PORT, "/api/v1/orchestrator/agents", {},
        query="?name=smoke&agent_type=react&system_prompt=test&tools=",
    )
    agent_ok = code in (200, 400)  # 400 = agent already exists from a prior run
    if not agent_ok:
        return Result("agent-platform → orchestrator → gateway", False, f"create agent HTTP {code}")
    code, body = _post_json(
        AGENT_PORT, "/api/v1/orchestrator/chat", {},
        query="?agent_id=smoke&session_id=smoke-e2e&message=Plan%20a%20task",
    )
    ok = code == 200 and "success" in body and "llm_calls" in body
    return Result("agent-platform → orchestrator → gateway", ok, f"HTTP {code}" + ("" if ok else f" | {body[:120]}"))


def check_observability() -> Result:
    code, body = _get(f"http://localhost:{OBSERVABILITY_PORT}/health")
    ok = code == 200
    return Result("observability-platform health", ok, f"HTTP {code}" + ("" if ok else f" | {body[:120]}"))


# ── Runner ────────────────────────────────────────────────────────────────
def main() -> int:
    print("═" * 64)
    print("Enterprise AI Platform — E2E Smoke Test")
    print("═" * 64)

    results: list[Result] = []

    # 1) Health for all 6 services
    for name, port in SERVICES.items():
        results.append(check_health(name, port))

    # 2) Cross-service LLM integration through the gateway
    results.append(check_gateway_mock())
    results.append(check_financial_stream())
    results.append(check_agent_orchestration())
    results.append(check_observability())

    # Report
    print()
    width = max(len(r.name) for r in results)
    failed = 0
    for r in results:
        status = "✅ PASS" if r.ok else "❌ FAIL"
        if not r.ok:
            failed += 1
        print(f"  {status}  {r.name:<{width}}  {r.detail}")
    print()
    print(f"  {len(results) - failed}/{len(results)} checks passed")
    print("═" * 64)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
