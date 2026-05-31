import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
export const repoRoot = path.resolve(scriptDir, '..');

export function repoPath(...segments) {
  return path.join(repoRoot, ...segments);
}

export async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

export async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(data, null, 2)}\n`);
}

export async function writeText(filePath, contents) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, contents);
}

export async function readText(filePath) {
  return fs.readFile(filePath, 'utf8');
}

export async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function recreateDir(dirPath) {
  await fs.rm(dirPath, { recursive: true, force: true });
  await fs.mkdir(dirPath, { recursive: true });
}

export async function copyDir(source, destination) {
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.cp(source, destination, { recursive: true, force: true });
}

export async function copyFile(source, destination) {
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.copyFile(source, destination);
}

export async function listFilesRecursive(rootDir) {
  const entries = await fs.readdir(rootDir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (entry.name === 'node_modules' || entry.name === 'build') continue;

    const absolutePath = path.join(rootDir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await listFilesRecursive(absolutePath)));
    } else if (entry.isFile()) {
      files.push(absolutePath);
    }
  }

  return files.sort();
}

export async function hashFiles(files) {
  const hash = crypto.createHash('sha256');

  for (const file of files) {
    hash.update(`${path.relative(repoRoot, file)}\n`);
    hash.update(await fs.readFile(file));
    hash.update('\n');
  }

  return hash.digest('hex');
}

export async function getContext() {
  const rootPackage = await readJson(repoPath('package.json'));
  const sevenPackage = await readJson(
    repoPath('core', 'apps', 'seven', 'package.json'),
  );
  const addonPackage = await readJson(
    repoPath('packages', '{{ cookiecutter.frontend_addon_name }}', 'package.json'),
  );
  const catalog = await readJson(repoPath('core', 'catalog.json'));
  const packageVersions = await collectPackageVersions();

  return {
    addonPackage,
    catalog,
    packageVersions,
    rootPackage,
    sevenPackage,
  };
}

async function collectPackageVersions() {
  const locations = [
    repoPath('core', 'apps'),
    repoPath('core', 'packages'),
    repoPath('packages'),
  ];
  const versions = {};

  for (const location of locations) {
    let entries = [];
    try {
      entries = await fs.readdir(location, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const manifestPath = path.join(location, entry.name, 'package.json');
      try {
        const manifest = await readJson(manifestPath);
        if (manifest.name && manifest.version) {
          versions[manifest.name] = manifest.version;
        }
      } catch {
        // Ignore directories that are not packages.
      }
    }
  }

  return versions;
}

export function rewriteManifest(manifest, context, overrides = {}) {
  const cloned = JSON.parse(JSON.stringify(manifest));
  const sections = [
    'dependencies',
    'devDependencies',
    'peerDependencies',
    'optionalDependencies',
  ];

  for (const section of sections) {
    if (!cloned[section]) continue;
    for (const [dependency, specifier] of Object.entries(cloned[section])) {
      const override = overrides[section]?.[dependency];
      cloned[section][dependency] =
        override ?? resolveSpecifier(dependency, specifier, context);
    }
  }

  return cloned;
}

export function resolveSpecifier(dependency, specifier, context) {
  if (specifier === 'catalog:' || String(specifier).startsWith('catalog:')) {
    const resolved = context.catalog[dependency];
    if (!resolved) {
      throw new Error(`Unable to resolve catalog dependency "${dependency}"`);
    }
    return resolved;
  }

  if (String(specifier).startsWith('workspace:')) {
    const resolved = context.packageVersions[dependency];
    if (!resolved) {
      throw new Error(`Unable to resolve workspace dependency "${dependency}"`);
    }
    return resolved;
  }

  return specifier;
}
