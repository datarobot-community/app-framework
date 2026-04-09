# Design Principles

The App Framework is built for mid-maturity developers and data scientists to hit the ground running. These principles guide every decision:

**1. Batteries Included — Not so DRY**
If a consumer of an app template needs to modify something and that code lives elsewhere, re-evaluate. Co-location beats indirection. We'll know we've broken this when we start getting PRs to installable shared libraries.

**2. Minimize Startup Friction**
Getting started is where we lose users. Make configuration easy, reduce README steps with automation and product features.

**3. Rapid Iteration is King**
Fast iteration cycles for the most common customizations makes development enjoyable. Custom models, Flask servers, Vite — changes should be instant. Set expectations clearly when something can't be fast.

**4. Nerdy is Great**
We're building for developers. If it's enjoyable to use, chances are customers will enjoy it too (unless it's too obtuse).

**5. DataRobot API Token is All You Need**
Everything but AI (and storage, hopefully) is easy to swap out for preferred technology stacks. One credential to rule them all.

**6. Make Updates Easy**
With many templates and many clones, automated/guided updates are essential. File structure, dependency isolation, and tools like `copier` are critical for merge-conflict-free updates.

**7. Monorepos not Monoliths**
An app template is multiple services, custom models, and notebooks together. Each top-level folder must stay completely independent with its own dependency definitions. Separate deps for each. Modern, fast tooling: `uv`, `pnpm`, `wasm`.

**8. The Project Management Triangle**
- *App Templates:* Fast and Cheap — App authors make them Good
- *App Framework (ATDK):* Good and Cheap — App Template authors make them Fast
- *CLI:* Good and Cheap — delivered fast for App authors
