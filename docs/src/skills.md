# Skills

App Framework Studio ships a set of AI agent skills that can be installed into any AI coding assistant (GitHub Copilot, Gemini, Cursor, and others) that supports the `ai-agent-skills` standard.

## Installing skills

Install all skills from this repository using [`npx ai-agent-skills`](https://github.com/ai-agent-skills/cli):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```

This registers the following skills in your AI assistant:

| Skill | Description |
|-------|-------------|
| `datarobot-app-framework` | Build and deploy applications on DataRobot using the App Framework component system — FastAPI apps, LLM integrations, and agentic workflows. |
| `datarobot-app-framework-doc-update` | Generate and intelligently merge README documentation for a component using its `copier-module.yaml` schema. |

## Available skills

### `datarobot-app-framework`

Guides your AI assistant through scaffolding, configuring, and deploying App Framework recipes using `af-component-*` building blocks. Covers agents (CrewAI, LangGraph, LlamaIndex), FastAPI backends, React frontends, and LLM integrations.

Trigger it by asking your assistant to:
- Build or deploy an app on DataRobot using the App Framework.
- Add a component (`dr component add`, `uvx copier copy`).
- Wire components together or configure an agent.

### `datarobot-app-framework-doc-update`

Generates a structured `README.generated.md` scaffold from a component's `copier-module.yaml`, then intelligently merges it with the existing `README.md` — preserving human-written content and using the template's authoring hints to fill any gaps.

Trigger it by asking your assistant to:
- Update or regenerate the README for a component repo.
- Generate documentation from `copier-module.yaml`.

#### Running locally (before pushing to GitHub)

```bash
# Step 1 — generate the scaffold (from the app-framework-studio root).
cd ~/code/app-framework-studio
uv run --project tools/af_component_doc_update af-component-doc-update ~/code/<your-component>

# Step 2 — invoke the skill in Copilot chat.
```

```
#skills/datarobot-app-framework-doc-update/SKILL.md Update the README for ~/code/<your-component>. For Step 1, use the local variant: cd ~/code/app-framework-studio && uv run --project tools/af_component_doc_update af-component-doc-update ~/code/<your-component>
```
