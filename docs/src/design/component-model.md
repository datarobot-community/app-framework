# Component model

![Studio Component Model](../img/studio-component-model.png)

The App Framework Template Studio is the templating and update-management layer behind the component system described in these docs. It solves two core problems:

1. **Maintenance at scale** — A bug fix to five foundation application templates with 100 applications per template means the fix needs to reach 500 cloned applications. Manual propagation does not scale.
2. **Template creation speed** — There is value in standing up the latest AI blueprint on DataRobot quickly. You need good building blocks.

Components are `copier`-style templates. Each is a top-level folder or file set that you can add to your recipe. The answers you give during template application are recorded in `.datarobot/` as YAML, enabling future automated updates at the component-instance level.

## Global components

These appear once per application template:

| Component | Repository | Description |
|-----------|------------|-------------|
| **Base** | [af-component-base](https://github.com/datarobot-community/af-component-base) | Pulumi project, task runner, `.datarobot/` configuration, CI/CD scaffolding, `LICENSE`, `CODEOWNERS`. |
| **LLM** | [af-component-llm](https://github.com/datarobot-community/af-component-llm) | LLM Gateway or external model integration via the DataRobot LLM Deployment. |

## One-to-many components

These can be applied multiple times as you build out the template:

| Component | Repository | Description |
|-----------|------------|-------------|
| **FastAPI Backend** | [af-component-fastapi-backend](https://github.com/datarobot-community/af-component-fastapi-backend) | Local development tasks, FastAPI API documentation, and Pulumi configuration for Custom Application deployment. |
| **React Frontend** | [af-component-react](https://github.com/datarobot-community/af-component-react) | Development server, API proxy, static asset build, and prebuilt tests. |
| **Agent** | [af-component-agent](https://github.com/datarobot-community/af-component-agent) | CrewAI, LangGraph, LlamaIndex, or YAML-based NeMo Agent Toolkit. |
| **DataRobot MCP** | [af-component-datarobot-mcp](https://github.com/datarobot-community/af-component-datarobot-mcp) | FastMCP server with DataRobot predictive tools and third-party integrations. |


## Technical underpinnings

It's all built on top of [Copier](https://copier.readthedocs.io/). Similar to Yeoman or Cookiecutter, but with Git semantics that make updates after you copy the template baked into the box.

## Update model

![Copier Update](../img/studio-copier-update.png)

The App Framework uses copier and git fork semantics to keep things updated.
