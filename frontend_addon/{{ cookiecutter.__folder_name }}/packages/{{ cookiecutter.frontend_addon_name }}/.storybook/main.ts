import type { StorybookConfig } from '@storybook/react-vite';
import path from 'path';

const addonName = path.basename(process.cwd()); // Get the addon name dynamically

const config: StorybookConfig = {
  stories: ['../**/*.mdx', `../**/*.stories.@(js|jsx|mjs|ts|tsx)`],
  addons: [
    '@chromatic-com/storybook',
    '@storybook/addon-a11y',
    '@storybook/addon-docs',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-links',
    '@storybook/addon-onboarding',
    'storybook-react-intl',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  staticDirs: [`../../../public`],
  viteFinal: async (config) => {
    // Adjust paths as needed for the dynamically named addon
    config.resolve = {
      ...config.resolve,
      alias: {
        ...config.resolve?.alias,
        [`@${addonName}`]: path.resolve(
          __dirname,
          `../../../packages/${addonName}/src/`,
        ),
      },
    };

    // Markdown support (if needed)
    config.plugins?.push({
      name: 'vite-plugin-markdown',
      transform(src, id) {
        if (id.endsWith('.md')) {
          return `export default ${JSON.stringify(src)}`;
        }
      },
    });
    return config;
  },
};

export default config;
