# react

**Repository:** [github.com/datarobot-community/af-component-react](https://github.com/datarobot-community/af-component-react)

Adds a React + Vite frontend to your recipe, wired to an existing FastAPI backend. The component ships a React scaffold, a Vite build pipeline, and the Pulumi infrastructure glue that embeds the compiled frontend into a DataRobot `ApplicationSource`.

Like [fastapi-backend](fastapi-backend.md), this component is repeatable — apply it multiple times with different `react_app` names to add multiple independent frontends to one recipe.

## Prerequisites

- Python 3.11+
- Node.js 18+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed
- The [base](base.md) component already applied
- The [fastapi-backend](fastapi-backend.md) component already applied

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-react .
```

Or with copier directly:

```bash
uvx copier copy datarobot-community/af-component-react .
```

The wizard asks for a `react_app` name (e.g. `frontend`). This namespaces all generated files and the answers file.

## Component dependencies

| Component | Required |
|-----------|----------|
| [base](base.md) | Yes |
| [fastapi-backend](fastapi-backend.md) | Yes |

## Wiring to the FastAPI backend

After applying both components, one manual step connects them in Pulumi. In `infra/infra/<fastapi_app>.py`, import the React frontend module and update the `ApplicationSource` to wait for the Vite build:

```python
from .<react_app_name> import <react_app_name>
```

```diff
 <fastapi_app>_app_source = pulumi_datarobot.ApplicationSource(
-    files=get_<fastapi_app>_app_files(runtime_parameter_values=<fastapi_app>_app_runtime_parameters),
+    files=frontend_web.stdout.apply(
+        lambda _: get_<fastapi_app>_app_files(
+            runtime_parameter_values=<fastapi_app>_app_runtime_parameters
+        )
+    ),
     runtime_parameter_values=<fastapi_app>_app_runtime_parameters,
     ...
 )
```

This ensures the Vite build completes before Pulumi collects the compiled assets.

## Local development

Start the Vite dev server from the generated frontend directory:

```bash
cd frontend_<react_app_name>
npm install
npm run dev
```

The dev server proxies API requests to the FastAPI backend on its configured port. See the generated `vite.config.ts` for proxy settings.

## Update

```bash
uvx copier update -a .datarobot/answers/react-<react_app>.yml -A
```

## Troubleshooting

**Frontend assets not included in the deployed app**

You likely skipped the `ApplicationSource` wiring step above. Confirm that `files=` uses `.stdout.apply(...)` rather than calling `get_*_app_files(...)` directly.

**`uvx copier copy` fails on Node version**

The Vite build requires Node.js 18+. Run `node --version` and upgrade if needed.

**Multiple frontends stomping on each other**

Each `react_app` name must be unique. Check `.datarobot/answers/` — each frontend should have its own `react-<name>.yml` file.

**Copier update overwrites local changes**

Customizations should be placed in files copier does not manage. Copier tracks generated files via the answers file and re-applies them on update.
