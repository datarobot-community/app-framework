# Workload contract: container + HTTP endpoints

Language-independent — the app can be Go/JVM/TS/Python/etc. This is the surface every language must
satisfy; the Pulumi infra (always Python) is in `pulumi.md`.

## Container

- Image MUST have a **linux/amd64** manifest. Build: `docker buildx build --platform linux/amd64 -t <ref> --push .`
- Listen on an HTTP port **≥ 1024** (the Workload injects `PORT`; bind it). Don't default to `8080`
  (or `3000`, `5000`, `8000`) for the app's own `DefaultPort`/local-dev fallback — those are exactly
  the ports other local services/proxies/dev tools already commonly claim, causing "address already
  in use" the moment a dev runs `task dev`/`docker compose up` alongside anything else. Pick something
  in **8100–8200** instead. Whatever you pick, it must be a single overridable value, not a literal
  copy-pasted into every file that mentions it — the Dockerfile's `EXPOSE` (documentation only, not
  enforced), `docker-compose.yml`'s host+container port mapping, the app's own `DefaultPort` fallback,
  and the infra `PORT` Tunable **all read from the one $PORT env var / one chosen literal**, so
  changing it later, or a developer overriding it locally, is a one-variable change, not a grep-and-
  replace across four files.
- `GET /health` returns 200 quickly — used by readiness/liveness probes.
- Image must live in a registry DataRobot can pull (public, or one the org pre-configured). The
  Workload API does not yet take image-pull credentials at create time.

## HTTP endpoints (wire protocols — implement in any language)

**OpenAI Chat Completions** — `POST /v1/chat/completions`, body `{model, messages[], stream}`.
Non-stream → `{id, object:"chat.completion", choices:[{message:{role,content}, finish_reason}]}`.
Stream → SSE `data: {object:"chat.completion.chunk", choices:[{delta:{content}}]}` then `data: [DONE]`.
Many frameworks ship a server for this; otherwise it is ~40 lines around the agent's run/stream call.

**AG-UI** — `POST /ag-ui`, SSE out. Event `type`s: `RUN_STARTED`, `TEXT_MESSAGE_START`,
`TEXT_MESSAGE_CONTENT` (`delta`), `TEXT_MESSAGE_END`, `RUN_FINISHED` (also `MESSAGES_SNAPSHOT`,
`RUN_ERROR`). Field names camelCase (`threadId`, `runId`, `messageId`). Spec: https://docs.ag-ui.com/
Some frameworks provide a native AG-UI server; the TypeScript ecosystem (CopilotKit) has first-class support.

A single agent instance can back both endpoints.

## Serving an HTML UI / browser client: use RELATIVE URLs

The workload is reached at a URL *prefix* (`{endpoint}/endpoints/workloads/<id>/`) and the container
never learns its own external URL — and you can't inject it as a runtime parameter either, because
Pulumi only knows the endpoint *after* the workload is created (dependency cycle). So a page served at
the app root that does `fetch("/ag-ui")` hits the **domain** root, not the prefix, and breaks. Resolve
API paths relative to the current page (the app root), robust to a missing trailing slash:
```js
function appUrl(path) {                       // call as appUrl("ag-ui"), appUrl("v1/chat/completions")
  const here = new URL(window.location.href);
  if (!here.pathname.endsWith("/")) here.pathname += "/";
  return new URL(path, here).href;
}
```
Same rule for any asset/link: relative (`ag-ui`, `assets/x.js`), never absolute (`/ag-ui`). Server-side
routing is unaffected — DataRobot strips the prefix, so the container still sees `/ag-ui` etc.
