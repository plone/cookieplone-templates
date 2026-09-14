import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Language settings
  {%- if cookiecutter.volto_version < '19' %}
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['{{ cookiecutter.language_code }}'];
  {%- endif %}
  config.settings.defaultLanguage = '{{ cookiecutter.language_code }}';
  // Additional language settings for Volto 19 and above, add as many supported languages as needed
  // Languages not added to supportedLanguages will not be included in the build
  // config.settings.supportedLanguages = ['{{ cookiecutter.language_code }}'];

  return config;
}
