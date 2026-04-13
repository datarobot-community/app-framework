<p align="center">
  <a href="https://github.com/datarobot-community/app-framework">
    <img src="https://af.datarobot.com/img/datarobot_logo.avif" width="600px" alt="DataRobot Logo"/>
  </a>
</p>
<p align="center">
    <span style="font-size: 1.5em; font-weight: bold; display: block;">App Framework Studio</span>
</p>

<p align="center">
  <a href="https://datarobot.com">Homepage</a>
  ·
  <a href="https://af.datarobot.com">Documentation</a>
  ·
  <a href="https://docs.datarobot.com/en/docs/get-started/troubleshooting/general-help.html">Support</a>
</p>

<p align="center">
  <a href="https://af.datarobot.com">
    <img src="https://img.shields.io/badge/af.datarobot.com-a?label=Docs&labelColor=30373D&color=5B8FF9" alt="Documentation">
  </a>
  <a href="https://join.slack.com/t/datarobot-community/shared_invite/zt-3uzfp8k50-SUdMqeux25ok9_5wr4okrg">
    <img src="https://img.shields.io/badge/%23applications-a?label=Slack&labelColor=30373D&color=81FBA6" alt="Slack #applications">
  </a>
</p>

Tooling to apply and update App Framework components.

## Installing skills

Install all skills from this repository into your AI agent using [`ai-agent-skills`](https://github.com/datarobot-community/ai-agent-skills):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```

## Components

| Component | Description |
|-----------|-------------|
| [`af-component-base`](https://github.com/datarobot-community/af-component-base) | Task runner, Pulumi project, CI/CD, `.datarobot/` config. |
| [`af-component-fastapi-backend`](https://github.com/datarobot-community/af-component-fastapi-backend) | FastAPI server and Custom App deployment. |
| [`af-component-react`](https://github.com/datarobot-community/af-component-react) | React frontend. |
| [`af-component-llm`](https://github.com/datarobot-community/af-component-llm) | LLM Gateway / external model integration. |
| [`af-component-agent`](https://github.com/datarobot-community/af-component-agent) | Agentic workflows (CrewAI, LangGraph, LlamaIndex). |
| [`af-component-datarobot-mcp`](https://github.com/datarobot-community/af-component-datarobot-mcp) | FastMCP server with DataRobot predictive tools and third-party integrations. |

## Development

See the [Developer Guide](https://af.datarobot.com/developer/) for setup instructions, running docs locally, and using `copier-watch` to iterate on component templates.
