import { defineConfig } from 'vitest/config';

// The tests of the add-on. Without this file, Vitest would use the app's
// `vite.config.ts`, with the React Router plugin.
export default defineConfig({
  test: {},
});
