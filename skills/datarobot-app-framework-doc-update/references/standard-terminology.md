# Standard terminology

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
| Configure | Advanced detailed parameters (also used in input labels; see [Input fields](ui-copy.md#input-fields)). |

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
