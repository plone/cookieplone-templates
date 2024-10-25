import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';
import react from '@vitejs/plugin-react';
import path from 'path';
import fixReactVirtualized from 'esbuild-plugin-react-virtualized';

// Dynamically get the name of the generated addon
const addonName = path.basename(process.cwd());
const projectRootPath = path.resolve('../..');

// Vite configuration with dynamic addon name
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  optimizeDeps: {
    esbuildOptions: {
      plugins: [fixReactVirtualized as any],
    },
    include: ['@plone/volto/constants/Languages.cjs'],
  },
  resolve: {
    alias: [
      { find: /^~@root/, replacement: projectRootPath },
      {
        find: `@${addonName}`,
        replacement: `${projectRootPath}/packages/${addonName}/src/`,
      },
      { find: /^~/, replacement: '' },
    ],
  },
  logLevel: 'error',
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
  },
});
