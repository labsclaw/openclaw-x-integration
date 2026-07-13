#!/usr/bin/env node
/**
 * bm25-retrieve.js
 * 
 * BM25-based retrieval over wiki pages with contextual prefix.
 * Inspired by claude-obsidian's wiki-retrieve + Anthropic's Contextual Retrieval.
 * 
 * Usage:
 *   node scripts/bm25-retrieve.js build          — Build index
 *   node scripts/bm25-retrieve.js query "search query" [--top=5]
 *   node scripts/bm25-retrieve.js query "search query" --json
 * 
 * No external dependencies. Pure Node.js BM25 implementation.
 */

const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.resolve(__dirname, '..', 'wiki');
const MEMORY_DIR = path.resolve(__dirname, '..', 'memory');
const INDEX_DIR = path.join(MEMORY_DIR, 'bm25');
const INDEX_FILE = path.join(INDEX_DIR, 'index.json');
const CHUNKS_DIR = path.join(INDEX_DIR, 'chunks');

const K1 = 1.5;
const B = 0.75;

// ============================================
// TOKENIZATION
// ============================================

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length > 1 && t.length < 50);
}

function generateChunks(text, targetTokens = 200, overlap = 30) {
  const sentences = text.split(/(?<=[.!?])\s+/);
  const chunks = [];
  let currentChunk = [];
  let currentTokens = 0;
  
  for (const sentence of sentences) {
    const tokens = tokenize(sentence);
    
    if (currentTokens + tokens.length > targetTokens && currentChunk.length > 0) {
      chunks.push(currentChunk.join(' '));
      
      // Keep overlap tokens
      const overlapTokens = currentChunk.join(' ').split(/\s+/).slice(-overlap);
      currentChunk = [overlapTokens.join(' ')];
      currentTokens = overlapTokens.length;
    }
    
    currentChunk.push(sentence);
    currentTokens += tokens.length;
  }
  
  if (currentChunk.length > 0) {
    chunks.push(currentChunk.join(' '));
  }
  
  return chunks;
}

// ============================================
// CONTEXTUAL PREFIX
// ============================================

function generateContextualPrefix(chunk, pageTitle, pageTags) {
  // Lightweight contextual prefix (no LLM needed)
  // Uses page metadata to give context to each chunk
  const firstWords = chunk.split(/\s+/).slice(0, 15).join(' ');
  return `[${pageTitle}] ${pageTags.length > 0 ? `[${pageTags.join(', ')}] ` : ''}${firstWords}...`;
}

// ============================================
// BM25 SCORING
// ============================================

class BM25Index {
  constructor() {
    this.docs = [];           // { id, path, pageTitle, chunks: [{ text, contextualText }] }
    this.docFreqs = {};       // term -> number of docs containing term
    this.termFreqs = {};      // docId -> { term -> count }
    this.avgDocLength = 0;
    this.totalDocs = 0;
    this.totalTokens = 0;
  }
  
  addDocument(id, path, pageTitle, pageTags, chunks) {
    const docId = this.docs.length;
    this.docs.push({ id, path, pageTitle, pageTags, chunks: [] });
    
    for (const chunk of chunks) {
      const tokens = tokenize(chunk);
      const contextualText = generateContextualPrefix(chunk, pageTitle, pageTags);
      const chunkTokens = tokenize(contextualText);
      
      this.docs[docId].chunks.push({
        text: chunk,
        contextualText,
        tokens: chunkTokens,
      });
      
      // Update term frequencies
      this.termFreqs[`${docId}:${this.docs[docId].chunks.length - 1}`] = {};
      for (const token of chunkTokens) {
        this.termFreqs[`${docId}:${this.docs[docId].chunks.length - 1}`][token] = 
          (this.termFreqs[`${docId}:${this.docs[docId].chunks.length - 1}`][token] || 0) + 1;
        
        // Update document frequency
        const docKey = `${docId}:${token}`;
        if (!this.docFreqs[token]) this.docFreqs[token] = new Set();
        this.docFreqs[token].add(docId);
        
        this.totalTokens++;
      }
    }
    
    this.totalDocs++;
  }
  
