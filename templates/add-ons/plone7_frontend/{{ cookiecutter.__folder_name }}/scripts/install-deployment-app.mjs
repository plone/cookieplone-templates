import { execSync } from 'node:child_process';
import path from 'node:path';
import {
  pathExists,
  readJson,
  readText,
  repoPath,
  writeText,
} from './deploy-utils.mjs';

const deployRoot = repoPath('.deploy');
const statePath = path.join(deployRoot, '.deploy-state.json');
const installMarkerPath = path.join(deployRoot, '.deploy-installed-hash');
const modulesYamlPath = path.join(deployRoot, 'node_modules', '.modules.yaml');

async function main() {
  execSync('node ./scripts/generate-deployment-app.mjs', {
    cwd: repoPath(),
    stdio: 'inherit',
  });

  const { sourceHash } = await readJson(statePath);
  const hasInstall =
    (await pathExists(modulesYamlPath)) && (await pathExists(installMarkerPath));

  if (hasInstall) {
    const installedHash = (await readText(installMarkerPath)).trim();
    if (installedHash === sourceHash) {
      process.stdout.write('Deploy workspace install is up to date\n');
      return;
    }
  }

  execSync('CI=1 pnpm install --dir .deploy --ignore-workspace', {
    cwd: repoPath(),
    stdio: 'inherit',
    shell: true,
  });

  await writeText(installMarkerPath, `${sourceHash}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
