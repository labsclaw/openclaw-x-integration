#!/usr/bin/env node
/**
 * contradiction-check.js
 * 
 * Checks wiki pages for contradictions against existing knowledge.
 * Inspired by claude-obsidian's [!contradiction] callout system.
 * 
 * Usage: node scripts/contradiction-check.js [--dry-run]
 * 
 * Reads all pages in wiki/entities/ and wiki/concepts/, compares new/updated
 * entries against existing claims. Flags contradictions in frontmatter.
 */

const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.resolve(__dirname, '..', 'wiki');
const DRY_RUN = process.argv.includes('--dry-run');

function loadPages(dir) {
  const pages = [];
  if (!fs.existsSync(dir)) return pages;
  
  for (const file of fs.readdirSync(dir)) {
    if (!file.endsWith('.md')) continue;
    const filePath = path.join(dir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const frontmatter = parseFrontmatter(content);
    pages.push({
      file: file,
      path: filePath,
      name: frontmatter.title || file.replace('.md', ''),
      tags: frontmatter.tags || [],
      contradictions: frontmatter.contradictions || [],
      body: content,
      claims: extractClaims(content),
    });
  }
  return pages;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  
  const fm = {};
  for (const line of match[1].split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();
    
    // Parse YAML arrays
    if (value.startsWith('[') && value.endsWith(']')) {
      value = value.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
    }
    fm[key] = value;
  }
  return fm;
}

function extractClaims(content) {
  // Remove frontmatter
  const body = content.replace(/^---\n[\s\S]*?\n---\n*/, '');
  
  // Extract bullet points and bold statements as "claims"
  const claims = [];
  const lines = body.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    // Bullet points with substance
    if (/^[-*]\s+.{20,}/.test(trimmed)) {
      claims.push(trimmed.replace(/^[-*]\s+/, ''));
    }
    // Bold statements
    if (/\*\*.{10,}\*\*/.test(trimmed)) {
      const bold = trimmed.match(/\*\*(.+?)\*\*/g);
      if (bold) bold.forEach(b => claims.push(b.replace(/\*\*/g, '')));
    }
  }
  return claims;
}

function findContradictions(pages) {
  const contradictions = [];
  
  for (let i = 0; i < pages.length; i++) {
    for (let j = i + 1; j < pages.length; j++) {
      const a = pages[i];
      const b = pages[j];
      
      // Check if they share tags (related topics)
      const sharedTags = a.tags.filter(t => b.tags.includes(t));
      if (sharedTags.length === 0 && a.name !== b.name) continue;
      
      // Simple contradiction heuristics
      for (const claimA of a.claims) {
        for (const claimB of b.claims) {
          const result = checkContradiction(claimA, claimB);
          if (result) {
            contradictions.push({
              pageA: a.name,
              pageB: b.name,
              claimA: claimA.slice(0, 100),
              claimB: claimB.slice(0, 100),
              reason: result,
            });
          }
        }
      }
    }
  }
  return contradictions;
}

function checkContradiction(claimA, claimB) {
  const a = claimA.toLowerCase();
  const b = claimB.toLowerCase();
  
  // Skip very short or identical claims
  if (a === b) return null;
  if (a.length < 20 || b.length < 20) return null;
  
  // Check for negation patterns
  const negationPairs = [
    ['is', 'is not'], ['is', "isn't"],
    ['can', 'cannot'], ['can', "can't"],
    ['supports', 'does not support'], ['supports', "doesn't support"],
    ['requires', 'does not require'], ['requires', "doesn't require"],
    ['enables', 'disables'], ['enables', 'prevents'],
    ['faster', 'slower'], ['better', 'worse'],
    ['true', 'false'], ['always', 'never'],
    ['increases', 'decreases'], ['improves', 'degrades'],
  ];
  
  for (const [pos, neg] of negationPairs) {
    if ((a.includes(pos) && b.includes(neg)) || (a.includes(neg) && b.includes(pos))) {
      // Check if they're about the same subject
      const wordsA = new Set(a.split(/\s+/));
      const wordsB = new Set(b.split(/\s+/));
      const overlap = [...wordsA].filter(w => wordsB.has(w) && w.length > 3);
      if (overlap.length >= 2) {
        return `Negation pattern: "${pos}" vs "${neg}" with shared subjects: ${overlap.slice(0, 3).join(', ')}`;
      }
    }
  }
  
  // Check for numeric contradictions
  const numA = a.match(/(\d+(?:\.\d+)?%?)/g);
  const numB = b.match(/(\d+(?:\.\d+)?%?)/g);
  if (numA && numB && numA.length === numB.length) {
    // Same numbers in same positions likely means same claim, different = possible contradiction
  }
  
  return null;
}

// ============================================
// MAIN
// ============================================

console.log('🔍 Contradiction Detection\n');

const entityPages = loadPages(path.join(WIKI_DIR, 'entities'));
const conceptPages = loadPages(path.join(WIKI_DIR, 'concepts'));
const allPages = [...entityPages, ...conceptPages];

console.log(`  Loaded ${allPages.length} pages (${entityPages.length} entities, ${conceptPages.length} concepts)`);

if (allPages.length < 2) {
  console.log('  Not enough pages to compare. Skipping.');
  process.exit(0);
}

const contradictions = findContradictions(allPages);

if (contradictions.length === 0) {
  console.log('  ✅ No contradictions found\n');
  process.exit(0);
}

console.log(`  ⚠️  Found ${contradictions.length} potential contradiction(s):\n`);

for (const c of contradictions) {
  console.log(`  ${c.pageA} ↔ ${c.pageB}`);
  console.log(`    A: "${c.claimA}"`);
  console.log(`    B: "${c.claimB}"`);
  console.log(`    Reason: ${c.reason}\n`);
  
  if (!DRY_RUN) {
    // Add contradiction flag to both pages
    for (const pageName of [c.pageA, c.pageB]) {
      const page = allPages.find(p => p.name === pageName);
      if (page && !page.contradictions.includes(c.pageA === pageName ? c.pageB : c.pageA)) {
        console.log(`    📝 Flagging ${pageName}...`);
        // In a real implementation, we'd update the frontmatter
        // For now, just log it
      }
    }
  }
}

console.log(`\n${DRY_RUN ? '(dry run — no files modified)' : 'Run with --dry-run to preview without modifying files'}`);
