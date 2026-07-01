# Pulumi: build, Artifact + Workload (Python `pulumi_datarobot`)

The infra module is always Python (it is `base`'s IaC), regardless of the app's language.

## Build & push the image as part of `task deploy` (always — not a question)

Don't make users push manually. Base's infra already depends on `pulumi-command`, so add a
`pulumi_command.local.Command` that runs the build, and have the Artifact `depends_on` it (so the
image exists before the Workload starts):
```python
import pulumi, pulumi_command as command
build = command.local.Command(f"{NAME} Build Image",
    create="./build-image.sh",
    dir=str(app_dir), environment={"IMAGE_URI": IMAGE_URI},
    triggers=[source_hash(app_dir), IMAGE_URI])   # rebuild only when source/uri changes
artifact = datarobot.Artifact(..., opts=pulumi.ResourceOptions(depends_on=[build]))
```
Requires local Docker logged in to the registry. (`pulumi_docker.Image` also works but adds a dep to
base's infra `pyproject.toml`, which a component can't edit — `pulumi-command` is already present.)
CI that pushes separately can delete this Command + the Artifact's `depends_on`.

### Pin `image_uri` to the digest just pushed (avoid a stale-tag pull)

A mutable `:tag` isn't enough — the registry or the Workload API's own pull path can still resolve
the tag to a previously-cached image instead of the one just pushed, so the workload silently keeps
running old code. Fix: resolve the digest the tag *now* points to (right after the push) and pin
`image_uri` to `repo:tag@sha256:...`, so the pull is content-addressed and can never be stale.
`docker images --digests` only reads the **local** image store — empty here, since a
`docker buildx build --push` (no `--load`) never populates it. Query the registry instead:
```python
image_digest = command.local.Command(f"{NAME} Image Digest",
    create='docker buildx imagetools inspect "$IMAGE_URI" --format "{{.Manifest.Digest}}"',
    environment={"IMAGE_URI": IMAGE_URI},
    triggers=[build.stdout])          # re-run only when the build actually reran

image_repo, _, image_tag = IMAGE_URI.rpartition(":")

def _pin_digest(digest):
    # digest is None when this Command didn't actually run — e.g. a
    # `--target`-scoped/dev-mode deploy that legitimately excludes it.
    # Fall back to the plain tag instead of crashing on `.strip()`.
    if not digest or not digest.strip():
        return IMAGE_URI
    return image_repo + ":" + image_tag + "@" + digest.strip()

pinned_image_uri = image_digest.stdout.apply(_pin_digest)
# then: image_uri=pinned_image_uri
```
**Must tolerate `--target`-scoped deploys.** Any DataRobot dev workflow that runs a targeted
`pulumi up` (e.g. a `deploy-dev` task that only targets certain resources) still executes this
entire Python program to build the resource graph — it just skips *applying* untargeted resources.
An untargeted `command.local.Command` never runs its `create` script, so its `.stdout` Output
resolves to `None`, and any `.apply()` reading it (here, or anywhere else in the file) must handle
that instead of assuming the command always ran. The unguarded version above crashes with
`AttributeError: 'NoneType' object has no attribute 'strip'` the moment a dev workflow doesn't
target the image build — not a preview/up-specific bug, a "does this program work under partial,
targeted deploys" bug. Audit every `.apply()` on a `Command`'s `.stdout`/`.stderr` for this.

Note the *inverted* dependency direction vs. the self-provisioned-credential case in gotcha 4 below:
there, an unknown Output had to be resolved to a concrete string outside Pulumi's graph before the
Artifact was even declared. Here `pinned_image_uri` stays a genuine Pulumi `Output[str]` (unknown at
`preview`) and is passed straight into `image_uri=` — verified working with a real `pulumi preview`.
Unlike `environmentVars` (gotcha 4), the Artifact provider does **not** reject an unknown top-level
`image_uri`, so no eager REST-style resolution is needed here.

If templating this inside a Jinja `.jinja` infra file, wrap the Go-template braces in
`{% raw %}{{.Manifest.Digest}}{% endraw %}` (a bare `{{.Manifest.Digest}}` gets parsed as a Jinja
expression and breaks rendering), and build `pinned_image_uri` with `+` string concatenation rather
than an f-string — an f-string's `{name}` sitting directly against a Jinja `{{ name }}` substitution
is easy to get wrong (stray/mismatched braces once rendered).

## Artifact + Workload

`Artifact` = immutable *what runs*; `Workload` = *runtime* (replicas/resources).
```python
import pulumi_datarobot as datarobot

artifact = datarobot.Artifact(
    f"{NAME} Artifact",
    type="service",
    spec=datarobot.ArtifactSpecArgs(container_groups=[
        datarobot.ArtifactSpecContainerGroupArgs(containers=[
            datarobot.ArtifactSpecContainerGroupContainerArgs(
                name="main", image_uri=IMAGE_URI, primary=True, port=PORT,
                # Unlike Custom Applications/Models, the Workload API does NOT auto-inject
                # DATAROBOT_API_TOKEN/DATAROBOT_ENDPOINT — declare them explicitly. See gotcha 4.
                environment_vars=[
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_API_TOKEN", source="string", value=token),
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_ENDPOINT", source="string", value=endpoint),
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="LLM_DEFAULT_MODEL", source="string", value=default_model),
                    # ...more source="string" vars (LLM wiring, app-specific config); OMIT any whose
                    # value == "" (see gotcha 3)...
                ],
                readiness_probe=datarobot.ArtifactSpecContainerGroupContainerReadinessProbeArgs(
                    path="/health", port=PORT, initial_delay_seconds=10, period_seconds=10),
                liveness_probe=datarobot.ArtifactSpecContainerGroupContainerLivenessProbeArgs(
                    path="/health", port=PORT, initial_delay_seconds=30, period_seconds=30),
            )])]))

workload = datarobot.Workload(
    f"{NAME} Workload",
    artifact_id=artifact.artifact_id,           # ← .artifact_id (DataRobot id), NOT .id (Pulumi UUID)
    importance="low",                           # low|moderate|high|critical
    runtime=datarobot.WorkloadRuntimeArgs(container_groups=[
        datarobot.WorkloadRuntimeContainerGroupArgs(
            # NO name= here — runtime container-group name is read-only (server sets "default")
            replica_count=1,                    # OR autoscaling=... (mutually exclusive)
            containers=[datarobot.WorkloadRuntimeContainerGroupContainerArgs(
                name="main",                    # MUST match the artifact container name
                resource_allocation=datarobot.WorkloadRuntimeContainerGroupContainerResourceAllocationArgs(
                    cpu=1.0, memory=2 * 1024**3))])]))  # memory in BYTES, not Mi/Gi
```

Autoscaling instead of `replica_count`:
```python
autoscaling=datarobot.WorkloadRuntimeContainerGroupAutoscalingArgs(enabled=True, policies=[
    datarobot.WorkloadRuntimeContainerGroupAutoscalingPolicyArgs(
        scaling_metric="cpuAverageUtilization", target=70, min_count=2, max_count=8)])
```

- Inspect the live schema: clone `datarobot-community/pulumi-datarobot` and read
  `provider/cmd/pulumi-resource-datarobot/schema.json` (resources `Artifact`, `Workload`).
- GPU/VRAM: set `resource_bundles=["gpu.l4.small"]` on the runtime container group instead of cpu/memory.

## Gotchas (each fails the deploy — all verified against the live API)

1. **`artifact.artifact_id`, not `artifact.id`.** The Pulumi `.id` is an internal UUID; the Workload
   API rejects it as `422 … artifactId … invalid ID`. Use the `.artifact_id` output.
2. **Never set the runtime container-group `name`.** It is read-only (server-assigns `default`);
   setting it → `Invalid Configuration for Read-Only Attribute … runtime.containerGroups[0].name`.
   (The container *inside* it still needs `name=` matching the artifact's container.)
3. **Drop empty-string env vars.** A `source="string"` var with `value=""` → `422 … Field required`.
   Build the string vars in a dict and emit only non-empty ones; let app defaults cover the rest.
4. **`environmentVars` must be fully KNOWN at plan time — never pass a Pulumi Output.** The Artifact
   provider validates each env var during `preview` and rejects unknown *leaf* values with `Missing
   value`/`Missing dr_credential_id`, or a wholly-unknown list wrapped in `Output.all(...).apply(...)`
   with `Value Conversion Error`. Ways this actually happens, and how DATAROBOT_API_TOKEN/ENDPOINT are
   the exception:
   - **DATAROBOT_API_TOKEN / DATAROBOT_ENDPOINT are NOT auto-injected — unlike Custom
     Applications/Models, the Workload API does not put these into the container unless you ask.**
     (An earlier version of this guidance said the platform injects them automatically; that was
     wrong.) The DataRobot REST API itself supports a `source="api-key"` env var that has the
     platform inject a live token with no `value` needed — but `pulumi_datarobot`'s
     `ArtifactSpecContainerGroupContainerEnvironmentVarArgs` doesn't expose that source type yet (its
     `source` field only documents `"string"`/`"dr-credential"`; passing `"api-key"` anyway either
     fails client-side validation or is silently unsupported depending on provider version — don't
     rely on it). So both vars are passed through as plain `source="string"` values, read from
     infra's own deploy-time environment — the same live token/endpoint `dr dotenv setup` already
     populated there:
     ```python
     token = os.environ["DATAROBOT_API_TOKEN"]
     endpoint = os.environ.get("DATAROBOT_ENDPOINT", "").rstrip("/")
     # ...then source="string", value=token / value=endpoint in environment_vars.
     ```
     This also means the REST-eager-credential-resolution pattern (`dr.Client(...)` + upserting an
     `api_token` credential to get a concrete id for `source="dr-credential"`) is unnecessary for
     this var — don't add that complexity back for `DATAROBOT_API_TOKEN`. Revisit
     `source="api-key"` once `pulumi_datarobot` actually supports it; until then this plain
     pass-through is the correct pattern, not a workaround to later remove.
   - **`OTEL_ENTITY_ID`: still don't try to supply this.** The platform injects it
     (`experiment_container-<use_case_id>`) once a Use Case is attached to the stack — empty before
     that, and the app should skip OTel export gracefully rather than send with a blank entity id, not
     error. This one is unaffected by the DATAROBOT_API_TOKEN/ENDPOINT correction above.
   - **A genuinely new Pulumi-managed resource's id, e.g. `LLM_DEPLOYMENT_ID` sourced from
     af-component-llm's `custom_model_runtime_parameters`.** Several `llm` configurations (anything
     that provisions its own Blueprint/Deployment, e.g. `blueprint_with_llm_gateway`) set that
     parameter's value to `some_deployment.id` — a `datarobot.Deployment` created in the *same*
     `pulumi up`, so its `.id` is an unresolved Output at this point in your program, not a string.
     Passing it straight into `environment_vars` hits exactly this "Missing value" error. Fix: when
     reading such a value, require `isinstance(value, str)` before using it, and treat anything else
     (an Output) as unavailable — filter it out of `environment_vars` like any other empty value (see
     gotcha 3), rather than trying to resolve it. For configs like this, falling back to the LLM
     Gateway when the deployment id isn't a known string is *correct* behavior, not a workaround: those
     configs still set `USE_DATAROBOT_LLM_GATEWAY=1`, meaning DataRobot's governance for the
     Blueprint/Deployment happens behind the Gateway, not by the app calling the deployment directly.
     (A credential *you* provision, with no platform `source` equivalent, is the one case where eager
     REST resolution at plan time — upsert via `dr.Client`, get a concrete id, use
     `source="dr-credential"` — is still the right pattern.)
