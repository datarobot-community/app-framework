# llm

**Repository:** [github.com/datarobot-community/af-component-llm](https://github.com/datarobot-community/af-component-llm)

Adds LLM integration to your recipe via DataRobot's LLM Gateway or a directly deployed model. This is the building block for any recipe that needs to call a language model — it's also a prerequisite for the [agent](agent.md) component.

The component provisions the Pulumi infrastructure to create an LLM Deployment in DataRobot and exposes configuration for switching between LLM Gateway, an external model, or an already-deployed model — all via environment variables.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed
- The [base](base.md) component already applied

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-llm .
```

Or with copier directly:

```bash
uvx copier copy https://github.com/datarobot-community/af-component-llm .
```

## Component dependencies

| Component | Required |
|-----------|----------|
| [base](base.md) | Yes |

## Configuration

After applying, run the environment setup wizard:

```bash
dr dotenv setup
```

When prompted for `INFRA_ENABLE_LLM`, choose your integration type:

| Option | When to use |
|--------|-------------|
| `gateway_direct.py` | LLM Gateway — simplest, most production-ready |
| `blueprint_with_llm_gateway.py` | LLM Gateway + Vector Database support |
| `blueprint_with_external_llm.py` | External model (OpenAI, Anthropic, etc.) via LLM Gateway |
| `deployed_llm.py` | An already-deployed DataRobot LLM Deployment |

## Deploy

```bash
dr task deploy
```

Retrieve deployment info at any time:

```bash
dr task infra:info
```

## Update

```bash
uvx copier update -a .datarobot/answers/llm-<llm_name>.yml -A
```

## What it adds

- `infra/infra/llm.py` — Pulumi resources for the LLM deployment and playground
- `infra/configurations/llm/` — LLM configuration blueprints
- `.datarobot/answers/llm-<name>.yml` — recorded answers
- `.datarobot/cli/llm.yml` — CLI configuration for `dr dotenv setup`
