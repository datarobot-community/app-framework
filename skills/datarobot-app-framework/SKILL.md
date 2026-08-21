---
name: datarobot-app-framework
description: Build a single component or a customized combination on DataRobot using the App Framework component system — a standalone agent, FastAPI app, LLM integration, or a non-default recipe wired by hand. For a fully integrated agentic application (MCP server, agent, backend, and frontend bundled and tested together), use datarobot-agent-assist instead.
---

# DataRobot App Framework

Build and deploy applications on DataRobot using composable `af-component-*` building blocks.

## Trigger Conditions

Use this skill when the user wants **just one piece**, or a **customized combination** they are
assembling themselves, rather than the full bundle:
- Wants just an agent (no API, no frontend, no MCP server bundled with it)
- Wants just a FastAPI backend, a React frontend, or an LLM integration, on its own
- Wants a highly customized recipe — a specific, non-default combination of components, or a
  component wired up in a way `datarobot-agent-assist` doesn't scaffold
- Wants to set up an App Framework recipe, or add a component to an existing one
- Wants to wire components together by hand (FastAPI ↔ Agent, LLM ↔ Agent, etc.)
- Mentions `dr component add`, `af-component`, `copier copy`, or `recipe-` in an AF context
- Wants to author, change, or debug a component, or know what one provisions

## Not This Skill

