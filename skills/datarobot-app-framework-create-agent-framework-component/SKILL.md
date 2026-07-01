---
name: datarobot-app-framework-create-agent-framework-component
description: Create a DataRobot App Framework (af-component-*) component that hosts an agent — built in ANY language/framework — as a container on the DataRobot Workload API, exposing OpenAI-compatible chat completions and/or AG-UI over HTTP, wired to af-component-llm and instrumented with OpenTelemetry. Use when the user wants to package an agent framework (e.g. "host X framework on the Workload API", Microsoft Agent Framework, LangGraph, CrewAI, Spring AI, LangChain4j, Mastra, LangChain.js, langchaingo, eino, or any JVM/TypeScript/Go/Python agent) as a one-to-many AF component deployed via Pulumi.
---

# Create an Agent-Framework Workload Component

Scaffold an `af-component-*` Copier template that runs an agent (any language/framework) as a container
on the **DataRobot Workload API**, provisioned with **Pulumi**, fed by **af-component-llm**, traced via
**OpenTelemetry**. Start from the scaffold (read the [guide](https://af.datarobot.com/guides/creating-a-component/)):
https://github.com/datarobot-community/scaffold-af-component — depends on `base` + `llm`.

## Key insight: the DataRobot contract is language-agnostic

Only the agent's internal code changes per framework; the rest is a fixed contract any language meets:

1. a **linux/amd64 container** listening on HTTP port ≥ 1024;
2. **HTTP endpoints** — `GET /health` + OpenAI `POST /v1/chat/completions` and/or AG-UI `POST /ag-ui` (SSE);
3. a **Python Pulumi layer** — `datarobot.Artifact` (container spec) + `datarobot.Workload` (runtime);
4. **LLM access** via an OpenAI-compatible URL from af-component-llm;
5. **OpenTelemetry → DataRobot** via the language's OTLP/HTTP exporter.

"Do it for framework X on language Y" = write the agent in Y, expose (2), reuse 1/3/4/5 unchanged.

## References — load the one you need

| File | Read when |
|------|-----------|
| `references/workload-contract.md` | Building the app: container rules + HTTP wire protocols + serving a UI behind the URL prefix |
| `references/pulumi.md` | Writing `infra/`: build step, `Artifact`+`Workload` schema, deploy-blocking gotchas, endpoint-URL exports |
| `references/llm.md` | Wiring the model (import af-component-llm's module) + OpenAI/litellm base URLs |
| `references/observability.md` | OTel → DataRobot (endpoint, headers, DELTA metrics) |
| `references/copier.md` | `copier.yml`/`copier-module.yaml`, minimal questions, `_external_data`, answers naming, exec bit |
| `references/ci-and-verify.md` | `task validate`, the verify script, and the CI validator workflow |
| `scripts/verify_workload_endpoints.sh <base_url>` | Post-deploy check — fires real requests at the endpoints |

## Workflow

1. **Scaffold** from `scaffold-af-component`; set `copier-module.yaml` `repeatable: true`, `depends_on: base + llm`.
2. **Questions** (`copier.yml`): minimal — app name + image URI + `_external_data`; everything else is a `Tunables` constant, not a prompt. → `copier.md`
3. **App** (`template/<app_name>/`, any language): `/health` + agent endpoint(s), config from env, linux/amd64 `Dockerfile` binding `$PORT`. → `workload-contract.md`
4. **Infra** (`template/infra/infra/<name>_file.py.jinja`, Python): build+push image, then `Artifact`+`Workload`. → `pulumi.md`, `llm.md`, `observability.md`
5. **Runtime params / answers / docs** under `.datarobot/` and `docs/`. → `copier.md`
6. **Taskfile** (`dev`, `dev-docker`, `lint-check`, `test`); `.env` via `dr dotenv setup -y`.
7. **CI**: the validator must render AND install+run the app's `lint-check`/`test`. → `ci-and-verify.md`

## Non-negotiable gotchas (silent failure; detail in the references)

- **linux/amd64** image (else `exec format error`); **port ≥ 1024**; image must be **publicly pullable**.
- **Pulumi**: Workload uses `artifact.artifact_id` (not `.id`); don't set the runtime group `name` (read-only);
  memory in **bytes**; drop empty-string env vars; `environmentVars` must be **known at plan time** —
  resolve credential + entity ids to concrete strings via REST, never as Pulumi Outputs. → `pulumi.md`
- **Secrets** injected by reference (`source:"dr-credential"`), never plaintext.
- **OTel** metrics need **DELTA** temporality + the two `X-DataRobot-*` headers.
- **UI** uses relative URLs — the workload is served behind a URL prefix it can't know.

## Verify before declaring done

Render `base → llm → component`, `dr dotenv setup -y`, deploy, then run
`scripts/verify_workload_endpoints.sh <base_url>` — require a real model answer from
`/v1/chat/completions` (and `/ag-ui`), not just a `/health` 200.
