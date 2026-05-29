# UI library

[dr-ui](https://dr-ui.datarobot.com/en/docs/) is the App Framework's shared React component layer. It is a [shadcn](https://ui.shadcn.com/)-compatible registry of AI-native UI components (buttons, tables, chat with AG-UI integration, theme configs, hooks) distributed as JSON artifacts and copied into your project on install.

## Why it exists

Application templates build the same complex UI patterns repeatedly: data tables, code and text editors, chat interfaces. Reinventing them per app costs weeks and produces inconsistent user experiences. dr-ui solves this by letting teams build a component once and reuse it across recipes without forking a template or depending on a versioned npm package.

The registry is shadcn-compatible, so dr-ui components coexist with the upstream shadcn library you already use. Each item is added through the standard shadcn CLI and lives in your source tree, which preserves full control over styling and behavior.

## How it fits with the framework

dr-ui is orthogonal to the copier and Pulumi layers. It is an opt-in dependency consumed inside any frontend built with the [react](../components/react.md) component, for both foundation templates and custom recipes. The App Framework does not pin you to dr-ui. It is the recommended path when you want a consistent DataRobot look and feel and a head start on complex components.

## Key properties

- **shadcn-compatible**: installed via `shadcn@latest add` and configured through `components.json`.
- **AI-native**: components are structured for AI coding assistants and code generation tools.
- **Customizable**: installed components live in your repo, so you edit them like any other source file.
- **Tailwind + Radix**: built on accessible primitives with first-class dark mode and theming.

## Reference

- [dr-ui documentation](https://dr-ui.datarobot.com/en/docs/)
- [Using dr-ui in a React frontend](../guides/using-dr-ui.md)
