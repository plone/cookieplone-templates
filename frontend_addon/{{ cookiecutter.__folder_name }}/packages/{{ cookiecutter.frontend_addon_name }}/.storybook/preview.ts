import React from 'react';
import path from 'path';
import '@kitconcept/volto-light-theme/customizations/@root/theme';
import '../../../core/packages/volto/test-setup-config';

import {
  Title,
  Subtitle,
  Description,
  Controls,
  Stories,
} from '@storybook/blocks';
import { Decorator, Preview } from '@storybook/react';
import { deMessages, enMessages, frMessages } from './localesWrapper';
import Wrapper from '../../../core/packages/volto/src/storybook';

// Dynamically resolve the addon’s name and paths
const addonName = path.basename(process.cwd());
const messagesMap = {
  de: deMessages,
  en: enMessages,
  fr: frMessages,
};

const getMessages = (locale: string) =>
  messagesMap[locale as keyof typeof messagesMap];

const decorators: Decorator[] = [
  (Story, context) => {
    return (
      <Wrapper
        customStore={{
          intl: {
            locale: context.globals.locale,
            messages: getMessages(context.globals.locale),
          },
        }}
      >
        <Story locale={context.globals.locale} />
      </Wrapper>
    );
  },
];

const parameters = {
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  docs: {
    page: () => (
      <>
        <Title />
        <Subtitle />
        <Description />
        <Stories />
        <Controls />
      </>
    ),
  },
};

const reactIntl = {
  defaultLocale: 'de',
  locales: ['en', 'de', 'fr'],
};

const preview: Preview = {
  globals: {
    locale: reactIntl.defaultLocale,
    locales: {
      en: { icon: '🇺🇸', title: 'English', right: 'EN' },
      de: { icon: '🇩🇪', title: 'Deutsch', right: 'DE' },
      fr: { icon: '🇫🇷', title: 'Français', right: 'FR' },
    },
  },
  parameters: {
    reactIntl,
    ...parameters,
  },
  decorators,
};

export default preview;
