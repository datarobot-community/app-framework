# Local dev, verification, and CI

## Render + local checks

- The [`scaffold-af-component`](https://github.com/datarobot-community/scaffold-af-component) repo
  ships `task copy` (quick render to `./tmp/template`) and `task validate` (full render WITH dependency
  resolution, same as CI) — run these first to confirm the template renders.
- `dr dotenv setup -y` populates the project `.env` (token, endpoint, LLM selection) non-interactively.
- Generated-app `Taskfile`: `dev` runs the server binding `${AGENT_PORT:-<port>}`; `dev-docker` runs
  `docker compose up --build` (compose reads the project-root `.env`).

## Verify a real deploy (the bar)

Render `base → llm → component` into a temp project, deploy, then hit the endpoints with
`scripts/verify_workload_endpoints.sh <base_url>`. A real model answer from `/v1/chat/completions`
(and `/ag-ui` if present) — not just a `/health` 200 — is the bar.

## CI: the validator workflow must exercise the app's tasks

The scaffold's default `.github/workflows/*framework-test.yaml` only *renders* the template — it does
NOT install deps or run the app's `lint`/`test`. **If the generated app ships a `Taskfile` with
`lint-check`/`test` (it should), the workflow must render, then install and run those tasks in the
rendered app dir** — otherwise broken app code passes CI. Distilled from
[`af-component-fastapi-backend`](https://github.com/datarobot-community/af-component-fastapi-backend/blob/main/.github/workflows/afcomponentfastapi-framework-test.yaml):

```yaml
jobs:
  test-framework:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/astral-sh/uv:python3.12-bookworm   # uv preinstalled
    steps:
      - uses: actions/checkout@v5
      - name: Render template
        uses: datarobot-oss/copier-template-validator@main   # renders base+deps → ./rendered
        with: { working-directory: ., rendered-dir: ./rendered }
      - { name: Install, shell: sh, working-directory: ./rendered/<app_name>,
          run: uvx --from go-task-bin task install, env: { UV_CACHE_DIR: /.uv_cache } }
      - { name: Lint,    shell: sh, working-directory: ./rendered/<app_name>,
          run: uvx --from go-task-bin task lint-check, env: { UV_CACHE_DIR: /.uv_cache } }
      - { name: Test,    shell: sh, working-directory: ./rendered/<app_name>,
          run: uvx --from go-task-bin task test, env: { UV_CACHE_DIR: /.uv_cache } }
```

- `<app_name>` is the rendered app folder = the copier name answer's **default** (CI renders with
  defaults). Add `--data <question>=<value>` under the validator step's `with: copier-args:` only for
  questions that have no default.
- The container ships `uv` but not `task`; run tasks via `uvx --from go-task-bin task <name>`.
- Set `UV_CACHE_DIR: /.uv_cache` (the container `$HOME` isn't writable) or the install step fails.
- App tests must not need network/DataRobot — stub the agent/LLM (see the app's `tests/conftest.py`).