5. **Destroy order.** Creating an Artifact auto-locks it (`status=locked`, `version=1`); `pulumi
   destroy` fails `409 … still used by workloads` if a workload (even a failed one) references it —
   delete the workload first (`DELETE /workloads/{id}/`).
6. **Image must be pullable by DataRobot.** A private `ghcr.io`/registry image (anonymous
   `GET …/manifests/<tag>` → `401`) leaves the workload `errored` with the container `waiting`,
   `restarts=0`, and no app logs — an image-pull failure, not a code bug. Make the image public (or use
   a pre-configured registry); the Workload API takes no pull creds at create.

## Export the actionable serving URL, not just the id

The Workload's authenticated endpoint is `{DATAROBOT_ENDPOINT}/endpoints/workloads/{workload_id}/`
(call with `Authorization: Bearer <token>`). Export the base plus concrete routes so `pulumi up`
output is directly usable:
```python
ep = workload.id.apply(lambda wid: f"{endpoint}/endpoints/workloads/{wid}/")
export("…_ENDPOINT_URL", ep)
export("…_CHAT_COMPLETIONS_URL", pulumi.Output.concat(ep, "v1/chat/completions"))
export("…_AG_UI_URL", pulumi.Output.concat(ep, "ag-ui"))
```
Keep the apply variable short (e.g. `ep` / `_endpoint_url`, not `<longname>_endpoint_url`) so the
`Output.concat(...)` lines stay under the formatter's line length regardless of the agent name.
