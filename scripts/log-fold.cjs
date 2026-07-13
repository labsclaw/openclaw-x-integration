#!/usr/bin/env node
/**
 * log-fold.js
 * 
 * Compacts daily logs older than N days into topic segments.
 * Inspired by claude-obsidian's DragonScale fold operator.
 * 
 * Usage: node scripts/log-fold.js [--dry-run] [--days=7]
 * 
 * Reads memory/daily/*.md, groups entries by topic tags,
 * and appends summarized content to memory/segments/.
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.resolve(__dirname, '..', 'memory');
const DAILY_DIR = path.join(MEMORY_DIR, 'daily');
const SEGMENTS_DIR = path.join(MEMORY_DIR, 'segments');
const DRY_RUN = process.argv.includes('--dry-run');
const MAX_DAYS = parseInt(process.argv.find(a => a.startsWith('--days='))?.split('=')[1] || '7');

function getDailyFiles() {
  if (!fs.existsSync(DAILY_DIR)) return [];
  
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - MAX_DAYS);
  
  return fs.readdirSync(DAILY_DIR)
    .filter(f => f.endsWith('.md'))
    .map(f => {
      // Match formats: 2026-05-19.md or 2026-05-19-1637.md or 2026-05-19-1655-2.md
      const dateMatch = f.match(/^(\d{4}-\d{2}-\d{2})/);
      if (!dateMatch) return null;
      const dateStr = dateMatch[1];
      const date = new Date(dateStr);
      return { file: f, path: path.join(DAILY_DIR, f), date, dateStr };
    })
    .filter(f => f && !isNaN(f.date.getTime()) && f.date < cutoff)
    .sort((a, b) => a.date - b.date);
}

function parseDailyLog(content) {
  const entries = [];
  const lines = content.split('\n');
  let currentEntry = null;
  
  for (const line of lines) {
    // Match timestamp entries like "### 09:30 - Topic"
    const headerMatch = line.match(/^###\s+(\d{2}:\d{2})\s*[-–]\s*(.+)/);
    // Match session headers like "# Session: 2026-05-19 16:37:02 GMT-3"
    const sessionMatch = line.match(/^#\s+Session:\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})/);
    // Match section headers like "## Topic"
    const sectionMatch = line.match(/^##\s+(.+)/);
    
    if (headerMatch) {
      if (currentEntry) entries.push(currentEntry);
      currentEntry = {
        time: headerMatch[1],
        topic: headerMatch[2].trim(),
        content: [],
        tags: [],
      };
      continue;
    }
    
    if (sessionMatch) {
      if (currentEntry) entries.push(currentEntry);
      currentEntry = {
        time: sessionMatch[1].split(' ')[1] || '00:00',
        topic: 'session',
        content: [],
        tags: ['session'],
      };
      continue;
    }
    
    if (sectionMatch && currentEntry && currentEntry.topic === 'session') {
      currentEntry.topic = sectionMatch[1].trim();
      continue;
    }
    
    // Match tags like "**Tags:** tag1, tag2"
    const tagMatch = line.match(/\*\*Tags?:\*\*\s*(.+)/i);
    if (tagMatch && currentEntry) {
      currentEntry.tags = tagMatch[1].split(',').map(t => t.trim().toLowerCase());
      continue;
    }
    
    if (currentEntry) {
      currentEntry.content.push(line);
    }
  }
  
  if (currentEntry) entries.push(currentEntry);
  return entries;
}

function groupByTopic(allEntries) {
  const groups = {};
  
  for (const entry of allEntries) {
    // Use first tag as primary topic, or infer from content
    const topic = entry.tags[0] || inferTopic(entry);
    if (!groups[topic]) groups[topic] = [];
    groups[topic].push(entry);
  }
  
  return groups;
}

function inferTopic(entry) {
  const text = entry.content.join(' ').toLowerCase();
  const topicKeywords = {
    'infrastructure': ['server', 'deploy', 'docker', 'pm2', 'gateway', 'restart', 'crash'],
    'paper': ['paper', 'draft', 'arxiv', 'publish', 'reference', 'citation'],
    'skills': ['skill', 'plugin', 'extension', 'install', 'template'],
    'memory': ['memory', 'segment', 'cache', 'retrieval', 'wiki'],
    'incidents': ['incident', 'bug', 'fix', 'error', 'outage', 'down'],
    'social': ['post', 'tweet', 'thread', 'x.com', 'telegram', 'message'],
  };
  
  for (const [topic, keywords] of Object.entries(topicKeywords)) {
    if (keywords.some(kw => text.includes(kw))) return topic;
  }
  return 'general';
}

function summarizeEntries(entries) {
  // Extract key decisions and outcomes (not the "how")
  const summaries = [];
  
  for (const entry of entries) {
    const text = entry.content.join('\n').trim();
    if (text.length < 10) continue;
    
    // Extract decision lines (lines with "→", "decided", "resolved", "shipped")
    const decisions = text.split('\n').filter(line => 
      /decided|resolved|shipped|merged|created|implemented|fixed|deployed/i.test(line)
    );
    
    if (decisions.length > 0) {
      summaries.push(`- **${entry.time}** ${entry.topic}: ${decisions[0].trim().slice(0, 150)}`);
    } else if (text.length > 20) {
      // Keep first meaningful line
      const firstMeaningful = text.split('\n').find(l => l.trim().length > 15);
      if (firstMeaningful) {
        summaries.push(`- **${entry.time}** ${entry.topic}: ${firstMeaningful.trim().slice(0, 150)}`);
      }
    }
  }
  
  return summaries;
}

function getSegmentId(topic) {
  const existing = fs.readdirSync(SEGMENTS_DIR).filter(f => f.startsWith('s'));
  const maxId = existing.reduce((max, f) => {
    const num = parseInt(f.match(/s(\d+)/)?.[1] || '0');
    return Math.max(max, num);
  }, 0);
  return `s${String(maxId + 1).padStart(3, '0')}`;
}

function createSegment(topic, entries, dateRange) {
  const id = getSegmentId(topic);
  const summaries = summarizeEntries(entries);
  
  const content = `---
id: ${id}
created: ${dateRange.start}
updated: ${dateRange.end}
weight: 0.8
accessCount: 0
folded: true
source_dates: ${dateRange.start} to ${dateRange.end}
---

# ${id} — Fold: ${topic} (${dateRange.start} to ${dateRange.end})

## Resumo
Compacted from ${entries.length} daily entries across ${dateRange.span} days.

## Entries
${summaries.join('\n')}
`;

  return { id, content, filePath: path.join(SEGMENTS_DIR, `${id}-fold-${topic}.md`) };
}

// ============================================
// MAIN
// ============================================

console.log('📦 Log Fold\n');

const dailyFiles = getDailyFiles();
console.log(`  Found ${dailyFiles.length} daily files older than ${MAX_DAYS} days`);

if (dailyFiles.length === 0) {
  console.log('  Nothing to fold. Exiting.\n');
  process.exit(0);
}

// Parse all entries from old daily files
const allEntries = [];
for (const df of dailyFiles) {
  const content = fs.readFileSync(df.path, 'utf-8');
  const entries = parseDailyLog(content);
  entries.forEach(e => e.sourceDate = df.dateStr);
  allEntries.push(...entries);
}

console.log(`  Extracted ${allEntries.length} entries from ${dailyFiles.length} files`);

// Group by topic
const groups = groupByTopic(allEntries);
console.log(`  Groups: ${Object.keys(groups).join(', ')}\n`);

// Create segments for groups with 2+ entries
const dateRange = {
  start: dailyFiles[0].dateStr,
  end: dailyFiles[dailyFiles.length - 1].dateStr,
  span: dailyFiles.length,
};

for (const [topic, entries] of Object.entries(groups)) {
  if (entries.length < 2) {
    console.log(`  Skipping "${topic}" (${entries.length} entries, need 2+)`);
    continue;
  }
  
  const segment = createSegment(topic, entries, dateRange);
  
  if (DRY_RUN) {
    console.log(`  [DRY RUN] Would create: ${segment.filePath}`);
    console.log(`    Entries: ${entries.length}`);
    console.log(`    Content preview:\n${segment.content.slice(0, 200)}...\n`);
  } else {
    fs.writeFileSync(segment.filePath, segment.content, 'utf-8');
    console.log(`  ✅ Created: ${segment.id}-fold-${topic}.md (${entries.length} entries)`);
    
    // Archive (don't delete, just rename)
    for (const df of dailyFiles) {
      const archivePath = df.path.replace('.md', '.archived.md');
      if (!fs.existsSync(archivePath)) {
        fs.renameSync(df.path, archivePath);
        console.log(`    📁 Archived: ${df.file}`);
      }
    }
  }
}

console.log(`\n${DRY_RUN ? '(dry run — no files modified)' : 'Done. Daily files archived, segments created.'}`);
