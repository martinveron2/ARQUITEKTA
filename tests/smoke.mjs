import fs from 'node:fs';
const checks=[
 ['page', 'src/app/page.tsx'],
 ['shell','src/components/AppShell.tsx'],
 ['catalog','src/lib/catalog.ts'],
 ['principle0','AGENTS.md'],
 ['roadmap','ROADMAP.md'],
 ['portable','infrastructure/portable']
];
for(const [name,path] of checks){if(!fs.existsSync(new URL('../'+path,import.meta.url))) throw new Error(`Missing ${name}: ${path}`)}
const agents=fs.readFileSync(new URL('../AGENTS.md',import.meta.url),'utf8');
if(!/PRINCIPIO 0/.test(agents)) throw new Error('Principio 0 missing');
console.log(`ARQUITEKTA smoke OK — ${checks.length} checks`);
