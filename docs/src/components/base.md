# base

**Repository:** [github.com/datarobot-community/af-component-base](https://github.com/datarobot-community/af-component-base)

The foundational scaffold required for every App Framework recipe. Apply this first — all other components build on top of it.

`af-component-base` sets up the task runner, Pulumi project structure, CI/CD scaffolding, and the `.datarobot/` configuration directory. It walks you through a short wizard and writes the answers to `.datarobot/answers/base.yml`, which subsequent components inherit.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed

## Apply

```bash
dr component add https://github.com/datarobot-community/af-component-base .
```

Or with copier directly:

```bash
uvx copier copy datarobot-community/af-component-base .
```

The wizard prompts for:

| Question | Notes |
|----------|-------|
| Template name | Human-readable display name (e.g. `My Sales Assistant`). |
| Template code name | Auto-derived slug; override if needed. |
| Template description | Shown in the App Framework gallery. |
| Copyright year | Defaults to current year. |
| Include core library | Shared `core` package for multi-component recipes (default: yes). |

## Component dependencies

None. This is the root of every App Framework component graph.

## Update

```bash
uvx copier update -a .datarobot/answers/base.yml -A
```

## What it adds

- `Taskfile.yaml`&mdash;task runner with `.env` auto-loading and tab completion.
- `Pulumi.yaml` + `infra/`&mdash;base Pulumi project that other components plug into.
- `.datarobot/answers/base.yml`&mdash;recorded answers reused by all subsequent components.
- `.github/`&mdash;CI/CD workflows for updates, tests, and deployment.
- `LICENSE`, `CONTRIBUTING.md`, `.github/CODEOWNERS`

## Troubleshooting

**Copier asks questions I already answered**

`.datarobot/answers/base.yml` may be missing or out of date. Use `-A` to skip interactive prompts:

```bash
uvx copier update -a .datarobot/answers/base.yml -A
```

**Template conflicts after `copier update`**

Copier shows a diff for any file with local modifications. Review each conflict, keep your changes where appropriate, and commit the result.
