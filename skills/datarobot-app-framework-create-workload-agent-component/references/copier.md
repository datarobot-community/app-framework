# Copier / component specifics

## Keep questions minimal

Every prompt is friction. Ask only for what genuinely can't be defaulted, derived, or edited in code
afterward. For this kind of component that's essentially two user questions: the **app name** and the
**container image URI** (plus the `base`/`llm` answers-file paths for `_external_data`). Everything
else — port, instructions, model, importance, replicas, autoscaling, whether to build — is a
**constant in a `Tunables` block in the rendered infra/app** (or env-driven), not a question. The
image build is always part of `task deploy`; don't make it a question.

## Files

- `copier-module.yaml`: `module`, `short_description`, `repeatable: true`,
  `depends_on: {base: {url}, llm: {url}}`.
- `copier.yml`: questions; a hidden derived var
  `name_file: {default: "{{name|lower|replace('-','_')}}", when: false}` for python file naming;
  `_external_data: {base: "{{base_answers_file}}", llm: "{{llm_answers_file}}"}`; `_subdirectory: template`.
- `_answers_file` — because the component is **one-to-many** (`repeatable: true`), every instance must
  write a distinct answers file, so include a fixed component prefix AND the instance name:
  `_answers_file: ".datarobot/answers/<component>-{{name}}.yml"`. Matches the ecosystem convention
  (`llm-<name>.yml`, `fastapi-<name>.yml`); a bare `{{name}}.yml` collides across instances and breaks
  `dr component update`. Other components reference yours via this exact path (e.g. an `llm_answers_file`
  answer defaulting to `.datarobot/answers/llm-llm.yml`).

## `template/` conventions

- Path templating: `{{ var }}` in file/dir names; `.jinja` suffix is stripped after render; use
  `.jinja.jinja` for files that must keep Jinja at runtime.
- Layout: `infra/infra/` (Pulumi), `.datarobot/cli/<name>.yaml` (runtime params), `docs/<name>.md`.
- Read base answers via `{{ _external_data.base.template_name }}`, `{{ _external_data.base.copyright_year }}`.

## Executable scripts

`chmod +x` the source `*.sh`/`*.sh.jinja` and `git update-index --chmod=+x` them (commit mode `100755`);
Copier preserves the bit on render, so `create="./build-image.sh"` and `CMD ["./start.sh"]` work.
