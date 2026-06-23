# Documentation Style Specification

Style standards for App Framework component READMEs and other GitHub Markdown documentation. Follow these rules when creating or updating documentation to ensure consistency with the DataRobot corporate style guide.

**Authoritative reference**: [datarobot-style-guide-github.md](./datarobot-style-guide-github.md)

**External references**: [DataRobot design system](https://design-system.drdev.io/), [Google Developer Documentation Style Guide](https://developers.google.com/style).

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
- ✅ Use active voice: "The wizard guides through setup."
- ❌ Avoid passive voice when active is clearer

### Words to avoid

- ❌ **Please** — drop; adds no information
- ❌ **We / our** — rephrase with *DataRobot* or a neutral subject
- ❌ **Currently, now, new, latest, soon** — see [Timeless documentation](#timeless-documentation)
- ❌ **Should** — state definite behavior instead
- ❌ **Simply, It's easy, quickly** — filler that adds no value
- ❌ Exclamation points, emojis, and internet slang

### Lists

Two valid description-list styles:

**Run-in style (preferred for glossary-style lists)**:

```markdown
- **Authentication**. Manage DataRobot credentials.
- **Templates**. Clone and configure applications.
```

**Em dash style (valid for CLI-style docs)**:

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

### Contractions

- ✅ Allowed in technical documentation: negation contractions (*isn't*, *don't*, *won't*, *can't*)
- ❌ Avoid noun+verb possessive contractions: *browser's* → *browser is*; *template's* → *the template configuration*
- ❌ Do not use *we're* or other first-person contractions (never use *we*)
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
- ❌ Avoid idioms, slang, culturally specific humor, and directional language (*above*, *below*)
- ❌ Do not attribute human qualities to software (*The service sees…* → *The service detects…*)

### GitHub Markdown callouts

GitHub does not support MkDocs admonitions. Use blockquotes:

```markdown
> **Note:** Useful but non-required information.

> **Warning:** This action cannot be undone.

> **Important:** Back up the configuration before proceeding.
```

Capitalize the callout type, use a colon, and end with a period.

## Detailed rules

### 1. Headings and document structure

**Sentence case**

```markdown
✅ ## Getting started
✅ ### Quick setup guide
✅ ## Configuration options

❌ ## Getting Started
❌ ### Quick Setup Guide
❌ ## Configuration Options
```

**Structure**

- Every heading section must have a sentence or paragraph of intro text before subsections or lists.
- Use descriptive, unique headings to aid navigation and screen readers.
- Avoid code in headings when possible; if required, add a descriptive noun (*the `config.yaml` file*).
- In a section that summarizes subsections, use *in the following sections* (not *in this section*).

**Special cases**

```markdown
✅ ## DataRobot CLI features
✅ ### OAuth authentication setup
✅ ## PostgreSQL configuration

Proper nouns always capitalized
```

Do not use the possessive form of DataRobot followed by a product name (*DataRobot's Data Registry*). Rephrase: *The capabilities of Data Registry are vast.*

### 2. Voice and person

**Never use *we* or *our***

```markdown
✅ DataRobot provides several installation methods.
✅ The CLI manages DataRobot applications.

❌ We provide several installation methods.
❌ Our CLI manages DataRobot applications.
```

**Minimize *you* and *your***

```markdown
✅ Enable authentication before deploying.
✅ Configure the CLI using the following steps.
✅ Run this command to authenticate.

❌ You must enable authentication before deploying.
❌ You can configure the CLI using the following steps.
```

**Present tense and active voice**

```markdown
✅ The CLI provides authentication management.
✅ This command generates shell completions.
✅ The wizard validates input.

❌ The CLI will provide authentication management.
❌ Completions can be generated by running this command.
❌ Input will be validated by the wizard.
```

### 3. Lists and bullets

**Description lists**

```markdown
✅ - **Authentication** — manage DataRobot credentials.
✅ - **Templates**. Clone and configure applications.

❌ - **Authentication** - manage DataRobot credentials
❌ - **Templates**: clone and configure applications
❌ - **Task runner** - execute application tasks
```

**Periods in lists**

```markdown
✅ Add periods to complete sentences:
- This is a complete sentence.
- Another complete sentence.

✅ Add periods to list items with verbs:
- Install prerequisites.
- Clone the repository.
- Build the binary.

❌ No periods for single words:
- Authentication
- Templates
- Configuration

❌ No periods for code-only items:
- `dr auth login`
- `dr templates list`
```

**Nested lists**

```markdown
✅ - **Main item** — description.
     - Subitem with description.
     - Another subitem.

Add periods consistently to all levels
```

**Procedures**

- Introduce procedures with context; the intro can end with a colon (if immediately before steps) or a period.
- Put conditional clauses before instructions, not after.
- Mark optional steps: *(Optional)* as the first word of the step, in parentheses, no period.

### 4. Contractions

**Allowed (negation contractions in technical docs)**

```markdown
✅ It isn't difficult to get started.
✅ Don't commit `.env` files to version control.
✅ The CLI won't overwrite existing credentials.
```

**Avoid (noun possessive contractions)**

```markdown
✅ The browser opens automatically.
✅ The template configuration includes…
✅ Use the system default settings.

❌ The browser's automatic opening…
❌ The template's configuration includes…
❌ Use the system's default settings.
```

### 5. Placeholders and variables

**Inline and procedural text**

```markdown
✅ dr templates clone TEMPLATE_NAME
✅ export DATABASE_URL=postgresql://…
✅ cd YOUR_PROJECT_DIR

❌ dr templates clone <template-name>
❌ export DATABASE_URL=<database-url>
❌ cd <your-project-dir>
```

**In tables**

```markdown
✅ | Parameter | Description |
   |-----------|-------------|
   | TEMPLATE_NAME | Name of the template. |
   | DATABASE_URL | Database connection string. |
```

### 6. Code examples

**Single commands**

```markdown
✅ dr auth login
✅ task build
✅ go test ./...

❌ $ dr auth login   (when $ could be confused with env vars)
```

**Multi-line scripts**

```markdown
✅ # Clone the repository.
   git clone https://github.com/datarobot-community/af-component-agent.git
   cd af-component-agent

   # Build the component.
   task build
```

**Inline code**

Use backticks for commands, flags, filenames, paths, environment variables, and user-typed values:

```markdown
✅ Use the `dr auth login` command to authenticate.
✅ The `--verbose` flag enables detailed logging.
✅ Edit the `config.yaml` file.
```

Do not inflect code terms as verbs or make them possessive (*POST the data* → *Send a `POST` request*).

### 7. Tables

- Precede every table with a complete introductory sentence (for example, *The following table lists…*).
- Use sentence case for column headers; omit articles; no ending punctuation on headers.
- Add periods to description cells that are complete sentences.
- Use an em dash (—) for empty cells, not *N/A* or blank cells.

```markdown
✅ The following table lists available commands.

   | Command | Description |
   |---------|-------------|
   | `dr auth` | Authentication management. |
   | `dr templates` | Template operations. |
```

### 8. Links and cross-references

```markdown
✅ See [Getting started](getting-started.md) for details.
✅ For more information, see [Managing deployments](managing-deployments.md).
✅ Visit the [DataRobot website](https://datarobot.com).

Use sentence case for link text
Include `.md` extension in repository-relative links
Put punctuation outside link text when possible
Use descriptive link text — not "click here" or raw URLs
```

**See also sections**

```markdown
✅ ## See also

- [Getting started](getting-started.md) — installation guide.
- [Authentication](authentication.md) — managing credentials.
- [Templates](templates.md) — working with templates.
```

End pages with a **See also** section when helpful.

### 9. Callouts and notes

Use GitHub blockquote callouts, not MkDocs admonition syntax:

```markdown
✅ > **Note:** The CLI requires Go 1.25.8 or later.

✅ > **Important:** Never commit `.env` files to version control.

✅ > **Tip:** Use tab completion to discover commands.

Capitalize type, use colon, add period at end
```

For long optional content, use collapsible sections:

```markdown
<details>
<summary>Click to expand optional details</summary>

Additional content here.

</details>
```

### 10. Special terms

**DataRobot-specific**

```markdown
✅ DataRobot (always capitalized)
✅ DataRobot CLI
✅ OAuth (not oAuth or oauth)
✅ API key (not API Key or api key in running text)
✅ ID (capitalized unless referring to a field name, e.g., `association_id`)
```

**Technical terms**

```markdown
✅ Bash, Zsh, Fish, PowerShell (shell names)
✅ macOS, Linux, Windows (operating systems)
✅ PostgreSQL, MongoDB (databases)
✅ GitHub, GitLab (services)
```

**Abbreviations**

- Spell out on first use unless widely recognized: AI, ML, LLM, API, SDK, JSON, YAML, URL, REST.
- Spell out on first use, then abbreviate: MCP (Model Context Protocol), RAG (retrieval-augmented generation).
- Prefer *that is* and *for example* over *i.e.* and *e.g.*
- Pluralize abbreviations like ordinary words: APIs, LLMs.

### 11. Grammar and punctuation

- Use American English spelling and punctuation.
- Leave one space between sentences, not two.
- Use the Oxford comma in lists of three or more items.
- Use em dashes (—) for breaks in flow — no spaces around the em dash.
- Use colons to separate an item from its description (*Appendix A: Title*), not em dashes.
- End complete sentences with a period, including table cell descriptions.
- Do not add periods to headings, button labels, or table column headers.
- Use **bold** for UI element names; do not use quotation marks around UI labels.
- Spell out *and*; do not use `&` in headings or body text (exception: UI labels containing `&`).

### 12. Timeless documentation

Document current product behavior. Avoid words that anchor content to a moment in time:

- ❌ *currently*, *now*, *new*, *newer*, *latest*, *soon*, *eventually*
- ❌ *as of this writing*, *at present*, *does not yet*, *in the future*

```markdown
✅ These subcommands support HTTP load balancing.
❌ These new subcommands let you interact with HTTP load balancing.
```

Release notes and announcements are an exception — dates, version numbers, and *new* / *preview* / *GA* are expected there.

### 13. Accessibility and inclusive language

- Use semantic structure: heading hierarchy, lists for steps, tables introduced in prose.
- Always provide meaningful alt text for images.
- Do not present information only in images — include equivalent text.
- Avoid ableist figures of speech (*sanity check*, *blind to*).
- Use *allowlist* / *denylist* instead of *whitelist* / *blacklist*.
- Use singular *they* for gender-neutral references; do not use *he/she*.
- Aim for sentences of about 26 words or fewer when practical.
- Left-align text; do not center or full-justify.

### 14. GitHub Markdown authoring

- Use Markdown, not HTML, unless GFM does not support the feature (for example, `<details>`).
- Use single blank lines between blocks (headings, paragraphs, lists, tables, fences).
- Do not use horizontal rules (`---`) as section separators unless separating unrelated content.
- Do not use MkDocs/Pymdown extensions (`!!! note`, `{ target=_blank }`, `{: #anchor }`) — they render as literal text on GitHub.
- Store images in a project-relative folder (for example, `images/`).
- Mermaid diagrams work in fenced `mermaid` blocks; prefer text for essential information.

## App Framework README checklist

When updating component documentation, verify these elements:

- [ ] Sentence-case headings with intro text under every section
- [ ] No `[[INSERT … HERE]]` placeholders or HTML comment instructions in final output
- [ ] Imperative or neutral voice — no *we* / *our*; minimal *you* / *your*
- [ ] Present tense, active voice
- [ ] Lists use consistent punctuation and parallel structure
- [ ] Placeholders use `UPPERCASE_WITH_UNDERSCORES` in procedural text
- [ ] Code blocks have language tags; single-line commands omit `$` when ambiguous
- [ ] Links use descriptive text and `.md` extensions for repo-relative paths
- [ ] Callouts use blockquote syntax, not MkDocs admonitions
- [ ] Timeless language (no *currently*, *new*, *latest*)
- [ ] Component dependencies section matches `copier-module.yaml` (auto-generated; do not override)

## Verification process

### Manual review

1. Check all headings use sentence case and have intro text
2. Verify voice: no *we* / *our*; imperatives preferred over *you can* / *you must*
3. Confirm present tense and active voice
4. Verify lists use correct punctuation and parallel structure
5. Check placeholders use the correct format for context
6. Confirm no noun possessive contractions
7. Verify command examples and code blocks follow GitHub Markdown conventions
8. Confirm timeless language (except in release notes)
9. Check callouts use blockquote format

## Common mistakes

### Heading case

```markdown
❌ ## Getting Started With DataRobot CLI
✅ ## Getting started with DataRobot CLI

❌ ### Installation And Setup
✅ ### Installation and setup
```

### Voice issues

```markdown
❌ We provide a CLI for managing applications.
✅ The CLI manages DataRobot applications.

❌ You can enable authentication in the settings.
✅ Enable authentication in the settings.

❌ The CLI will generate completions.
✅ The CLI generates completions.
```

### List formatting

```markdown
❌ - **Feature** - this is a feature
✅ - **Feature** — this is a feature.

❌ - Install the CLI
   - Run the command
✅ - Install the CLI.
   - Run the command.
```

### Placeholder format

```markdown
❌ dr templates clone <template-name>
✅ dr templates clone TEMPLATE_NAME

❌ export DATABASE_URL=<your-url>
✅ export DATABASE_URL=YOUR_DATABASE_URL
```

## Exception cases

### Acronyms and abbreviations

- Keep standard acronyms uppercase: API, CLI, URL, HTTP, REST, JSON
- Use official product names: DataRobot, PostgreSQL, MongoDB

### Code blocks

- Code content follows language conventions (not style guide rules)
- Comments within code should have periods

### External links

- Use the official name/title of external resources
- Example: "Bubble Tea" (official name) not "bubble tea"

## Updates and maintenance

### When to update this spec

- DataRobot style guide changes (update [datarobot-style-guide-github.md](./datarobot-style-guide-github.md) first, then align this spec)
- New documentation patterns emerge in App Framework components
- User feedback indicates unclear guidelines

### Version history

| Date | Change |
|------|--------|
| 2026-06-23 | Aligned with [datarobot-style-guide-github.md](./datarobot-style-guide-github.md): voice/person rules, contractions, GitHub Markdown callouts, timeless docs, accessibility, placeholder formats, and link conventions. |
| 2025-10-24 | Initial specification created based on DataRobot corporate style guide review. |

## Reference

This specification is derived from:

- [datarobot-style-guide-github.md](./datarobot-style-guide-github.md) — authoritative DataRobot style guide for GitHub Markdown
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- Technical writing best practices for App Framework component READMEs

For the full docs-site guide (MkDocs Material, Vale, repository paths), see [datarobot-style-guide.md](./datarobot-style-guide.md) if available in your workspace.
