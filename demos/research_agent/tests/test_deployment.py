"""Smoke tests against the DEPLOYED research agent (langgraph dev on :2024).

These are deployment tests, not unit tests: they exercise the same HTTP
API that LangGraph Studio, the SDK, and the HTML console use. Run the
dev server first, then:

    cd demos/research_agent
    langgraph dev            # terminal 1
    python -m pytest tests/  # terminal 2  (or: python tests/test_deployment.py)

The full-run test costs a handful of LLM + Tavily calls (~cents).
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:2024"
GRAPH_ID = "research_agent"


def _post(path: str, payload: dict, timeout: int = 300):
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read())


def _get(path: str, timeout: int = 10):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=timeout) as resp:
        return resp.status, json.loads(resp.read())


def test_server_healthy():
    status, body = _get("/ok")
    assert status == 200
    assert body == {"ok": True}


def test_graph_is_registered():
    status, assistants = _post("/assistants/search", {})
    assert status == 200
    graph_ids = {a["graph_id"] for a in assistants}
    assert GRAPH_ID in graph_ids, f"expected '{GRAPH_ID}' in {graph_ids}"


def test_input_schema_exposes_research_topic():
    """The public input contract (ResearchInput) is served by the API."""
    status, assistants = _post("/assistants/search", {})
    assistant_id = next(a["assistant_id"] for a in assistants if a["graph_id"] == GRAPH_ID)
    status, schemas = _get(f"/assistants/{assistant_id}/schemas")
    assert status == 200
    props = schemas["input_schema"]["properties"]
    assert "research_topic" in props


def test_invalid_input_is_rejected():
    """Missing required `research_topic` must fail, not silently run."""
    try:
        status, body = _post(
            "/runs/wait",
            {"assistant_id": GRAPH_ID, "input": {"wrong_field": "x"}},
            timeout=60,
        )
    except urllib.error.HTTPError as e:
        assert e.code in (400, 422)
        return
    # Some server versions accept the run then surface a validation error.
    assert isinstance(body, dict) and "__error__" in json.dumps(body), (
        f"expected a validation error, got: {str(body)[:200]}"
    )


def test_full_run_produces_cited_report():
    """End-to-end: topic in → markdown report with sources out."""
    status, result = _post(
        "/runs/wait",
        {
            "assistant_id": GRAPH_ID,
            "input": {"research_topic": "What is the Model Context Protocol (MCP)?"},
        },
    )
    assert status == 200
    report = result.get("final_report")
    assert report, f"no final_report in result keys: {list(result)}"
    assert len(report) > 500, "report suspiciously short"
    assert "## Sources" in report, "report is missing its Sources section"
    assert "http" in report, "report contains no URLs"


if __name__ == "__main__":
    tests = [
        test_server_healthy,
        test_graph_is_registered,
        test_input_schema_exposes_research_topic,
        test_invalid_input_is_rejected,
        test_full_run_produces_cited_report,
    ]
    failed = 0
    for t in tests:
        name = t.__name__
        try:
            t()
            print(f"PASS  {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {name}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
