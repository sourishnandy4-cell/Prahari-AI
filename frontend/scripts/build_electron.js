import os from 'os';
import path from 'path';
import fs from 'fs';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const localDist = path.join(frontendDir, 'dist_electron');

// Build in system temp directory to prevent OneDrive file-locking EPERM errors
const tempOutDir = path.join(os.tmpdir(), 'prahari_electron_build');

console.log('====================================================');
console.log('  PRAHARI AI — Desktop Electron Installer Builder');
console.log('====================================================');
console.log(`[1/3] Building Vite production web app...`);
execSync('npm run build', { cwd: frontendDir, stdio: 'inherit' });

console.log(`\n[2/3] Running electron-builder (isolated temp outDir: ${tempOutDir})...`);
if (fs.existsSync(tempOutDir)) {
  fs.rmSync(tempOutDir, { recursive: true, force: true });
}
fs.mkdirSync(tempOutDir, { recursive: true });

try {
  execSync(
    `npx electron-builder --win --x64 -c.directories.output="${tempOutDir}"`,
    { cwd: frontendDir, stdio: 'inherit' }
  );
} catch (err) {
  console.error('[!] Error building Electron package:', err.message);
  process.exit(1);
}

console.log(`\n[3/3] Copying built installers to ${localDist}...`);
if (!fs.existsSync(localDist)) {
  fs.mkdirSync(localDist, { recursive: true });
}

const files = fs.readdirSync(tempOutDir);
let foundExe = false;
for (const file of files) {
  if (file.endsWith('.exe') || file.endsWith('.blockmap') || file.endsWith('.yml')) {
    const src = path.join(tempOutDir, file);
    const dest = path.join(localDist, file);
    fs.copyFileSync(src, dest);
    console.log(`  ✓ Copied: ${file} (${(fs.statSync(dest).size / (1024 * 1024)).toFixed(1)} MB)`);
    if (file.endsWith('.exe')) foundExe = true;
  }
}

if (foundExe) {
  console.log('\n====================================================');
  console.log('  🎉 SUCCESS: Windows Desktop App Packaged!');
  console.log(`  📁 Location: ${localDist}`);
  console.log('====================================================\n');
} else {
  console.log('\n[!] Warning: No .exe files found in output directory.');
}
