# Create a new component

This guide walks you through creating a custom App Framework component from the [scaffold template](https://github.com/datarobot-community/scaffold-af-component). It covers the basics common to all components and then shows patterns for three component types: a Python application, an agentic workflow, and a TypeScript frontend.

## What is a component

At its core, a component is a [Copier](https://copier.readthedocs.io/) template with a small set of required files:

| File | Purpose |
|------|---------|
| `copier.yml` | Defines the questions Copier asks and template configuration. |
| `copier-module.yaml` | Declares the component name, description, and dependencies. |
| `template/docs/{{name}}.md.jinja` | User-facing documentation for the component. |
| `template/infra/infra/{{name}}.py.jinja` | Pulumi infrastructure code that provisions DataRobot resources. |

The infrastructure file is technically optional&mdash;components deeper in the dependency graph (like the React frontend, which delegates resource creation to the FastAPI component it depends on) may not need one. But most components provision at least one DataRobot resource.

Everything beyond these files&mdash;application code directories, Taskfiles, CLI configs, skills&mdash;is added based on what your component actually does.

## Prerequisites

- A GitHub account.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
- Familiarity with [Copier](https://copier.readthedocs.io/) templates and [Jinja2](https://jinja.palletsprojects.com/) syntax.

## Step 1: Create your repository

1. Go to [scaffold-af-component](https://github.com/datarobot-community/scaffold-af-component) and click **Use this template** → **Create a new repository**.
2. Name it `af-component-YOUR_COMPONENT` (e.g. `af-component-dashboard`).
3. Clone it locally:

```bash
git clone git@github.com:YOUR_ORG/af-component-YOUR_COMPONENT.git
cd af-component-YOUR_COMPONENT
```

## Step 2: Define your component identity

Edit `copier-module.yaml` to declare the component name, description, and dependencies:

```yaml
module: af-component-your-component
short_description: "Adds a dashboard deployed as a DataRobot Custom Application"
repeatable: true
depends_on:
  base:
    url: https://github.com/datarobot-community/af-component-base
```

All components must depend on `base`. Add additional entries if your component requires others&mdash;for example, the [agent component](https://github.com/datarobot-community/af-component-agent) declares dependencies on `llm` and `mcp`:

```yaml
depends_on:
  base:
    url: https://github.com/datarobot-community/af-component-base
  llm:
    url: https://github.com/datarobot-community/af-component-llm
    repeatable: true
```

## Step 3: Configure questions

Edit `copier.yml` to define the interactive prompts users see when applying your component. At minimum, keep the app name question and the base answers loader:

```yaml
component_app_name:
  type: str
  default: "myapp"
  help: "The name/folder for this component."

# Hidden derived variable for Python-safe file names
component_app_name_file:
  type: str
  default: "{{component_app_name|lower|replace('-','_')}}"
  when: false

base_answers_file:
  type: str
  default: ".datarobot/answers/base.yml"
  help: "Path to the base component answers file"

_external_data:
  base: "{{ base_answers_file }}"

_subdirectory: template
_answers_file: ".datarobot/answers/component-{{ component_app_name }}.yml"
```

Add component-specific questions as needed. See the [Copier question docs](https://copier.readthedocs.io/en/stable/configuring/#questions) for the full syntax.

## Step 4: Build the template directory

The `template/` directory contains everything that gets copied into the user project. The scaffold starts with:

```
template/
├── docs/
│   └── {{component_app_name}}.md.jinja      # Component documentation
└── infra/
    └── infra/
        └── {{component_app_name_file}}.py.jinja  # Pulumi infrastructure
```

Use `{{ variable }}` in file and directory names for path templating. Files ending in `.jinja` have the suffix stripped after rendering. Use `.jinja.jinja` for files that should retain Jinja syntax at runtime (e.g. `metadata.yaml`).

### Adding an application directory

If your component deploys a runnable application, add a `{{component_app_name}}/` directory. This is where application code, build scripts, tests, and a `Taskfile` live. The three examples below show what this looks like in practice.

---

## Example: Python Custom Application (FastAPI)

The [af-component-fastapi-backend](https://github.com/datarobot-community/af-component-fastapi-backend) deploys a [FastAPI](https://fastapi.tiangolo.com/) server as a DataRobot Custom Application.

### Questions (`copier.yml`)

```yaml
fastapi_app_name:
  type: str
  default: "web"
  help: "The name/folder of your FastAPI Web App."

fastapi_local_port:
  type: int
  default: "8080"
  help: "The port to run this FastAPI Web App"
```

### Template structure

```
template/
├── {{fastapi_app_name}}/
│   ├── app/                          # FastAPI application code
│   │   ├── __init__.py.jinja
│   │   ├── main.py
│   │   └── config.py
    ├── build-app.sh                  # Build script for Custom App packaging.
    ├── start-app.sh                  # Entrypoint for the Custom App runtime.
│   ├── metadata.yaml.jinja.jinja     # Runtime parameter definitions.
│   ├── pyproject.toml.jinja          # Python dependencies (managed by uv).
│   └── Taskfile.yaml.jinja           # Dev tasks: install, dev, lint, test.
├── .datarobot/cli/{{fastapi_app_name}}.yaml  # CLI config (secrets, env vars).
└── infra/infra/{{fastapi_app_name_file}}.py.jinja  # Pulumi resources.
```

### Infrastructure (`infra/infra/`)

The Pulumi module creates an `ApplicationSource` and `CustomApplication` using the [pulumi-datarobot provider](https://www.pulumi.com/registry/packages/datarobot/):

```python
import pulumi_datarobot

app_source = pulumi_datarobot.ApplicationSource(
    f"{PROJECT_NAME} Application Source",
    files=get_app_files(runtime_parameter_values),
    runtime_parameter_values=runtime_parameter_values,
)

app = pulumi_datarobot.CustomApplication(
    f"{PROJECT_NAME} Application",
    source_id=app_source.id,
    use_case_ids=[use_case.id],
)
```

### CLI config (`.datarobot/cli/`)

Define runtime secrets and environment variables that the `dr` CLI manages:

```yaml
root:
  - env: SESSION_SECRET_KEY
    type: secret_string
    generate: true
    help: "Secret key used to sign session cookies."
```

### Taskfile

Provide `install`, `dev`, `lint`, and `test` tasks using [uv](https://docs.astral.sh/uv/) and [Taskfile](https://taskfile.dev/):

```yaml
tasks:
  install:
    cmds:
      - uv sync --all-extras --dev
  dev:
    cmds:
      - uv run uvicorn app.main:app --host 0.0.0.0 --port {{ fastapi_local_port }} --reload
  lint:
    cmds:
      - uv run ruff format .
      - uv run ruff check . --fix
      - uv run mypy --pretty .
```

---

## Example: agentic workflow

The [af-component-agent](https://github.com/datarobot-community/af-component-agent) deploys an AI agent as a DataRobot Custom Model Deployment.

### Additional dependencies

The agent component depends on `llm` and `mcp` components, so its `copier-module.yaml` declares those in `depends_on`. The `copier.yml` loads their answers:

```yaml
_external_data:
  base: "{{ base_answers_file }}"
  llm: "{{ llm_answers_file }}"
  mcp: "{{ mcp_answers_file }}"
```

### Framework choice question

The agent lets users pick a framework at apply time:

```yaml
agent_template_framework:
  type: str
  default: base
  help: "Choose the agentic framework template to start with:"
  choices:
    Base: base
    CrewAI: crewai
    LangGraph: langgraph
    LlamaIndex: llamaindex
```

### Infrastructure pattern

Instead of a `CustomApplication`, the agent creates a `CustomModelDeployment`&mdash;a model endpoint rather than a web app:

```python
from datarobot_pulumi_utils.pulumi.custom_model_deployment import CustomModelDeployment

agent_deployment = CustomModelDeployment(
    name=f"{PROJECT_NAME} Agent",
    source_path=agent_application_path,
    target_type="TextGeneration",
    ...
)
```

### Template structure

```
template/
├── {{agent_app_name}}/
│   ├── code/                    # Agent implementation code.
│   ├── pyproject.toml.jinja
│   └── Taskfile.yml.jinja
├── .datarobot/cli/{{agent_app_name}}.yaml.jinja
├── .skills/                     # AI coding assistant skills.
└── infra/infra/{{agent_app_name_file}}.py.jinja
```

---

## Example: TypeScript frontend (React)

The [af-component-react](https://github.com/datarobot-community/af-component-react) adds a [React](https://react.dev/) + [Vite](https://vite.dev/) frontend that pairs with a FastAPI backend. It depends on `fastapi-backend`:

```yaml
# copier-module.yaml
depends_on:
  base:
    url: https://github.com/datarobot-community/af-component-base
  fastapi-backend:
    url: https://github.com/datarobot-community/af-component-fastapi-backend
```

### Cross-component references

It loads the FastAPI answers to reference the backend configuration:

```yaml
# copier.yml
fastapi_answers_file:
  type: str
  default: ".datarobot/answers/fastapi-web.yml"
  help: "Path to the FastAPI answers file you want to pair with this frontend"

_external_data:
  base: "{{ base_answers_file }}"
  fastapi: "{{ fastapi_answers_file }}"
```

### Infrastructure pattern

The React component doesn't create its own DataRobot resource&mdash;it builds the frontend and the FastAPI component serves the output. The Pulumi module runs `npm install && npm run build` via a `pulumi_command.local.Command`:

```python
import pulumi_command as command

build_react_app = command.local.Command(
    f"{PROJECT_NAME} Build Frontend",
    create=f"cd {frontend_dir} && npm install && npm run build",
    triggers=[source_hash],  # Rebuild only when source files change
)
```

### Template structure

```
template/
├── {{react_app_name}}/
│   ├── src/                     # React source code.
│   ├── public/                  # Static assets.
│   ├── package.json.jinja
│   ├── vite.config.ts.jinja
│   ├── tsconfig.json
│   └── Taskfile.yaml            # npm-based tasks (no .jinja needed).
└── infra/infra/{{ react_app_name }}.py.jinja
```

### Taskfile (npm-based)

TypeScript components use `npm` instead of `uv`.

```yaml
tasks:
  install:
    cmds: [npm install]
  dev:
    cmds: [npm run dev]
  lint:
    cmds: [npm run lint:fix]
  test:
    cmds: [npm run test]
  build:
    cmds: [npm run build]
```

---

## Step 5: Add documentation

Create documentation files in `template/docs/`. Every component must include documentation that covers purpose, configuration, usage, and troubleshooting. See the [documentation specification](../design/documentation.md) for requirements.

## Step 6: Test your component

The scaffold provides two test modes:

```bash
# Quick render — no dependency resolution.
task copy

# Full validation — resolves dependencies like CI does.
task validate
```

The included [GitHub Actions workflow](https://github.com/datarobot-oss/copier-template-validator) runs `validate` on every push and PR that touches `template/`.

## Step 7: Publish

1. Push to GitHub as `af-component-YOUR_COMPONENT`.
2. Tag releases with [semantic versioning](https://semver.org/).
3. Users apply it with:

```bash
dr component add https://github.com/YOUR_ORG/af-component-YOUR_COMPONENT .
```

## Further reading

- [Component Model](../design/component-model.md)&mdash;how components are structured and composed.
- [Components overview](../components/index.md)&mdash;existing components.
- [Working with Copier](working-with-copier.md)&mdash;tips for Copier-based workflows.
- [Copier documentation](https://copier.readthedocs.io/)&mdash;template engine reference.
- [Pulumi DataRobot provider](https://www.pulumi.com/registry/packages/datarobot/)&mdash;infrastructure resources.
- [DataRobot documentation](https://docs.datarobot.com/)&mdash;platform docs.
