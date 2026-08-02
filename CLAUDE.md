# CLAUDE.md

Read [AGENTS.md](AGENTS.md) before working in this repository. It is the single set of
instructions for AI agents here and covers:

- What this repository holds and how it is laid out.
- Building, serving, and publishing the documentation site.
- Regenerating and verifying the architecture diagram, the method behind it, and the public
  sources its content was harvested from.
- Keeping `skills/`, the docs pages, the diagram, and `README.md` in sync.
- The review every published change must pass. The shallow review — public-repository and link
  checks, plus a read against the recurring-defects list — runs on every change. The full
  adversarial review runs only when the user asks for it.
- The checks to run before committing.

Everything in this repository is published — the docs site is public and `skills/` is installed
into third-party AI assistants. Treat every file here as external-facing.

Repository-specific rules in AGENTS.md take precedence over general preferences. Where
AGENTS.md is silent, fall back to the global standards in `~/.claude/CLAUDE.md`.
