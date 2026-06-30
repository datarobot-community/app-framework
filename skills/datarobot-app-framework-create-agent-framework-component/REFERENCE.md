# Reference: exact contracts

Everything below is language-independent unless noted. The app can be Go/JVM/TS/Python/etc.;
the Pulumi infra is always Python (it is the `base` component's IaC).

## 1. Container contract (DataRobot Workload API)

- Image MUST have a **linux/amd64** manifest. Build: `docker buildx build --platform linux/amd64 -t <ref> --push .`
- Listen on an HTTP port **≥ 1024** (the Workload injects `PORT`; bind it).
- `GET /health` returns 200 quickly — used by readiness/liveness probes.
- Image must live in a registry DataRobot can pull (public, or one the org pre-configured).
  The Workload API does not yet take image-pull credentials at create time.

**Build & push the image as part of `task deploy` (always — not a question).** Don't make users
push manually, and don't gate it behind a copier prompt. Base's infra already depends on
`pulumi-command`, so add a `pulumi_command.local.Command` that runs the build, and have the Artifact
`depends_on` it (so the image exists before the Workload starts):
```python
import pulumi, pulumi_command as command
build = command.local.Command(f"{NAME} Build Image",
    create="./build-image.sh",
    dir=str(app_dir), environment={"IMAGE_URI": IMAGE_URI},
    triggers=[source_hash(app_dir), IMAGE_URI])   # rebuild only when source/uri changes
artifact = datarobot.Artifact(..., opts=pulumi.ResourceOptions(depends_on=[build]))
```
Requires local Docker logged in to the registry. (`pulumi_docker.Image` also works but adds a dep to
base's infra `pyproject.toml`, which a component can't edit — `pulumi-command` is already present.)
CI that pushes separately can delete this Command + the Artifact's `depends_on`.

- **Make the shell scripts executable in git.** `chmod +x` the source `*.sh`/`*.sh.jinja` and
  `git update-index --chmod=+x` them (commit mode `100755`); Copier preserves the bit on render, so
  `create="./build-image.sh"` and `CMD ["./start.sh"]` work.

## 2. HTTP endpoints (wire protocols — implement in any language)

**OpenAI Chat Completions** — `POST /v1/chat/completions`, body `{model, messages[], stream}`.
Non-stream → `{id, object:"chat.completion", choices:[{message:{role,content}, finish_reason}]}`.
Stream → SSE `data: {object:"chat.completion.chunk", choices:[{delta:{content}}]}` then `data: [DONE]`.
Many frameworks ship a server for this; otherwise it is ~40 lines around the agent's run/stream call.

**AG-UI** — `POST /ag-ui`, SSE out. Event `type`s: `RUN_STARTED`, `TEXT_MESSAGE_START`,
`TEXT_MESSAGE_CONTENT` (`delta`), `TEXT_MESSAGE_END`, `RUN_FINISHED` (also `MESSAGES_SNAPSHOT`,
`RUN_ERROR`). Field names camelCase (`threadId`, `runId`, `messageId`). Spec: https://docs.ag-ui.com/
Some frameworks provide a native AG-UI server; the TypeScript ecosystem (CopilotKit) has first-class support.

A single agent instance can back both endpoints.

**Serving an HTML UI / browser client: use RELATIVE URLs.** The workload is reached at a URL
*prefix* (`{endpoint}/endpoints/workloads/<id>/`) and the container never learns its own external
URL — and you can't inject it as a runtime parameter either, because Pulumi only knows the endpoint
*after* the workload is created (dependency cycle). So a page served at the app root that does
`fetch("/ag-ui")` hits the **domain** root, not the prefix, and breaks. Resolve API paths relative to
the current page (the app root), robust to a missing trailing slash:
```js
function appUrl(path) {                       // call as appUrl("ag-ui"), appUrl("v1/chat/completions")
  const here = new URL(window.location.href);
  if (!here.pathname.endsWith("/")) here.pathname += "/";
  return new URL(path, here).href;
}
```
Same rule for any asset/link: relative (`ag-ui`, `assets/x.js`), never absolute (`/ag-ui`). Server-side
routing is unaffected — DataRobot strips the prefix, so the container still sees `/ag-ui` etc.

## 3. Pulumi: Artifact + Workload (Python `pulumi_datarobot`)

Two resources. `Artifact` = immutable *what runs*; `Workload` = *runtime* (replicas/resources).

```python
import pulumi_datarobot as datarobot

artifact = datarobot.Artifact(
    f"{NAME} Artifact",
    type="service",
    spec=datarobot.ArtifactSpecArgs(container_groups=[
        datarobot.ArtifactSpecContainerGroupArgs(containers=[
            datarobot.ArtifactSpecContainerGroupContainerArgs(
                name="main", image_uri=IMAGE_URI, primary=True, port=PORT,
                environment_vars=[
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_API_TOKEN", source="dr-credential",
                        dr_credential_id=token_cred.id, key="apiToken"),
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_ENDPOINT", source="string", value=endpoint),
                    # ...more source="string" vars; OMIT any whose value == "" (see gotchas)...
                ],
                readiness_probe=datarobot.ArtifactSpecContainerGroupContainerReadinessProbeArgs(
                    path="/health", port=PORT, initial_delay_seconds=10, period_seconds=10),
                liveness_probe=datarobot.ArtifactSpecContainerGroupContainerLivenessProbeArgs(
                    path="/health", port=PORT, initial_delay_seconds=30, period_seconds=30),
            )])]))

workload = datarobot.Workload(
    f"{NAME} Workload",
    artifact_id=artifact.artifact_id,           # ← .artifact_id (DataRobot id), NOT .id (Pulumi UUID)
    importance="low",                           # low|moderate|high|critical
    runtime=datarobot.WorkloadRuntimeArgs(container_groups=[
        datarobot.WorkloadRuntimeContainerGroupArgs(
            # NO name= here — runtime container-group name is read-only (server sets "default")
            replica_count=1,                    # OR autoscaling=... (mutually exclusive)
            containers=[datarobot.WorkloadRuntimeContainerGroupContainerArgs(
                name="main",                    # MUST match the artifact container name
                resource_allocation=datarobot.WorkloadRuntimeContainerGroupContainerResourceAllocationArgs(
                    cpu=1.0, memory=2 * 1024**3))])]))  # memory in BYTES, not Mi/Gi
```

Autoscaling instead of `replica_count`:
```python
autoscaling=datarobot.WorkloadRuntimeContainerGroupAutoscalingArgs(enabled=True, policies=[
    datarobot.WorkloadRuntimeContainerGroupAutoscalingPolicyArgs(
        scaling_metric="cpuAverageUtilization", target=70, min_count=2, max_count=8)])
```

- Token credential: `token_cred = datarobot.ApiTokenCredential(name, api_token=os.environ["DATAROBOT_API_TOKEN"])`.
- Inspect the live schema: clone `datarobot-community/pulumi-datarobot` and read
  `provider/cmd/pulumi-resource-datarobot/schema.json` (resources `Artifact`, `Workload`).
- GPU/VRAM: set `resource_bundles=["gpu.l4.small"]` on the runtime container group instead of cpu/memory.

### Artifact/Workload gotchas (each one fails the deploy — all verified against the live API)

1. **`artifact.artifact_id`, not `artifact.id`.** The Pulumi `.id` is an internal UUID; the
   Workload API rejects it as `422 … artifactId … invalid ID`. Use the `.artifact_id` output.
2. **Never set the runtime container-group `name`.** It is read-only (server-assigns `default`);
   setting it → `Invalid Configuration for Read-Only Attribute … runtime.containerGroups[0].name`.
   (The container *inside* it still needs `name=` matching the artifact's container.)
3. **Drop empty-string env vars.** A `source="string"` var with `value=""` → `422 … Field required`.
   Build the string vars in a dict and emit only non-empty ones; let app defaults cover the rest.
4. **`environmentVars` must be fully KNOWN at plan time — resolve ids eagerly, don't pass
   Outputs.** The Artifact provider validates each env var during `preview` and tolerates
   neither unknown *leaf* values (a freshly-created credential's `.id`, a use-case-derived
   entity id → `Missing dr_credential_id` / `Missing value`) nor a wholly-unknown list wrapped
   in `Output.all(...).apply(...)` (→ `Value Conversion Error`). So a normal single-pass
   `pulumi up` fails. **Fix: resolve the values to concrete strings via the DataRobot REST API
   at plan time** (the token + endpoint are already known env vars), instead of creating Pulumi
   resources with unknown ids:
   ```python
   import datarobot as dr
   client = dr.Client(token=token, endpoint=endpoint)
   # idempotent upsert → concrete credential id (no plaintext token in Pulumi state)
   creds = client.get("credentials/").json().get("data", [])
   cred_id = next((c["credentialId"] for c in creds
                   if c["name"] == NAME and c["credentialType"] == "api_token"), None) \
             or client.post("credentials/", data={"name": NAME, "credentialType": "api_token",
                                                   "apiToken": token}).json()["credentialId"]
   # entity id: prefer DATAROBOT_DEFAULT_USE_CASE; else look up the project Use Case by name; else ""
   ```
   Then `dr_credential_id=cred_id` and `DATAROBOT_ENTITY_ID=f"experiment_container-{uc_id}"`
   are plain strings → single-pass `pulumi up` (i.e. `task deploy`) works. Trade-offs: the
   eager credential lives outside Pulumi's graph (name it per-stack, idempotent; `pulumi destroy`
   won't remove it), and on a first deploy the Use Case may not exist yet so entity id is omitted
   (tracing attaches once it does, or immediately if `DATAROBOT_DEFAULT_USE_CASE` is set). Doing
   REST writes during `preview` is the deliberate cost of keeping deploys single-pass.
- Creating an Artifact auto-locks it (`status=locked`, `version=1`); a `pulumi destroy` fails with
  `409 … still used by workloads` if a workload (even a failed one) references it — delete the
  workload first (`DELETE /workloads/{id}/`).
- **Image must be pullable by DataRobot.** A private `ghcr.io`/registry image (anonymous
  `GET …/manifests/<tag>` → `401`) leaves the workload `errored` with the container `waiting`,
  `restarts=0`, and no app logs — that's an image-pull failure, not a code bug. Make the image
  public (or use a registry the org pre-configured); the Workload API takes no pull creds at create.
- **Export the actionable serving URL, not just the id.** The Workload's authenticated endpoint is
  `{DATAROBOT_ENDPOINT}/endpoints/workloads/{workload_id}/` (call it with `Authorization: Bearer
  <token>`). Export that base plus the concrete routes so `pulumi up` output is directly usable:
  ```python
  ep = workload.id.apply(lambda wid: f"{endpoint}/endpoints/workloads/{wid}/")
  export("…_ENDPOINT_URL", ep)
  export("…_CHAT_COMPLETIONS_URL", pulumi.Output.concat(ep, "v1/chat/completions"))
  export("…_AG_UI_URL", pulumi.Output.concat(ep, "ag-ui"))
  ```
  Keep the apply variable short (e.g. `ep` / `_endpoint_url`, not `<longname>_endpoint_url`) so the
  `Output.concat(...)` lines stay under the formatter's line length regardless of the agent name.

## 4. LLM access (from af-component-llm)

**Import the LLM config from the llm component's infra module — don't reconstruct it from
prefixed env vars.** Every af-component-llm configuration (gateway, deployed, blueprint, …)
renders an `infra/infra/<llm_app_name>.py` that exports the SAME two symbols: `default_model`
(the litellm model id) and `custom_model_runtime_parameters` (a list of runtime-param args with
`.key`/`.value`, including the deployment id and `USE_DATAROBOT_LLM_GATEWAY`). So a Python infra
just imports them — robust across all llm configs, no string-prefix guessing:

```python
from .{{ _external_data.llm.llm_app_name }} import custom_model_runtime_parameters as llm_custom_model_runtime_parameters
from .{{ _external_data.llm.llm_app_name }} import default_model

def _llm_component_config_value(key):           # read one runtime param by key
    for p in llm_custom_model_runtime_parameters:
        if isinstance(p.key, str) and p.key == key:
            return None if isinstance(p.value, str) and not p.value else p.value
    return None

llm_deployment_id = _llm_component_config_value(
    "{{ _external_data.llm.llm_app_name | upper }}_DEPLOYMENT_ID") or ""
```

Two separate `from .<name> import …` lines (don't pre-combine into one parenthesized import):
ruff's isort leaves them split because `combine-as-imports` is off by default, and `default_model`
is imported unaliased — matching the `af-component-agent` reference.

**This requires `_external_data.llm` in `copier.yml`** — without it `{{ _external_data.llm.llm_app_name }}`
renders empty and you get a broken `from . import …`:
```yaml
_external_data:
  base: "{{ base_answers_file }}"
  llm: "{{ llm_answers_file }}"
```
`{{ _external_data.llm.llm_app_name }}` resolves to the active llm module (base symlinks the chosen
config to `infra/infra/<name>.py`); importing it also orders llm resources before yours. The module
only exists once the llm dependency is rendered — fine in a real project (base+llm are required deps)
and under `task validate`; a standalone `copier copy` without deps renders the empty `from .` form.
(Re-injecting via prefixed `os.environ.get(f"{PREFIX}_DEPLOYMENT_ID")` is brittle — avoid it.)

OpenAI-compatible base URLs (api key = `DATAROBOT_API_TOKEN`):
- **Gateway**: `{DATAROBOT_ENDPOINT}/genai/llmgw` — client appends `/chat/completions`. Model = a
  gateway catalog id, e.g. `azure/gpt-4o-mini` (list: `GET {DATAROBOT_ENDPOINT}/genai/llmgw/catalog/`).
- **Deployment**: `{DATAROBOT_ENDPOINT}/deployments/{id}` — client appends `/chat/completions`;
  model name is ignored.

litellm note (Python only): the `datarobot/` provider appends the gateway path *itself*, so pass
`api_base={DATAROBOT_ENDPOINT}` (bare) and model `datarobot/<catalog-id>`. A plain OpenAI-style
client in any language must NOT use the `datarobot/` prefix and DOES point base_url at the
`/genai/llmgw` (or `/deployments/{id}`) URL above.

## 5. OpenTelemetry → DataRobot (any language's OTLP/HTTP exporter)

- Endpoint base = `DATAROBOT_ENDPOINT` with `/api/v2` stripped, then `/otel`. Signals at
  `/otel/v1/traces`, `/otel/v1/logs`, `/otel/v1/metrics`.
- Headers on every exporter: `X-DataRobot-Entity-Id: experiment_container-<use_case_id>` and
  `X-DataRobot-Api-Key: <DATAROBOT_API_TOKEN>`. The use-case id is `use_case.id` in infra
  (export it as `DATAROBOT_ENTITY_ID = experiment_container-<id>`).
- **Metrics: DELTA aggregation temporality** (DataRobot requires it). Prefer simple/synchronous
  span export on short-lived processes. Emit GenAI semantic-convention attributes
  (`gen_ai.prompt`, `gen_ai.completion`, `gen_ai.request.model`, `tool_name`, ...).
- Pass `endpoint`/`headers` directly to exporters; avoid `OTEL_EXPORTER_OTLP_*` env vars, which
  some frameworks detect and use to spin up conflicting providers.

## 6. Copier / component specifics

- `copier-module.yaml`: `module`, `short_description`, `repeatable: true`,
  `depends_on: {base: {url}, llm: {url}}`.
- `copier.yml`: questions; a hidden derived var `name_file: {default: "{{name|lower|replace('-','_')}}", when: false}`
  for python file naming; `_external_data: {base: "{{base_answers_file}}", llm: "{{llm_answers_file}}"}`;
  `_subdirectory: template`.
- `_answers_file` — because the component is **one-to-many** (`repeatable: true`), every instance
  must write a distinct answers file, so include both a fixed component prefix and the instance
  name: `_answers_file: ".datarobot/answers/<component>-{{name}}.yml"`. This matches the
  ecosystem convention (`llm-<name>.yml`, `fastapi-<name>.yml`); a bare `{{name}}.yml` would
  collide across instances and break `dr component update`. Other components reference yours via
  this exact path — e.g. an `llm_answers_file` answer defaulting to `.datarobot/answers/llm-llm.yml`.
- `template/` path templating: `{{ var }}` in file/dir names; `.jinja` suffix is stripped after
  render; use `.jinja.jinja` for files that must keep Jinja at runtime. Conventions:
  `infra/infra/` (Pulumi), `.datarobot/cli/<name>.yaml` (runtime params), `docs/<name>.md`.
- Read base answers via `{{ _external_data.base.template_name }}`, `{{ _external_data.base.copyright_year }}`.

## 7. Local dev + verification

- The [`scaffold-af-component`](https://github.com/datarobot-community/scaffold-af-component)
  repo ships `task copy` (quick render to `./tmp/template`) and `task validate` (full render with
  dependency resolution, same as CI) — run these first to confirm the template renders.
- `dr dotenv setup -y` populates the project `.env` (token, endpoint, LLM selection) non-interactively.
- `Taskfile` (in the generated app): `dev` runs the server binding `${AGENT_PORT:-<port>}`;
  `dev-docker` runs `docker compose up --build` (compose reads the project-root `.env`).
- Then render `base → llm → component` into a temp project, run it, and hit the endpoints with
  `scripts/verify_workload_endpoints.sh`. A real model answer — not just `/health` 200 — is the bar.
