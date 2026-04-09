# App Framework Studio

Tooling to apply and update App Framework Components.

**Documentation:** https://af.datarobot.com

## Installing Skills

Install all skills from this repository into your AI agent using [`ai-agent-skills`](https://github.com/datarobot-community/ai-agent-skills):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```

## Components

| Component | Description |
|-----------|-------------|
| [`af-component-base`](https://github.com/datarobot-community/af-component-base) | Task runner, Pulumi project, CI/CD, `.datarobot/` config |
| [`af-component-fastapi-backend`](https://github.com/datarobot-community/af-component-fastapi-backend) | FastAPI server and Custom App deployment |
| [`af-component-react`](https://github.com/datarobot-community/af-component-react) | React frontend |
| [`af-component-llm`](https://github.com/datarobot-community/af-component-llm) | LLM Gateway / external model integration |
| [`af-component-agent`](https://github.com/datarobot-community/af-component-agent) | Agentic workflows (CrewAI, LangGraph, LlamaIndex) |

## Development

See the [Developer Guide](https://datarobot-oss.github.io/app-framework/developer/) for setup instructions, running docs locally, and the `copier-watch` tool for iterating on component templates.
