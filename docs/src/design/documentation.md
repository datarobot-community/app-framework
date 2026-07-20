# App Framework documentation

## Overview

This specification defines how documentation and agent skills are organized, distributed, and maintained within DataRobot App Framework components. The core principle is that documentation and skills live closest to the component they describe, enabling offline usage, ensuring consistency, and providing both human and LLM-friendly access to information.

## Motivation

### Documentation distribution
- **Offline-first** — Components must be usable without internet connectivity.
- **Self-contained** — Templates and apps include all necessary documentation.
- **LLM-friendly** — Documentation is structured for both human readers and AI agents.
- **Consistency** — Location and format are standardized across all components.

### Skills distribution
- **Component-specific knowledge** — The unique capabilities of each component are discoverable by AI agents.
- **Institutional knowledge** — Skills capture patterns and practices that do not exist in LLM training data.
- **Portability** — Skills work across multiple agent frameworks until standards emerge.
- **Reusability** — General skills are shared across the ecosystem.

## Documentation structure

### File organization

Each component must create documentation files within the template's `docs` folder, following this convention:

```
template/
├── docs/
│   ├── react.md                    # Single-file component docs
│   ├── agent/              # Multifile component docs
│   │   ├── README.md
│   │   ├── deployment.md
│   │   └── troubleshooting.md
│   ├── llm.md
│   └── Taskfile.yml               # Documentation compilation tasks
├── .agents/skills/                # Component skills (see below)
└── ...
```

### Naming convention

**Single-file documentation**:
- Format: `docs/<component-name>.md`
- Example: `docs/react.md`, `docs/llm.md`

**Multifile documentation:**

Must have a README.md in the folder, and may or may not contain additional files.

- Format: `docs/<component-name>/README.md` (plus any additional files added to the folder)
- Example: `docs/custom-model/README.md`, `docs/custom-model/deployment.md`

This convention prevents collisions similar to the existing `infra/infra` and `infra/configurations` folder structure.

Additionally, it encourages deduplication of repeatable components. Specifically, when four agent components share different names, they overwrite the docs with the most recently updated version. For instance-specific documentation differences, use the multifile pattern and paths like `docs/agent/{{ agent_app_name }}.md` or `docs/agent/{{ agent_template_framework }}.md`.

### Documentation requirements

All component documentation must be:

1. **Comprehensive** — Cover all aspects of the component including:
   - Purpose and use cases.
   - Installation and setup.
   - Configuration options.
   - Usage examples including common integrations with other components, features, and platform amenities.
   - Troubleshooting.
   - Best practices.

2. **LLM-friendly** — To be LLM-consumable, include:
   - Clear section headers.
   - Code examples with context.
   - Explicit prerequisites.
   - Common patterns and anti-patterns.
   - Links to related components.

3. **Maintainable** — To ensure accuracy, component documentation must be:
   - Version-controlled alongside component code.
   - Updated with component changes.
   - Reviewed as part of a PR process.

## Documentation compilation

The [base component](../components/base.md) adds a Taskfile that creates a table of contents by compiling all `docs` items at the file level. Use descriptive file names for components that have multiple markdown documents.

## Skills distribution

See [Skills](../skills.md) for an overview of the skill system and how to use skills in App Framework applications.

### File organization

Each component bundles its skills in a `.agents/skills` folder within the template:

```
template/
├── .agents/
│   └── skills/
│       ├── datarobot-app-framework-cicd/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   └── examples/
│       ├── datarobot-app-framework-react-testing/
│       │   └── SKILL.md
│       └── datarobot-app-framework-fastapi-backend-debugging/
│           └── SKILL.md
├── .claude/
│   └── skills/                    # Symlinks to ../.agents/skills/*
└── docs/
```

`.agents/skills/` is the canonical, agent-agnostic location for component skills.
The [base component](../components/base.md) provides the `.claude/skills` symlinks to `.agents/skills/` directly, so **do not** add those symlinks in individual components.

### Naming convention

Skills must follow this naming pattern:

**Format:** `datarobot-app-framework-<component>-<skill>`

**Examples:**
- `datarobot-app-framework-custom-model-deployment`
- `datarobot-app-framework-streamlit-debugging`
- `datarobot-app-framework-react-testing`

