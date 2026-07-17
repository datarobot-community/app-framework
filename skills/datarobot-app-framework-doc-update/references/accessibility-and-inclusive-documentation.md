# Accessibility and inclusive documentation

Write documentation so readers using screen readers, keyboard navigation, or translation tools can use it effectively.

### Accessibility

- Use semantic structure: heading hierarchy, lists for steps, tables introduced in prose.
- Introduce tables before they appear.
- Label form fields; write clear validation errors (*Name is a required field*).
- Do not rely on color or position alone to convey meaning; add text labels or icons as secondary cues.
- Avoid camelCase and ALL CAPS in prose when possible (screen readers may read letters individually).
- Do not use & instead of *and* in headings or body text (exception: UI labels that include `&`); see [Text formatting](technical-documentation.md#text-formatting).
- Left-align text; do not center or full-justify.
- Do not force hard line breaks inside sentences.
- Aim for sentences of about 26 words or fewer when practical.

### Inclusive language

- Avoid ableist figures of speech (*sanity check*, *blind to*, *cripple*, *dummy*).
- Avoid gendered terms (*man-hours*, *mankind*); for gender-neutral singular references, see [Pronouns](grammar-and-punctuation.md#pronouns).
- Avoid violent metaphors (*kill*, *hang*, *hit a wall*) and harmful jargon where simpler terms exist.
- Replace charged technical terms when possible: *allowlist* / *denylist* instead of *whitelist* / *blacklist*; write around *master* / *slave* in prose (use field names in code font only when required by code).
- Use diverse names and examples; avoid US-centric holidays, sports, or idioms unless relevant.
- Avoid seasons in global-facing docs; use months or quarters (see also [Dates and times (documentation)](formatting-conventions.md#dates-and-times-documentation)).
- When discussing disability, use respectful, person-first or identity-first language per community preference; avoid *victim of*, *suffering from*, or euphemisms like *handi-capable*.
- Do not describe people without disabilities as *normal* or *healthy*; prefer *nondisabled* or *people without disabilities* when contrast is needed.
