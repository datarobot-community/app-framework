# fastapi-backend

**Repository:** [github.com/datarobot-community/af-component-fastapi-backend](https://github.com/datarobot-community/af-component-fastapi-backend)

Adds a FastAPI server to your recipe, deployed as a DataRobot Custom Application. This is the standard API layer for App Framework templates — it pairs with the [react](react.md) component for full-stack apps, or stands alone for pure API or server-side-rendered use cases.

The component is repeatable: apply it multiple times with different `fastapi_app` names to include multiple independent FastAPI backends in a single recipe.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed
- A DataRobot account with permissions to create Custom Applications
- The [base](base.md) component already applied

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-fastapi-backend .
```

Or with copier directly:

```bash
uvx copier copy datarobot-community/af-component-fastapi-backend .
```

The wizard asks for a `fastapi_app` name. Use a short, lowercase identifier (e.g., `api` or `web`). This name namespaces all generated files and the answers file.

## Component dependencies

| Component | Required |
|-----------|----------|
| [base](base.md) | Yes |

## Local development

Start the server:

```bash
dr run dev
```

Or directly with uvicorn:

```bash
uv run uvicorn FASTAPI_APP.app:app --reload --port 8080
```

The server is available at `http://localhost:8080`. FastAPI autodocs are at `/docs` and `/redoc`.

**Key paths:**

| Path | Purpose |
|------|---------|
| `FASTAPI_APP/app/__init__.py` | FastAPI application and routes. |
| `FASTAPI_APP/templates/index.html` | Jinja template served by the catch-all route. |
| `FASTAPI_APP/app/static/` | Static assets served at `/static/`. |
| `infra/infra/FASTAPI_APP.py` | Pulumi Custom Application resources. |

## Update

```bash
uvx copier update -a .datarobot/answers/fastapi-FASTAPI_APP.yml -A
```

## Adding multiple backends

Because this component is repeatable, run the apply command again with a different `fastapi_app` name:

```bash
uvx copier copy datarobot-community/af-component-fastapi-backend .
# Enter a different `fastapi_app` name when prompted.
```

## Troubleshooting

### Application fails to start on DataRobot

Check Custom Application logs in the DataRobot UI. The most common cause is a missing environment variable — confirm all required runtime parameters are set in the deployment configuration.

### `uv run` reports a missing package

Run `uv sync` to install dependencies declared in `pyproject.toml`.

### Port conflict on local dev

Change the `--port` flag in the `uvicorn` command, or stop any other process already bound to port `8080`.
