#!/usr/bin/env node
/**
 * memory-mtime-sync.cjs
 * 
 * Mtime-based sync for memory segment writes.
 * Inspired by Prime Agent's HarnessState._sync_from_disk()
 * 
 * Prevents corruption when multiple processes write to memory files concurrently.
 * 
 * Usage:
 *   node scripts/memory-mtime-sync.cjs check <file>       — check if file was modified externally
 *   node scripts/memory-mtime-sync.cjs sync <file>        — reload if modified, return content
 *   node scripts/memory-mtime-sync.cjs save <file> <data> — save with mtime tracking
 * 
 * Tracks mtime in a sidecar file: <file>.mtime.json
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.join(__dirname, '..', 'memory', 'segments');

function getMtimePath(filePath) {
  return filePath + '.mtime.json';
}

function readMtimeCache(filePath) {
  const mtimePath = getMtimePath(filePath);
  try {
    return JSON.parse(fs.readFileSync(mtimePath, 'utf8'));
  } catch {
    return null;
  }
}

function writeMtimeCache(filePath, stat) {
  const mtimePath = getMtimePath(filePath);
  fs.writeFileSync(mtimePath, JSON.stringify({
    mtimeNs: stat.mtimeNs,
    size: stat.size,
    checkedAt: new Date().toISOString()
  }), 'utf8');
}

function check(filePath) {
  const abs = path.resolve(filePath);
  const cache = readMtimeCache(abs);
  const stat = fs.statSync(abs);
  
  if (!cache) {
    writeMtimeCache(abs, stat);
    return { status: 'first_check', modified: false, mtimeNs: stat.mtimeNs };
  }
  
  const modified = stat.mtimeNs !== cache.mtimeNs;
  return {
    status: modified ? 'modified_externally' : 'clean',
    modified,
    mtimeNs: stat.mtimeNs,
    cachedMtimeNs: cache.mtimeNs,
    lastChecked: cache.checkedAt
  };
}

function sync(filePath) {
  const abs = path.resolve(filePath);
  const checkResult = check(abs);
  
  if (checkResult.modified) {
    // File was modified externally — reload
    const content = fs.readFileSync(abs, 'utf8');
    writeMtimeCache(abs, fs.statSync(abs));
    return { ...checkResult, content, action: 'reloaded' };
  }
  
  return { ...checkResult, content: null, action: 'no_reload_needed' };
}

function save(filePath, data) {
  const abs = path.resolve(filePath);
  const dir = path.dirname(abs);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(abs, data, 'utf8');
  writeMtimeCache(abs, fs.statSync(abs));
  return { status: 'saved', mtimeNs: fs.statSync(abs).mtimeNs };
}

// CLI
const [,, cmd, filePath, ...rest] = process.argv;

if (!cmd || !filePath) {
  console.error('Usage: node memory-mtime-sync.cjs <check|sync|save> <file> [data]');
  process.exit(1);
}

try {
  let result;
  switch (cmd) {
    case 'check':
      result = check(filePath);
      break;
    case 'sync':
      result = sync(filePath);
      break;
    case 'save':
      const data = rest.join(' ');
      result = save(filePath, data);
      break;
    default:
      console.error(`Unknown command: ${cmd}`);
      process.exit(1);
  }
  console.log(JSON.stringify(result, null, 2));
} catch (err) {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
}
