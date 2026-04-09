# Component Model

![Studio Component Model](../img/studio-component-model.png)

The App Framework — Template Studio is the templating and update management layer. It solves two core problems:

1. **Maintenance at scale** — A bugfix to all 5 Foundation App Templates with 100 apps per template means the fix needs to reach 500 cloned apps. Manual propagation doesn't scale.
2. **Template creation speed** — There is market value in standing up the latest AI blueprint on DataRobot fast. You need good lego blocks.

Components are `copier`-style templates. Each is a top-level folder or file-set you can add to your recipe. The answers you give during template application are recorded in `.datarobot/` as YAML, enabling future automated updates at the component-instance level.

## Global components

These appear once per app template:

| Component | Repository | Description |
|-----------|------------|-------------|
| **Base** | [af-component-base](https://github.com/datarobot-community/af-component-base) | Pulumi project, task runner, `.datarobot/` config, CI/CD scaffolding, `LICENSE`, `CODEOWNERS` |
| **LLM** | [af-component-llm](https://github.com/datarobot-community/af-component-llm) | LLM Gateway or external model integration via DataRobot's LLM Deployment |

## One-to-many components

These can be applied multiple times as you build out the template:

| Component | Repository | Description |
|-----------|------------|-------------|
| **FastAPI Backend** | [af-component-fastapi-backend](https://github.com/datarobot-community/af-component-fastapi-backend) | Local dev tasks, FastAPI autodocs, Pulumi config for Custom App deployment |
| **React Frontend** | [af-component-react](https://github.com/datarobot-community/af-component-react) | Dev server, proxy to API, static asset build, pre-baked tests |
| **Agent** | [af-component-agent](https://github.com/datarobot-community/af-component-agent) | CrewAI, LangGraph, LlamaIndex, or YAML-based NeMo Agent Toolkit |

## Update model

![Copier Update](../img/studio-copier-update.png)

The Studio uses a Dependabot-like approach: automated pull requests to all App Template repos that use the component answers, with PR-per-component granularity. App Template authors can selectively or completely disable updates at the component-instance level.

This is powered by **Diffington** — an agent built using the App Framework itself — that monitors your recipe for component updates and creates PRs when updates are available. To set it up, request your repo be added to Diffington's watch list in the `#applications` Slack channel.
