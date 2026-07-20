# UI copy

### Buttons and action labels

**Structure**:

- **Action buttons** — verb-based: Search, Save, Upload, Filter.
- **Menu buttons** — noun or noun/verb; menu items are verb-based.

**Rules**:

| Rule | Guidance |
|------|----------|
| Case | [Sentence case](grammar-and-punctuation.md#sentence-case). |
| Length | One to three words, one line; plan for ~50% text expansion in other languages. |
| Articles | Drop *a* and *the* for conciseness (*Reset password*, not *Reset the password*). |
| Specificity | [Words to avoid (UI-specific)](words-to-avoid.md#ui-specific) — use *Delete* / *Cancel*, not *Yes* / *No*. |
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

- Follow [Periods](grammar-and-punctuation.md#periods); use for essential instructions — tooltips for supplemental definitions.
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
| Loading | Ongoing action; start with verb + [ellipsis](grammar-and-punctuation.md#ellipses). | Importing dataset… |

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
