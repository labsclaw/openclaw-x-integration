#!/usr/bin/env node
/**
 * memory-snapshot.mjs
 * 
 * Weekly backup of critical memory files. Creates timestamped snapshots
 * in memory/snapshots/ for quick recovery if index.json or MEMORY.md
 * get corrupted.
 * 
 * Usage: node scripts/memory-snapshot.mjs
 * 
 * Keeps last 8 weekly snapshots (auto-prunes older ones).
 */

import fs from 'fs';
import path from 'path';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || 'C:\\Users\\ClawLabs\\.openclaw\\workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const SNAPSHOTS_DIR = path.join(MEMORY_DIR, 'snapshots');
const MAX_SNAPSHOTS = 8;

const FILES_TO_BACKUP = [
  { src: path.join(MEMORY_DIR, 'index.json'), name: 'index.json' },
  { src: path.join(WORKSPACE, 'MEMORY.md'), name: 'MEMORY.md' },
  { src: path.join(MEMORY_DIR, 'dream-log.md'), name: 'dream-log.md' },
];

// Also backup all segment files
const SEGMENTS_DIR = path.join(MEMORY_DIR, 'segments');

function main() {
  const now = new Date();
  const brt = new Date(now.getTime() - 3 * 3600 * 1000);
  const dateStr = brt.toISOString().split('T')[0];
  const weekNum = getWeekNumber(brt);
  const snapshotName = `${dateStr}-w${weekNum}`;
  const snapshotDir = path.join(SNAPSHOTS_DIR, snapshotName);

  console.log(`Memory snapshot: ${snapshotName}`);

  if (!fs.existsSync(SNAPSHOTS_DIR)) fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true });
  if (!fs.existsSync(snapshotDir)) fs.mkdirSync(snapshotDir, { recursive: true });

  // Backup core files
  let backed = 0;
  for (const file of FILES_TO_BACKUP) {
    if (fs.existsSync(file.src)) {
      const content = fs.readFileSync(file.src, 'utf8');
      fs.writeFileSync(path.join(snapshotDir, file.name), content, 'utf8');
      backed++;
    }
  }

  // Backup segments
  const segDir = path.join(snapshotDir, 'segments');
  if (fs.existsSync(SEGMENTS_DIR)) {
    if (!fs.existsSync(segDir)) fs.mkdirSync(segDir, { recursive: true });
    const segFiles = fs.readdirSync(SEGMENTS_DIR).filter(f => f.endsWith('.md'));
    for (const f of segFiles) {
      fs.copyFileSync(path.join(SEGMENTS_DIR, f), path.join(segDir, f));
      backed++;
    }
  }

  console.log(`Backed up ${backed} files to ${snapshotDir}`);

  // Prune old snapshots
  const snapshots = fs.readdirSync(SNAPSHOTS_DIR)
    .filter(f => fs.statSync(path.join(SNAPSHOTS_DIR, f)).isDirectory())
    .sort();

  let pruned = 0;
  if (snapshots.length > MAX_SNAPSHOTS) {
    const toRemove = snapshots.slice(0, snapshots.length - MAX_SNAPSHOTS);
    for (const dir of toRemove) {
      const dirPath = path.join(SNAPSHOTS_DIR, dir);
      fs.readdirSync(dirPath).forEach(f => fs.unlinkSync(path.join(dirPath, f)));
      fs.rmdirSync(dirPath);
      console.log(`Pruned old snapshot: ${dir}`);
      pruned++;
    }
  }

  // Create latest symlink-like file
  fs.writeFileSync(path.join(SNAPSHOTS_DIR, 'latest.txt'), snapshotName, 'utf8');

  const remaining = snapshots.length + 1 - pruned;
  console.log(`DONE (${remaining} snapshots on record)`);
}

function getWeekNumber(d) {
  const oneJan = new Date(d.getFullYear(), 0, 1);
  const days = Math.floor((d - oneJan) / 86400000);
  return Math.ceil((days + oneJan.getDay() + 1) / 7);
}

main();
