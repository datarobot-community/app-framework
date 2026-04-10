# Design principles

The App Framework is built for mid-maturity developers and data scientists to hit the ground running. These principles guide every decision:

**1. Batteries included — not so DRY**
If a consumer of an app template needs to modify something and that code lives elsewhere, re-evaluate. Co-location beats indirection. A sign this principle is broken: PRs appear for installable shared libraries.

**2. Minimize startup friction**
Getting started is where users drop off. Make configuration easy, reduce README steps with automation and product features.

**3. Rapid iteration is king**
Fast iteration cycles for the most common customizations makes development enjoyable. Custom models, Flask servers, Vite — changes should be instant. Set expectations clearly when something can't be fast.

**4. Nerdy is great**
This framework is built for developers. If it's enjoyable to use, chances are customers will enjoy it too (unless it's too obtuse).

**5. DataRobot API token is all you need**
Everything but AI (and storage, hopefully) is easy to swap out for preferred technology stacks. One credential to rule them all.

**6. Make updates easy**
With many templates and many clones, automated/guided updates are essential. File structure, dependency isolation, and tools like `copier` are critical for merge-conflict-free updates.

**7. Monorepos not monoliths**
An app template is multiple services, custom models, and notebooks together. Each top-level folder must stay completely independent with its own dependency definitions. Separate deps for each. Modern, fast tooling: `uv`, `pnpm`, `wasm`.

**8. The project management triangle**
- *App Templates:* Fast and Cheap — App authors make them Good.
- *App Framework:* Good and Cheap — App Template authors make them Fast.
- *CLI:* Good and Cheap — delivered fast for App authors.
