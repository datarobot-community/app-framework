# DataRobot App Framework

The App Framework is the software and tooling that makes building, updating, and shipping DataRobot applications fast. It gives developers and data scientists a code-first starting point, similar to Helm charts or full-stack starters, but built specifically for DataRobot.

![App Framework Architecture](img/architecture-overview.png)

## What it is

App templates are code-first recipes that bundle everything needed to build and run a full-stack DataRobot application: infrastructure-as-code, a local development loop, CI/CD, and deployment to DataRobot Custom Applications, all from a single repository. Foundation templates already exist for:

- **[Talk to My Docs](https://github.com/datarobot-community/talk-to-my-docs-agents)**&mdash;Guarded RAG Assistant.
- **[Talk to My Data](https://github.com/datarobot-community/talk-to-my-data-agent)**&mdash;Data Analyst.
- **[DataRobot Agentic starter](https://github.com/datarobot-community/datarobot-agent-application)**&mdash;Multi-agent orchestration starter.
- **[DataRobot MCP](https://github.com/datarobot-community/af-component-datarobot-mcp)**&mdash;FastMCP server with DataRobot predictive tools and third-party integrations.

This documentation explains how the framework is organized, how components fit together, and how to build or extend an application template. If you are new to the project, start here and then continue to the getting-started and design pages.

## Before you begin

Most guides assume that you already have:

- A DataRobot account and API token.
- The [DataRobot CLI](https://cli.datarobot.com) installed.
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed.
- A GitHub repository where you can create or clone an application template.

## How it works

The framework is built around three ideas:

**Components** are copier-style templates, each a top-level folder or file set, that you layer into your repository to add capabilities. You apply them one at a time and answer a few questions. Your answers are recorded in `.datarobot/`, so the stack can be updated automatically later.

| Component | What it adds |
|-----------|-------------|
| [**base**](components/base.md) | Task runner, Pulumi project, CI/CD scaffolding, `.datarobot/` configuration. |
| [**fastapi-backend**](components/fastapi-backend.md) | FastAPI server, local development loop, Custom Application deployment. |
| [**react**](components/react.md) | React + Vite frontend with a development proxy and static asset build. |
| [**llm**](components/llm.md) | LLM Gateway or external model integration. |
| [**agent**](components/agent.md) | CrewAI, LangGraph, LlamaIndex, or NeMo agent workflow. |
| [**datarobot-mcp**](components/datarobot-mcp.md) | FastMCP server with DataRobot predictive tools and third-party integrations. |

**The DataRobot CLI** (`dr`) is your primary interface. It handles authentication, environment setup, local development, and deployment, so you never have to manually edit YAML files or track down the right command.

**The Declarative API** (via Pulumi) manages your DataRobot resources, including use cases, deployments, playgrounds, and custom applications, as infrastructure-as-code. This makes your stack reproducible across environments.

For readers who are new to the terminology:

- A **recipe** is the repository for one application template or application instance.
- A **component** is a reusable template that adds one capability, such as a FastAPI backend or React frontend.
- An **answers file** is the YAML file in `.datarobot/answers/` that stores the choices you made when applying a component.

## Get started

- [**0-Vibe: Build your first application**](guides/zero-vibe.md)&mdash;Go from an empty repository to a deployed application in minutes.
- [**Design**](design/index.md)&mdash;Understand the architecture, repository model, and building blocks.
- [**Components**](components/index.md)&mdash;Learn what each component adds and the order in which to apply them.
- [**Adding custom pages**](guides/custom-pages.md)&mdash;Extend FastAPI templates with new routes and templates.
- [**Adding a vector database**](guides/vector-database.md)&mdash;Ground your agent in real documents.
- [**Developer guide**](developer.md)&mdash;Run the docs site locally and contribute.
- [**Skills**](skills.md)&mdash;AI agent skills for your coding assistant.
