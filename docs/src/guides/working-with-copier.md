# Working with Copier

The App Framework component system is built on [Copier](https://copier.readthedocs.io/en/stable/), a project templating tool with built-in Git-based update semantics. Copier is what makes it possible to apply a component once, answer a few questions, and then receive upstream improvements automatically as the component evolves.

The [DataRobot CLI](https://cli.datarobot.com/dev-docs/commands/component-managed-updates/) wraps Copier behind `dr component add` and `dr component update`, so you rarely need to interact with Copier directly. When you do, this guide explains the concepts and commands you need.

## How answers files work

Every time you apply a component, Copier records your answers in a YAML file inside `.datarobot/answers/`. Each component gets its own file:

| Component | Answers file |
|-----------|-------------|
| base | `.datarobot/answers/base.yml` |
| llm | `.datarobot/answers/llm-NAME.yml` |
| fastapi-backend | `.datarobot/answers/fastapi-NAME.yml` |
| react | `.datarobot/answers/react-NAME.yml` |
| agent | `.datarobot/answers/agent-NAME.yml` |
| datarobot-mcp | `.datarobot/answers/datarobot-mcp.yml` |

These files contain the choices you made during the wizard plus internal metadata (`_src_path` and `_commit`) that Copier uses to track which template version produced your current project. Together, they enable automated updates at the component-instance level. See the [Copier answers file documentation](https://copier.readthedocs.io/en/stable/configuring/#the-copier-answersyml-file) for details on the file format.

!!! warning

    Do not edit answers files by hand. The Copier update algorithm relies on the answers file accurately reflecting the state that produced the current project files. Manual edits break that assumption and lead to unpredictable merge behavior. See [why manual edits are unsupported](https://copier.readthedocs.io/en/stable/updating/#never-change-the-answers-file-manually) in the Copier documentation.

## Changing answers after initial apply

If you gave a wrong answer or want to change a choice after applying a component, there are two supported approaches. Both use the [DataRobot CLI `component update`](https://cli.datarobot.com/dev-docs/commands/component-managed-updates/) or the Copier `update` command directly.

### Re-answer interactively

Run `copier update` without the `-A` (skip-answered) flag so that Copier re-prompts every question, defaulting to your previous answers. Change whichever answers you need:

```bash
uvx copier update -a .datarobot/answers/COMPONENT.yml .
```

Replace `COMPONENT.yml` with the actual answers file, for example `agent-myagent.yml`.

### Change a single answer non-interactively

Use the `--data` flag to override one answer while keeping all others. The `--defaults` flag accepts the previous answers for every question you don't override:

```bash
uvx copier update -a .datarobot/answers/COMPONENT.yml --defaults --data KEY=VALUE .
```

To change answers without also upgrading to a newer template version, pin the current version with `--vcs-ref=:current:`:

```bash
uvx copier update -a .datarobot/answers/COMPONENT.yml --defaults --data KEY=VALUE --vcs-ref=:current: .
```

See the [Copier update documentation](https://copier.readthedocs.io/en/stable/updating/) for the full list of flags, including `--data-file` for passing multiple overrides from a YAML file.

## Recovering from wrong answers

A common scenario: you applied the [agent](../components/agent.md) component and chose `nat` (NeMo Agent Toolkit) when you meant to choose `langgraph`. There is no generated code worth keeping yet and you need to switch frameworks.

### Option 1: Re-run interactively (preferred)

Re-run the update interactively and pick the correct framework when prompted:

```bash
uvx copier update -a .datarobot/answers/agent-myagent.yml .
```

Copier applies a three-way merge: it regenerates the old template output, diffs it against your current project, applies the new template, and re-applies your project-specific changes. Review the result with `git diff` and commit the result.

### Option 2: Override with `--data`

If you know the exact key to change, skip the interactive prompts:

```bash
uvx copier update -a .datarobot/answers/agent-myagent.yml --defaults --data agent_framework=langgraph .
```

### Option 3: Clean slate

When the answer change is so large that the generated file set is entirely different — as it is when switching agent frameworks — it can be simpler to remove the component and re-apply from scratch:

```bash
rm -rf agent/ .datarobot/answers/agent-myagent.yml
dr component add https://github.com/datarobot-community/af-component-agent .
```

After any recovery path, review `git diff`, resolve any conflicts, and commit the result.

## What happens during an update

When you run `dr component update` or `copier update`, Copier performs a [three-way merge](https://copier.readthedocs.io/en/stable/updating/#how-the-update-works):

1. It regenerates a fresh copy of the project using the **old** template version and your recorded answers.
2. It computes the diff between that fresh copy and your **current** project (capturing your local changes).
3. It generates a fresh copy from the **new** template version.
4. It applies the diff from step 2 on top of the new copy.

If a hunk cannot be applied cleanly, Copier creates a conflict. The default mode (`--conflict inline`) adds inline conflict markers. You can also use `--conflict rej` to get separate `.rej` files.

Files you intentionally deleted from your project are [not regenerated during updates](https://copier.readthedocs.io/en/stable/updating/#handling-of-deleted-paths). If you need to bring a deleted file back, use `copier recopy`.

### When updates break: `copier recopy`

If the update algorithm itself fails — for example, because the old template version is no longer available — you can fall back to [`copier recopy`](https://copier.readthedocs.io/en/stable/generating/#regenerating-a-project). This discards all project evolution and re-applies the template as if it were the first time, while keeping your answers. It is a [last resort](https://copier.readthedocs.io/en/stable/updating/#recover-from-a-broken-update):

```bash
uvx copier recopy -a .datarobot/answers/COMPONENT.yml .
```

Review the result carefully, because any local modifications to template-managed files will be overwritten.
