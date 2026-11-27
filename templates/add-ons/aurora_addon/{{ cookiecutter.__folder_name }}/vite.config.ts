import { reactRouter } from '@react-router/dev/vite';
import { defineConfig } from 'vite';
import { PloneAuroraVitePlugin } from '@plone/aurora/vite';

export default defineConfig({
  // `PloneAuroraVitePlugin()` goes before `reactRouter()`.
  plugins: [PloneAuroraVitePlugin(), reactRouter()],
  resolve: {
    tsconfigPaths: true,
  },
  server: {
    port: 3000,
  },
});
