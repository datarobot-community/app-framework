# Design

The App Framework is built around a clear set of architectural decisions. This section covers how it works, why it was designed this way, and what each layer does.

## Overview

Application Templates are code-first recipes for building full-stack DataRobot applications. Think Helm charts, or full-stack starters like the [FastAPI full-stack template](https://github.com/fastapi/full-stack-fastapi-template) — but with DataRobot's AI blueprints baked in and everything wired together for production.

![App Framework Architecture Overview](../img/architecture-overview.png)

The north star is enabling customers to deploy something like an NVIDIA VSS directly on DataRobot, add DataRobot value, make it production-grade, and keep it easily customizable.

Foundation App Templates are the reference implementations built from this framework:

| Template | Description |
|----------|-------------|
| [Talk to My Docs](https://github.com/datarobot-community/talk-to-my-docs-agents) | Guarded RAG Assistant. |
| [Talk to My Data](https://github.com/datarobot-community/talk-to-my-data-agent) | Data Analyst. |
| [DataRobot Agent Application](https://github.com/datarobot-community/datarobot-agent-application) | Multi-agent orchestration starter. |

Each Foundation App Template is a private repo that publishes to a corresponding OSS repo via GitHub release mechanics.

**So, what is the App Framework?**

Simply put: the software and templates that build App Templates, and enable them to be more customizable and more complex. The App Framework is successful when adding new features to App Templates, creating App Templates from scratch, and upgrading App Templates is simple.

## In this section

- [**Principles**](principles.md)&mdash;The design decisions that guide every component.
- [**Component model**](component-model.md)&mdash;How templates are structured, applied, and updated.
- [**CLI**](cli.md)&mdash;The `dr` command and what it handles.
- [**Declarative API**](declarative-api.md)&mdash;Infrastructure-as-code for DataRobot resources.
