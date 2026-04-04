# Google ADK — DataRobot OTel Integration

## Critical: ADK Overwrites the Global TracerProvider

Google ADK's web server calls `_setup_telemetry()` at startup, which **replaces any TracerProvider set earlier**. This means the standard `configure_otel()` trace setup will be overwritten. Logs and metrics are NOT affected.

| Signal    | ADK Overrides? | Strategy                                                        |
|-----------|----------------|-----------------------------------------------------------------|
| **Traces**  | YES            | Lazy injection — add span processor to ADK's provider on first request |
| **Metrics** | No*            | Standard setup at import time with direct exporter config       |
| **Logs**    | No             | Standard setup at import time                                   |

*ADK will override MeterProvider if `OTEL_EXPORTER_OTLP_*` env vars are set. Never set these.

## Modified `dr_otel_config.py` for ADK

For ADK, the generated `dr_otel_config.py` must be modified from the generic pattern:

1. **Do NOT configure traces in `configure_otel()`** — traces will be lost when ADK replaces the TracerProvider
2. **Build `dr_span_processor` at module level** — this is injected lazily later
3. **Export `dr_span_processor`** so the metrics callback module can access it
4. **Call `configure_otel()` at module level** (import time), not deferred

```python
# In dr_otel_config.py — ADK variant
# ... (same imports as generic, plus:)

def configure_otel():
    """Configure logs and metrics only. Traces use lazy injection."""
    headers = _build_dr_headers()
    endpoint = _get_endpoint()
    if not endpoint:
        return
    resource = Resource.create()

    # Logs — ADK does NOT override LoggerProvider
    # (same as generic pattern)

    # Metrics — direct exporter config (no env vars!)
    # (same as generic pattern)

    # NOTE: Traces are NOT configured here. See dr_span_processor below.


# Build trace processor at import time — injected lazily on first request
dr_span_processor = SimpleSpanProcessor(
    OTLPSpanExporter(
        endpoint=f"{_get_endpoint()}/v1/traces",
        headers=_build_dr_headers(),
    )
)

configure_otel()
```

## Custom Metrics Callback Module

Generate `dr_agent_metrics.py` with callbacks for ADK agent lifecycle events.

```python
"""DataRobot metrics instrumentation for ADK agent.

Callbacks for LlmAgent lifecycle events that record OTel metrics
and handle lazy trace injection into ADK's TracerProvider.
"""

import logging
import threading
import time

from opentelemetry import metrics, trace

_meter = metrics.get_meter("agent-name")  # Replace with actual agent name

request_counter = _meter.create_counter(
    "agent.requests", unit="1",
    description="Total requests processed by the agent",
)
request_duration = _meter.create_histogram(
    "agent.request.duration_ms", unit="ms",
    description="End-to-end agent request duration",
)
llm_call_counter = _meter.create_counter(
    "agent.llm.calls", unit="1",
    description="Number of LLM API calls made",
)
llm_duration = _meter.create_histogram(
    "agent.llm.duration_ms", unit="ms",
    description="Individual LLM call duration",
)
tool_call_counter = _meter.create_counter(
    "agent.tool.calls", unit="1",
    description="Number of tool invocations",
)

_t = threading.local()
_trace_injected = False


def _ensure_trace_export():
    """Inject DataRobot span processor into ADK's TracerProvider on first call.

    ADK overwrites the global TracerProvider at server startup. We piggyback
    on ADK's provider by adding our span processor on the first request,
    when ADK's provider is guaranteed to be active.
    """
    global _trace_injected
    if _trace_injected:
        return
    _trace_injected = True
    try:
        from dr_otel_config import dr_span_processor

        provider = trace.get_tracer_provider()
        # ADK may wrap the real provider in a proxy
        real_provider = getattr(provider, "_real_tracer_provider", provider)
        if hasattr(real_provider, "add_span_processor"):
            real_provider.add_span_processor(dr_span_processor)
            logging.info("Injected DataRobot span processor into ADK's TracerProvider")
        else:
            logging.warning("TracerProvider does not support add_span_processor")
    except Exception as e:
        logging.error(f"Failed to inject DataRobot span processor: {e}")


async def before_agent(callback_context):
    """Called before agent processes a request. Injects trace export on first call."""
    _ensure_trace_export()
    _t.agent_start = time.time()
    return None


async def after_agent(callback_context):
    """Called after agent completes. NOTE: only 1 argument, not 2."""
    elapsed_ms = (time.time() - getattr(_t, "agent_start", time.time())) * 1000
    request_counter.add(1, {"status": "success"})
    request_duration.record(elapsed_ms)
    return None


async def before_model(callback_context, llm_request):
    """Called before each LLM API call."""
    _t.llm_start = time.time()
    return None


async def after_model(callback_context, llm_response):
    """Called after each LLM API call."""
    elapsed_ms = (time.time() - getattr(_t, "llm_start", time.time())) * 1000
    model = getattr(llm_response, "model", "unknown") or "unknown"
    llm_call_counter.add(1, {"model": model})
    llm_duration.record(elapsed_ms, {"model": model})
    return None


async def after_tool(tool, args, tool_context, tool_response):
    """Called after each tool invocation."""
    tool_call_counter.add(1, {"tool": tool.name})
    return None
```

## Wiring Callbacks to ADK Agents

In the user's agent definition file, wire the callbacks:

```python
from dr_otel_config import configure_otel  # noqa: F401 (called at import time)
import dr_agent_metrics

root_agent = LlmAgent(
    name="my_agent",
    model="gemini-2.5-flash",
    # ... other config ...
    before_agent_callback=dr_agent_metrics.before_agent,
    after_agent_callback=dr_agent_metrics.after_agent,
    before_model_callback=dr_agent_metrics.before_model,
    after_model_callback=dr_agent_metrics.after_model,
    after_tool_callback=dr_agent_metrics.after_tool,
)
```

**Important**: Import `dr_otel_config` before `dr_agent_metrics` to ensure logs and metrics providers are set before metrics instruments are created.

## Extra Dependencies

Add to the project's dependency file:
```
opentelemetry-resourcedetector-gcp
```

Note: The package name is `opentelemetry-resourcedetector-gcp` (no hyphen between "resource" and "detector"). Getting this wrong causes build failures.

## Known Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Traces not appearing | ADK replaced TracerProvider | Verify `_ensure_trace_export()` fires (check logs for "Injected DataRobot span processor") |
| `after_agent() missing 1 required positional argument` | Wrong callback signature | `after_agent(callback_context)` takes 1 arg, not 2 |
| Callbacks not called | Not `async` | All ADK callbacks must be `async def` (ADK v1.18+) |
| Metrics missing | `OTEL_EXPORTER_OTLP_*` env vars set | Remove all `OTEL_EXPORTER_OTLP_*` env vars |
| Build fails on `opentelemetry-resource-detector-gcp` | Wrong package name | Correct: `opentelemetry-resourcedetector-gcp` |
| ADK creates duplicate spans | ADK detects OTEL env vars | Never set `OTEL_EXPORTER_OTLP_ENDPOINT` or similar env vars |