If the user wants a **fully integrated agentic application** — MCP server, agent, backend API, and
frontend, all in the box together and tested to work as a whole — that is
`datarobot-agent-assist` in DataRobot's official skill pack,
[`datarobot-oss/datarobot-agent-skills`](https://github.com/datarobot-oss/datarobot-agent-skills).
That is the default for "build me a LangGraph/CrewAI/LlamaIndex agent" with no further
qualification: it produces the complete, tested bundle rather than one piece of it. Route there
for:

- "Build me an agent" with no other constraint — the integrated bundle is the right default.
- Taking an agent from idea to deployment as a guided workflow — agent design, dress rehearsal
  against the LLM Gateway, and adversarial simulation.
- Instrumenting an agent with OpenTelemetry for traces, logs, and metrics.
- Running container workloads on the Workload API.
- Setting up CI/CD for a DataRobot application.
- The platform's AI/ML APIs: AutoML training, prediction deployments, batch and real-time
  predictions, feature engineering, drift monitoring, SHAP and explainability, data preparation.

Stay in this skill only once the user has said they want a single component, or a customization
beyond what the bundle scaffolds.

> **Note on overlapping vocabulary:** "agent" and "deployment" mean different things across the two
> packs. Here, "agent" means an LLM agentic app assembled from `af-component-agent`, and "deployment"
> means a Custom Application. In the AI/ML skills, "deployment" means an ML model deployment serving
> predictions.


## Pick Your Scenario

| What you want to build | Scenario |
|---|---|
| Agent API + playground UI (no custom frontend) | **Default — see below** |
| Simple FastAPI app / custom web UI | `scenarios/fastapi-app.md` |
| LLM integration in a notebook | `scenarios/llm-notebook.md` |

## Component Map

Every component lives in the [`datarobot-community`](https://github.com/datarobot-community)
GitHub org. A `github.com/datarobot/af-component-*` URL is wrong and 404s.

Core components:

| Component | Role | Requires |
|---|---|---|
| af-component-base | Foundation: Taskfile, Pulumi project, CI/CD, `.datarobot/` — always first, applied once | — |
| af-component-llm | LLM connectivity through the LLM Gateway or an external model | base |
| af-component-agent | Agent orchestration: CrewAI / LangGraph / LlamaIndex / NeMo Agent Toolkit | base + llm |
| af-component-fastapi-backend | FastAPI server deployed as a Custom Application | base |
| af-component-react | React + Vite frontend wired to the FastAPI backend | base + fastapi-backend |
| af-component-datarobot-mcp | FastMCP server with DataRobot predictive tools and third-party integrations | base |

The catalog is the search result, not this table — check
[`org:datarobot-community af-component`](https://github.com/search?q=org%3Adatarobot-community+af-component&type=repositories)
before telling a user a component does or does not exist. Only name a component whose repository resolves for an anonymous reader.

Capabilities the catalog does not cover are still reachable through Pulumi. A vector database,
for example, is added by writing `infra/infra/vdb.py` with
[`pulumi_datarobot`](https://github.com/datarobot-community/pulumi-datarobot) — see
[Adding a vector database](https://af.datarobot.com/guides/vector-database/).

For extended scenarios, load the relevant file from `scenarios/`.

## Prerequisites

```bash
curl https://cli.datarobot.com/install | sh     # macOS / Linux; Windows: irm https://cli.datarobot.com/winstall | iex
curl -LsSf https://astral.sh/uv/install.sh | sh
dr auth set-url && dr auth login
```

---

## Default Recipe: Minimal Agent

Outputs: API endpoint + DataRobot agent playground UI.

### Step 1 — Create recipe directory

```bash
mkdir recipe-my-agent && cd recipe-my-agent
```

> Convention: always prefix with `recipe-`. For team projects, create the repo in the DataRobot GitHub org first and clone it.

### Step 2 — Scaffold base

```bash
uvx copier copy https://github.com/datarobot-community/af-component-base .
```

Answer the interactive questions about your recipe name and settings. Defaults are safe.

### Step 3 — Add LLM

```bash
uvx copier copy https://github.com/datarobot-community/af-component-llm .
```

Key prompts:
- **LLM folder name**: `llm` (default)
- **Model name**: `azure-openai-gpt-4o-mini` or as required
- **Base answers file**: `.datarobot/answers/base.yml`

Creates `infra/infra/llm.py` and gateway config files.

### Step 4 — Add agent

```bash
dr component add https://github.com/datarobot-community/af-component-agent .
```

Key prompts:
- **Agent folder name**: `agent` (default)
- **Low-code YAML (NeMo Toolkit)?**: No (unless user specifically requests it)
- **Framework**: CrewAI / LangGraph / LlamaIndex — choose based on user need
- **Base answers file**: `.datarobot/answers/base.yml`
- **LLM answers file**: `.datarobot/answers/llm-llm.yml`
- **MCP answers file**: `.datarobot/answers/drmcp-mcp_server.yml` (optional — skip if not using MCP tools)

Creates:
```
agent/
├── agent/myagent.py   ← multi-agent workflow (customize here)
├── cli.py             ← local testing tool
├── dev.py             ← local dev server
└── tests/
infra/infra/agent.py   ← Pulumi deployment config
```

### Step 5 — Configure environment

```bash
dr dotenv setup
```

Key prompts:
- **Agent port**: 8842 (default)
- **DataRobot execution environment**: select from available environments
- **Execution environment version ID**: ID of the environment version to use
- **Pulumi passphrase**: any value (used for state encryption)
- **Use case**: can leave blank
- **LLM Gateway config**: select LLM Gateway with External Model

Press enter to accept defaults for most prompts.

### Step 6 — Test locally

```bash
cd agent
uv run python cli.py execute --user_prompt "Write a blog post about AI in healthcare"
cat execute_output.json | jq -r '.choices[0].message.content'
```

For iterative development with auto-reload:

```bash
dr run dev                                                              # Terminal 1
cd agent && uv run python cli.py execute --user_prompt "Test prompt"   # Terminal 2
```

Server runs at `http://localhost:8842` and reloads on code changes.

### Step 7 — Deploy

```bash
dr task deploy
```

Prompts to create a stack (name it anything), previews LLM + Agent resources, then deploys both. Outputs deployment IDs and URLs.

Check deployment info anytime:

```bash
dr task infra:info
```

## What you get

- Default: Planner agent (research + outline) + Writer agent (content creation)
- Sequential workflow with MCP tools support
- Agent playground UI in DataRobot
- API endpoint for integration

## Deploy updates

```bash
dr run deploy
```

## Tear down

```bash
dr task infra:down
```

## Customize

Edit `agent/agent/myagent.py` to:
- Change agent roles, goals, or task descriptions
- Add more agents to the crew
- Integrate additional MCP tools
- Switch framework (CrewAI → LangGraph → LlamaIndex)

## Resources

- App Framework docs: https://af.datarobot.com — see [Design](https://af.datarobot.com/design/) for the architecture and the interactive diagram
- DataRobot CLI: https://docs.datarobot.com/en/docs/agentic-ai/cli/overview.html and https://cli.datarobot.com
- Agent Templates: https://github.com/datarobot-community/datarobot-agent-templates
- Components: [`org:datarobot-community af-component`](https://github.com/search?q=org%3Adatarobot-community+af-component&type=repositories) — public repositories only

