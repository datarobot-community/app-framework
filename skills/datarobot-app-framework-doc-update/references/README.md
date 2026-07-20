# Style guide reference dictionary

Each file in this folder covers one topic from the DataRobot GitHub Markdown style guide. Use this dictionary to decide which files to load — do not read the entire folder unless the task spans multiple content types.

**Entry points**:

- [`documentation-style-spec.md`](../documentation-style-spec.md) — quick reference and README checklist (read first).
- [`datarobot-style-guide-github.md`](../datarobot-style-guide-github.md) — full style guide index.

## Default set (every App Framework README merge)

Read these six files for every component README merge, in addition to `documentation-style-spec.md`:

| File | What it covers | When to read |
|------|----------------|--------------|
| [grammar-and-punctuation.md](./grammar-and-punctuation.md) | Sentence case, periods, abbreviations, pronouns, contractions, voice, tense, person (we / you) | Always — applies to every heading, sentence, and list in the README. |
| [words-to-avoid.md](./words-to-avoid.md) | Banned words and tone constraints (please, we, should, filler) | Always — scan merged output for banned words before writing. |
| [technical-documentation.md](./technical-documentation.md) | Headings, lists, procedures, links, tables, code blocks, images | Always — READMEs are technical documentation; this is the primary structural guide. |
| [github-markdown-authoring.md](./github-markdown-authoring.md) | GFM features, blockquote callouts, fences, collapsible sections | Always — READMEs render on GitHub; use GFM conventions, not MkDocs syntax. |
| [code-in-text.md](./code-in-text.md) | Inline code, method names, placeholder formats, command examples | Always — component READMEs include install commands, config paths, and code samples. |
| [timeless-documentation.md](./timeless-documentation.md) | Avoid time-anchor words (currently, new, latest) | Always — READMEs are reference documentation, not release notes. |

## Load on demand (by README section or content type)

Read these files only when the section you are writing matches the "When to read" criteria. Skip files that do not apply to the current README.

| File | What it covers | When to read |
|------|----------------|--------------|
| [purpose-and-voice.md](./purpose-and-voice.md) | Brand voice, audience assumptions, documentation voice | Writing or rewriting the project overview, scope statement, or audience orientation — especially when tone feels too casual or too stiff. |
| [capitalization-and-proper-nouns.md](./capitalization-and-proper-nouns.md) | Brand names, DataRobot proper nouns, technical terms, API field names in prose | Mentioning DataRobot products (Autopilot, AI Catalog, Workbench), vendor names (OAuth, PostgreSQL), or API identifiers. |
| [ui-copy.md](./ui-copy.md) | Buttons, inputs, validation, tables, modals, empty states | Documenting UI interactions the component exposes — button labels, form fields, validation messages, or table column names. Rare for component READMEs. |
| [api-and-sdk-documentation.md](./api-and-sdk-documentation.md) | API descriptions, parameters, changelog conventions | Documenting REST endpoints, SDK methods, or parameter tables in the README. |
| [error-messages.md](./error-messages.md) | Error message structure and wording | Documenting error scenarios, troubleshooting steps, or example error output. |
| [accessibility-and-inclusive-documentation.md](./accessibility-and-inclusive-documentation.md) | Semantic structure, inclusive language, screen reader considerations | Adding images (alt text required), writing for a global audience, or choosing inclusive terminology. |
| [anthropomorphism.md](./anthropomorphism.md) | Do not attribute human qualities to software | Describing what the component or service does — avoid verbs like sees, knows, tells. |
| [formatting-conventions.md](./formatting-conventions.md) | Dates, times, numbers, units, file formats, default names | Including dates, version numbers, file size limits, or file format names (CSV, JSON) in prose. |
| [standard-terminology.md](./standard-terminology.md) | Action vocabulary, data terms, standardized product terms | Choosing verbs for user actions (Create vs Add vs Generate) or data concepts (dataset vs data source). |
| [content-best-practices.md](./content-best-practices.md) | Minimum viable content, scannability, local consistency | A section is too long, dense, or repetitive — restructure for scanning without losing information. |
| [platform-and-deployment-terminology.md](./platform-and-deployment-terminology.md) | Workbench, Console, Registry, platform naming | Referencing DataRobot deployment surfaces or platform tiers (SaaS, Self-Managed). |
| [release-notes-and-announcements.md](./release-notes-and-announcements.md) | Version notes, feature summaries, issue-fix wording | Writing a changelog, release notes, or "what's new" section in the README. Time-anchor words are allowed here. |

## Reference only (do not load during README merges)

| File | What it covers | When to read |
|------|----------------|--------------|
| [quick-reference.md](./quick-reference.md) | Context-to-section index for common authoring tasks | Unsure which topic file applies — use this index to find the right file. |
| [appendix-google-alignment-gaps.md](./appendix-google-alignment-gaps.md) | Intentional divergences from the Google style guide | Resolving a conflict between Google style and DataRobot style — background context only. |
| [document-history.md](./document-history.md) | Style guide change log | Updating or maintaining the style guide itself — not for README authoring. |

## README section → reference mapping

Use this table to load topic files based on the `README.generated.md` section you are filling:

| README section (typical) | Load in addition to the default set |
|--------------------------|-------------------------------------|
| Project overview / scope | [purpose-and-voice.md](./purpose-and-voice.md), [content-best-practices.md](./content-best-practices.md) |
| Quick start / installation | [code-in-text.md](./code-in-text.md) (already in default set) |
| Configuration / environment variables | [code-in-text.md](./code-in-text.md), [formatting-conventions.md](./formatting-conventions.md) |
| API reference / endpoints | [api-and-sdk-documentation.md](./api-and-sdk-documentation.md), [capitalization-and-proper-nouns.md](./capitalization-and-proper-nouns.md) |
| Troubleshooting / errors | [error-messages.md](./error-messages.md) |
| DataRobot integration / deployment | [platform-and-deployment-terminology.md](./platform-and-deployment-terminology.md), [capitalization-and-proper-nouns.md](./capitalization-and-proper-nouns.md), [standard-terminology.md](./standard-terminology.md) |
| UI / console interactions | [ui-copy.md](./ui-copy.md) |
| Screenshots / diagrams | [accessibility-and-inclusive-documentation.md](./accessibility-and-inclusive-documentation.md), [github-markdown-authoring.md](./github-markdown-authoring.md) (Mermaid) |
| Changelog / release notes | [release-notes-and-announcements.md](./release-notes-and-announcements.md) — time-anchor words allowed |