  score(query, docId, chunkIdx) {
    const queryTokens = tokenize(query);
    const chunkKey = `${docId}:${chunkIdx}`;
    const tf = this.termFreqs[chunkKey] || {};
    const chunkTokens = this.docs[docId].chunks[chunkIdx]?.tokens || [];
    const docLength = chunkTokens.length;
    
    let score = 0;
    
    for (const qt of queryTokens) {
      const df = this.docFreqs[qt]?.size || 0;
      const idf = Math.log((this.totalDocs - df + 0.5) / (df + 0.5) + 1);
      const termFreq = tf[qt] || 0;
      const tfNorm = (termFreq * (K1 + 1)) / (termFreq + K1 * (1 - B + B * docLength / this.avgDocLength));
      
      score += idf * tfNorm;
    }
    
    return score;
  }
  
  search(query, topK = 5) {
    const results = [];
    
    for (let docIdx = 0; docIdx < this.docs.length; docIdx++) {
      const doc = this.docs[docIdx];
      
      for (let chunkIdx = 0; chunkIdx < doc.chunks.length; chunkIdx++) {
        const score = this.score(query, docIdx, chunkIdx);
        if (score > 0) {
          results.push({
            docId: doc.id,
            path: doc.path,
            pageTitle: doc.pageTitle,
            chunkIdx,
            score,
            snippet: doc.chunks[chunkIdx].text.slice(0, 200),
          });
        }
      }
    }
    
    // Sort by score, dedupe by docId (keep highest scoring chunk per doc)
    results.sort((a, b) => b.score - a.score);
    
    const seen = new Set();
    const deduped = [];
    for (const r of results) {
      if (!seen.has(r.docId)) {
        seen.add(r.docId);
        deduped.push(r);
      }
    }
    
    return deduped.slice(0, topK);
  }
  
  calculateAvgDocLength() {
    let totalLength = 0;
    let count = 0;
    
    for (const doc of this.docs) {
      for (const chunk of doc.chunks) {
        totalLength += chunk.tokens.length;
        count++;
      }
    }
    
    this.avgDocLength = count > 0 ? totalLength / count : 0;
  }
  
  serialize() {
    return {
      docs: this.docs.map(d => ({
        id: d.id,
        path: d.path,
        pageTitle: d.pageTitle,
        pageTags: d.pageTags,
        chunks: d.chunks.map(c => ({ text: c.text, contextualText: c.contextualText })),
      })),
      docFreqs: Object.fromEntries(
        Object.entries(this.docFreqs).map(([k, v]) => [k, Array.from(v)])
      ),
      termFreqs: this.termFreqs,
      avgDocLength: this.avgDocLength,
      totalDocs: this.totalDocs,
      totalTokens: this.totalTokens,
    };
  }
  
  static deserialize(data) {
    const index = new BM25Index();
    index.docs = data.docs;
    index.docFreqs = Object.fromEntries(
      Object.entries(data.docFreqs).map(([k, v]) => [k, new Set(v)])
    );
    index.termFreqs = data.termFreqs;
    index.avgDocLength = data.avgDocLength;
    index.totalDocs = data.totalDocs;
    index.totalTokens = data.totalTokens;
    return index;
  }
}

// ============================================
// BUILD INDEX
// ============================================

