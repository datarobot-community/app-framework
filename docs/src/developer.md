# Developer guide

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Task](https://taskfile.dev/installation/)

### Install Task

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

This will install dependencies and start a local server at [http://localhost:8000](http://localhost:8000). The site reloads automatically as you edit files in the `docs/` directory.
