# App Framework documentation

## Overview

This specification defines how documentation and agent skills should be organized, distributed, and maintained within DataRobot App Framework components. The core principle is that documentation and skills should live closest to the component they describe, enabling offline usage, ensuring consistency, and providing both human and LLM-friendly access to information.

## Motivation

### Documentation distribution
- **Offline-first**&mdash;Components must be usable without internet connectivity.
- **Self-contained**&mdash;Templates and apps should include all necessary documentation.
- **LLM-friendly**&mdash;Documentation must be structured for both human readers and AI agents.
- **Consistency**&mdash;Location and format should be standardized across all components.

### Skills distribution
- **Component-specific knowledge**&mdash;The unique capabilities of each component should be discoverable by AI agents.
- **Institutional knowledge**&mdash;Skills capture patterns and practices that don't exist in LLM training data.
- **Portability**&mdash;Skills should work across multiple agent frameworks until standards emerge.
- **Reusability**&mdash;General skills should be shared across the ecosystem.

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
├── .skills/                       # Component skills (see below)
└── ...
```

### Naming convention

**Single-file documentation:**
- Format: `docs/<component-name>.md`
- Example: `docs/react.md`, `docs/llm.md`

**Multifile documentation:**
- Format: `docs/<component-name>/README.md` (plus additional files)
- Example: `docs/agent/README.md`, `docs/agent/crewai.md`

This convention prevents collisions similar to the existing `infra/infra` and `infra/configurations` folder structure.

### Documentation requirements

All component documentation must be:

1. **Comprehensive**&mdash;Cover all aspects of the component including:
   - Purpose and use cases.
   - Installation and setup.
   - Configuration options.
   - Usage examples including common use cases and extensions.
   - Troubleshooting.
   - Best practices.

2. **LLM-friendly**&mdash;To be LLM-consumable, include:
   - Clear section headers.
   - Code examples with context.
   - Explicit prerequisites.
   - Common patterns and anti-patterns.
   - Links to related components.

3. **Maintainable&mdash;To ensure accuracy, be sure the component documentation is:**
   - Version-controlled alongside component code.
   - Updated with component changes.
   - Reviewed as part of a PR process.

## Documentation compilation

The [base component](../components/base.md) adds a Taskfile that creates a table of contents by compiling all `docs` items at the file level. Use descriptive file names for components that have multiple markdown documents.

## Skills distribution

See [Skills](../skills.md) for an overview of the skill system and how to use skills in App Framework applications.

### File organization

Each component bundles its skills in a `.skills` folder within the template:

```
template/
├── .skills/
│   ├── datarobot-app-framework-cicd/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── examples/
│   ├── datarobot-app-framework-react-testing/
│   │   └── SKILL.md
│   └── datarobot-app-framework-fastapi-backend-debugging/
│       └── SKILL.md
├── .claude/
│   └── skills/                    # Symlinks to .skills/*
├── .agents/
│   └── skills/                    # Symlinks to .skills/*
└── docs/
```

The [base component](../components/base.md) provides the symlinks to `.claude/skills` and `.agents/skills` directly, so **do not** do that in your component.

### Naming convention

Skills must follow this naming pattern:

**Format:** `datarobot-app-framework-<component>-<skill>`

**Examples:**
- `datarobot-app-framework-custom-model-deployment`
- `datarobot-app-framework-streamlit-debugging`
- `datarobot-app-framework-react-testing`

**Special case&mdash;Base component:**
When the skill is in the base component and applies generally, omit the component name:
- `datarobot-app-framework-cicd` (not `datarobot-app-framework-base-cicd`)
- `datarobot-app-framework-configuration`

### Global skills repository

Skills that are general to all app components must:

1. **Exist in both locations:**
   - `af-component-base/.skills/` (for template distribution).
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

1. **Be human-authored**&mdash;LLM-generated skills are prohibited (see [research](https://arxiv.org/abs/2602.11988)).
2. **Include comprehensive descriptions**&mdash;Prompt "when should I use this?" not just "what does this do?".
3. **Provide working examples**&mdash;Use real code that executes successfully.
4. **Document dependencies**&mdash;Describe external tools, environment variables, and prerequisites.
5. **Specify context costs**&mdash;Provide estimated token usage and context window requirements.

## Implementation guidelines

### For component authors

When creating a new component:

1. Create `docs/<component-name>.md` or `docs/<component-name>/README.md`.
2. Write comprehensive documentation covering all requirements.
3. Create `.skills/<skill-name>/` for each component-specific capability.
4. Ensure skill names follow the naming convention.
5. Add documentation compilation tasks to `docs/Taskfile.yml`.
6. Test that symlinks work correctly in `.claude/skills/` and `.agents/skills/`.

## See also

- [Components](../components/index.md)&mdash;Available App Framework components.
- [Skills](../skills.md)&mdash;Overview of the skill system and available skills.
- [Component model](./component-model.md)&mdash;Description of how App Framework components are structured and updated.
- [Design principles](./principles.md)&mdash;Guiding principles behind App Framework design.
