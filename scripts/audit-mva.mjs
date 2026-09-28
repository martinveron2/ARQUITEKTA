import fs from 'node:fs';
const required=['README.md','AGENTS.md','ROADMAP.md','PROJECT_STATUS.md','PROJECT_LEDGER.md','ARCHITECTURE.md','CHANGELOG.md','LICENSE','docs/USER_MANUAL.md','docs/OPERATIONS_MANUAL.md','docs/DEVELOPER_GUIDE.md','docs/SYSTEM_STATES.md','docs/SECURITY_MODEL.md','docs/screenshots/arquitekta-concept.webp'];
const missing=required.filter(p=>!fs.existsSync(new URL('../'+p,import.meta.url)));
const result={standard:'MVA seed audit',required:required.length,missing,ok:missing.length===0};
console.log(JSON.stringify(result,null,2));
process.exit(result.ok?0:1);