**Special case — Base component:**
When the skill is in the base component and applies generally, omit the component name:
- `datarobot-app-framework-cicd` (not `datarobot-app-framework-base-cicd`)
- `datarobot-app-framework-configuration`

### Global skills repository

Skills that are general to all app components must:

1. **Exist in both locations:**
   - `af-component-base/.agents/skills/` (for template distribution).
   - [`datarobot-oss/datarobot-agent-skills`](https://github.com/datarobot-oss/datarobot-agent-skills) (for global discovery).

2. **Stay synchronized:**
   - Changes to general skills must be propagated to both the component and agent skills repositories.

   **Note:** Consider investigating automation such as git submodules or GitHub Actions to ensure synchronization.

3. **To contribute to the global skills repository, skills additions must:**
   - Pass evaluation tests.
   - Include comprehensive examples.
   - Document token costs and context requirements.

### Skill quality requirements

All skills must:

1. **Be human-authored** — LLM-generated skills are prohibited (see [research](https://arxiv.org/abs/2602.11988)).
2. **Include comprehensive descriptions** — Prompt "when should I use this?" not just "what does this do?".
3. **Provide working examples** — Use real code that executes successfully.
4. **Document dependencies** — Describe external tools, environment variables, and prerequisites.
5. **Specify context costs** — Provide estimated token usage and context window requirements.

## Writing style

Component README files and GitHub Markdown documentation must follow the DataRobot documentation style standards. The authoritative references are:

- [`documentation-style-spec.md`](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/documentation-style-spec.md) — entry point for App Framework READMEs: quick reference, checklist, and links to topic files.
- [`references/README.md`](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/references/README.md) — dictionary of every topic file with "when to read" guidance.
- [`references/`](https://github.com/datarobot-community/app-framework/tree/main/skills/datarobot-app-framework-doc-update/references) — one topic file per style guide section (voice, grammar, GitHub Markdown, and so on).
- [`datarobot-style-guide-github.md`](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/datarobot-style-guide-github.md) — index of the full DataRobot style guide for GitHub Markdown.

Use the [`datarobot-app-framework-doc-update`](https://github.com/datarobot-community/app-framework/tree/main/skills/datarobot-app-framework-doc-update) skill and the `af-component-doc-update` tool to scaffold and merge component README files from `copier-module.yaml`.

### Key style rules for component authors

- **Headings** — Sentence case; imperative verbs for procedural topics; no periods at the end of headings; intro text under every section.
- **Voice** — Never use *we* or *our*; prefer imperatives and neutral phrasing over *you can* / *you must* when clarity allows; present tense and active voice.
- **Lists** — Parallel structure; periods on complete sentences; Oxford comma; description lists use em dashes or run-in style (`**Term**. Description.`).
- **Placeholders** — `UPPERCASE_WITH_UNDERSCORES` in procedural text; `<camelCase>` in code samples; `{curlyBraces}` in REST API paths.
- **Code blocks** — Language tags on fenced blocks; no `$` prompt on single-line commands when ambiguous.
- **Callouts** — Blockquotes on GitHub (`> **Note:** …`); MkDocs admonitions (`!!! note`) on the docs site only.
- **Timeless language** — Avoid *currently*, *new*, *latest*, and similar time-anchor words in reference documentation.
- **Links** — Descriptive link text; include `.md` extension on repository-relative paths.

For the full rule set, see the style spec linked above.

## Implementation guidelines

### For component authors

When creating a new component:

1. Create `docs/<component-name>.md` or `docs/<component-name>/README.md`.
2. Write comprehensive documentation covering all requirements.
3. Create `.agents/skills/<skill-name>/` for each component-specific capability.
4. Ensure skill names follow the naming convention.
5. Add documentation compilation tasks to `docs/Taskfile.yml`.
6. Test that the base-provided symlinks resolve `.claude/skills/` to `.agents/skills/`.

## See also

- [Components](../components/index.md) — Available App Framework components.
- [Skills](../skills.md) — Overview of the skill system and available skills.
- [Component model](./component-model.md) — Description of how App Framework components are structured and updated.
- [Design principles](./principles.md) — Guiding principles behind App Framework design.
- [Documentation style spec](https://github.com/datarobot-community/app-framework/blob/main/skills/datarobot-app-framework-doc-update/documentation-style-spec.md) — Style standards for component README files.
