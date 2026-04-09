# Components

App Framework components are [copier](https://copier.readthedocs.io/) templates that you layer into your recipe one at a time. Each component adds a top-level folder or file-set, and records your answers in `.datarobot/answers/` so the stack can be updated automatically later.

## Core components

| Component | Description | Repeatable |
|-----------|-------------|-----------|
| [**base**](base.md) | Task runner, Pulumi project, CI/CD scaffolding, and `.datarobot/` config. Required first for every recipe. | No |
| [**llm**](llm.md) | LLM Gateway or external model integration via DataRobot's LLM Deployment. | Yes |
| [**fastapi-backend**](fastapi-backend.md) | FastAPI server deployed as a DataRobot Custom Application. | Yes |
| [**react**](react.md) | React + Vite frontend wired to a FastAPI backend, with dev proxy and production asset build. | Yes |
| [**agent**](agent.md) | Agentic workflow scaffold supporting CrewAI, LangGraph, LlamaIndex, and NeMo Agent Toolkit. | Yes |

## Typical apply order

```
base → llm → fastapi-backend → react
                 ↓
              agent
```

`base` must always come first. `agent` requires both `base` and `llm`. `react` requires both `base` and `fastapi-backend`.

## Adding a component

Using the CLI (recommended):

```bash
dr component add https://github.com/datarobot-community/af-component-<name> .
```

Using copier directly:

```bash
uvx copier copy datarobot-community/af-component-<name> .
```

## Updating a component

Each applied component leaves an answers file in `.datarobot/answers/`. Pass it to `copier update` to pull in changes non-interactively:

```bash
uvx copier update -a .datarobot/answers/<component>-<name>.yml -A
```

To update all components at once:

```bash
uvx copier update -a .datarobot/answers/*.yml -A
```

## Adding your own

Built something others might want? The `#applications` Slack channel is the place to share. Components live in their own repos — search for `af-component` in the `datarobot-community` GitHub org to see the full catalog.
