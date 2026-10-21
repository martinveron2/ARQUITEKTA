let token = '', timer, imageUrls = [];
const el = id => document.getElementById(id);
const node = (tag, text) => { const n = document.createElement(tag); n.textContent = text; return n; };
async function api(path, options = {}) {
  const response = await fetch(path, {...options, headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}});
  const body = await response.json();
  if (!response.ok) throw Error(body.error || 'Error de conexión');
  return body;
}
function message(text) { el('message').textContent = text; }
async function refresh() {
  const runs = await api('/api/runs');
  imageUrls.forEach(URL.revokeObjectURL); imageUrls = [];
  el('runs').replaceChildren();
  if (!runs.length) el('runs').append(node('p', 'Todavía no ejecutaste pruebas.'));
  for (const run of runs) {
    const article = node('article', '');
    article.append(node('h3', run.project + ' · ' + run.id), node('span', run.state));
    article.lastChild.className = 'state';
    if (run.error) article.append(node('p', run.error));
    const latest = run.after || run.before;
    if (latest) {
      article.append(node('p', `${latest.checks.length} recorridos · ${latest.findings.length} hallazgos`));
      const list = node('ul', '');
      latest.findings.slice(0, 20).forEach(f => list.append(node('li', `${f.check}: ${f.kind} — ${f.detail}`)));
      article.append(list, node('p', latest.coverage));
    }
    const details = node('details', '');
    details.append(node('summary', 'Ver progreso y reparación'), node('pre', (run.events || []).map(e => `${e.state}: ${e.detail}`).join('\n')));
    if (run.branch) details.append(node('p', 'Rama: ' + run.branch));
    article.append(details);
    if (run.before) {
      const button = node('button', 'Ver captura móvil inicial');
      button.onclick = async () => {
        try {
          const response = await fetch(`/api/evidence/${run.id}/before/mobile-0.png`, {headers: {'Authorization': 'Bearer ' + token}});
          if (!response.ok) throw Error('Captura no disponible');
          const url = URL.createObjectURL(await response.blob()); imageUrls.push(url);
          const img = document.createElement('img'); img.alt = 'Evidencia móvil antes de reparar'; img.src = url;
          // Blob images require explicit CSP permission, see server.
          button.replaceWith(img);
        } catch(e) { message(e.message); }
      };
      article.append(button);
    }
    el('runs').append(article);
  }
  clearTimeout(timer);
  if (runs.some(r => ['QUEUED','PREPARING','TESTING','ANALYZING','REPAIRING','VERIFYING'].includes(r.state)))
    timer = setTimeout(() => refresh().catch(e => message(e.message)), 3000);
}
el('connect').onclick = async () => {
  token = el('token').value;
  try {
    const projects = await api('/api/projects'); el('project').replaceChildren();
    projects.forEach(p => { const option = node('option', p.name); option.value = p.id; el('project').append(option); });
    el('test').disabled = el('repair').disabled = !projects.length;
    message(projects.length ? 'Motor conectado. Elegí una app y ejecutá.' : 'Sin proyectos: configurar projects.json.');
    await refresh();
  } catch(e) { el('test').disabled = el('repair').disabled = true; message(e.message); }
};
for (const mode of ['test','repair']) el(mode).onclick = async () => {
  try { await api('/api/runs', {method:'POST', body:JSON.stringify({project:el('project').value,mode})}); message('Ejecución iniciada. El progreso se actualiza automáticamente.'); await refresh(); }
  catch(e) { message(e.message); }
};
el('refresh').onclick = () => refresh().catch(e => message(e.message));
