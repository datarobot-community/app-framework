# Technical documentation

Standards for published technical documentation. Some rules differ from UI and API copy to support instructional prose.

### Voice, tense, and clause order

Follow [Documentation voice](purpose-and-voice.md#documentation-voice) and [First and second person](grammar-and-punctuation.md#first-and-second-person-we-you). Additional procedural patterns:

| Preferred | Avoid |
| --- | --- |
| The CLI provides authentication management. | The CLI will provide authentication management. |
| For more information, see `[Managing deployments](managing-deployments.md)`. | For more information, please see… |
- Put conditional clauses before instructions, not after.
- Use future tense only when emphasizing something that will happen later.
- Avoid placeholder phrases (*please*, *note*, *at this time*), filler (*Simply*, *It's easy*, *quickly*), and overusing *You can* / *You must* / *To do* / *Let's* at sentence starts.

### Headings and document structure

Follow [Sentence case](grammar-and-punctuation.md#sentence-case) for titles, headings, table headers, captions, and list items. Additional rules:

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
- Omit ellipsis from button labels in docs (*Browse*, not *Browse…*); see [Ellipses](grammar-and-punctuation.md#ellipses).
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
- Use **sentence case** column headers; see [Sentence case](grammar-and-punctuation.md#sentence-case). Omit articles; no ending punctuation on headers.
- Sort rows logically or alphabetically.
- Avoid tables inside numbered procedures or single-column tables (use a list instead).

For table accessibility, see [Accessibility](accessibility-and-inclusive-documentation.md#accessibility).

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

Follow [Grammar and punctuation](grammar-and-punctuation.md#grammar-and-punctuation) and [Formatting conventions](formatting-conventions.md#formatting-conventions) for commas, hyphens, and ellipses. Documentation-specific rules:

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
