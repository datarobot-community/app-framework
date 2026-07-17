# Formatting conventions

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
