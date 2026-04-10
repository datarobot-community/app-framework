# Developer guide

This guide is for developers who want to contribute to the App Framework. It covers the prerequisites and how to run the documentation site locally.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Task](https://taskfile.dev/installation/)

### Install the Task runner

#### macOS

```bash
brew install go-task/tap/go-task
```

#### Linux

```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
```

#### Windows

```powershell
choco install go-task
```

## Running the documentation site locally

```bash
task docs-serve
```

This command installs dependencies and starts a local server at [http://localhost:8000](http://localhost:8000). The site reloads automatically as you edit files in the `docs/` directory.

## Copier watch

`tools/copier-watch/copier-watch.py` is a development tool for iterating efficiently on [copier](https://copier.readthedocs.io/en/stable/) templates such as `af-component-fastapi-backend`.

The script watches all file changes in a source template repository. When you edit a template, it:

1. Creates a local commit on the source repository and amends it on each subsequent change.
2. Runs `copier update` on the destination repository using that local commit.

This lets you iterate on Jinja templates without pushing remote commits. For each change in the source repository, it also resets the destination repository and applies the full changeset from scratch, so you do not accumulate partial changes.

!!! warning
    This script modifies Git repositories and can cause data loss. Ensure the destination repository has a clean `git status` before use. It runs `git reset` and `git clean` on the destination.

### Copier watch usage

```bash
uv run tools/copier-watch/copier-watch.py \
  --commit-message 'Adjusted backend' \
  --answers-file .datarobot/answers/fastapi-web.yml \
  ~/code/af-component-fastapi-backend \
  ~/code/recipe-talk-to-my-docs
```

Arguments:

| Argument | Description |
|----------|-------------|
| `--commit-message` | Message for the local amended commit on the source repository. |
| `--answers-file` | Path to the copier answers file in the destination repository. |
| `SOURCE_REPOSITORY` | Path to the component template repository being edited. |
| `DESTINATION_REPOSITORY` | Path to the recipe repository that receives the changes. |

### Typical workflow

- Top terminal: `pytest` watcher running in the destination repository.
- Bottom-left terminal: `copier-watch` watching `af-component-fastapi-backend` for changes.
- Bottom-right terminal: template editing. When tests change, the updated template is applied to the destination repository, and `pytest-watcher` detects the updates automatically.

![copier-watch demo](img/copier-watch-demo.gif)

---

## Component doc update

`tools/af_component_doc_update` generates a `README.generated.md` scaffold for App Framework component repositories. It reads the component's `copier-module.yaml`, which declares the module name, description, dependencies, and whether the component is repeatable, and renders a structured README template with standard sections prefilled plus placeholder comments for the parts that need human authoring.

### Component doc update usage

From the `tools/af_component_doc_update` directory:

```bash
uv run af-component-doc-update ~/code/af-component-fastapi-backend
```

This writes `README.generated.md` into the target component repository. The output includes:

- Header with badges (version, license) and links.
- Quick start (`dr component add` and `uvx copier copy` commands).
- Component dependencies table (required and collaborates-with), populated from `copier-module.yaml`.
- Section scaffolding with inline authoring guidance for: prerequisites, local development, troubleshooting, next steps, and contributing.

The `[[INSERT ... HERE]]` placeholders and comment blocks guide what to write in each section. Delete the comments once the section is filled in.
