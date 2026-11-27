import type { Config } from '@react-router/dev/config';
import { ploneAurora } from '@plone/aurora/preset';

export default {
  ssr: true,
  // Generates the Plone registry files, including the add-ons' routes, before
  // React Router reads `app/routes.ts`.
  presets: [ploneAurora()],
} satisfies Config;
