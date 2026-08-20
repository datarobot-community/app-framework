# base

**Repository:** [github.com/datarobot-community/af-component-base](https://github.com/datarobot-community/af-component-base)

The infrastructure-as-code foundation required for every App Framework recipe. Apply this first — all other components build on top of it.

`af-component-base` exists to provide the `infra/` folder: the Pulumi project every other component contributes a resource module to. Alongside it come the `.datarobot/` configuration directory, an optional shared `core` library, and per-folder lint and test workflows. It runs a short wizard and writes the answers to `.datarobot/answers/base.yml`, which subsequent components inherit.

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
uvx copier copy https://github.com/datarobot-community/af-component-base .
```

The wizard prompts for:

| Question | Notes |
|----------|-------|
| Template name | Human-readable display name (e.g., `My Sales Assistant`). |
| Template code name | Auto-derived slug; override if needed. |
| Template description | Shown in the App Framework gallery. |
| Copyright year | Defaults to current year. |
| Include core library | Shared `core` package for multi-component recipes (default: yes). |

## Component dependencies

None. This is the root of every App Framework component graph.

## Update

```bash
dr component update .datarobot/answers/base.yml
```

## What it adds

- `infra/` — the Pulumi project other components plug into: `Pulumi.yaml`, an `__main__.py` that auto-discovers every module under `infra/infra/`, `configurations/` for swappable modules, `feature_flags/` for the platform flags a component requires, `tests/`, and the folder's own Taskfile and `pyproject.toml`.
- `.datarobot/answers/base.yml` — recorded answers reused by all subsequent components — and `.datarobot/cli/base.yml`, the environment schema `dr dotenv setup` reads.
- `core/` — optional shared Python package: a persistent filesystem over DataRobot storage, SQLite and DuckDB drivers on top of it, and a read/write lock.
- `.env.template`, `.gitignore`, `docs/`, and `.agents/skills/` for coding assistants.
- `.github/` — per-folder lint and test workflows, Dockerfile lint, shellcheck, yamlfmt, and Dependabot.

Base ships a Taskfile per folder rather than one at the repository root; `dr task compose` assembles the root runner from the rendered subdirectories.

## Troubleshooting

### Copier asks questions I already answered

`.datarobot/answers/base.yml` may be missing or out of date. Use `-A` to skip interactive prompts:

```bash
uvx copier update -a .datarobot/answers/base.yml -A
```

### `dr component add` is not found

Install or update the DataRobot CLI. See [cli.datarobot.com](https://cli.datarobot.com) for installation instructions.

### Template conflicts after `copier update`

Copier shows a diff for any file with local modifications. Review each conflict, keep local changes where appropriate, and commit the result.
