# OpenTelemetry → DataRobot

Works from any language's OTLP/HTTP exporter.

- Endpoint base = `DATAROBOT_ENDPOINT` with `/api/v2` stripped, then `/otel`. Signals at
  `/otel/v1/traces`, `/otel/v1/logs`, `/otel/v1/metrics`.
- Headers on every exporter: `x-datarobot-entity-id: experiment_container-<use_case_id>` and
  `x-datarobot-api-key: <DATAROBOT_API_TOKEN>` (lowercase — matches the canonical
  `DataRobotAppFrameworkBaseSettings` header-assembly logic; HTTP headers are case-insensitive but
  match the canonical form anyway). The entity id is injected into the container by the platform
  itself once a Use Case is attached — infra never sets it. `DATAROBOT_API_TOKEN` is different: the
  Workload API does NOT auto-inject it, so infra must pass through its own deploy-time
  `DATAROBOT_API_TOKEN` as a plain `source="string"` env var (see `pulumi.md` gotcha 4) — the app
  still just reads the resulting env var.
- **The entity id env var is `OTEL_ENTITY_ID`, not `DATAROBOT_ENTITY_ID`** — that's what
  af-component-base's infra exports (`pulumi.export("OTEL_ENTITY_ID", ...)`) and what
  `DataRobotAppFrameworkBaseSettings` reads. It's only present once a Use Case is attached to the
  stack, so it can legitimately be empty: treat that as "skip export for now" (log and return), not
  an error.
- **Read `DATAROBOT_ENDPOINT`/`OTEL_ENTITY_ID` with an env-first, `pulumi_config.json`-fallback
  lookup**, not env-only. `DataRobotAppFrameworkBaseSettings` (Python) checks real env vars first,
  then a `pulumi_config.json` file (Pulumi stack outputs, e.g. from a notebook/local run that never
  went through real container env injection) searched upward from the working directory the same way
  `.env` resolution works. Port the same two-source lookup in other languages — plain env-only misses
  the local/notebook case.
- **Metrics: DELTA aggregation temporality** (DataRobot requires it). Prefer simple/synchronous
  (non-batched) span *and log* export on short-lived request/response processes — a batched processor
  can mean nothing is exported before the process is killed/restarted, which looks exactly like
  "instrumentation isn't wired up" even though it technically is. Emit GenAI semantic-convention
  attributes (`gen_ai.prompt`, `gen_ai.completion`, `gen_ai.request.model`, `tool_name`, ...).
- Pass `endpoint`/`headers` directly to the exporters; avoid `OTEL_EXPORTER_OTLP_*` env vars, which
  some frameworks detect and use to spin up conflicting providers.

## Don't assume tracing is "on" just because a span/trace exporter is configured

Two near-misses that both look like "OTel isn't wired up" from the outside, but aren't fixed by more
exporter config:

- **Prompt/response content is elided by default in several GenAI SDKs.** e.g. adk-go (and others
  following the OTel GenAI semantic conventions) only emit real message content in logs when
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` is set — otherwise every log body is the
  literal string `<elided>`. Set this env var (in-process, e.g. `os.Setenv`/`process.env` at startup,
  gated behind your own privacy toggle) alongside setting up the exporters, or spans/logs will exist
  but look empty.
- **Traces need a *logs* pipeline too, not just a tracer.** A GenAI SDK's own instrumentation
  frequently emits BOTH spans (`generate_content`, `execute_tool`, ...) AND log records (`gen_ai.*.message`
  events carrying the actual prompt/completion text) — the interesting content is often in the log
  records, not the span attributes. Wire an OTLP log exporter + LoggerProvider (DELTA-equivalent:
  simple/synchronous processor) in addition to the TracerProvider, or you'll see spans with no visible
  content and conclude tracing "isn't really working."

## Libraries that grab their tracer/logger before you call Setup

Some GenAI SDKs (adk-go included) obtain their tracer/logger from the OTel *global* provider in a
package-level variable, initialized once at program startup — necessarily *before* your own
`main()`/`Setup()` function ever runs and installs the real provider. This is safe, not a bug to code
around: the OTel API's global registration (`otel.SetTracerProvider`/`global.SetLoggerProvider` in Go,
equivalents elsewhere) is specifically a delegating proxy — anything obtained from the global provider
before the real one is installed still forwards to it once installed. Verified directly (not assumed)
against the OTel Go SDK: a tracer/logger captured before `SetTracerProvider`/`SetLoggerProvider` still
delivers spans/records to the exporter installed afterward. So calling your OTel setup from `main()`,
after the SDK's own package-level captures already ran, still works correctly — don't restructure the
app to call setup earlier "just in case," and don't assume a library's tracing is dead just because it
grabbed its tracer before you configured anything.
