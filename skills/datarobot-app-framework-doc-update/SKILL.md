---
name: datarobot-app-framework-doc-update
description: Generate and intelligently merge README documentation for a DataRobot App Framework component using its copier-module.yaml schema.
---

# datarobot-app-framework-doc-update

Generate and merge README documentation for an App Framework component. The tool produces a structured scaffold (`README.generated.md`) from the component's `copier-module.yaml`; the skill then merges it with the existing `README.md`, preserving all human-written content.

## Trigger conditions

Use this skill when the user:
- Wants to update, regenerate, or scaffold a README for an `af-component-*` repo
- Mentions `copier-module.yaml` in relation to documentation
- Asks to "update the component docs" or "generate the component README"
- Has a component repo and wants its README to match the standard template

## Prerequisites

```bash
# Ensure the repo has a copier-module.yaml at its root.
# The tool will error clearly if it is missing.
```

## Steps

### Step 1 — Run the generator tool

Run this command against the component repo to produce `README.generated.md`:

```bash
uvx --from "git+https://github.com/datarobot-community/app-framework-studio#subdirectory=tools/af_component_doc_update" af-component-doc-update <repo_path>
```

If working from a local clone of `app-framework-studio` (use this for branch testing before pushing):

```bash
# Run from the app-framework-studio workspace root
cd <path-to-app-framework-studio>
uv run --project tools/af_component_doc_update af-component-doc-update <repo_path>
```

The tool will write `README.generated.md` alongside `README.md` in `<repo_path>`.

### Step 2 — Read both files

Read the full contents of:
- `<repo_path>/README.generated.md` — the new structural scaffold
- `<repo_path>/README.md` — the existing README (may be empty, minimal, or fully written)

### Step 3 — Merge intelligently

Produce a single merged README using these rules:

**Structure source**: `README.generated.md` is authoritative for structure and section order. Use it as the skeleton.

**Content transplant**: For each section in `README.generated.md` that contains a `[[INSERT ... HERE]]` placeholder:
- Search `README.md` for the matching section (by heading).
- If the existing section has real human-written content (not just the `[[INSERT ... HERE]]` placeholder), transplant that content into the merged output.
- If the existing section is empty, has only placeholders, or does not exist, **write appropriate content for that section yourself** based on the component's context (module name, description, dependencies, and anything else visible in the repo). Do not leave any `[[INSERT ... HERE]]` placeholders in the final output — every section must be filled.

**Use the HTML comments as writing instructions**: `README.generated.md` contains HTML comments (`<!-- ... -->`) immediately after each `[[INSERT ... HERE]]` placeholder. These comments are structured authoring guidance — bullet points describing exactly what that section should cover, what tone to use, and what to include or omit. Treat them as your instructions when writing content for that section. Remove all HTML comments from the final `README.md` output — they are for the AI only, not for readers.

**No placeholders in final output**: The merged `README.md` must contain zero `[[INSERT ... HERE]]` strings and zero `<!-- ... -->` comment blocks. Verify this before writing.

**Auto-filled sections**: The following sections are always taken from `README.generated.md` because they are code-generated from `copier-module.yaml` — never override them with stale content from `README.md`:
- The HTML header block (logo, badges, links)
- The intro paragraph (`short_description`)
- "Quick start" `uvx copier copy` command block
- "Component dependencies" section (entire section)

**Preserve extra sections**: If `README.md` has sections that don't appear in `README.generated.md`, append them after the standard sections (before the `---` footer).

### Step 4 — Write merged README

Write the merged content to `<repo_path>/README.md`.

### Step 5 — Clean up

Delete `<repo_path>/README.generated.md`.

## Schema reference

`copier-module.yaml` fields used by the generator:

| Field | Required | Description |
|-------|----------|-------------|
| `module` | Yes | Component name, matches the GitHub repo name (e.g. `af-component-agent`) |
| `short_description` | Yes | One-line description shown below the header |
| `repeatable` | No | Whether this component can be applied multiple times |
| `depends_on` | No | Map of required component dependencies (name → url, ref[, repeatable]) |
| `collaborates_with` | No | Map of optional/peer component integrations (name → url, ref[, repeatable]) |

## Example `copier-module.yaml`

```yaml
module: af-component-agent
short_description: "The agent component"
repeatable: true
depends_on:
  llm:
    url: https://github.com/datarobot-community/af-component-llm
    ref: v11.7.1
collaborates_with:
  mcp:
    url: https://github.com/datarobot-community/af-component-fastmcp-server
    ref: main
    repeatable: true
```

## Notes

- All repos live under the `datarobot-community` GitHub org.
- The generator is pure code — no LLM calls. Only the merge step (this skill) uses AI judgment.
- If `copier-module.yaml` is missing from the repo, ask the user to add it before proceeding.
