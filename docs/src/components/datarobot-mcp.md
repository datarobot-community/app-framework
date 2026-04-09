# datarobot-mcp

**Repository:** [github.com/datarobot-community/af-component-datarobot-mcp](https://github.com/datarobot-community/af-component-datarobot-mcp)

Adds a [FastMCP](https://github.com/jlowin/fastmcp) server to your recipe, deployed as a DataRobot Custom Application. The component ships a ready-to-deploy MCP server with a comprehensive set of DataRobot predictive tools (projects, models, deployments, predictions) and optional integrations for Google Drive, Jira, Confluence, and Microsoft Graph via DataRobot OAuth providers.

Like [fastapi-backend](fastapi-backend.md), this component is repeatable — apply it multiple times with different `mcp_app_name` values to run multiple independent MCP backends from a single recipe.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed
- The [base](base.md) component already applied

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-datarobot-mcp .
```

Or with copier directly:

```bash
uvx copier copy datarobot-community/af-component-datarobot-mcp .
```

The wizard asks for an `mcp_app_name` (e.g. `mcp`). This scopes all generated files and the answers file, allowing multiple instances in the same project.

## Component dependencies

| Component | Required |
|-----------|----------|
| [base](base.md) | Yes |

## What it adds

```
<mcp_app_name>/
├── <mcp_app_name>/   # MCP server source (tools, server entrypoint)
└── dev.md            # Local dev guide and OAuth setup
infra/infra/<mcp_app_name>.py   # Pulumi deployment resources
.datarobot/answers/drmcp-<mcp_app_name>.yml
```

## Available tools

### DataRobot predictive tools

| Category | Tools |
|----------|-------|
| Data management | Upload datasets to AI Catalog, list catalog items |
| Deployment info | Get deployment info, generate prediction templates, validate data |
| Deployment management | List deployments, get model info, deploy a model |
| Model management | Get best model, score datasets, list models |
| Predictions | Batch predictions (file or AI Catalog), real-time predictions, time series |
| Project management | List projects, get project datasets |
| Training & analysis | Analyze datasets, suggest use cases, start Autopilot, ROC curve, feature impact, lift chart |

### Integration tools (requires OAuth)

| Platform | Tools |
|----------|-------|
| Google Drive | Read files, manage access |
| Jira | Search, get, create, update, and transition issues |
| Confluence | Get, create, update pages; add comments; search |
| Microsoft Graph | Search SharePoint and OneDrive content |

Integration tools require OAuth providers configured in DataRobot. See the generated `dev.md` for setup instructions.

## Local development

Run the MCP server locally:

```bash
uv run python -m <mcp_app_name>
```

## Deploy

```bash
dr task deploy
```

## Update

```bash
uvx copier update -a .datarobot/answers/drmcp-<mcp_app_name>.yml -A
```

To update all instances at once:

```bash
uvx copier update -a .datarobot/answers/drmcp-*.yml -A
```

## Troubleshooting

**Integration tools return auth errors**

OAuth providers must be configured in DataRobot before integration tools will work. See the generated `dev.md` inside the template directory.

**Multiple instances conflict**

Each instance must use a unique `mcp_app_name`. If two instances share a name, their answers files and generated directories will collide. Check `.datarobot/answers/` — each instance should have its own `drmcp-<name>.yml`.
