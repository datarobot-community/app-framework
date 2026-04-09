# DataRobot App Framework

The App Framework is the software and tooling that makes building, updating, and shipping DataRobot applications fast. It gives mid-maturity developers and data scientists a code-first, batteries-included starting point — think Helm charts or full-stack starters, but purpose-built for DataRobot.

![App Framework Architecture](img/architecture-overview.png)

## What it is

App Templates are code-first recipes that bundle everything needed to build and run a full-stack DataRobot application: infrastructure-as-code, a local dev loop, CI/CD, and deployment to DataRobot Custom Applications — all from a single repo. Foundation templates already exist for:

- **[Talk to My Docs](https://github.com/datarobot-community/talk-to-my-docs-agents)** — Guarded RAG Assistant
- **[Talk to My Data](https://github.com/datarobot-community/talk-to-my-data-agent)** — Data Analyst
- **[DataRobot Agent Application](https://github.com/datarobot-community/datarobot-agent-application)** — Multi-agent orchestration starter

The App Framework is successful when bolting on new features, creating templates from scratch, and upgrading existing ones is simple.

## How it works

The framework is built around three ideas:

**Components** are copier-style templates — each a top-level folder or file-set — that you layer into your repo to add capabilities. You apply them one at a time and answer a few questions; your answers are recorded in `.datarobot/` so the stack can be updated automatically later.

| Component | What it adds |
|-----------|-------------|
| [**base**](components/base.md) | Task runner, Pulumi project, CI/CD scaffolding, `.datarobot/` config |
| [**fastapi-backend**](components/fastapi-backend.md) | FastAPI server, local dev loop, Custom App deployment |
| [**react**](components/react.md) | React + Vite frontend with dev proxy and static asset build |
| [**llm**](components/llm.md) | LLM Gateway or external model integration |
| [**agent**](components/agent.md) | CrewAI, LangGraph, LlamaIndex, or NeMo agent workflow |
| [**datarobot-mcp**](components/datarobot-mcp.md) | FastMCP server with DataRobot predictive tools and third-party integrations |

**The CLI** (`dr`) is your primary interface. It handles authentication, environment setup, local development, and deployment so you never have to manually edit YAML or track down the right command.

**The Declarative API** (via Pulumi) manages your DataRobot resources — use cases, deployments, playgrounds, custom apps — as infrastructure-as-code, making your stack reproducible and promotable across environments.

## Get started

- [**Design**](design/index.md) — Understand the architecture, principles, and building blocks
- [**0-Vibe: Build Your First App**](guides/zero-vibe.md) — Go from empty repo to deployed app in minutes
- [**Adding Custom Pages**](guides/custom-pages.md) — Extend FastAPI templates with new routes and templates
- [**Adding a Vector Database**](guides/vector-database.md) — Ground your agent in real documents
- [**Developer Guide**](developer.md) — Run the docs site locally and contribute
- [**Skills**](skills.md) — AI agent skills for your coding assistant
