module.exports = function (api) {
  api.cache(true);
{%- if cookiecutter.volto_version >= '19' %}
  const presets = ['@plone/razzle'];
{%- else %}
  const presets = ['razzle'];
{%- endif %}
  const plugins = [
    [
      'react-intl', // React Intl extractor, required for the whole i18n infrastructure to work
      {
        messagesDir: './build/messages/',
      },
    ],
  ];

  return {
    plugins,
    presets,
  };
};
