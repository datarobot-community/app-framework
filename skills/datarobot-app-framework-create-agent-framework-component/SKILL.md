---
name: datarobot-app-framework-create-agent-framework-component
description: Create a DataRobot App Framework (af-component-*) component that hosts an agent — built in ANY language/framework — as a container on the DataRobot Workload API, exposing OpenAI-compatible chat completions and/or AG-UI over HTTP, wired to af-component-llm and instrumented with OpenTelemetry. Use when the user wants to package an agent framework (e.g. "host X framework on the Workload API", Microsoft Agent Framework, LangGraph, CrewAI, Spring AI, LangChain4j, Mastra, LangChain.js, langchaingo, eino, or any JVM/TypeScript/Go/Python agent) as a one-to-many AF component deployed via Pulumi.
---

# Create an Agent-Framework Workload Component

Scaffold an `af-component-*` Copier template that runs an agent — written in **any
language/framework** — as a container on the **DataRobot Workload API**, provisioned with
**Pulumi**, fed by **af-component-llm**, and traced to DataRobot via **OpenTelemetry**.

## Key insight: the DataRobot contract is language-agnostic

Only the agent's internal code changes per framework. Everything DataRobot cares about is
a fixed contract that any language satisfies:

1. **A linux/amd64 container** that listens on an HTTP port ≥ 1024.
2. **HTTP endpoints**: `GET /health` (probe) plus the agent surface — OpenAI-compatible
   `POST /v1/chat/completions` and/or AG-UI `POST /ag-ui` (SSE). These are wire protocols;
   implement them with whatever the framework provides, or by hand.
3. **A Python Pulumi layer** (`infra/infra/<name>.py`) creating a `datarobot.Artifact`
   (container spec) + `datarobot.Workload` (runtime). This is always Python regardless of the
   app language — it is the base component's IaC, not the app.
4. **LLM access** over an OpenAI-compatible URL from af-component-llm (gateway or deployment),
   authed with the DataRobot API token.
5. **OpenTelemetry → DataRobot** using that language's OTLP/HTTP exporter.

So: "do this for *framework X* on *language Y*" = write the agent in Y, build it into a
container exposing the endpoints in (2), and reuse (1,3,4,5) unchanged.

→ Exact schemas, URLs, headers, and gotchas: **[REFERENCE.md](REFERENCE.md)**.

## Prerequisites

- Read the component-authoring guide first: https://af.datarobot.com/guides/creating-a-component/
- Start from the official scaffold (a GitHub template repo with `copier.yml`,
  `copier-module.yaml`, a `template/` skeleton, `Taskfile` with `copy`/`validate`, and CI):
  **https://github.com/datarobot-community/scaffold-af-component**

Components are Copier templates layered onto a project; this one depends on `base` and `llm`.

## Workflow

1. **Scaffold**: clone/"Use this template" from
   [`scaffold-af-component`](https://github.com/datarobot-community/scaffold-af-component) (or
   copy an existing `af-component-*`). Rename the repo `af-component-<your-component>`.
   Set `copier-module.yaml`: `module`, `short_description`, `repeatable: true`, and
   `depends_on:` both `base` and `llm`.
2. **Questions** (`copier.yml`): **keep them minimal — every prompt is friction.** Ask only for
   what genuinely can't be defaulted, derived, or edited in code afterward. For this kind of
   component that's essentially two: the app name (+ a `..._file` derived snake_case var via
   `when: false`) and the container image URI, plus the `base`/`llm` answers-file paths for
   `_external_data: { base: ..., llm: ... }`. Everything else — port, instructions, model,
   importance, replicas, autoscaling, whether to build — is a **constant/`Tunables` block in the
   rendered code** (or env-driven), not a question. Build the image automatically; don't ask.
3. **App** (`template/<app_name>/`, any language): implement `/health` and the agent
   endpoint(s). Read config from env (see REFERENCE for the injected vars). Containerize for
   **linux/amd64** with a `Dockerfile`; entrypoint binds `$PORT`.
4. **Infra** (`template/infra/infra/<name>_file.py.jinja`): a `pulumi_command` step that builds &
   pushes the image, then the `Artifact` (depends on the build) + `Workload`, injecting the API
   token as a `dr-credential` and the LLM/OTel env vars. See REFERENCE schema.
5. **Runtime params** (`.datarobot/cli/<app_name>.yaml`) + **answers**
   (`.datarobot/answers/{{_copier_conf.answers_file}}.jinja`) + **docs** (`docs/<app_name>.md.jinja`).
6. **Local dev**: a `Taskfile` with `dev` (binds `$PORT`/`$AGENT_PORT`, default the chosen port)
   and `dev-docker` (docker-compose); `.env` populated by `dr dotenv setup -y`.

Build the image **as part of `task deploy`** (Pulumi `command.local.Command` → `./build-image.sh`),
not as a manual prereq — gate it behind a copier bool so CI can opt out. See REFERENCE §1.

## Non-negotiable gotchas (cause silent failure)

- **linux/amd64** image, or the workload crash-loops with `exec format error` (Apple Silicon
  defaults to arm64). Build with `docker buildx build --platform linux/amd64`.
- **Port ≥ 1024** and the container must actually listen on it; `/health` must answer there.
- **Memory in bytes** in the Pulumi runtime (not `Mi`/`Gi`).
- **Inject secrets by reference** (`source: "dr-credential"`), never as plaintext env.
- **OTel metrics need DELTA temporality** and the two `X-DataRobot-*` headers, or nothing lands.
- **LLM base URL**: the gateway path is appended differently per client — see REFERENCE
  (a Python `litellm datarobot/` provider appends it itself; a plain OpenAI client does not).
- **Pulumi Artifact/Workload** (all deploy-blocking; details + exact errors in REFERENCE §3):
  Workload uses `artifact.artifact_id` not `.id`; never set the runtime container-group `name`
  (read-only); omit empty-string env vars; and the Artifact's `environmentVars` must be **fully
  known at plan time** — resolve the credential id and Use-Case entity id to concrete strings via
  the DataRobot REST API (eager, idempotent) rather than passing unknown Pulumi Outputs, so a
  single `pulumi up` (`task deploy`) works. The image must be **publicly pullable** by DataRobot.

## Verify (always, before declaring done)

Render `base → llm → your component` into a throwaway project, `dr dotenv setup -y`, build/run,
then fire real requests with `scripts/verify_workload_endpoints.sh <base_url>`. Confirm a real
answer comes back from `/v1/chat/completions` (and `/ag-ui` if present) — a 200 on `/health`
is not enough.
