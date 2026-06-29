#!/usr/bin/env bash
# Verify an agent-framework workload's HTTP contract end-to-end.
#
# Usage:   verify_workload_endpoints.sh <base_url> [prompt]
# Example: verify_workload_endpoints.sh http://localhost:8077 "In one sentence, what is DataRobot?"
#
# Checks, in order: /health, /v1/chat/completions (non-stream), /v1/chat/completions (stream),
# /ag-ui (stream). Endpoints that 404 are reported as "not present" (skipped), not failed —
# a component may expose only one of the two agent protocols. The bar for success is a real
# model answer, not just a 200 on /health.
set -uo pipefail

BASE_URL="${1:?usage: verify_workload_endpoints.sh <base_url> [prompt]}"
BASE_URL="${BASE_URL%/}"
PROMPT="${2:-In one short sentence, what is DataRobot?}"
fail=0

say() { printf '\n=== %s ===\n' "$1"; }

# Reconstruct streamed text from either OpenAI SSE chunks or AG-UI events.
collect_stream() {
  python3 -c '
import sys, json
out = ""
for line in sys.stdin:
    line = line.strip()
    if not line.startswith("data:"):
        continue
    payload = line[5:].strip()
    if payload == "[DONE]":
        continue
    try:
        e = json.loads(payload)
    except ValueError:
        continue
    if e.get("object") == "chat.completion.chunk":
        out += (e.get("choices", [{}])[0].get("delta", {}).get("content") or "")
    elif e.get("type") == "TEXT_MESSAGE_CONTENT":
        out += e.get("delta", "")
print(out.strip())'
}

say "GET /health"
if curl -sf "${BASE_URL}/health" -o /tmp/_vw_health 2>/dev/null; then
  cat /tmp/_vw_health; echo
else
  echo "FAIL: /health did not return 200"; fail=1
fi

say "POST /v1/chat/completions (non-streaming)"
code=$(curl -sS -o /tmp/_vw_cc -w '%{http_code}' "${BASE_URL}/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"messages":[{"role":"user","content":sys.argv[1]}]}))' "$PROMPT")")
if [ "$code" = "404" ]; then
  echo "not present (404) — skipping"
elif [ "$code" = "200" ]; then
  ans=$(python3 -c 'import json;print(json.load(open("/tmp/_vw_cc"))["choices"][0]["message"]["content"])' 2>/dev/null)
  if [ -n "$ans" ]; then echo "answer: $ans"; else echo "FAIL: 200 but no answer"; cat /tmp/_vw_cc; fail=1; fi
else
  echo "FAIL: HTTP $code"; cat /tmp/_vw_cc; fail=1
fi

say "POST /v1/chat/completions (streaming)"
code=$(curl -sS -o /tmp/_vw_ccs -w '%{http_code}' -N "${BASE_URL}/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"stream":True,"messages":[{"role":"user","content":sys.argv[1]}]}))' "$PROMPT")")
if [ "$code" = "404" ]; then echo "not present (404) — skipping"
elif [ "$code" = "200" ]; then
  ans=$(collect_stream < /tmp/_vw_ccs)
  if [ -n "$ans" ]; then echo "streamed answer: $ans"; else echo "FAIL: empty stream"; fail=1; fi
else echo "FAIL: HTTP $code"; fail=1; fi

say "POST /ag-ui (streaming)"
code=$(curl -sS -o /tmp/_vw_agui -w '%{http_code}' -N "${BASE_URL}/ag-ui" \
  -H 'Content-Type: application/json' -H 'Accept: text/event-stream' \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"messages":[{"role":"user","content":sys.argv[1]}]}))' "$PROMPT")")
if [ "$code" = "404" ]; then echo "not present (404) — skipping"
elif [ "$code" = "200" ]; then
  ans=$(collect_stream < /tmp/_vw_agui)
  if [ -n "$ans" ]; then echo "ag-ui answer: $ans"; else echo "FAIL: no TEXT_MESSAGE_CONTENT events"; cat /tmp/_vw_agui | head; fail=1; fi
else echo "FAIL: HTTP $code"; fail=1; fi

rm -f /tmp/_vw_health /tmp/_vw_cc /tmp/_vw_ccs /tmp/_vw_agui
say "RESULT"
[ "$fail" = "0" ] && echo "OK — agent answered over HTTP" || echo "FAILURES above"
exit "$fail"
