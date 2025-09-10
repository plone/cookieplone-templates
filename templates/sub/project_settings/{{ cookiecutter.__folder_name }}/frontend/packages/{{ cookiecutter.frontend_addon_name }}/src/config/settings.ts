import type { ConfigType } from "@plone/registry";

export default function install(config: ConfigType) {
  // Language settings
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ["{{ cookiecutter.language_code }}"];
  config.settings.defaultLanguage = "{{ cookiecutter.language_code }}";

  return config;
}
