# OpenTelemetry → DataRobot

Works from any language's OTLP/HTTP exporter.

- Endpoint base = `DATAROBOT_ENDPOINT` with `/api/v2` stripped, then `/otel`. Signals at
  `/otel/v1/traces`, `/otel/v1/logs`, `/otel/v1/metrics`.
- Headers on every exporter: `X-DataRobot-Entity-Id: experiment_container-<use_case_id>` and
  `X-DataRobot-Api-Key: <DATAROBOT_API_TOKEN>`. The use-case id is `use_case.id` in infra (inject it
  as `DATAROBOT_ENTITY_ID = experiment_container-<id>`; see `pulumi.md` on resolving it to a concrete
  string at plan time).
- **Metrics: DELTA aggregation temporality** (DataRobot requires it). Prefer simple/synchronous span
  export on short-lived processes. Emit GenAI semantic-convention attributes (`gen_ai.prompt`,
  `gen_ai.completion`, `gen_ai.request.model`, `tool_name`, ...).
- Pass `endpoint`/`headers` directly to the exporters; avoid `OTEL_EXPORTER_OTLP_*` env vars, which
  some frameworks detect and use to spin up conflicting providers.
