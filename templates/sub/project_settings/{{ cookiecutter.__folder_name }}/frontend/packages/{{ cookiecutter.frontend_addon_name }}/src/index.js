const applyConfig = (config) => {
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['{{ cookiecutter.language_code }}'];
  config.settings.defaultLanguage = '{{ cookiecutter.language_code }}';

  return config;
};

export default applyConfig;
