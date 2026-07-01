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
pinned_image_uri = image_digest.stdout.apply(
    lambda d: image_repo + ":" + image_tag + "@" + d.strip())
# then: image_uri=pinned_image_uri
```
Note the *inverted* dependency direction vs. the credential/entity-id workaround in gotcha 4 below:
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
                environment_vars=[
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_API_TOKEN", source="dr-credential",
                        dr_credential_id=cred_id, key="apiToken"),
                    datarobot.ArtifactSpecContainerGroupContainerEnvironmentVarArgs(
                        name="DATAROBOT_ENDPOINT", source="string", value=endpoint),
                    # ...more source="string" vars; OMIT any whose value == "" (see gotchas)...
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
4. **`environmentVars` must be fully KNOWN at plan time — resolve ids eagerly, don't pass Outputs.**
   The Artifact provider validates each env var during `preview` and tolerates neither unknown *leaf*
   values (a freshly-created credential's `.id`, a use-case-derived entity id → `Missing
   dr_credential_id` / `Missing value`) nor a wholly-unknown list wrapped in `Output.all(...).apply(...)`
   (→ `Value Conversion Error`). So a normal single-pass `pulumi up` fails. **Fix: resolve values to
   concrete strings via the DataRobot REST API at plan time** (token + endpoint are known env vars),
   instead of creating Pulumi resources with unknown ids:
   ```python
   import datarobot as dr
   client = dr.Client(token=token, endpoint=endpoint)
   # idempotent upsert → concrete credential id (no plaintext token in Pulumi state)
   creds = client.get("credentials/").json().get("data", [])
   cred_id = next((c["credentialId"] for c in creds
                   if c["name"] == NAME and c["credentialType"] == "api_token"), None) \
             or client.post("credentials/", data={"name": NAME, "credentialType": "api_token",
                                                   "apiToken": token}).json()["credentialId"]
   # entity id: prefer DATAROBOT_DEFAULT_USE_CASE; else look up the project Use Case by name; else ""
   ```
   Then `dr_credential_id=cred_id` and `DATAROBOT_ENTITY_ID=f"experiment_container-{uc_id}"` are plain
   strings → single-pass `task deploy` works. Trade-offs: the eager credential lives outside Pulumi's
   graph (name it per-stack, idempotent; `pulumi destroy` won't remove it), and on a first deploy the
   Use Case may not exist yet so entity id is omitted (tracing attaches once it does, or immediately if
   `DATAROBOT_DEFAULT_USE_CASE` is set). REST writes during `preview` are the deliberate cost of single-pass.
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
