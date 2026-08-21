<p align="center">
  <a href="https://github.com/datarobot-community/app-framework">
    <img src="https://af.datarobot.com/img/datarobot_logo.avif" width="600px" alt="DataRobot Logo"/>
  </a>
</p>
<h2 align="center">App Framework Studio</h2>

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

## Which skill pack?

DataRobot's official skill pack for coding assistants is
[`datarobot-agent-skills`](https://github.com/datarobot-oss/datarobot-agent-skills). Its
`datarobot-agent-assist` skill builds a **fully integrated agentic application** — MCP server,
agent, backend API, and frontend, all in the box together and tested to work as a whole. Install
it for "build me an agent" with no further qualification:

```bash
npx ai-agent-skills install datarobot-oss/datarobot-agent-skills
```

The skills in **this** repository are for when you want **just one piece**, or a **customized
combination** you assemble yourself — just an agent, just a FastAPI app, a non-default recipe, or
a component wired up by hand outside what the bundle scaffolds. They also cover authoring and
documenting `af-component-*` components. Both packs can be installed in the same assistant.

## Installing skills

Install all skills from this repository into your AI agent using [`ai-agent-skills`](https://github.com/skillcreatorai/Ai-Agent-Skills):

```bash
npx ai-agent-skills install datarobot-community/app-framework
```

## Components

The following App Framework components are maintained in separate repositories under the [`datarobot-community`](https://github.com/datarobot-community) GitHub organization:

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

## Documentation style

Component README files follow the [Documentation Style Specification](skills/datarobot-app-framework-doc-update/documentation-style-spec.md). Use the [`datarobot-app-framework-doc-update`](skills/datarobot-app-framework-doc-update/SKILL.md) skill and the `af-component-doc-update` tool to scaffold and merge README content from `copier-module.yaml`.
