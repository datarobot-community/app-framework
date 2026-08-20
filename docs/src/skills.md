# Skills

App Framework Studio ships a set of AI agent skills that can be installed into any AI coding assistant (GitHub Copilot, Gemini, Cursor, and others) that supports the `ai-agent-skills` standard.

## Which skill pack?

DataRobot maintains two skill packs. Use this table to pick the right install command (both packs can be installed in the same assistant).

| You want to… | Skill pack | Install |
|--------------|------------|---------|
| Scaffold and deploy **App Framework** recipes: `af-component-*`, `dr component add`, copier templates, LLM Gateway, agent frameworks, `dr run deploy` | **App Framework Studio** (this repo) | `npx ai-agent-skills install datarobot-community/app-framework` |
| Train and operate **tabular ML** models: projects, AutoML, prediction deployments, monitoring, explainability, data prep | [OSS ML skills](https://github.com/datarobot-oss/datarobot-agent-skills) | `npx ai-agent-skills install datarobot-oss/datarobot-agent-skills` |

The `datarobot-app-framework` skill includes routing guidance when a request belongs in the OSS pack instead (and vice versa if you install both). If you only install one pack, choose the row that matches your primary work — wrong-pack installs are a common source of incorrect CLI or SDK guidance.

## Installing skills

Install all skills from this repository using [`npx ai-agent-skills`](https://github.com/skillcreatorai/Ai-Agent-Skills):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```

This registers the following skills in the AI assistant:

| Skill | Description |
|-------|-------------|
| `datarobot-app-framework` | Build and deploy applications on DataRobot using the App Framework component system — FastAPI applications, LLM integrations, and agentic workflows. |
| `datarobot-app-framework-doc-update` | Generate and intelligently merge README documentation for a component using its `copier-module.yaml` schema and the [Documentation Style Specification](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/documentation-style-spec.md). |

## Available skills

### `datarobot-app-framework`

Guides an AI assistant through scaffolding, configuring, and deploying App Framework recipes using `af-component-*` building blocks. Covers agents (CrewAI, LangGraph, LlamaIndex), FastAPI backends, React frontends, and LLM integrations.

Trigger the skill by asking the assistant to:

- Build or deploy an application on DataRobot using the App Framework.
- Add a component (`dr component add`, `uvx copier copy`).
- Wire components together or configure an agent.

### `datarobot-app-framework-doc-update`

Generates a structured `README.generated.md` scaffold from a component's `copier-module.yaml`, then intelligently merges it with the existing `README.md` — preserving human-written content, applying the [Documentation Style Specification](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/documentation-style-spec.md), and using the template's authoring hints to fill any gaps.

Trigger the skill by asking the assistant to:

- Update or regenerate the README for a component repository.
- Generate documentation from `copier-module.yaml`.

#### Running locally before pushing to GitHub

```bash
# Step 1. Generate the scaffold from the app-framework-studio root.
cd ~/code/app-framework-studio
uv run --project tools/af_component_doc_update af-component-doc-update ~/code/YOUR_COMPONENT_DIR

# Step 2. Invoke the skill in Copilot Chat.
```

```text
#skills/datarobot-app-framework-doc-update/SKILL.md Update the README for ~/code/YOUR_COMPONENT_DIR. For Step 1, use the local variant: cd ~/code/app-framework-studio && uv run --project tools/af_component_doc_update af-component-doc-update ~/code/YOUR_COMPONENT_DIR
```
