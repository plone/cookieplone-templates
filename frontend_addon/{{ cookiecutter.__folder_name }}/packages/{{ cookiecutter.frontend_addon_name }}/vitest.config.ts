import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['**/*.vitest.tsx'],
    globals: true,
    reporters: 'verbose',
    environment: 'jsdom',
  },
});
