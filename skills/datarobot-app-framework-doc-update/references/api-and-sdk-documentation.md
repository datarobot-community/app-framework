# API and SDK documentation

Established conventions for API changelog entries, class/method descriptions, and parameter documentation apply to all API and SDK content.

Follow [Voice and tense](grammar-and-punctuation.md#voice-and-tense) (active voice; no passive in API descriptions), [Words to avoid](words-to-avoid.md#words-to-avoid), [Contractions](grammar-and-punctuation.md#contractions) (prefer positive phrasing), and [Capitalization and proper nouns](capitalization-and-proper-nouns.md#capitalization-and-proper-nouns). For filenames in prose, see [File formats](formatting-conventions.md#file-formats).

### Formatting references

For code font rules, see [Code in text](code-in-text.md#code-in-text). API-specific formatting:

| Element | Format | Example |
|---------|--------|---------|
| Parameter names in prose | Single backticks. | Either `llm_blueprint` or `chat` is required. |
| API names, classes, methods, constants in descriptions | Quoted. | Intakes the "llmBlueprintId". |
| Field names in API payloads | Untranslated API identifiers. | `llmBlueprintId`. |

### Description patterns

All descriptions begin with a capital letter and end with a period — see [Periods](grammar-and-punctuation.md#periods).

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
