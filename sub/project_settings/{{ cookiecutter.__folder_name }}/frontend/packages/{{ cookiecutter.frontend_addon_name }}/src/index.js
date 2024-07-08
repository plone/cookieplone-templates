const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['{{ cookiecutter.language_code }}'],
    defaultLanguage: '{{ cookiecutter.language_code }}',
  };
  return config;
};

export default applyConfig;
