# LLM access (from af-component-llm)

**Import the LLM config from the llm component's infra module — don't reconstruct it from prefixed
env vars.** Every af-component-llm configuration (gateway, deployed, blueprint, …) renders an
`infra/infra/<llm_app_name>.py` that exports the SAME two symbols: `default_model` (the litellm model
id) and `custom_model_runtime_parameters` (a list of runtime-param args with `.key`/`.value`,
including the deployment id and `USE_DATAROBOT_LLM_GATEWAY`). So the Python infra just imports them —
robust across all llm configs, no string-prefix guessing:

```python
from .{{ _external_data.llm.llm_app_name }} import custom_model_runtime_parameters as llm_custom_model_runtime_parameters
from .{{ _external_data.llm.llm_app_name }} import default_model

def _llm_component_config_value(key):           # read one runtime param by key
    for p in llm_custom_model_runtime_parameters:
        if isinstance(p.key, str) and p.key == key:
            return None if isinstance(p.value, str) and not p.value else p.value
    return None

llm_deployment_id = _llm_component_config_value(
    "{{ _external_data.llm.llm_app_name | upper }}_DEPLOYMENT_ID") or ""
```

Two separate `from .<name> import …` lines (don't pre-combine into one parenthesized import): ruff's
isort leaves them split because `combine-as-imports` is off by default, and `default_model` is imported
unaliased — matching the `af-component-agent` reference.

**Requires `_external_data.llm` in `copier.yml`** — without it `{{ _external_data.llm.llm_app_name }}`
renders empty and you get a broken `from . import …`:
```yaml
_external_data:
  base: "{{ base_answers_file }}"
  llm: "{{ llm_answers_file }}"
```
`{{ _external_data.llm.llm_app_name }}` resolves to the active llm module (base symlinks the chosen
config to `infra/infra/<name>.py`); importing it also orders llm resources before yours. The module
only exists once the llm dependency is rendered — fine in a real project (base+llm are required deps)
and under `task validate`; a standalone `copier copy` without deps renders the empty `from .` form.
(Re-injecting via prefixed `os.environ.get(f"{PREFIX}_DEPLOYMENT_ID")` is brittle — avoid it.)

## OpenAI-compatible base URLs (api key = `DATAROBOT_API_TOKEN`)

- **Gateway**: `{DATAROBOT_ENDPOINT}/genai/llmgw` — client appends `/chat/completions`. Model = a
  gateway catalog id, e.g. `azure/gpt-4o-mini` (list: `GET {DATAROBOT_ENDPOINT}/genai/llmgw/catalog/`).
- **Deployment**: `{DATAROBOT_ENDPOINT}/deployments/{id}` — client appends `/chat/completions`; model
  name is ignored.

litellm note (Python only): the `datarobot/` provider appends the gateway path *itself*, so pass
`api_base={DATAROBOT_ENDPOINT}` (bare) and model `datarobot/<catalog-id>`. A plain OpenAI-style client
in any language must NOT use the `datarobot/` prefix and DOES point base_url at the `/genai/llmgw` (or
`/deployments/{id}`) URL above.
