#!/usr/bin/env node
/**
 * path-protection.cjs
 * 
 * Path protection hooks — blocks writes to sensitive paths.
 * Inspired by Prime Agent's extension-based tool_call interception.
 * 
 * Usage:
 *   node scripts/path-protection.cjs check <file>         — check if write is allowed
 *   node scripts/path-protection.cjs validate <command>   — validate a shell command
 * 
 * Protected paths: .env, credentials, secrets, private keys, node_modules writes
 */

const path = require('path');
const fs = require('fs');

const WORKSPACE = path.resolve(__dirname, '..');

// Paths that should never be written to
const BLOCKED_WRITE_PATTERNS = [
  /\.env$/i,
  /\.env\./i,
  /credentials\.md$/i,
  /secrets/i,
  /\.pem$/i,
  /\.key$/i,
  /id_rsa/i,
  /node_modules\//i,
  /\.git\/config$/i,
  /token\.json$/i,
  /\.openclaw\/config\.json$/i,
];

// Commands that should never be executed
const BLOCKED_COMMANDS = [
  /rm\s+-rf\s+[\/~]/i,
  /rmdir\s+\/s\s+/i,
  /format\s+c:/i,
  /del\s+\/[sfq]/i,
  /taskkill\s+\/f/i,
  /shutdown/i,
  /reboot/i,
];

function isWriteAllowed(filePath) {
  const abs = path.resolve(filePath);
  const rel = path.relative(WORKSPACE, abs);
  
  for (const pattern of BLOCKED_WRITE_PATTERNS) {
    if (pattern.test(abs) || pattern.test(rel)) {
      return {
        allowed: false,
        reason: `Path matches blocked pattern: ${pattern}`,
        path: rel,
        pattern: pattern.source
      };
    }
  }
  
  return { allowed: true, path: rel };
}

function isCommandAllowed(command) {
  for (const pattern of BLOCKED_COMMANDS) {
    if (pattern.test(command)) {
      return {
        allowed: false,
        reason: `Command matches blocked pattern: ${pattern}`,
        command: command.substring(0, 100),
        pattern: pattern.source
      };
    }
  }
  
  return { allowed: true };
}

// CLI
const [,, cmd, ...args] = process.argv;

if (!cmd) {
  console.error('Usage: node path-protection.cjs <check|validate> <target>');
  process.exit(1);
}

try {
  let result;
  switch (cmd) {
    case 'check':
      result = isWriteAllowed(args.join(' '));
      break;
    case 'validate':
      result = isCommandAllowed(args.join(' '));
      break;
    default:
      console.error(`Unknown command: ${cmd}`);
      process.exit(1);
  }
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.allowed ? 0 : 1);
} catch (err) {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
}
