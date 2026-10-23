from pathlib import Path
from urllib.parse import urljoin, urlparse
from .core import Blocked

VIEWPORTS = [('mobile', 390, 844), ('small-mobile', 320, 740), ('tablet', 768, 1024), ('desktop', 1440, 900)]

# Deterministic signals, not aesthetic judgments. Screenshots remain evidence for review.
LAYOUT = r'''() => {
 const issues = [];
 const width = document.documentElement.clientWidth;
 if (document.documentElement.scrollWidth > width + 2)
   issues.push({kind:'horizontal-overflow', detail:`${document.documentElement.scrollWidth}px > ${width}px`});
 const scope = document.querySelector('dialog:modal') || document;
 const controls = [...scope.querySelectorAll('button,a[href],input,select,textarea,[role="button"]')];
 for (const el of controls) {
   const r = el.getBoundingClientRect(), s = getComputedStyle(el);
   if (!r.width || !r.height || s.visibility === 'hidden' || s.display === 'none') continue;
   if (r.right <= 0 || r.left >= width || el.closest('[inert]')) continue;
   const detail = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('name') || el.tagName).trim().slice(0,100);
   if (r.left < -2 || r.right > width + 2) issues.push({kind:'control-outside-width', detail});
   if (r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= width) {
     const top = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
     if (top && !el.contains(top) && !top.contains(el)) issues.push({kind:'covered-control', detail});
   }
 }
 return issues.slice(0,60);
}'''


def probe(project, output, progress=None):
    try:
        from playwright.sync_api import sync_playwright, expect
    except ImportError as e:
        raise Blocked('Instalar requirements.txt y los navegadores Playwright') from e
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    findings, checks = [], []
    origin = urlparse(project['base_url']).netloc
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for label, width, height in VIEWPORTS:
                for index, journey in enumerate(project['journeys']):
                    context = browser.new_context(viewport={'width': width, 'height': height},
                                                  is_mobile='mobile' in label, has_touch='mobile' in label)
                    # Local test copies may not send emails, payments or access production services.
                    context.route('**/*', lambda route: route.continue_() if
                                  urlparse(route.request.url).netloc == origin and
                                  (not project.get('attach_readonly') or route.request.method in {'GET','HEAD','OPTIONS'}) else route.abort())
                    context.tracing.start(screenshots=True, snapshots=True, sources=False)
                    page = context.new_page()
                    for name, value in project.get('test_storage', {}).items():
                        import json
                        page.add_init_script('localStorage.setItem(' + json.dumps(name) + ',' + json.dumps(value) + ')')
                    page.set_default_timeout(5000)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)[:300]))
                    page.on('console', lambda msg: errors.append('Console: ' + msg.text[:300]) if msg.type == 'error' else None)
                    page.on('requestfailed', lambda req: errors.append('Request failed: ' + urlparse(req.url).path))
                    page.on('response', lambda r: errors.append(f'HTTP {r.status}: {urlparse(r.url).path}')
                            if r.status >= 400 else None)
                    key = f'{label}-{index}'
                    if progress:
                        progress(f'{label} · {journey["name"]} ({index + 1}/{len(project["journeys"])})')
                    checks.append({'id': key, 'journey': journey['name'], 'viewport': label})
                    step_index = 0
                    try:
                        for step_index, step in enumerate(journey['steps'], 1):
                            action = step['action']
                            if action == 'goto':
                                url = urljoin(project['base_url'], step['path'])
                                if urlparse(url).netloc != origin:
                                    raise Blocked('Recorrido fuera del origen local')
                                page.goto(url, wait_until='networkidle', timeout=20000)
                            elif action == 'click':
                                page.locator(step.get('mobile_selector', step['selector']) if width < 768 else step['selector']).click()
                            elif action == 'fill':
                                page.locator(step['selector']).fill(step['value'])
                            elif action == 'expect_text':
                                expect(page.locator(step['selector'])).to_contain_text(step['value'])
                            elif action == 'expect_visible':
                                expect(page.locator(step['selector'])).to_be_visible()
                            elif action == 'reload':
                                page.reload(wait_until='networkidle')
                            else:
                                raise Blocked('Acción no soportada: ' + action)
                            for issue in page.evaluate(LAYOUT):
                                findings.append(dict(issue, check=key))
                    except Exception as e:
                        findings.append({'check': key, 'kind': 'journey-failed', 'detail': str(e)[:1200]})
                    finally:
                        for finding in findings:
                            if finding['check'] == key:
                                finding.update(severity='high' if finding['kind'] == 'journey-failed' else 'medium',
                                               screenshot=f'{key}.png', trace=f'{key}.zip',
                                               journey=journey['name'], viewport={'width':width,'height':height},
                                               steps=journey['steps'][:step_index],
                                               reproduction='Repetir los pasos adjuntos en una copia con datos sintéticos')
                        try:
                            page.screenshot(path=str(output / f'{key}.png'), full_page=True)
                        finally:
                            context.tracing.stop(path=str(output / f'{key}.zip'))
                            context.close()
                    findings.extend({'check': key, 'kind': 'runtime-error', 'detail': e,
                                     'severity':'high', 'screenshot':f'{key}.png', 'trace':f'{key}.zip',
                                     'journey':journey['name'], 'viewport':{'width':width,'height':height},
                                     'steps':journey['steps'][:step_index]} for e in errors)
        finally:
            browser.close()
    unique = {(f['check'], f['kind'], f['detail']): f for f in findings}
    return {'checks': checks, 'findings': list(unique.values()),
            'coverage': 'Recorridos configurados y geometría responsive en Chromium. No equivale a toda la app, Safari/iOS real ni auditoría completa de accesibilidad.'}
