import type { ConfigType } from '@plone/registry';
import { Client } from '@robgietema/nick/src/client';

export default function install(config: ConfigType) {
  config.registerUtility({
    name: 'ploneClient',
    type: 'client',
    method: () => Client,
  });

  return config;
}