function buildIndex() {
  console.log('🔨 Building BM25 index...\n');
  
  const index = new BM25Index();
  
  // Scan wiki directories
  const dirs = ['entities', 'concepts', 'sources', 'synthesis', 'projects', 'comparisons'];
  
  for (const dir of dirs) {
    const dirPath = path.join(WIKI_DIR, dir);
    if (!fs.existsSync(dirPath)) continue;
    
    for (const file of fs.readdirSync(dirPath)) {
      if (!file.endsWith('.md')) continue;
      
      const filePath = path.join(dirPath, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // Parse frontmatter
      const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
      let title = file.replace('.md', '');
      let tags = [];
      
      if (fmMatch) {
        for (const line of fmMatch[1].split('\n')) {
          if (line.startsWith('title:')) title = line.split(':').slice(1).join(':').trim().replace(/"/g, '');
          if (line.startsWith('tags:')) {
            const tagMatch = line.match(/\[([^\]]+)\]/);
            if (tagMatch) tags = tagMatch[1].split(',').map(t => t.trim().replace(/"/g, ''));
          }
        }
      }
      
      // Extract body (remove frontmatter)
      const body = content.replace(/^---\n[\s\S]*?\n---\n*/, '');
      
      // Generate chunks
      const chunks = generateChunks(body);
      
      if (chunks.length > 0) {
        const id = `${dir}/${file.replace('.md', '')}`;
        index.addDocument(id, `${dir}/${file}`, title, tags, chunks);
        console.log(`  📄 ${title}: ${chunks.length} chunks`);
      }
    }
  }
  
  index.calculateAvgDocLength();
  
  // Save index
  fs.mkdirSync(INDEX_DIR, { recursive: true });
  fs.writeFileSync(INDEX_FILE, JSON.stringify(index.serialize(), null, 2), 'utf-8');
  
  // Save chunks for reference
  fs.mkdirSync(CHUNKS_DIR, { recursive: true });
  for (const doc of index.docs) {
    const chunkFile = path.join(CHUNKS_DIR, `${doc.id.replace(/\//g, '_')}.json`);
    fs.mkdirSync(path.dirname(chunkFile), { recursive: true });
    fs.writeFileSync(chunkFile, JSON.stringify(doc.chunks, null, 2), 'utf-8');
  }
  
  console.log(`\n✅ Index built:`);
  console.log(`   Documents: ${index.totalDocs}`);
  console.log(`   Unique terms: ${Object.keys(index.docFreqs).length}`);
  console.log(`   Total tokens: ${index.totalTokens}`);
  console.log(`   Saved to: ${INDEX_FILE}`);
}

// ============================================
// QUERY
// ============================================

function queryIndex(queryStr, topK = 5) {
  if (!fs.existsSync(INDEX_FILE)) {
    console.error('❌ Index not found. Run: node bm25-retrieve.js build');
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf-8'));
  const index = BM25Index.deserialize(data);
  
  const results = index.search(queryStr, topK);
  
  if (results.length === 0) {
    console.log(`\n🔍 No results for: "${queryStr}"\n`);
    return [];
  }
  
  console.log(`\n🔍 Results for: "${queryStr}"\n`);
  
  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    console.log(`  ${i + 1}. ${r.pageTitle} (score: ${r.score.toFixed(3)})`);
    console.log(`     Path: ${r.path}`);
    console.log(`     Snippet: ${r.snippet.slice(0, 120)}...\n`);
  }
  
  return results;
}

// ============================================
// MAIN
// ============================================

const command = process.argv[2];

switch (command) {
  case 'build':
    buildIndex();
    break;
  
  case 'query': {
    const queryStr = process.argv[3];
    const topK = parseInt(process.argv.find(a => a.startsWith('--top='))?.split('=')[1] || '5');
    const jsonOutput = process.argv.includes('--json');
    
    if (!queryStr) {
      console.error('Usage: node bm25-retrieve.js query "search query" [--top=5]');
      process.exit(1);
    }
    
    const results = queryIndex(queryStr, topK);
    
    if (jsonOutput) {
      console.log(JSON.stringify(results, null, 2));
    }
    break;
  }
  
  default:
    console.log('Usage:');
    console.log('  node bm25-retrieve.js build          — Build BM25 index');
    console.log('  node bm25-retrieve.js query "query"  — Search the index');
    process.exit(1);
}
