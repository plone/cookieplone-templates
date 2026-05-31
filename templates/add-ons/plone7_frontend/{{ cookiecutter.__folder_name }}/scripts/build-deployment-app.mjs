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
const buildMarkerPath = path.join(deployRoot, '.deploy-built-hash');
const serverBuildPath = path.join(deployRoot, 'build', 'server', 'index.js');

async function main() {
  execSync('node ./scripts/install-deployment-app.mjs', {
    cwd: repoPath(),
    stdio: 'inherit',
  });

  const { sourceHash } = await readJson(statePath);
  const hasBuild =
    (await pathExists(serverBuildPath)) && (await pathExists(buildMarkerPath));

  if (hasBuild) {
    const builtHash = (await readText(buildMarkerPath)).trim();
    if (builtHash === sourceHash) {
      process.stdout.write('Deploy workspace build is up to date\n');
      return;
    }
  }

  execSync('pnpm --dir .deploy build', {
    cwd: repoPath(),
    stdio: 'inherit',
    shell: true,
  });

  await writeText(buildMarkerPath, `${sourceHash}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
