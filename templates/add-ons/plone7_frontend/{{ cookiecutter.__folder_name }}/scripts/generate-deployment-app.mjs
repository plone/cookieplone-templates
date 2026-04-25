import path from 'node:path';
import {
  copyDir,
  copyFile,
  getContext,
  hashFiles,
  listFilesRecursive,
  pathExists,
  readText,
  recreateDir,
  repoPath,
  rewriteManifest,
  writeJson,
  writeText,
} from './deploy-utils.mjs';

const deployRoot = repoPath('.deploy');
const statePath = path.join(deployRoot, '.deploy-state.json');

async function main() {
  const context = await getContext();
  const deployRegistryConfig = await createDeployRegistryConfig();
  const sourceHash = await getDeploySourceHash();
  const currentState = (await pathExists(statePath))
    ? await getCurrentState()
    : null;

  if (currentState?.sourceHash === sourceHash) {
    process.stdout.write(`Deploy workspace up to date at ${deployRoot}\n`);
    return;
  }

  await recreateDir(deployRoot);

  await Promise.all([
    copyDir(repoPath('core', 'apps', 'seven', 'app'), path.join(deployRoot, 'app')),
    copyDir(
      repoPath('core', 'apps', 'seven', 'public'),
      path.join(deployRoot, 'public'),
    ),
    copyDir(
      repoPath('packages', '{{ cookiecutter.frontend_addon_name }}'),
      path.join(deployRoot, 'packages', '{{ cookiecutter.frontend_addon_name }}'),
    ),
    copyFile(
      repoPath('core', 'apps', 'seven', 'react-router.config.ts'),
      path.join(deployRoot, 'react-router.config.ts'),
    ),
    copyFile(
      repoPath('core', 'apps', 'seven', 'registry.config.ts'),
      path.join(deployRoot, 'registry.base.config.ts'),
    ),
    copyFile(
      repoPath('core', 'packages', 'components', 'vite-plugin-svgr.js'),
      path.join(deployRoot, 'vite-plugin-svgr.js'),
    ),
    copyFile(
      repoPath('core', 'packages', 'components', 'vite-plugin-svgr.d.ts'),
      path.join(deployRoot, 'vite-plugin-svgr.d.ts'),
    ),
  ]);

  await writeText(
    path.join(deployRoot, 'registry.config.ts'),
    deployRegistryConfig,
  );

  await writeJson(path.join(deployRoot, 'package.json'), createDeployPackage(context));
  await writeJson(
    path.join(
      deployRoot,
      'packages',
      '{{ cookiecutter.frontend_addon_name }}',
      'package.json',
    ),
    createDeployAddonPackage(context),
  );

  await writeText(path.join(deployRoot, 'tsconfig.json'), createTsConfig());
  await writeText(path.join(deployRoot, 'vite.config.ts'), createViteConfig());
  await writeText(path.join(deployRoot, '.gitignore'), createGitIgnore());
  await writeJson(statePath, { sourceHash });

  process.stdout.write(`Generated deploy workspace at ${deployRoot}\n`);
}

function createDeployPackage(context) {
  const baseManifest = {
    name: context.sevenPackage.name,
    version: context.rootPackage.version,
    private: true,
    sideEffects: false,
    type: 'module',
    exports: {
      './package.json': './package.json',
      './app/*': './app/*',
      './.plone/*': './.plone/*',
      './registry.config': './registry.config.ts',
    },
    scripts: {
      dev: 'pnpm exec init-loaders && react-router dev',
      build: 'pnpm exec init-loaders && react-router build',
      'start:prod': 'react-router-serve ./build/server/index.js',
      typecheck: 'react-router typegen && tsc',
    },
    dependencies: {
      ...context.sevenPackage.dependencies,
      '{{ cookiecutter.__npm_package_name }}':
        'file:./packages/{{ cookiecutter.frontend_addon_name }}',
    },
    devDependencies: context.sevenPackage.devDependencies,
    engines: context.sevenPackage.engines,
    packageManager: context.rootPackage.packageManager,
    pnpm: context.rootPackage.pnpm,
  };

  baseManifest.devDependencies['vite-plugin-svgr'] = '^4.5.0';
  baseManifest.devDependencies['@svgr/plugin-svgo'] = '^8.1.0';
  baseManifest.devDependencies['@svgr/plugin-jsx'] = '^8.1.0';
  baseManifest.devDependencies['tailwindcss-react-aria-components'] = '^2.0.0';

  return rewriteManifest(baseManifest, context);
}

