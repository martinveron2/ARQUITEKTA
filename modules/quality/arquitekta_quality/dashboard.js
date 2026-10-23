let token = '', timer, imageUrls = [];
const localPath = path => new URL('.' + path, location.href).pathname;
const el = id => document.getElementById(id);
const node = (tag, text) => { const n = document.createElement(tag); n.textContent = text; return n; };
async function api(path, options = {}) {
  const response = await fetch(localPath(path), {...options, headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}});
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
  const filter = el('project').value;
  for (const run of runs.filter(r => !filter || r.project === filter)) {
    const article = node('article', '');
    article.append(node('h3', run.project + ' · ' + run.id), node('span', ['QUEUED','PREPARING','TESTING','ANALYZING','REPAIRING','VERIFYING'].includes(run.state) ? 'ARKITECTA está trabajando · ' + (run.events?.at(-1)?.detail || run.state) : run.state));
    article.lastChild.className = 'state';
    if (run.error) article.append(node('p', run.error));
    const latest = run.after || run.before;
    if (latest) {
      article.append(node('p', `${latest.checks.length} recorridos · ${latest.findings.length} hallazgos`));
      const list = node('ul', '');
      latest.findings.slice(0, 20).forEach(f => list.append(node('li', `${f.check}: ${f.kind} — ${f.detail}`)));
      const findings = node('details', '');
      findings.append(node('summary', 'Ver hallazgos (hasta 20; salida completa en JSON)'), list);
      article.append(findings, node('p', latest.coverage));
    }
    const details = node('details', '');
    details.append(node('summary', 'Ver progreso y reparación'), node('pre', (run.events || []).map(e => `${e.state}: ${e.detail}`).join('\n')));
    if (run.branch) details.append(node('p', 'Rama: ' + run.branch));
    article.append(details);
    const download = node('button', 'Descargar informe completo JSON');
    download.onclick = () => {
      const url = URL.createObjectURL(new Blob([JSON.stringify(run, null, 2)], {type:'application/json'}));
      imageUrls.push(url); const link = node('a', ''); link.href = url; link.download = run.id + '.json'; link.click();
    };
    article.append(download);
    for (const phase of ['before', ...((run.attempts || []).map(a => 'after-' + a.number))]) {
      const result = phase === 'before' ? run.before : run.after;
      if (!result) continue;
      const gallery = node('details', ''); gallery.append(node('summary', phase === 'before' ? 'ANTES · todas las capturas' : 'DESPUÉS · intento ' + phase.split('-')[1]));
      for (const check of result.checks) {
        const show = node('button', check.viewport + ' · ' + check.journey);
        show.onclick = async () => {
          try {
            const response = await fetch(localPath(`/api/evidence/${run.id}/${phase}/${check.id}.png`), {headers:{Authorization:'Bearer ' + token}});
            if (!response.ok) throw Error('Captura no disponible');
            const url = URL.createObjectURL(await response.blob()); imageUrls.push(url);
            const img = node('img', ''); img.alt = phase + ' · ' + check.journey; img.src = url; show.replaceWith(img);
          } catch(e) { message(e.message); }
        };
        gallery.append(show);
      }
      article.append(gallery);
    }
    if (run.before) {
      const button = node('button', 'Ver captura móvil inicial');
      button.onclick = async () => {
        try {
          const response = await fetch(localPath(`/api/evidence/${run.id}/before/mobile-0.png`), {headers: {'Authorization': 'Bearer ' + token}});
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
    el('register').disabled = el('test').disabled = !projects.length;
    const requested = new URLSearchParams(location.search).get('project');
    if (projects.some(p => p.id === requested)) el('project').value = requested;
    const scope = () => {const p=projects.find(p=>p.id===el('project').value); el('repair').disabled=!p || p.permissions?.join(',') === 'audit';};
    el('project').onchange = () => {scope(); refresh().catch(e=>message(e.message));}; scope();
    message(projects.length ? 'Motor conectado. Elegí una app y ejecutá.' : 'Sin proyectos: configurar projects.json.');
    await refresh();
  } catch(e) { el('test').disabled = el('repair').disabled = true; message(e.message); }
};
for (const mode of ['test','repair']) el(mode).onclick = async () => {
  try { await api('/api/runs', {method:'POST', body:JSON.stringify({project:el('project').value,mode})}); message('Ejecución iniciada. El progreso se actualiza automáticamente.'); await refresh(); }
  catch(e) { message(e.message); }
};
el('refresh').onclick = () => refresh().catch(e => message(e.message));


el('register').onclick = async () => {try {await api('/api/connections',{method:'POST',body:JSON.stringify({project:el('project').value})}); message('Aplicación conectada · permiso de auditoría · datos sintéticos');} catch(e) {message(e.message);}};
el('clear').onclick = () => {el('project').selectedIndex=-1; refresh().catch(e=>message(e.message));};
