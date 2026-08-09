#!/usr/bin/env node
/**
 * auto-journal.mjs
 * 
 * Extracts user-visible conversation from JSONL session files for a
 * given date and writes a daily log entry. This replaces the agent
 * relying on manual writes to memory/daily/.
 * 
 * Usage: node scripts/auto-journal.mjs [YYYY-MM-DD]
 *   - Default: yesterday (for the 23:30 BRT cron)
 *   - Explicit date: processes that date
 */

import fs from 'fs';
import path from 'path';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || 'C:\\Users\\ClawLabs\\.openclaw\\workspace';
const SESSIONS_DIR = 'C:\\Users\\ClawLabs\\.openclaw\\agents\\main\\sessions';
const DAILY_DIR = path.join(WORKSPACE, 'memory', 'daily');

function getTargetDate(explicit) {
  if (explicit && /^\d{4}-\d{2}-\d{2}$/.test(explicit)) return explicit;
  // Yesterday in BRT (UTC-3)
  const now = new Date(Date.now() - 3 * 3600 * 1000);
  now.setDate(now.getDate() - 1);
  return now.toISOString().split('T')[0];
}

function extractConversations(filePath, dateStr) {
  const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
  const conversations = [];
  let current = null;

  for (const line of lines) {
    let obj;
    try { obj = JSON.parse(line); } catch { continue; }
    if (obj.type !== 'message' || !obj.message) continue;

    const ts = obj.timestamp;
    if (!ts || !ts.startsWith(dateStr)) continue;

    const { role, content } = obj.message;
    if (role !== 'user' && role !== 'assistant') continue;

    // Extract text from content
    let text;
    if (typeof content === 'string') {
      text = content;
    } else if (Array.isArray(content)) {
      const textParts = content
        .filter(c => c.type === 'text' && c.text)
        .map(c => c.text);
      text = textParts.join('\n');
    }
    if (!text || text.trim().length === 0) continue;

    // Skip NO_REPLY and heartbeat noise
    const clean = text.trim();
    if (clean === 'NO_REPLY' || clean === 'HEARTBEAT_OK') continue;

    const time = ts.substring(11, 16);
    if (role === 'user') {
      // New conversation turn starts with user message
      if (current) conversations.push(current);
      current = { user: clean, assistant: '', time };
    } else if (role === 'assistant' && current) {
      current.assistant = clean;
    }
  }
  if (current) conversations.push(current);
  return conversations;
}

function generateMarkdown(dateStr, sessions) {
  const lines = [`# ${dateStr} — Daily Log\n`];

  if (sessions.length === 0) {
    lines.push(`## Summary\nNo conversation activity on this date.\n`);
    return lines.join('\n');
  }

  lines.push(`## Summary\n`);
  lines.push(`- ${sessions.length} conversation(s) extracted from session logs\n`);
  lines.push(`---\n`);

  let i = 1;
  for (const s of sessions) {
    const userPreview = s.user.length > 300 ? s.user.substring(0, 300) + '...' : s.user;
    lines.push(`### ${i}. [${s.time}] User`);
    lines.push(`> ${userPreview.replace(/\n/g, '\n> ')}\n`);

    if (s.assistant) {
      const asstPreview = s.assistant.length > 500 ? s.assistant.substring(0, 500) + '...' : s.assistant;
      lines.push(`**Assistant:** ${asstPreview.replace(/\n/g, '\n> ')}\n`);
    }
    i++;
  }

  return lines.join('\n');
}

// --- Main ---
const targetDate = getTargetDate(process.argv[2]);
const outputPath = path.join(DAILY_DIR, `${targetDate}.md`);

// Don't overwrite if manually written (no auto-journal marker)
if (fs.existsSync(outputPath)) {
  const existing = fs.readFileSync(outputPath, 'utf8');
  if (existing.includes('<!-- auto-journal -->')) {
    // Already auto-generated — safe to regenerate
  } else {
    console.log(`Skipping ${targetDate} — file exists without auto-journal marker`);
    process.exit(0);
  }
}

if (!fs.existsSync(SESSIONS_DIR)) {
  console.error(`Sessions dir not found: ${SESSIONS_DIR}`);
  process.exit(1);
}

const jsonlFiles = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.jsonl'));
console.log(`Scanning ${jsonlFiles.length} session files for ${targetDate}...`);

let allSessions = [];
for (const file of jsonlFiles) {
  try {
    const convos = extractConversations(path.join(SESSIONS_DIR, file), targetDate);
    allSessions.push(...convos);
  } catch { /* skip corrupt files */ }
}

const md = generateMarkdown(targetDate, allSessions);

if (!fs.existsSync(DAILY_DIR)) fs.mkdirSync(DAILY_DIR, { recursive: true });
fs.writeFileSync(outputPath, md + '\n<!-- auto-journal -->\n', 'utf8');

console.log(`Wrote ${allSessions.length} conversations to ${outputPath}`);
