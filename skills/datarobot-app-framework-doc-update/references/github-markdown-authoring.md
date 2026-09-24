# GitHub Markdown authoring

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
> **Note**: Useful but non-required information.
```

**Warning or potential data loss**:

```markdown
> **Warning**: This action cannot be undone.
```

**Required action or high-consequence outcome**:

```markdown
> **Important**: Back up the configuration before proceeding.
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
