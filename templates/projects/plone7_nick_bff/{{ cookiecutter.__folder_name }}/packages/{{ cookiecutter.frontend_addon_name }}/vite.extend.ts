const knexOptionalDrivers = [
  'better-sqlite3',
  'sqlite3',
  'mysql',
  'mysql2',
  'oracledb',
  'tedious',
  'pg-native',
];

export default function extendViteConfig(config: any) {
  return {
    ...config,
    ssr: {
      ...(config.ssr || {}),
      external: [
        ...new Set([...(config.ssr?.external || []), ...knexOptionalDrivers]),
      ],
    },
    build: {
      ...(config.build || {}),
      rollupOptions: {
        ...(config.build?.rollupOptions || {}),
        external: [
          ...new Set([
            ...(config.build?.rollupOptions?.external || []),
            ...knexOptionalDrivers,
          ]),
        ],
      },
    },
  };
}
