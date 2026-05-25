# Use dr-ui in a React frontend

This guide shows how to add [dr-ui](https://dr-ui.datarobot.com/en/docs/) components to a recipe that uses the [react](../components/react.md) component. dr-ui is a [shadcn](https://ui.shadcn.com/)-compatible registry, so installation goes through the standard `shadcn` CLI and components are copied into your source tree.

For background on what dr-ui is and why it exists, see [UI library](../design/ui-library.md).

## Prerequisites

- A recipe with the [react](../components/react.md) component applied.
- Node.js 18+.
- Tailwind CSS added. The React scaffold ships with this.

## Step 1: Register the dr-ui registry

Open `frontend_REACT_APP_NAME/components.json` and add the dr-ui registry under `registries`:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "registries": {
    "@dr-ui": "https://dr-ui.datarobot.com/r/{name}.json"
  }
}
```

The `@dr-ui` namespace tells the shadcn CLI where to resolve registry items prefixed with `@dr-ui/`.

## Step 2: Set up theme

dr-ui ships its design tokens, base styles, and theming primitives as a shadcn preset. Install once at the project level so every component picks up the correct colors, typography, and dark-mode behavior.

**1. Install the theme preset from the project root.**

```bash
cd path/to/project
npx shadcn@latest add @dr-ui/theme @dr-ui/theme-toggle -yo
```

**2. Add the theme alias to `components.json`.**

```json
"aliases": {
  "theme": "@/theme"
}
```

**3. Import the generated preset CSS into your global stylesheet** (typically `globals.css`, `index.css`, or `app.css`). Adjust the import path if needed.

```css
@import './theme/preset.css';
```

**4. Make sure dr-ui colors are not overridden** by:

- the global stylesheet
- `tailwind.config.ts`
- `components.json` theme overrides
- hardcoded colors

The following CSS variables are reserved and must not be changed, renamed, or reassigned anywhere outside `preset.css`:

```css
--radius
--background
--foreground
--card
--card-foreground
--popover
--popover-foreground
--primary
--primary-foreground
--secondary
--secondary-foreground
--muted
--muted-foreground
--accent
--accent-foreground
--destructive
--destructive-foreground
--border
--input
--ring
--chart-1
--chart-2
--chart-3
--chart-4
--chart-5
--sidebar
--sidebar-foreground
--sidebar-primary
--sidebar-primary-foreground
--sidebar-accent
--sidebar-accent-foreground
--sidebar-border
--sidebar-ring
```

**5. Wrap the application root in `ThemeProvider`.**

```tsx
import { ThemeProvider } from '@/theme/theme-provider';

<ThemeProvider>
  <App />
</ThemeProvider>
```

**6. Add `ThemeToggle` to the main app component.**

```tsx
import { ThemeToggle } from '@/components/block/theme-toggle';

<ThemeToggle />
```

## Step 3: Use dr-ui design tokens

Prefer dr-ui [design tokens](https://dr-ui.datarobot.com/en/docs/foundation/tokens/) over Tailwind color utility classes (`bg-blue-500`, `text-gray-900`, etc.). Tokens are shadcn-compatible CSS variables that resolve to the correct color in light and dark themes, which makes the UI easier to customize and keeps it consistent with the rest of DataRobot.

```tsx
// Preferred: dr-ui token
<div className="bg-background">…</div>

// Avoid: raw Tailwind palette
<div className="bg-white">…</div>
```

Customer developers can override tokens in their own CSS to rebrand the application without touching component source.

## Step 4: Use dr-ui typography classes

dr-ui provides [typography classes](https://dr-ui.datarobot.com/en/docs/foundation/typography/) for headings, body copy, captions, and code. Prefer them over raw Tailwind utilities like `text-2xl font-semibold`, so type styles stay consistent and respond correctly to theme changes.

```tsx
// Preferred: dr-ui typography class
<h1 className="heading-01">Dashboard</h1>

