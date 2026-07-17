# Code in text

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
- File type suffixes in isolation when all caps with no period (**PDF**, **CSV**); see [File formats](formatting-conventions.md#file-formats).

### Method names

- Omit the class name when unambiguous: call `get()`, not `animal.get()`.
- Add empty parentheses to indicate a method: `close()`, not *close*.

### Do not inflect code terms

Do not use code keywords as verbs or make them possessive.

| Preferred | Avoid |
| --- | --- |
| Send a `POST` request. | `POST` the data. |
| Call `open()` before `close()`. | `Close`()ing requires `open`()ing first. |

For fenced code blocks, placeholders, and command-line syntax, see [Code, placeholders, and command line](technical-documentation.md#code-placeholders-and-command-line).
