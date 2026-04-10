# Components

App Framework components are [copier](https://copier.readthedocs.io/) templates that you layer into your recipe one at a time. Each component adds a top-level folder or file set and records your answers in `.datarobot/answers/`, so the stack can be updated automatically later.

If you are new to the framework, start with `base`. It creates the shared project structure that all other components depend on.

## Core components

| Component | Description | Repeatable |
|-----------|-------------|-----------|
| [**base**](base.md) | Task runner, Pulumi project, CI/CD scaffolding, and `.datarobot/` configuration. Required first for every recipe. | No |
| [**llm**](llm.md) | LLM Gateway or external model integration via the DataRobot LLM Deployment. | Yes |
| [**fastapi-backend**](fastapi-backend.md) | FastAPI server deployed as a DataRobot Custom Application. | Yes |
| [**react**](react.md) | React + Vite frontend wired to a FastAPI backend, with a development proxy and a production asset build. | Yes |
| [**agent**](agent.md) | Agentic workflow scaffold supporting CrewAI, LangGraph, LlamaIndex, and NeMo Agent Toolkit. | Yes |
| [**datarobot-mcp**](datarobot-mcp.md) | FastMCP server with DataRobot predictive tools and third-party integrations (Google Drive, Jira, Confluence, Microsoft Graph). | Yes |

## Typical apply order

```text
base → llm → fastapi-backend → react
                 ↓
              agent
base → datarobot-mcp
```

`base` must always come first. `agent` requires both `base` and `llm`. `react` requires both `base` and `fastapi-backend`. `datarobot-mcp` only requires `base`.

## Adding a component

The safest way to get started is to apply a real component with a complete command:

```bash
dr component add https://github.com/datarobot-community/af-component-[NAME] .
```

To apply a different component, replace the repository URL with the component repository you want to add.

You can also use Copier directly:

```bash
uvx copier copy https://github.com/datarobot-community/af-component-base .
```

The CLI is the recommended entry point because it handles authentication, environment setup, and component workflows in one interface.

## Updating a component

Each applied component leaves an answers file in `.datarobot/answers/`. Pass that answers file to `copier update` to pull in changes non-interactively:

```bash
uvx copier update -a .datarobot/answers/COMPONENT-NAME.yml -A
```

To update all components at once:

```bash
uvx copier update -a .datarobot/answers/*.yml -A
```

## Adding your own

If you build a component that others might want to use, share it in the `#applications` Slack channel. Components live in their own repositories. Search for `af-component` in the `datarobot-community` GitHub organization to see the full catalog.
