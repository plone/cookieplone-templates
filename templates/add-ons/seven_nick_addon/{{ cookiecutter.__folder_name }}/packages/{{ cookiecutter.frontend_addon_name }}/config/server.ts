import type { ConfigType } from '@plone/registry';
import { Client } from '@robgietema/nick/src/client';

export default function install(config: ConfigType) {
  const cli = Client.initialize({ token: undefined });

  config.registerUtility({
    name: 'ploneClient',
    type: 'client',
    method: () => cli,
  });

  return config;
}
