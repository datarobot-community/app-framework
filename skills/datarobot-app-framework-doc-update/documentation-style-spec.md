# Documentation Style Specification

Style standards for App Framework component READMEs and other GitHub Markdown documentation. Follow these rules when creating or updating documentation to ensure consistency with the DataRobot corporate style guide.

External references: [DataRobot design system](https://design-system.drdev.io/), [Google Developer Documentation Style Guide](https://developers.google.com/style).

## How to use this spec

This file is the entry point for the doc-update skill. It contains the quick-reference rules and README checklist agents need most often. For full rules, read the topic files in [`references/`](./references/).

Which reference files to load: See the [reference dictionary](./references/README.md) — it lists every topic file, what it covers, and when to read it. For every README merge, load the six-file default set from that dictionary; load additional files only when the section you are writing matches their "When to read" criteria.

For the complete style guide index, see [datarobot-style-guide-github.md](./datarobot-style-guide-github.md).

## Quick reference

### Headings

- ✅ Use sentence case: "Getting started", "Quick start guide"
- ❌ Avoid title case: "Getting Started", "Quick Start Guide"
- ✅ Use imperative verbs for procedural topics: "Install the CLI", "Configure authentication"
- ❌ Avoid gerunds in procedural headings: "Installing the CLI", "Configuring authentication"
- ❌ Do not end headings with periods
- Exception: Proper nouns remain capitalized (DataRobot, OAuth, PostgreSQL)
- One level-1 heading per document; do not skip heading levels

### Voice and tense

- ✅ Prefer imperative instructions: "Enable authentication before deploying.", "Run this command."
- ✅ Use neutral, factual phrasing: "The CLI provides authentication management."
- ❌ Never use first-person plural: "We provide", "Our CLI", "We're building"
- ❌ Minimize second person: avoid "You can…", "You must…", "You should…" when imperative or neutral phrasing works
- ✅ Use *you* or *your* only when removing them would be awkward, confusing, or overly complicated
- ✅ Use present tense: "The CLI provides", "This command generates"
- ❌ Avoid future tense unless emphasizing something that will happen later
- ✅ Use active voice: "The wizard guides the setup process."
- ❌ Avoid passive voice when active is clearer

### Words to avoid

- ❌ Please — drop; adds no information
- ❌ We / our — rephrase with *DataRobot* or a neutral subject
- ❌ Currently, now, new, latest, soon — see [timeless-documentation.md](./references/timeless-documentation.md)
- ❌ Should — state definite behavior instead
- ❌ Simply, It's easy, quickly — filler that adds no value
- ❌ Exclamation points, emojis, and internet slang

### Abbreviations

- ✅ Prefer *that is* and *for example* over *i.e.* and *e.g.*
- ✅ When *i.e.* or *e.g.* appear in non-code prose, follow with a comma: (e.g., `prod`), (i.e., timeouts)
- ❌ Omit the comma after *i.e.* or *e.g.* in prose: (e.g. `prod`), (i.e. timeouts)
- Exception: inside code blocks, inline code, or literal strings, follow the code convention

### Lists

Two valid description-list styles:

Run-in style (preferred for glossary-style lists):

```markdown
- **Authentication**. Manage DataRobot credentials.
- **Templates**. Clone and configure applications.
```

Em dash style (valid for CLI-style docs):

```markdown
- **Authentication** — manage DataRobot credentials.
- **Templates** — clone and configure applications.
```

General list rules:

- ✅ Start items with a capital letter
- ✅ Add periods to complete sentences and items with verbs
- ❌ Omit periods for single words, code-only items, or link/title-only items
- ✅ Keep items parallel in structure within a list
- ✅ Use numbered lists for ordered steps; bulleted lists for unordered items
- ✅ Use the Oxford comma in lists of three or more items
- ✅ Put the colon outside bold labels: `- **Authentication**: Manage credentials.`
- ❌ Do not bold the colon: `- **Authentication:** Manage credentials.`

### Contractions

- ✅ Allowed in technical documentation: negation contractions (isn't, don't, won't, can't)
- ❌ Avoid noun+verb possessive contractions: browser's → browser is; template's → the template configuration
- ❌ Do not use we're or other first-person contractions (never use we)
- ✅ Prefer positive phrasing over negative contractions when both work

### Placeholders

| Context | Format | Example |
|---------|--------|---------|
| Inline or procedural text | `UPPERCASE_WITH_UNDERSCORES` | `TEMPLATE_NAME`, `DATABASE_URL` |
| Code samples (general) | `<camelCase>` angle brackets | `<modelId>` |
| REST API / OpenAPI endpoints | `{curlyBraces}` | `{projectId}` |

Explain placeholders on first use.

### Command examples

- ✅ Single-line commands: `dr auth login` (no prompt symbol when `$` could be confused with environment variables)
- ✅ Multi-line terminal sessions: `$` prompt is acceptable for consistency
- ✅ Multi-line scripts: include `# Comments with periods.`
- ✅ Use fenced code blocks with a language tag (`bash`, `python`, `json`, etc.)

### Tone

- ✅ Conversational and direct without being frivolous
- ✅ Use imperative mood for instructions
- ✅ Write for a global, technically proficient audience
- ❌ Avoid idioms, slang, culturally specific humor, and directional language (above, below)
- ❌ Do not attribute human qualities to software (The service sees… → The service detects…)

### GitHub Markdown callouts

GitHub does not support MkDocs admonitions. Use blockquotes:

```markdown
> **Note**: Useful but non-required information.

> **Warning**: This action cannot be undone.

> **Important**: Back up the configuration before proceeding.
```

Capitalize the callout type, use a colon, and end with a period.

## Reference index

Each file in [`references/`](./references/) covers one topic from the full DataRobot style guide. For when to read each file, see the [reference dictionary](./references/README.md).

| Reference | Summary |
|-----------|---------|
| [purpose-and-voice.md](./references/purpose-and-voice.md) | Brand voice, audience assumptions, documentation voice |
| [grammar-and-punctuation.md](./references/grammar-and-punctuation.md) | Sentence case, periods, abbreviations, pronouns, contractions, voice/tense, person rules |
| [capitalization-and-proper-nouns.md](./references/capitalization-and-proper-nouns.md) | Brand names, DataRobot proper nouns, technical terms, API field names |
| [words-to-avoid.md](./references/words-to-avoid.md) | Universal and UI-specific banned words and phrases |
| [ui-copy.md](./references/ui-copy.md) | Buttons, inputs, validation, tables, modals, empty states |
| [api-and-sdk-documentation.md](./references/api-and-sdk-documentation.md) | API descriptions, parameters, changelog conventions |
| [error-messages.md](./references/error-messages.md) | Error message structure and wording |
| [technical-documentation.md](./references/technical-documentation.md) | Headings, lists, procedures, UI elements, links, code, tables, images |
| [accessibility-and-inclusive-documentation.md](./references/accessibility-and-inclusive-documentation.md) | Semantic structure, inclusive language, screen reader considerations |
| [timeless-documentation.md](./references/timeless-documentation.md) | Avoid time-anchor words in reference documentation |
| [anthropomorphism.md](./references/anthropomorphism.md) | Do not attribute human qualities to software |
| [code-in-text.md](./references/code-in-text.md) | When to use code font; method names; inflection rules |
| [formatting-conventions.md](./references/formatting-conventions.md) | Dates, times, numbers, units, file formats, default names |
| [standard-terminology.md](./references/standard-terminology.md) | Action vocabulary, data terms, standardized product terms |
| [content-best-practices.md](./references/content-best-practices.md) | Minimum viable content, scannability, local consistency |
| [github-markdown-authoring.md](./references/github-markdown-authoring.md) | GFM features, callouts, structure, diagrams, reusable content |
| [platform-and-deployment-terminology.md](./references/platform-and-deployment-terminology.md) | Workbench, Console, Registry, platform naming |
| [release-notes-and-announcements.md](./references/release-notes-and-announcements.md) | Version notes, feature summaries, issue-fix wording |
| [quick-reference.md](./references/quick-reference.md) | Context-to-section index for common authoring tasks |
| [appendix-google-alignment-gaps.md](./references/appendix-google-alignment-gaps.md) | Intentional divergences from the Google style guide |
| [document-history.md](./references/document-history.md) | Style guide change log |

## App Framework README checklist

When updating component documentation, verify these elements:

- [ ] Sentence-case headings with intro text under every section
- [ ] No `[[INSERT … HERE]]` placeholders or HTML comment instructions in final output
- [ ] Imperative or neutral voice — no we / our; minimal you / your
- [ ] Present tense, active voice
- [ ] Lists use consistent punctuation and parallel structure
- [ ] Non-code *i.e.*/*e.g.* use a trailing comma
- [ ] Bold labels use a colon outside the bold span
- [ ] Placeholders use `UPPERCASE_WITH_UNDERSCORES` in procedural text
- [ ] Code blocks have language tags; single-line commands omit `$` when ambiguous
- [ ] Links use descriptive text and `.md` extensions for repo-relative paths
- [ ] Callouts use blockquote syntax, not MkDocs admonitions
- [ ] Timeless language (no currently, new, latest)
- [ ] Component dependencies section matches `copier-module.yaml` (auto-generated; do not override)

## Verification process

1. Check all headings use sentence case and have intro text
2. Verify voice: no we / our; imperatives preferred over you can / you must
3. Confirm present tense and active voice
4. Verify lists use correct punctuation and parallel structure
5. Confirm non-code *i.e.*/*e.g.* use a trailing comma
6. Confirm bold labels place the colon outside the bold span
7. Check placeholders use the correct format for context
8. Confirm no noun possessive contractions
9. Verify command examples and code blocks follow GitHub Markdown conventions
10. Confirm timeless language (except in release notes)
11. Check callouts use blockquote format

## Version history

| Date | Change |
|------|--------|
| 2026-08-18 | Require trailing commas after non-code *i.e.*/*e.g.*; require colons outside bold spans in description lists and callouts. |
| 2026-07-20 | Added [reference dictionary](./references/README.md) with per-file "when to read" guidance for README merges. |
| 2026-07-17 | Split authoritative guide into [`references/`](./references/) topic files; this spec is now a slim entry point with quick reference and README checklist. |
| 2026-06-23 | Aligned with DataRobot GitHub style guide: voice/person rules, contractions, GitHub Markdown callouts, timeless docs, accessibility, placeholder formats, and link conventions. |
| 2025-10-24 | Initial specification created based on DataRobot corporate style guide review. |
