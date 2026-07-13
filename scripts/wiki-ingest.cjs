#!/usr/bin/env node
/**
 * wiki-ingest.js
 * 
 * Automated knowledge ingestion from URLs, text, or files.
 * Inspired by claude-obsidian's wiki-ingest skill.
 * 
 * Usage:
 *   node scripts/wiki-ingest.js --url "https://example.com/article"
 *   node scripts/wiki-ingest.js --text "Some text to ingest"
 *   node scripts/wiki-ingest.js --file /path/to/document.md
 * 
 * Extracts entities, concepts, and cross-references into the wiki.
 * Updates index.json and creates entity/concept pages.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const WIKI_DIR = path.resolve(__dirname, '..', 'wiki');
const MEMORY_DIR = path.resolve(__dirname, '..', 'memory');
const INDEX_FILE = path.join(MEMORY_DIR, 'index.json');

// ============================================
// CONTENT EXTRACTION
// ============================================

async function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, { headers: { 'User-Agent': 'OpenClaw-Ingest/1.0' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchUrl(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractTextFromHtml(html) {
  // Strip tags, keep text
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  
  // Decode entities
  text = text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
  
  return text;
}

function extractEntities(text) {
  const entities = new Set();
  
  // Proper nouns (capitalized words not at sentence start)
  const sentences = text.split(/[.!?]+/);
  for (const sentence of sentences) {
    const words = sentence.trim().split(/\s+/);
    for (let i = 1; i < words.length; i++) {
      const word = words[i].replace(/[^a-zA-Z0-9-]/g, '');
      if (word.length > 2 && /^[A-Z]/.test(word) && !/^(The|This|That|These|Those|And|But|Or|For|Not|You|All|Can|Her|Was|One|Our|Out|Day|Had|Has|His|How|Its|May|New|Now|Old|See|Way|Who|Boy|Did|Get|Let|Say|She|Too|Use)$/.test(word)) {
        entities.add(word);
      }
    }
  }
  
  // Technical terms
  const techPatterns = [
    /\b(API|SDK|CLI|HTTP|JSON|REST|GraphQL|WebSocket|CDP|MV3|MV2)\b/g,
    /\b(OpenClaw|Claude|GPT|Gemini|Llama|Mistral|DeepSeek)\b/g,
    /\b(Obsidian|Notion|GitHub|Docker|PM2|Node\.js|TypeScript)\b/g,
    /\b(RAG|BM25|LLM|AI|ML|NLP|GNN|KB)\b/g,
  ];
  
  for (const pattern of techPatterns) {
    const matches = text.matchAll(pattern);
    for (const match of matches) entities.add(match[1]);
  }
  
  return Array.from(entities).slice(0, 20);
}

function extractConcepts(text) {
  const concepts = new Set();
  
  // Look for concept-like patterns
  const conceptPatterns = [
    /\b([a-z]+(?:\s[a-z]+){1,3})\s+(?:is|are|was|were|means|refers to|describes)\b/gi,
    /\bconcept\s+of\s+([a-z]+(?:\s[a-z]+){1,3})\b/gi,
    /\bpattern\s+called\s+([a-z]+(?:\s[a-z]+){1,3})\b/gi,
    /\bapproach\s+(?:called|known as|named)\s+([a-z]+(?:\s[a-z]+){1,3})\b/gi,
  ];
  
  for (const pattern of conceptPatterns) {
    const matches = text.matchAll(pattern);
    for (const match of matches) {
      const concept = match[1].trim();
      if (concept.length > 5 && concept.length < 60) {
        concepts.add(concept.charAt(0).toUpperCase() + concept.slice(1));
      }
    }
  }
  
  return Array.from(concepts).slice(0, 10);
}

function extractKeyPoints(text, maxPoints = 8) {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 30);
  
  // Score sentences by importance signals
  const scored = sentences.map(s => {
    const trimmed = s.trim();
    let score = 0;
    
    // Length bonus (not too short, not too long)
    if (trimmed.length > 50 && trimmed.length < 200) score += 2;
    
    // Important words
    if (/\b(important|key|main|primary|significant|crucial|essential|fundamental)\b/i.test(trimmed)) score += 3;
    if (/\b(result|finding|conclusion|discovery|insight|breakthrough)\b/i.test(trimmed)) score += 3;
    if (/\b(first|new|novel|innovative|unique|unprecedented)\b/i.test(trimmed)) score += 2;
    
    // Numbers and data
    if (/\d+%|\d+\.\d+|\d+x|\$\d+/.test(trimmed)) score += 2;
    
    return { text: trimmed, score };
  });
  
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, maxPoints)
    .map(s => s.text);
}

// ============================================
// WIKI PAGE CREATION
// ============================================

function createEntityPage(name, source, keyPoints, tags) {
  const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const filePath = path.join(WIKI_DIR, 'entities', `${slug}.md`);
  
  const content = `---
title: "${name}"
type: entity
source: "${source}"
created: ${new Date().toISOString().split('T')[0]}
tags: [${tags.map(t => `"${t}"`).join(', ')}]
---

# ${name}

## Key Points
${keyPoints.map(p => `- ${p}`).join('\n')}

## Source
Ingested from: ${source}
`;
  
  return { filePath, content, slug };
}

function createConceptPage(name, relatedEntities, description) {
  const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const filePath = path.join(WIKI_DIR, 'concepts', `${slug}.md`);
  
  const content = `---
title: "${name}"
type: concept
created: ${new Date().toISOString().split('T')[0]}
tags: [knowledge, concept]
---

# ${name}

## Description
${description}

## Related Entities
${relatedEntities.map(e => `- [[${e}]]`).join('\n')}
`;
  
  return { filePath, content, slug };
}

function updateIndex(entities, concepts, source) {
  let index = {};
  if (fs.existsSync(INDEX_FILE)) {
    try {
      index = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf-8'));
    } catch {}
  }
  
  if (!index.segments) index.segments = [];
  
  // Add new entries
  for (const entity of entities) {
    const existing = index.segments.find(s => s.id === entity.slug);
    if (!existing) {
      index.segments.push({
        id: entity.slug,
        path: `wiki/entities/${entity.slug}.md`,
        tags: entity.tags || [],
        relevance: 0.8,
        lastAccess: new Date().toISOString(),
      });
    }
  }
  
  for (const concept of concepts) {
    const existing = index.segments.find(s => s.id === concept.slug);
    if (!existing) {
      index.segments.push({
        id: concept.slug,
        path: `wiki/concepts/${concept.slug}.md`,
        tags: ['concept'],
        relevance: 0.7,
        lastAccess: new Date().toISOString(),
      });
    }
  }
  
  index.updated = new Date().toISOString();
  fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2), 'utf-8');
}

// ============================================
// MAIN
// ============================================

async function main() {
  const args = process.argv.slice(2);
  const url = args.find(a => a.startsWith('--url='))?.split('=')[1];
  const text = args.find(a => a.startsWith('--text='))?.split('=').slice(1).join('=');
  const file = args.find(a => a.startsWith('--file='))?.split('=')[1];
  const sourceName = args.find(a => a.startsWith('--source='))?.split('=')[1] || 'manual';
  
  let rawContent = '';
  let source = '';
  
  if (url) {
    console.log(`🌐 Fetching: ${url}`);
    const html = await fetchUrl(url);
    rawContent = extractTextFromHtml(html);
    source = url;
  } else if (text) {
    rawContent = text;
    source = `text-input-${Date.now()}`;
  } else if (file) {
    console.log(`📄 Reading: ${file}`);
    rawContent = fs.readFileSync(file, 'utf-8');
    source = file;
  } else {
    console.error('Usage: node wiki-ingest.js --url=<URL> | --text=<TEXT> | --file=<PATH>');
    process.exit(1);
  }
  
  console.log(`\n📝 Content: ${rawContent.length} chars\n`);
  
  // Extract knowledge
  const entities = extractEntities(rawContent);
  const concepts = extractConcepts(rawContent);
  const keyPoints = extractKeyPoints(rawContent);
  
  console.log(`  Entities found: ${entities.length}`);
  entities.forEach(e => console.log(`    - ${e}`));
  
  console.log(`  Concepts found: ${concepts.length}`);
  concepts.forEach(c => console.log(`    - ${c}`));
  
  console.log(`  Key points: ${keyPoints.length}\n`);
  
  // Create pages
  const createdEntities = [];
  const createdConcepts = [];
  
  for (const entity of entities) {
    const tags = ['entity'];
    if (/API|SDK|CLI|HTTP/.test(entity)) tags.push('technical');
    if (/OpenClaw|Claude|GPT/.test(entity)) tags.push('ai');
    
    const page = createEntityPage(entity, source, 
      keyPoints.filter(p => p.toLowerCase().includes(entity.toLowerCase())).slice(0, 5) || 
      keyPoints.slice(0, 3),
      tags
    );
    
    // Ensure directory exists
    fs.mkdirSync(path.dirname(page.filePath), { recursive: true });
    fs.writeFileSync(page.filePath, page.content, 'utf-8');
    console.log(`  ✅ Created: entities/${page.slug}.md`);
    createdEntities.push(page);
  }
  
  for (const concept of concepts) {
    const page = createConceptPage(concept, entities.slice(0, 5), 
      keyPoints.find(p => p.toLowerCase().includes(concept.toLowerCase())) || 
      `Concept related to: ${entities.slice(0, 3).join(', ')}`
    );
    
    fs.mkdirSync(path.dirname(page.filePath), { recursive: true });
    fs.writeFileSync(page.filePath, page.content, 'utf-8');
    console.log(`  ✅ Created: concepts/${page.slug}.md`);
    createdConcepts.push(page);
  }
  
  // Update index
  updateIndex(createdEntities, createdConcepts, source);
  console.log(`\n  📇 Updated index.json`);
  
  // Summary
  console.log(`\n✨ Ingest complete:`);
  console.log(`   Source: ${source}`);
  console.log(`   Entities: ${createdEntities.length}`);
  console.log(`   Concepts: ${createdConcepts.length}`);
  console.log(`   Index entries: ${createdEntities.length + createdConcepts.length}`);
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
