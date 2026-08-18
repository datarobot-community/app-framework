# Grammar and punctuation

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
- When *i.e.* or *e.g.* appear in non-code prose, always follow with a comma.

  | Preferred | Avoid |
  | --- | --- |
  | Use a deployment label (e.g., `prod`) for production. | Use a deployment label (e.g. `prod`) for production. |
  | The service retries transient errors (i.e., timeouts and 503 responses). | The service retries transient errors (i.e. timeouts and 503 responses). |

  Exception: inside code blocks, inline code, or literal strings, follow the code convention — do not insert commas into code tokens.
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
