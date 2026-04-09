# agent

**Repository:** [github.com/datarobot-community/af-component-agent](https://github.com/datarobot-community/af-component-agent)

Adds an agentic workflow to your recipe. The component scaffolds a single or multi-agent system using your choice of framework: **CrewAI**, **LangGraph**, **LlamaIndex**, or **NeMo Agent Toolkit** (NAT). It includes a local dev server, a CLI for testing, a test suite, and Pulumi infrastructure for deployment to DataRobot.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) and [`uvx`](https://docs.astral.sh/uv/guides/tools/) installed
- [`dr`](https://cli.datarobot.com) installed
- The [base](base.md) component already applied
- The [llm](llm.md) component already applied

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-agent .
```

Or with copier directly:

```bash
uvx copier copy datarobot-community/af-component-agent .
```

When prompted, choose your agent framework:

| Framework | When to use |
|-----------|-------------|
| `base` | Minimal scaffold — bring your own agentic logic |
| `crewai` | Role-based multi-agent crews |
| `langgraph` | Graph-based stateful agent workflows |
| `llamaindex` | RAG and document-aware agent workflows |
| `nat` | YAML-based NeMo Agent Toolkit |

## Component dependencies

| Component | Required |
|-----------|----------|
| [base](base.md) | Yes |
| [llm](llm.md) | Yes |

## What it adds

```
agent/
├── agent/myagent.py   # Agent workflow — edit this to customize behavior
├── cli.py             # CLI for local testing
├── dev.py             # Local development server
├── tests/             # Test suite
└── public/            # UI assets
infra/infra/agent.py   # Pulumi deployment resources
```

## Configure

```bash
dr dotenv setup
```

The wizard asks for:

- Agent port (default: 8842)
- DataRobot execution environment
- Execution environment version ID
- Pulumi passphrase
- DataRobot default use case (optional)
- LLM Gateway configuration

## Local development

Start the local server:

```bash
dr run dev
```

Run the agent from another terminal:

```bash
uv run python cli.py execute --user_prompt "Write a blog post about AI in healthcare" --show_output
```

## Testing

Run all tests:

```bash
task test
```

Test a specific framework:

```bash
task test-<agent_framework>
```

Test the CLI:

```bash
task test-cli
```

## Deploy

```bash
dr task deploy
```

After deployment, the agent is available in the DataRobot workbench under your use case, accessible via the agent playground or the deployment API endpoint.

## Customizing agent behavior

Edit `agent/agent/myagent.py` to:

- Change agent roles and goals
- Modify task descriptions
- Add agents to the crew
- Integrate MCP tools

## Update

```bash
uvx copier update -a .datarobot/answers/agent-<agent_app>.yml -A
```

## End-to-end test

The component includes a full lifecycle E2E test (render → build → deploy → test → destroy):

```bash
task test-e2e
```

By default it tests all frameworks. To run a subset:

```bash
E2E_AGENT_FRAMEWORKS=base,crewai task test-e2e
```