// Avoid: ad-hoc Tailwind sizing
<h1 className="text-3xl font-bold">Dashboard</h1>
```

## Step 5: Add localization

dr-ui ships a `useTranslation` hook backed by [i18next](https://www.i18next.com/) and [react-i18next](https://react.i18next.com/). Install it from the registry:

```bash
npx shadcn@latest add @dr-ui/i18n
```

The command installs the hook along with `i18next`, `react-i18next`, and `i18next-cli`, and drops an `i18next.config.ts` into your project. Add a script to your `package.json` so translation keys can be extracted from source automatically:

```json
{
  "scripts": {
    "i18n:extract": "i18next"
  }
}
```

Then use the hook in any component:

```tsx
import { useTranslation } from "@/hooks/use-translation";

export function Greeting() {
  const { t } = useTranslation();
  return <p>{t("greeting.hello")}</p>;
}
```

Run `npm run i18n:extract` whenever you add new keys to regenerate the locale files. See the [dr-ui localization docs](https://dr-ui.datarobot.com/en/docs/localization/installation/) for the full setup and usage reference.

## Step 6: Install components

Use the shadcn CLI to copy a dr-ui component into your project:

```bash
npx shadcn@latest add @dr-ui/button
```

The command writes the component source into `src/components/` (per your `components.json` aliases), along with any `registryDependencies` it declares, for example the shared `@dr-ui/utils` module. The files are local to your repo, so there is no runtime dependency on a published package.

Import and use it like any other component:

```tsx
import { Button } from "@/components/ui/button";

export function Example() {
  return <Button>Run</Button>;
}
```

## Step 7: Mix dr-ui and upstream shadcn

dr-ui is additive. Components from the upstream shadcn registry continue to work without configuration changes, and dr-ui items can declare `registryDependencies` on both shadcn and other dr-ui modules. The CLI resolves everything in one pass.

If two registries provide a component with the same name, the namespaced form (`@dr-ui/button`) always disambiguates.

## Step 8: Customize a component

Because the component file lives in your repo, customization is a normal code edit. For example, to add a variant to the button:

```tsx
// src/components/ui/button.tsx
const buttonVariants = cva(..., {
  variants: {
    variant: {
      // existing variants...
      brand: "bg-brand text-brand-foreground hover:bg-brand/90",
    },
  },
});
```

You will not lose this change on the next `shadcn add`. The CLI only writes files you explicitly install or update.

## Troubleshooting

### Tailwind classes from a new component are not applied

The component file is outside Tailwind's `content` globs. Confirm `tailwind.config` includes `./src/**/*.{ts,tsx}` (or the equivalent for your layout) and restart the Vite dev server.

### `shadcn add @dr-ui/...` reports an unknown registry

The `registries` entry in `components.json` is missing or misspelled. Check that the key is exactly `@dr-ui` and that the URL ends with `/r/{name}.json`.

### dr-ui tokens or typography classes are not resolving

The `preset.css` import is missing from your global stylesheet, or a downstream stylesheet is overriding a reserved CSS variable. Re-check Step 2.

### A component fails to import `@dr-ui/utils`

The shared utils module was not installed alongside the component. Re-run the install command, or install it explicitly:

```bash
npx shadcn@latest add @dr-ui/utils
```

### Dark mode flickers on first paint

`ThemeProvider` reads from `localStorage` after hydration. Add the small inline script documented in the dr-ui theming guide to set the theme class before React mounts.

## Further reading

- [UI library](../design/ui-library.md) for design rationale and key properties.
- [dr-ui documentation](https://dr-ui.datarobot.com/en/docs/) for the full component catalog and API reference.
- [dr-ui design tokens](https://dr-ui.datarobot.com/en/docs/foundation/tokens/) and [typography](https://dr-ui.datarobot.com/en/docs/foundation/typography/).
- [dr-ui localization](https://dr-ui.datarobot.com/en/docs/localization/installation/) for `useTranslation` setup and usage.
