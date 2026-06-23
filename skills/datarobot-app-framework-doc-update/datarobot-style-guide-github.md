# DataRobot style guide (GitHub Markdown)

Writing standards for product UI copy, API descriptions, error messages, and technical documentation. This version uses **GitHub Flavored Markdown (GFM)** only — no MkDocs Material, Jinja, or datarobot-docs build features.

For the full docs-site guide (MkDocs Material, Vale, repository paths), see [datarobot-style-guide.md](datarobot-style-guide.md).

**External references**: [DataRobot design system](https://design-system.drdev.io/), [Google Developer Documentation Style Guide](https://developers.google.com/style).

## Table of contents

1. [Purpose and voice](#purpose-and-voice)
2. [Grammar and punctuation](#grammar-and-punctuation)
3. [Capitalization and proper nouns](#capitalization-and-proper-nouns)
4. [Words to avoid](#words-to-avoid)
5. [UI copy](#ui-copy)
6. [API and SDK documentation](#api-and-sdk-documentation)
7. [Error messages](#error-messages)
8. [Technical documentation](#technical-documentation)
9. [Accessibility and inclusive documentation](#accessibility-and-inclusive-documentation)
10. [Timeless documentation](#timeless-documentation)
11. [Anthropomorphism](#anthropomorphism)
12. [Code in text](#code-in-text)
13. [Formatting conventions](#formatting-conventions)
14. [Standard terminology](#standard-terminology)
15. [Content best practices](#content-best-practices)
16. [GitHub Markdown authoring](#github-markdown-authoring)
17. [Platform and deployment terminology](#platform-and-deployment-terminology)
18. [Release notes and announcements](#release-notes-and-announcements)
19. [Quick reference](#quick-reference)
20. [Appendix: Google alignment gaps](#appendix-google-alignment-gaps)

## Purpose and voice

### Brand voice

DataRobot provides a technical, no-nonsense product for serious business and AI problems. Copy should be:

- **Direct, correct, and action-oriented** — help users understand or decide quickly.
- **Factual and confident** — see [Words to avoid](#words-to-avoid) for tone constraints (no slang, emojis, exclamation points).
- **Written for a global audience** — simple, clear language with translation in mind.
- **Respectful of user intelligence** — users are skilled but may be unfamiliar with DataRobot-specific terms.

**Preferred**:

> Customizable end-to-end AI templates for quick, tailored successes.

**Avoid**:

> Feeling stuck? Our handy templates are here to help — just plug and play your way to success!

### Audience assumptions

- Assume users are smart and technically proficient.
- Do not oversimplify; explain DataRobot-specific behavior when needed.
- Confirm jargon is widely recognized before using it.
- Align with established industry terms where patterns are clear.

For abbreviations and acronyms, see [Abbreviations](#abbreviations).

### Documentation voice

Published documentation uses a distinct voice from UI and API copy. Follow [Voice and tense](#voice-and-tense) and [First and second person](#first-and-second-person-we-you).

- Conversational and friendly without being frivolous.
- Inclusive and global — avoid idioms, slang, culturally specific humor, and directional language (*above*, *below*).
- Readable — short, clear sentences; define DataRobot-specific terms as needed.

Do not use the possessive form of DataRobot followed by a product name (for example, DataRobot's Data Registry). Rephrase instead: *The capabilities of Data Registry are vast.*

## Grammar and punctuation

### Sentence case

Use sentence case for titles, headings, labels, buttons, column headers, and link text. Capitalize only the first word and proper nouns.

| Preferred | Avoid |
|-----------|-------|
| Create a feature list | Create a Feature List |
| Quick setup guide | Quick Setup Guide |
| Experiment type | Experiment Type |

### Periods

End complete sentences with a period, including descriptions in table cells. Do not add periods to headings, button labels, UI examples in comparison tables, or table column headers.

| Content type | Period? |
|--------------|---------|
| Complete sentences (descriptions, validation messages, list items that are sentences) | Yes. |
| API and parameter descriptions | Yes. |
| Error messages, tooltips (single or multiple sentences) | Yes. |
| Input labels, section headers, one-word UI text | No. |
| Button labels | No. |

### Oxford comma

Use a comma before the final conjunction in lists of three or more items.

> Select models, feature lists, or datasets.

### Abbreviations

- Spell out abbreviations on first use unless the audience will recognize them.
- Widely recognized in technical AI and ML documentation (typically no spell-out on first use): **AI**, **ML**, **LLM**, **API**, **SDK**, **GPU**, **CPU**, **JSON**, **YAML**, **UI**, **URL**, **HTML**, **REST**, **MB**, **GB**.
- Spell out on first use, then use the abbreviation: **MCP** (Model Context Protocol), **RAG** (retrieval-augmented generation), **GenAI** (generative AI), **NLP** (natural language processing), **MLOps** (machine learning operations), **LLMOps** (large language model operations), **RLHF** (reinforcement learning from human feedback), **HITL** (human in the loop), **NER** (named entity recognition), **OCR** (optical character recognition), **IoT** (Internet of Things), **ETL** (extract, transform, load), **SLA** (service level agreement).
- Use official capitalization for vendor and model names (for example, **GPT**, **BERT**, **Claude**); do not invent alternate spellings.
- If the first mention is in a heading, use the abbreviation in the heading and spell it out in the first paragraph below.
- Do not create nonstandard abbreviations; use industry-standard forms.
- Prefer *that is* and *for example* over *i.e.* and *e.g.*.
- Do not use internet slang (*tl;dr*, *ymmv*, *RTFM*).
- Pluralize abbreviations like ordinary words (*APIs*, *LLMs*, *OSes*).

### Pronouns

- Use **singular *they*** for gender-neutral references; do not use *he/she* or *(s)he*.
- Ensure pronouns have clear antecedents; prefer repeating the noun when *it* or *they* is ambiguous.
- Use optional pronouns (*that*, *who*) when they improve clarity (*Make sure that all files are correct*).
- Use ***who*** for people, not *that*.
- Use ***that*** for restrictive clauses (no comma); ***which*** for nonrestrictive clauses (with comma).
- For *we*, *our*, *you*, and *your*, see [First and second person](#first-and-second-person-we-you).

### American English

Use standard American spelling and punctuation throughout.

Leave **one space** between sentences, not two.

### Contractions

| Context | Contractions |
| --- | --- |
| UI copy, API descriptions, error messages | **Do not use** (Don't, can't, won't, you're, etc.). |
| Technical documentation | **Use** negation contractions (*isn't*, *don't*, *won't*, *can't*). **Avoid** noun+verb contractions (*browser's* → *browser is*). |
| All contexts | **Avoid** noun possessive contractions: *browser's*, *template's*, *system's*. |

Prefer positive phrasing over negative contractions:

| Preferred | Avoid |
|-----------|-------|
| Select up to three LLM blueprints | Do not select more than three LLM blueprints |
| Display multiple sections | Do not display fewer than two sections |

### Voice and tense

| Rule | UI / API / errors | Technical docs |
|------|-------------------|----------------|
| Tense | Present tense whenever possible. | Present tense. |
| Voice | Active voice. Passive voice is acceptable in UI copy and error messages when emphasizing the object or avoiding blame; avoid passive voice in API descriptions. | Active voice. |
| Person | See [First and second person](#first-and-second-person-we-you). | See [First and second person](#first-and-second-person-we-you). |
| Imperative | Use for instructions and buttons. | Use for procedures and instructions. |

**Active voice (preferred for instructions)**:

> Set the number of predictions to display.

**Passive voice (acceptable when appropriate)**:

> The file is saved.
> This model was trained using GPUs.
> Over 50 conflicts were found in the file.

### First and second person (*we*, *you*)

Applies to **UI copy, API descriptions, error messages, and documentation**.

#### Never use *we* or *our*

Do not use first-person plural in any context. When a subject is needed, use **DataRobot** or rephrase so no subject is required.

| Preferred | Avoid |
| --- | --- |
| DataRobot provides several installation methods. | We provide several installation methods. |
| The DataRobot model | Our model |
| DataRobot detects a configuration issue. | We detected a configuration issue. |

#### Minimize *you* and *your*

Prefer **imperative** instructions and neutral phrasing. Rephrase *You must…*, *You can…*, and *You should…* as direct commands or factual statements when clarity allows.

| Preferred | Avoid |
| --- | --- |
| Enable authentication before deploying. | You must enable authentication before deploying. |
| Configure the CLI using the following steps. | You can configure the CLI using the following steps. |
| Find out more about SSO by reading this article. | You can find out more about SSO by reading this article. |
| To delete a deployment, click **Delete**. | Click **Delete** if you want to delete a deployment. |

**Exception**: Use *you* or *your* only when removing them would make the sentence **awkward, confusing, or overly complicated** — not merely longer. When in doubt, try the imperative or neutral form first.

### Possessive pronouns in UI

Avoid *your* and *my* where possible; see [First and second person](#first-and-second-person-we-you).

| Preferred | Avoid |
|-----------|-------|
| Add custom metrics | Add your custom metrics |
| Dashboard | My dashboard |

Do not use possessive *DataRobot's* when referring to the product. Company references may use *DataRobot's* (e.g., *DataRobot's event*).

### Ellipses

Use ellipses (…) only to denote ongoing actions (loading states), not in menus, buttons, or dialogs.

> Importing dataset…
> Models will start training soon…

## Capitalization and proper nouns

### Brand and product names

| Term | Usage |
|------|-------|
| DataRobot | Always capitalized. |
| OAuth | Not oAuth or oauth. |
| API key | Lowercase *key* in running text. |
| ID | Capitalized unless referring to a field name (e.g., `association_id`). |

### DataRobot proper nouns (capitalize in descriptions)

When these terms appear in API or product descriptions, capitalize them as proper nouns. Use lowercase for generic nouns otherwise.

- Use Cases, Autopilot, Repository, Leaderboard
- Learning Curves, Speed vs Accuracy, Model Comparison, Dual Lift
- Feature Associations, Feature Discovery, Feature Fit, Feature Impact, Feature Effects
- Prediction Explanations, Neural Network Visualizer
- Data Quality Handling Report, Data Quality Assessment
- DataRobot Prime, Model Registry, Registry, Console, AI Catalog
- Accuracy Over Space, Accuracy Over Time, Series Insights, AI Accelerators
- Word Cloud, Smart Downsampling, Eureqa, Bias and Fairness
- Cross-Class Accuracy, Cross-Class Data Disparity
- Composable ML, Visual AI, Location AI, Document AI, Text AI
- SHAP, XEMP, Scoring Code, Portable Prediction Server

For deployment and UI surface names (Workbench, Console, Registry), see [Platform and deployment terminology](#platform-and-deployment-terminology).

### Technical terms (official capitalization)

| Category | Examples |
|----------|----------|
| Shells | Bash, Zsh, Fish, PowerShell |
| Operating systems | macOS, Linux, Windows |
| Databases | PostgreSQL, MongoDB |
| Services | GitHub, GitLab |

### API field names in prose

Reference API field names untranslated. Capitalization depends on position in the sentence.

| API identifier | Prose form |
|----------------|------------|
| `llmBlueprintId` | Use field name in descriptions. |
| LLMBlueprint | LLM blueprint. |
| ChatPrompt | chat prompt. |
| ComparisonPrompt | comparison prompt. |
| Custom Model LLM Validation | custom model LLM validation. |

## Words to avoid

### Universal (all contexts)

| Avoid | Use instead / reason |
|-------|----------------------|
| Please | Drop — adds no information. |
| We / our | Never use. Rephrase with *DataRobot* or a neutral subject; see [First and second person](#first-and-second-person-we-you). |
| You / your (when imperative works) | Imperative or neutral phrasing (*Enable authentication*, not *You must enable authentication*). |
| Your (for assets) | The (*the data*, *the endpoint*). |
| Currently | Implies future behavior; omit — see also [Timeless documentation](#timeless-documentation). |
| Should | State definite behavior. |
| Could (when possible) | Cannot (present tense). |
| Abort | Cancel, Stop, or Terminate. |
| Very | More specific wording. |
| Execution | More specific wording. |
| Exclamation points | Periods only. |
| Emojis | None in product UI. |
| Chat abbreviations (ASAP, EOW) | Full words. |

### UI-specific

- Uncertain phrasing (*can*, *may*, *might*) when describing product capabilities.
- Generic *Yes* / *No* button labels — use specific actions (*Delete*, *Cancel*).

For contractions and person, see [Contractions](#contractions) and [Voice and tense](#voice-and-tense).

## UI copy

### Buttons and action labels

**Structure**:

- **Action buttons** — verb-based: Search, Save, Upload, Filter.
- **Menu buttons** — noun or noun/verb; menu items are verb-based.

**Rules**:

| Rule | Guidance |
|------|----------|
| Case | [Sentence case](#sentence-case). |
| Length | One to three words, one line; plan for ~50% text expansion in other languages. |
| Articles | Drop *a* and *the* for conciseness (*Reset password*, not *Reset the password*). |
| Specificity | [Words to avoid (UI-specific)](#ui-specific) — use *Delete* / *Cancel*, not *Yes* / *No*. |
| Consistency | Same label to open and complete a flow (*Create feature list* → *Create feature list*). |
| One action | One action per button. |

**Button vs link**:

- Buttons — on-page actions.
- Link buttons — navigation to another location or URL.
- Documentation — use hyperlinked **Open documentation** (not in error banners).

### Input fields

**Labels**:

- Use nouns (*Target feature*, *Name*).
- No punctuation (*Name*, not *Name:*).
- Append *(optional)* in lowercase when the field is not required.
- Assume all inputs are mandatory unless marked optional.

**Descriptions**:

- Follow [Periods](#periods); use for essential instructions — tooltips for supplemental definitions.
- Start with a verb matching input type:

| Input type | Leading verb(s) |
|------------|-----------------|
| Select, dropdown, multiselect, radio/checkbox group | Select… / Choose… / Specify… |
| Single checkbox | When checked,… |
| Numeric input | Set… / Configure… |
| Free-text input | Enter… / Provide… |
| Toggle | Toggle label: verb phrase; description: When enabled,… |

**Checkbox and toggle labels**:

- Start with a verb describing what happens when enabled.
- Reference state in descriptions: *When checked,…* or *When enabled,…*

**Placeholders**:

- Do not use by default.
- Acceptable for format hints (*YYYY-MM-DD*) or search hints (*Search by name or ID*).

### Validation messages and alerts

Keep messages concise. Use scannable titles (three to four words) and one to two sentences in the body.

| Type | Purpose | Example title |
|------|---------|---------------|
| Success | Task completed; no further action. | Data import is complete |
| Warning | Potential issue or data loss. | License will expire in {{days}} days |
| Error | Issue occurred; state cause and action. | Experiment creation failed |
| Loading | Ongoing action; start with verb + [ellipsis](#ellipses). | Importing dataset… |

### Collapsible sections

Use *Show…* / *Hide…* with an appropriate noun. For content always visible, use *Show additional…* / *Hide additional…*.

### Tabs and tiles

Use **plural** names for tabs and navigation tiles when plural form is natural for the collection they represent.

| Preferred | Avoid |
| --- | --- |
| Deployments | Deployment |
| Experiments | Experiment |
| Registered models | Registered model |
| Prediction environments | Prediction environment |

Use singular only when the label refers to one fixed item, a proper noun, or plural would be awkward (*Overview*, *Summary*, *Settings*).

### Tables

Use **singular** nouns for table column headers — each column describes one value per row.

| Preferred | Avoid |
| --- | --- |
| Name | Names |
| Model | Models |
| Type | Types |
| Version | Versions |
| Status | Statuses |

**Common column headers**: Name, Model, Type, Version, Language, Accuracy, Service health, Global

**Timestamps and metadata** — match labels used in the product. Do **not** use *Date added* or *Date modified*; they do not appear in the UI.

| Label | Typical use |
| --- | --- |
| **Created by** | Column header or filter for the creator's username. |
| **Creation date** | Sort option and catalog views (for example, AI Catalog). |
| **Created** | Table column; in some views the cell includes both date/time and creator. |
| **Last modified** | Table column or filter for the most recent change. |
| **Modified** | Dataset and asset detail; last modified date (often with modifier). |
| **Updated** | Jobs and similar inventories. |
| **Added On** | Prediction environment inventory (Console). |
| **Created at** / **Last updated at** | Registered model version tables. |

When a single cell shows **both** date/time and author, put the date/time on the first line and the username on the second — not a *Created by* label inside the cell.

**Statistics labels (use full form when space permits)**: Standard deviation (or Std. dev.), Minimum (Min.), Maximum (Max.), Average (Avg.), Mean, Median, Index, Unique, Missing

**Empty cells**: Use an em dash (—), not blank cells, *N/A*, or *Not selected*.

### Drawers and modals

- Use modals sparingly and for temporary interactions.
- Align modal title with the button that opened it (*Add new* → *Add new policy template*).
- Informative modals — noun title (*Model performance*).
- Action modals — verb title (*Start walkthrough*).

**Deletion confirmation**:

| Element | Format |
|---------|--------|
| Title | Delete {{noun}}? |
| Description | Deleting "{{specific noun name}}" cannot be undone. |
| Cancel | Cancel |
| Primary action | Yes, delete {{nouns}} |

### Empty states

| Situation | Guidance |
|-----------|----------|
| No information | Explain why; offer next steps. |
| Loading | Action-oriented; avoid generic "Loading…". |
| Task complete | Confirm completion; highlight key metrics. |

**Empty state header pattern**: No matching {{nouns}}

**Clear actions**: Clear search / Clear filters

### Disabled settings

Use availability messaging:

> {{Object}} is only available {{reason/condition}}.

Examples:

> Exposure is only available for experiments with zero-inflated or regression targets.
> This setting is not available when Incremental Modeling is enabled.

## API and SDK documentation

Established conventions for API changelog entries, class/method descriptions, and parameter documentation apply to all API and SDK content.

Follow [Voice and tense](#voice-and-tense) (active voice; no passive in API descriptions), [Words to avoid](#words-to-avoid), [Contractions](#contractions) (prefer positive phrasing), and [Capitalization and proper nouns](#capitalization-and-proper-nouns). For filenames in prose, see [File formats](#file-formats).

### Formatting references

For code font rules, see [Code in text](#code-in-text). API-specific formatting:

| Element | Format | Example |
|---------|--------|---------|
| Parameter names in prose | Single backticks. | Either `llm_blueprint` or `chat` is required. |
| API names, classes, methods, constants in descriptions | Quoted. | Intakes the "llmBlueprintId". |
| Field names in API payloads | Untranslated API identifiers. | `llmBlueprintId`. |

### Description patterns

All descriptions begin with a capital letter and end with a period — see [Periods](#periods).

**Do not repeat the entity name** in the first sentence:

| Preferred | Avoid |
| --- | --- |
| Returns service health stats for the deployment. | The GetServiceStats function will return service health stats for the deployment. |

**Parameter descriptions**:

- Begin with an article when starting with a noun: *The dataset ID.*
- For defaults, explain behavior per value, then state default: *Default: false.*

**Operation descriptions**:

| Operation type | Start with |
|----------------|------------|
| Action returning data | Verb: *Adds a new dataset to the AI Catalog.* |
| Retrieval (non-boolean) | Gets: *Gets the dataset ID.* |
| Boolean check | Present-tense verb: *Checks whether the deployment has enabled sharing.* |
| Boolean parameter behavior | State behavior for true and false: *If true, validates the SSL certificate… If false, trusts the certificate without validating it.* |

### Sections to review in API PRs

- API changelog (`CHANGES.rst`).
- Class and method descriptions.
- Parameter descriptions.
- Strings wrapped in `description=gettext_openapi_noop()`.

## Error messages

Follow [Voice and tense](#voice-and-tense), [Words to avoid](#words-to-avoid), and [Periods](#periods). Error-specific rules:

| Rule | Guidance |
| --- | --- |
| Articles | Do not start with *the* or *a* (except multi-sentence messages). |
| Modals | Prefer *cannot* over *could*. |
| Field names | Capitalize *ID* unless it is a field name; use exact API field names in API responses. |

## Technical documentation

Standards for published technical documentation. Some rules differ from UI and API copy to support instructional prose.

### Voice, tense, and clause order

Follow [Documentation voice](#documentation-voice) and [First and second person](#first-and-second-person-we-you). Additional procedural patterns:

| Preferred | Avoid |
| --- | --- |
| The CLI provides authentication management. | The CLI will provide authentication management. |
| For more information, see `[Managing deployments](managing-deployments.md)`. | For more information, please see… |
- Put conditional clauses before instructions, not after.
- Use future tense only when emphasizing something that will happen later.
- Avoid placeholder phrases (*please*, *note*, *at this time*), filler (*Simply*, *It's easy*, *quickly*), and overusing *You can* / *You must* / *To do* / *Let's* at sentence starts.

### Headings and document structure

Follow [Sentence case](#sentence-case) for titles, headings, table headers, captions, and list items. Additional rules:

- **No period** at the end of a title or heading.
- Use **imperative verbs** in headings for procedural topics (*Transfer datasets*), not gerunds (*Transferring datasets*).
- Use a **heading hierarchy** — one level-1 heading per page; do not skip levels.
- Use **descriptive, unique** headings to aid navigation and screen readers.
- In a section that summarizes subsections, use *in the following sections* (not *in this section*).
- Avoid code in headings when possible; if required, add a descriptive noun (*the `config.yaml` file*).
- Keep headings concise and descriptive; avoid unnecessary modifiers.

### Lists

| List type | Use when |
| --- | --- |
| **Numbered** | Steps performed in order (procedures). |
| **Bulleted** | Items that are not a sequence or options. |
| **Description** | Terms with definitions (glossary-style). |
| **Bulleted description (run-in)** | Terms with definitions; bold the term, use a period after the term. |

**Capitalization and punctuation**:

- Start list items with a capital letter.
- End items with a period unless the item is a single word, has no verb, is entirely in code font, or is a link or title only.
- Keep items **parallel** in structure within a list.
- For description lists with run-in headings, use `* **Term**. Description.` — do not use a dash between term and description.

**Description lists (em dash style)** — also valid for CLI-style docs:

```markdown
- **Authentication** — manage DataRobot credentials.
- **Templates** — clone and configure applications.
```

### Procedures

- Introduce procedures with context; the intro can end with a colon (if immediately before steps) or a period.
- Do not introduce a procedure with a bare imperative (*Customize the buttons*:).
- Label sub-steps with lowercase letters; sub-sub-steps with lowercase Roman numerals.
- State **purpose before action**: *To start a new document, click **File > New > Document**.*
- State **location before action**: *In the Console, go to the **Deployments** page.*
- Mark optional steps: *(Optional)* as the first word of the step, in parentheses, no period.
- Avoid repeating full procedures — link to them instead.
- Do not include keyboard shortcuts in procedures (describe the action instead).

### UI elements in documentation

When documenting UI interactions:

- **Bold** UI element names: buttons, menus, dialogs, tabs, checkboxes (*Click **OK***); see [Text formatting](#text-formatting).
- Do not use quotation marks around UI element names.
- Match UI capitalization when consistent; use sentence case if labels are all caps or inconsistent.
- **Focus on the task** when practical (*Refresh the page* vs *Click **Refresh***).
- Use *the **LABEL** menu* or **File > Tools** (space before `>`; entire sequence in one bold span).
- Refer to expanders as **expander arrow** or **drop-down menu**.
- Omit ellipsis from button labels in docs (*Browse*, not *Browse…*); see [Ellipses](#ellipses).
- Format user-typed text in backticks; keyboard keys in backticks (*Press `Control+C`*).
- Spell out modifier keys (*Control*, *Command*); on Mac, note the Mac shortcut in parentheses.

### Links and cross-references

- Use **descriptive link text** — not *click here*, *this document*, or raw URLs.
- Introduce cross-references with *For more information, see* when referring the reader to another topic.
- Put **punctuation and quotation marks outside** link text when possible.
- Use **relative paths** to other Markdown files in the repository (for example, `[Topic](../path/to/page.md)`).
- Include the `.md` extension in repository links so links work in the GitHub file browser and in cloned repos.
- Say *about* a topic, not *on* a topic (*information about indexes*).
- Do not repeat the same link to the same document multiple times on one page unless justified.
- For download links, indicate file type (*download the README.txt file*).
- **Explain unexpected link behavior** when a link downloads a file or jumps within the page.
- Avoid adjacent links; separate with words or punctuation when possible.
- End pages with a **See also** section when helpful — use descriptive link text and a brief phrase after each link.
- Before linking to GitHub repositories that require sign-in, warn readers: *Log in to GitHub before clicking this link.*

**In-page links**: GitHub generates heading anchors automatically from heading text (lowercase, spaces become hyphens, punctuation removed). Link with `[Section name](#section-name)`.

### Code, placeholders, and command line

| Context | Placeholder format |
| --- | --- |
| Inline or procedural text | `UPPERCASE_WITH_UNDERSCORES` (explain on first use). |
| Code samples (general) | `<camelCase>` angle brackets (for example, `<modelId>`). |
| REST API / OpenAPI endpoints | `{curlyBraces}` (for example, `{projectId}`). |

**Code samples**:

- Use fenced code blocks with a **language tag** (`python`, `bash`, `json`, etc.).
- Indent with **spaces**, not tabs.
- Precede samples with an introductory sentence (colon if immediately before the block).
- Do not use `$` in one-line samples when `$` could be confused with environment variables; for multi-line terminal sessions, `$` is acceptable for consistency.

**Command-line syntax**:

- **Required** arguments: plain text, often in code font.
- **Optional** arguments: square brackets — `[GLOBAL_FLAG]`.
- **Mutually exclusive** arguments: braces and pipes — `{FILE_1|FILE_2}`.
- **Repeating** arguments: ellipsis — `[GLOBAL_FLAG ...]`.
- Separate **input and output** into different code blocks when showing both.

### Tables in documentation

- Precede every table with a **complete introductory sentence** (e.g., *the following table*).
- Use **sentence case** column headers; see [Sentence case](#sentence-case). Omit articles; no ending punctuation on headers.
- Sort rows logically or alphabetically.
- Avoid tables inside numbered procedures or single-column tables (use a list instead).

For table accessibility, see [Accessibility](#accessibility).

### Images and screenshots

- Store images in a project-relative folder (for example, `images/` or `docs/images/`).
- Use Markdown: `![Alt text describing the image](images/name-of-img.png)`.
- Always provide meaningful **alt text** — do not leave alt text empty unless the image is purely decorative.
- Do not present information only in images — include equivalent text.
- Blur confidential information in screenshots.
- Avoid directional language; use screenshots when UI location is hard to describe.
- Use numbered callouts in prose or tables: **1**, **2**, **3** (bold numerals in the surrounding text).

### Text formatting

| Element | Convention |
| --- | --- |
| **Bold** | UI elements in navigation (`**`, not `__`). |
| **Italic** | Terms as words, emphasis, parameter names in signatures, mathematical variables. |
| **Underline** | Do not use. |
| **Code font** | Inline code and fences. |
| **Ampersand** | Spell out *and*; exception for UI labels containing `&`. |
| **Quotations** | American English punctuation; shorter work titles in quotes unless linked. |
| **Words as words** | Italicize terms being discussed (*Select* means choose from a list). |
| **Letters as letters** | Italicize a letter referring to itself (*a variable named **n***). |

### Punctuation (documentation)

Follow [Grammar and punctuation](#grammar-and-punctuation) and [Formatting conventions](#formatting-conventions) for commas, hyphens, and ellipses. Documentation-specific rules:

- Use **em dashes** (—) for breaks in flow — no spaces around the em dash.
- Use **colons** to separate an item from its description (*Appendix A: Title*), not em dashes.
- When bold text precedes a colon, put the colon outside the bold span.
- Uppercase the first word after a colon in running text (unless proper noun, heading, or quotation).

### Parallel content variants

When a procedure differs by deployment type, UI surface, or platform, use **separate headings** or **collapsible sections** instead of tabbed content:

```markdown
### Workbench

Steps for Workbench…

### Console

Steps for Console…
```

For optional collapsible content, use HTML supported by GitHub:

```markdown
<details>
<summary>Click to expand optional details</summary>

Additional content here.

</details>
```

## Accessibility and inclusive documentation

Write documentation so readers using screen readers, keyboard navigation, or translation tools can use it effectively.

### Accessibility

- Use semantic structure: heading hierarchy, lists for steps, tables introduced in prose.
- Introduce tables before they appear.
- Label form fields; write clear validation errors (*Name is a required field*).
- Do not rely on color or position alone to convey meaning; add text labels or icons as secondary cues.
- Avoid camelCase and ALL CAPS in prose when possible (screen readers may read letters individually).
- Do not use & instead of *and* in headings or body text (exception: UI labels that include `&`); see [Text formatting](#text-formatting).
- Left-align text; do not center or full-justify.
- Do not force hard line breaks inside sentences.
- Aim for sentences of about 26 words or fewer when practical.

### Inclusive language

- Avoid ableist figures of speech (*sanity check*, *blind to*, *cripple*, *dummy*).
- Avoid gendered terms (*man-hours*, *mankind*); for gender-neutral singular references, see [Pronouns](#pronouns).
- Avoid violent metaphors (*kill*, *hang*, *hit a wall*) and harmful jargon where simpler terms exist.
- Replace charged technical terms when possible: *allowlist* / *denylist* instead of *whitelist* / *blacklist*; write around *master* / *slave* in prose (use field names in code font only when required by code).
- Use diverse names and examples; avoid US-centric holidays, sports, or idioms unless relevant.
- Avoid seasons in global-facing docs; use months or quarters (see also [Dates and times (documentation)](#dates-and-times-documentation)).
- When discussing disability, use respectful, person-first or identity-first language per community preference; avoid *victim of*, *suffering from*, or euphemisms like *handi-capable*.
- Do not describe people without disabilities as *normal* or *healthy*; prefer *nondisabled* or *people without disabilities* when contrast is needed.

## Timeless documentation

Document the **current** product behavior. Avoid words that anchor content to a moment in time unless writing release notes, blogs, or time-stamped announcements.

**Avoid in product and reference documentation**:

- *currently*, *now*, *new*, *newer*, *latest*, *soon*, *eventually*
- *as of this writing*, *at present*, *does not yet*, *in the future*
- *existing*, *old*, *older*, *presently*

**Preferred**: *These subcommands support HTTP load balancing.*

**Avoid**: *These new subcommands let you interact with HTTP load balancing.*

**Do not pre-announce** unreleased features or products in documentation unless legal and product teams have approved the content.

## Anthropomorphism

Do not attribute human qualities to software or hardware.

| Preferred | Avoid |
| --- | --- |
| A Delimiter object specifies where to split a string. | A Delimiter object tells the splitter where to break the string. |
| The service detects a new device. | The service sees a new device. |

## Code in text

In ordinary sentences (not code fences), use `code` font (Markdown backticks) for anything tied to code, commands, or machine input.

### Use code font for

- Class, method, and function names (with `()` for methods: `get()`).
- Variables, attributes, environment names, and placeholders.
- Filenames, paths, folders, and extensions when referring to specific files.
- Command-line utilities (`kubectl`, `gcloud`).
- HTTP verbs, status codes (*an HTTP `400 Bad Request` status code*), and content types.
- Language keywords, enum names, DNS record types, and port numbers.
- User-typed values and UI labels rendered from prior input — use **bold and code**: Click **`my-instance`**.
- Command output when shown as literal text.

### Do not use code font for

- Product, service, or organization names in prose.
- Domain names and reader-facing URLs (prefer descriptive links).
- File type suffixes in isolation when all caps with no period (**PDF**, **CSV**); see [File formats](#file-formats).

### Method names

- Omit the class name when unambiguous: call `get()`, not `animal.get()`.
- Add empty parentheses to indicate a method: `close()`, not *close*.

### Do not inflect code terms

Do not use code keywords as verbs or make them possessive.

| Preferred | Avoid |
| --- | --- |
| Send a `POST` request. | `POST` the data. |
| Call `open()` before `close()`. | `Close`()ing requires `open`()ing first. |

For fenced code blocks, placeholders, and command-line syntax, see [Code, placeholders, and command line](#code-placeholders-and-command-line).

## Formatting conventions

Documentation uses two date/time systems:

- **Product UI** — relative thresholds, 24-hour technical timestamps (see [Dates and times (UI)](#dates-and-times-ui) below).
- **Prose documentation** — spelled-out dates and 12-hour clock (see [Dates and times (documentation)](#dates-and-times-documentation)).

### Dates and times (documentation)

For narrative text in documentation:

- Spell out **month and day names** in full when space allows.
- Use **12-hour clock** with spaced **AM** / **PM** (*3:45 PM*); drop minutes for round hours (*3 PM*).
- Use **to** in spelled-out time ranges (*five to ten minutes ago*).
- Give the **full four-digit year** (*January 19, 2017*).
- Optional day of week before month: *Tuesday, April 27, 2021*.
- When abbreviating for space, abbreviate **both** day and month consistently (*Mon, Sep 3, 2018*).
- **Avoid numeric-only dates** (*04/05/09*) — ambiguous across locales.
- If numeric dates are required, use **YYYY-MM-DD** (*2017-04-15*).
- **Avoid seasons**; use months, quarters, or temperatures.
- Spell out time zones when needed; include UTC or GMT parenthetically.
- Mid-sentence dates: comma after year (*January 19, 2017, release*); no comma for month-year only (*January 2017 release*).

### Dates and times (UI)

For in-product display (Workbench, Console, and similar):

**General format**: `MMMM D YYYY` — November 16, 2022

**With time**: `MMMM D YYYY, h:mm:ss` — November 16, 2022, 2:32:59 pm

**Technical/ISO**: `YYYY-MM-DDTHH:mm:ss.SSSSSSZ`

**Limited space**: Abbreviate month; show full date/time in tooltip.

**Relative display thresholds**:

| Age | Display |
| --- | --- |
| 0–60 sec | Just now |
| 1–59 min | x min |
| 1–24 hr | x hour(s), x min |
| 24–48 hr | x hours |
| 2–7 days | x days |
| > 7 days | Month D, YYYY |

### Numbers

| Rule | Example |
| --- | --- |
| Use numerals for ten and greater. | 12 models |
| Spell out numbers one through nine in prose (except common expressions, codes, and UI literals). | six custom metrics |
| Commas in numbers over three digits. | 3,999,110 |
| Percent sign. | 52% complete |
| Ranges. | Use *to*: five to ten days |
| Round to hundredths. | 3266.528 → 3266.53 |
| Money. | $100, $0.015 |

**Abbreviated large numbers**: Confirm engineering standards for raw vs abbreviated (3,562,294 vs 3.6M). Compact suffix forms have no space between the numeral and suffix (*3.6M*, *437kB*, *5.64GB*). Use *k* for thousand, not *K*. When spelling out the full unit, use a space (*5.64 GB*).

### Units of measurement

- Put a **space** between a number and its unit in all contexts (*100 MB*, *5 ms*, *64 GB*, *2.5 GHz*). Do not run the number and unit together (*100MB*, *64GB*).
- **No space** before `%` or `$` when attached to the number (*65%*, *$10*). For angles, no space before `°` (*180°*).
- For temperature, use *50 °C* (space between the number and the unit).
- **Ranges with units**: repeat the unit; use *to*, not a hyphen (*-40 °C to 85 °C*).
- Use *k* for thousands only with a clarifying noun (*55k download operations*).
- Disambiguate currency when needed (*US$10*).
- Prefer *per* over slash for rates; use established forms (*Gbps*, not *Gb/s*).

### File formats

File type suffixes use **one of two forms only** — do not mix styles (for example, avoid `.CSV`, `Csv`, or `csv` without a period when referring to the format):

| Form | When to use | Example |
| --- | --- | --- |
| **All caps, no period** | Format names in prose or suffixes in isolation. | CSV, PDF, XLS, JSON |
| **Lowercase with period** | Filenames and paths (default). | `10kdiabetes.csv`, `config.yaml` |

| Preferred | Avoid |
| --- | --- |
| Upload a CSV file. | Upload a .csv file. (when naming the format, not a path) |
| Save the file as `results.csv`. | Save the file as `results.CSV`. |
| Supported formats include **PDF** and **SVG**. | Supported formats include **.pdf** and **.Svg**. |

**Filenames in prose**:

- Use lowercase (*Sample superstore.tds*).
- Use a **qualifying noun** with the filename — *the `example.yaml` file*, not *`example.yaml`* alone. Applies to API descriptions, UI copy, and documentation.

### Default object names

Format: `New {{object}} {{n}}`

- New feature list two
- New experiment five

Do not use timestamps in default names.

### User names

| Context | Format |
|---------|--------|
| Default | First Last (e.g., Arnold Schwarzenegger). |
| Constrained space | A. Schwarzenegger. |
| Avatar | First initials of first and last name. |
| Fallback | Full email if name unavailable. |

Truncate with tooltip showing full name. Do not expose internal user IDs to end users.

## Standard terminology

### Action vocabulary

#### Selection and modification

| Term | Usage |
|------|-------|
| Select | Choose from a predefined list (dropdown, checkboxes). |
| Choose | Alternative to Select; e.g., *Choose file*. |
| Set | Provide a value for a higher-level outcome. |
| Enter | Provide a value in numeric or free-text input. |
| Edit | Change an existing value (default modification label). |

#### Import vs upload vs delete

| Term | Meaning |
|------|---------|
| Import | File transfer with data processing. |
| Upload | File transfer without significant manipulation. |
| Delete | Permanently remove an object. |
| Remove | Remove from selection without deleting. |
| Archive | Move to non-usable state without deleting. |

#### Cancel vs discard vs close

| Term | Meaning |
|------|---------|
| Cancel | Leave flow without changes. |
| Discard | Leave flow; user input will be lost. |
| Close | Localized view; context easily reopened. |
| Exit | Final departure from application. |
| Done | Rich container where user was heavily involved. |

#### Setup vs settings

| Term | Usage |
|------|-------|
| Setup | Section label for onboarding / first-time configuration. |
| Set up experiment | Task name. |
| Settings | Global application parameters. |
| Configure | Advanced detailed parameters (also used in input labels; see [Input fields](#input-fields)). |

#### Given vs configured

| Term | Meaning |
|------|---------|
| Given | No user involvement. |
| Configured | User-edited or provided through prompts. |

#### Creation and movement

| Term | Meaning |
|------|---------|
| Create | New object in current view. |
| Add | Object exists elsewhere; adding to current view. |
| Generate | DataRobot creates object (backend work). |
| Export | Configure and review before download. |
| Download | Immediate download to local machine. |
| Duplicate | Preferred over *Copy* for creating another instance. |

### Data terminology

| Term | Definition |
|------|------------|
| Data source | Origin of data. |
| Data | Individual pieces. |
| Dataset | Structured collection for ML tasks. |

**Flow**: Data sources → Data extracted/processed → Datasets for tasks

### Features vs columns

- **Column** — raw attribute in tabular data.
- **Feature** — column or derived/transformed attribute used for modeling.

### Standardized terms (use these forms)

| Preferred | Avoid |
|-----------|-------|
| Train new model | Start tuning, Build tuned model, Run search grid. |
| Hostname | — |
| Open documentation | Link to documentation, Documentation. |
| Downloading large files | Large files downloading. |
| Accepted values | Valid values, Allowed values. |
| Export to notebook | Use data in notebook, Use in notebook. |
| Permutation | permutations. |
| Compute method | Compute using, Computation method. |

### Model actions (consistent verbs)

Register, delete, select, include, test, train, blend, deprecate, reset (for example, *Train new model*, *Blend selected models*).

## Content best practices

### Minimum viable content

Provide enough information for users to complete tasks — not so much that they are overwhelmed, not so little that they are confused. Consider user **intent** and **context**. Before adding explanatory copy, ask whether the experience can be simplified so less explanation is needed.

### Paragraph structure and scannability

- One idea per paragraph; often five or six sentences maximum.
- Put the most important information first at the section, paragraph, and sentence level.
- Use headings, lists, and visual hierarchy — most readers scan rather than read word-for-word.

| Preferred | Avoid |
|-----------|-------|
| Network health: Moderate risk detected | Our advanced cybersecurity monitoring system has conducted an exhaustive scan… |

For layout rules (left-align, line breaks, sentence length), see [Accessibility](#accessibility).

### Local consistency

Follow patterns within a container (e.g., all Autopilot setting descriptions use the same format). Global consistency across the platform is ideal but local consistency is the minimum bar. For disputed terms, see [Standard terminology](#standard-terminology) or contact **#content-design-systems** on Slack.

## GitHub Markdown authoring

Conventions for Markdown files rendered on GitHub (README files, wikis, `.md` docs in repositories).

### Supported features (use these)

| Feature | Syntax | Notes |
| --- | --- | --- |
| Headings | `#` through `######` | One H1 per document; GitHub auto-generates anchor links. |
| Emphasis | `*italic*`, `**bold**`, `` `code` `` | Prefer `**` for bold, not `__`. |
| Links | `[text](url)` or `[text](path/to/file.md)` | Include `.md` for repo-relative doc links. |
| Images | `![alt text](path/to/image.png)` | Alt text is required for accessibility. |
| Lists | `-`, `*`, `1.` | Task lists: `- [ ]` / `- [x]` |
| Tables | GFM pipe tables | Introduce tables in prose before the table. |
| Code fences | ` ```lang ` … ` ``` ` | Always specify a language tag when known. |
| Blockquotes | `> quoted text` | Use for notes, warnings, and callouts (see below). |
| Collapsible | `<details>` / `<summary>` | Supported HTML; use for optional or lengthy content. |
| Mermaid | ` ```mermaid ` … ` ``` ` | Supported on GitHub for diagrams; prefer text for essential information. |

### Callouts (replacing MkDocs admonitions)

GitHub does not support `!!! note` or `??? tip` syntax. Use blockquotes or collapsible sections:

**Note, tip, or supplemental information**:

```markdown
> **Note:** Useful but non-required information.
```

**Warning or potential data loss**:

```markdown
> **Warning:** This action cannot be undone.
```

**Required action or high-consequence outcome**:

```markdown
> **Important:** Back up the configuration before proceeding.
```

**Long optional content** (for example, release feature lists):

```markdown
<details>
<summary>Feature summary</summary>

- Feature one
- Feature two

</details>
```

### Structure and formatting

- Use **Markdown**, not HTML, unless GFM does not support the feature (for example, `<details>`).
- Use **single blank lines** between blocks (headings, paragraphs, lists, tables, fences).
- Do not use YAML frontmatter unless your tooling requires it — GitHub ignores most frontmatter in rendered Markdown.
- Do not use horizontal rules (`---`) as section separators unless separating unrelated content; blank lines are sufficient.
- Do not use `{ target=_blank }`, `{: #anchor }`, or other MkDocs/Pymdown attribute extensions — they render as literal text on GitHub.

### Diagrams

- **Mermaid** diagrams work in fenced `mermaid` blocks on GitHub.
- Prefer text and tables for simple relationships; do not put essential information only in a diagram.

### Reusable content

- Copy shared snippets directly into each file, or maintain snippets in separate `.md` files and link to them.
- GitHub does not support Jinja `{% include %}` or conditional includes in standard Markdown rendering.

## Platform and deployment terminology

Use official product names consistently. Do not invent shorthand (for example, *SM*, *NG*) in customer-facing documentation. Product feature names (Autopilot, Leaderboard, and similar) are in [DataRobot proper nouns](#datarobot-proper-nouns-capitalize-in-descriptions).

| Term | Usage |
| --- | --- |
| DataRobot | Company and product name (always capitalized). |
| DataRobot AI Platform | The end-to-end platform (umbrella term). |
| Managed AI Platform | SaaS-hosted offering (single-tenant or multi-tenant); acceptable in release announcements. |
| Self-Managed AI Platform | Customer-managed installation (on-premises or private cloud). |
| SaaS | Acceptable when distinguishing cloud from self-managed; spell out on first use in install-focused docs if needed. |
| Workbench | NextGen UI for building experiments and use cases. |
| Console | NextGen UI for deployment operations and monitoring. |
| Registry | NextGen UI for models, environments, jobs, and applications. |
| AI Catalog | Data asset catalog (proper noun). |

When a feature spans NextGen surfaces, state availability explicitly (for example, *In Workbench…* / *In Console…*) or use separate headings for each variant.

## Release notes and announcements

Release content is an **exception** to [Timeless documentation](#timeless-documentation): dates, version numbers, and *new* / *preview* / *GA* are expected.

| Content type | Conventions |
| --- | --- |
| SaaS monthly announcements | Month and year in title and body; link to related Self-Managed release notes when relevant. |
| Self-Managed version notes | Version in the title (for example, *Version 11.5.0*); group by capability (Agentic AI, MLOps, and so on). |
| Maintenance releases | Lead with version; reference parent feature release. |

Use a collapsible **Feature summary** section or a table with a **NextGen** availability column when listing many features. Link each feature to its anchored subsection on the same page.

Issue-fix sections use present tense for resolved bugs (*Fixes an issue where…*). Use present tense for ongoing behavior elsewhere in the document.

## Quick reference

Section index for common authoring contexts. Follow the linked section for full rules.

| Context | Primary sections |
| --- | --- |
| UI copy | [UI copy](#ui-copy), [Words to avoid](#words-to-avoid), [Voice and tense](#voice-and-tense) |
| API / SDK | [API and SDK documentation](#api-and-sdk-documentation), [Code in text](#code-in-text) |
| Error messages | [Error messages](#error-messages) |
| Technical docs | [Documentation voice](#documentation-voice), [Technical documentation](#technical-documentation) |
| GitHub Markdown | [GitHub Markdown authoring](#github-markdown-authoring) |
| Release notes | [Release notes and announcements](#release-notes-and-announcements), [Timeless documentation](#timeless-documentation) |

## Appendix: Google alignment gaps

DataRobot adopts most [Google Developer Documentation Style Guide](https://developers.google.com/style) practices. Intentional divergences:

| Topic | Google | DataRobot |
| --- | --- | --- |
| Person (*we*) | *We* acceptable in documentation. | Never use *we* / *our*; use *DataRobot* — see [First and second person](#first-and-second-person-we-you). |
| Person (*you*) | *You* common in documentation. | Minimize *you* / *your* in all contexts; prefer imperatives — see [First and second person](#first-and-second-person-we-you). |
| Contractions | Encouraged for friendly tone. | See [Contractions](#contractions). |
| Passive voice | Prefer active. | API forbids passive in API descriptions. |
| Ellipses | Avoid in general prose. | See [Ellipses](#ellipses) — allowed for UI loading states. |
| Command prompt `$` | Recommended for multi-line CLI. | See [Code, placeholders, and command line](#code-placeholders-and-command-line). |
| Exclamation points | Rare in docs. | See [Words to avoid](#words-to-avoid) — forbidden in UI. |
| Reading level | ~Fifth-grade target. | Technical audience; see [Audience assumptions](#audience-assumptions). |

## Document history

| Date | Change |
| --- | --- |
| 2026-05-27 | GitHub Markdown edition derived from [datarobot-style-guide.md](datarobot-style-guide.md). |
