// Fix index.json — strip doubled memory/ prefix from segment file paths
const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'memory', 'index.json');
const idx = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const memoryDir = path.join(__dirname, '..', 'memory');

let fixed = 0;
const issues = [];

for (const seg of idx.segments) {
    // Ensure file property exists
    if (!seg.file && seg.path) {
        seg.file = seg.path;
        delete seg.path;
        fixed++;
    }
    if (!seg.file) {
        seg.file = `segments/${seg.id}.md`;
        fixed++;
    }

    // Strip doubled "memory/" prefix
    if (seg.file.startsWith('memory/')) {
        seg.file = seg.file.replace(/^memory\//, '');
        fixed++;
    }

    // Validate
    const full = path.join(memoryDir, seg.file);
    const exists = fs.existsSync(full);
    const mark = exists ? 'OK' : 'MISSING';
    console.log(`  [${mark}] ${seg.id} -> ${seg.file}`);
    if (!exists) issues.push(seg.id);
}

// Update lastMaintenance
idx.lastMaintenance = new Date().toISOString().slice(0, 10);

fs.writeFileSync(indexPath, JSON.stringify(idx, null, 2), 'utf8');
console.log(`\nFixed ${fixed} entries. Saved index.json.`);
if (issues.length) {
    console.log(`ISSUES: ${issues.join(', ')}`);
    process.exit(1);
} else {
    console.log('All segments resolve correctly.');
}
