import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  config.settings.apiPath =
    process.env.PLONE_API_PATH || 'http://localhost:8080';

  return config;
}