function createDeployAddonPackage(context) {
  return rewriteManifest(context.addonPackage, context);
}

function createTsConfig() {
  return `{
  "include": [
    "**/*.ts",
    "**/*.tsx",
    "**/.server/**/*.ts",
    "**/.server/**/*.tsx",
    "**/.client/**/*.ts",
    "**/.client/**/*.tsx",
    ".react-router/types/**/*"
  ],
  "compilerOptions": {
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "types": ["@react-router/node", "vite/client", "@plone/components/icons"],
    "isolatedModules": true,
    "esModuleInterop": true,
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "target": "ES2022",
    "strict": true,
    "allowJs": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "paths": {
      "~/*": ["./app/*"],
      "seven/*": ["./*"]
    },
    "noEmit": true,
    "rootDirs": [".", "./.react-router/types"],
    "plugins": [{ "name": "@react-router/dev" }]
  }
}
`;
}

function createViteConfig() {
  return `import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import { reactRouter } from '@react-router/dev/vite';
import path from 'node:path';
import { defineConfig } from 'vite';
import { PloneRegistryVitePlugin } from '@plone/registry/vite-plugin';
import { PloneSVGRVitePlugin } from './vite-plugin-svgr.js';
import babel from 'vite-plugin-babel';
import tailwindcss from '@tailwindcss/vite';
import { visualizer } from 'rollup-plugin-visualizer';
import devtoolsJson from 'vite-plugin-devtools-json';

const viteLoaderPath = path.resolve(__dirname, '.plone', 'vite.loader.js');
const applyAddonViteConfiguration = fs.existsSync(viteLoaderPath)
  ? (await import(pathToFileURL(viteLoaderPath).href)).default
  : (config) => config;

export default defineConfig(({ command, mode, isSsrBuild }) => {
  const analyze = process.env.ANALYZE === 'true';
  const target = isSsrBuild ? 'server' : 'client';
  const statsDir = path.resolve(__dirname, 'build', 'stats');

  const baseConfig = {
    plugins: [
      PloneSVGRVitePlugin(),
      PloneRegistryVitePlugin(),
      tailwindcss(),
      reactRouter(),
      babel({
        filter: /app\\/.*\\.tsx?$/,
        babelConfig: {
          presets: ['@babel/preset-typescript'],
          plugins: ['babel-plugin-react-compiler'],
        },
      }),
      devtoolsJson(),
      ...(analyze
        ? [
            visualizer({
              filename: path.join(statsDir, \`stats-\${target}.html\`),
              template: 'treemap',
              gzipSize: true,
              brotliSize: true,
            }),
            visualizer({
              filename: path.join(statsDir, \`stats-\${target}.json\`),
              template: 'raw-data',
              gzipSize: true,
              brotliSize: true,
            }),
          ]
        : []),
    ],
    resolve: {
      alias: [
        {
          find: 'seven',
          replacement: __dirname,
        },
      ],
      tsconfigPaths: true,
    },
    server: {
      port: 3000,
      fs: {
        allow: ['../.'],
      },
    },
  };

  return applyAddonViteConfiguration(baseConfig, {
    command,
    mode,
    isSsrBuild,
  });
});
`;
}

function createGitIgnore() {
  return `node_modules
.plone
.react-router
build
public/locales
`;
}

async function createDeployRegistryConfig() {
  const source = await readText(repoPath('registry.config.ts'));
  return source.replace(
    /from ['"]seven\/registry\.config['"]/g,
    "from './registry.base.config'",
  );
}

async function getDeploySourceHash() {
  const explicitFiles = [
    repoPath('package.json'),
    repoPath('registry.config.ts'),
    repoPath('core', 'catalog.json'),
    repoPath('core', 'apps', 'seven', 'react-router.config.ts'),
    repoPath('core', 'apps', 'seven', 'registry.config.ts'),
    repoPath('core', 'packages', 'components', 'vite-plugin-svgr.js'),
    repoPath('core', 'packages', 'components', 'vite-plugin-svgr.d.ts'),
  ];

  const recursiveDirs = [
    repoPath('core', 'apps', 'seven', 'app'),
    repoPath('core', 'apps', 'seven', 'public'),
    repoPath('packages', '{{ cookiecutter.frontend_addon_name }}'),
  ];

  const files = [...explicitFiles];

  for (const dir of recursiveDirs) {
    files.push(...(await listFilesRecursive(dir)));
  }

  return hashFiles(files);
}

async function getCurrentState() {
  try {
    return JSON.parse(await readText(statePath));
  } catch {
    return null;
  }
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
