"""Local control plane. Fixed operator-owned project registry; no arbitrary commands over HTTP."""
import argparse
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import threading
import time
from urllib.parse import urlparse

from .core import Blocked, write_json
from .ollama import Ollama
from .runner import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects', default='projects.json')
    parser.add_argument('--data', default='quality-data')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8787)
    args = parser.parse_args()
    projects = json.loads(Path(args.projects).read_text())['projects']
    registry = {p['id']: p for p in projects}
    if len(registry) != len(projects):
        raise Blocked('IDs de proyecto duplicados')
    data = Path(args.data).resolve()
    data.mkdir(parents=True, exist_ok=True)
    for path in data.glob('*/report.json'):
        old = json.loads(path.read_text())
        if old['state'] in {'QUEUED', 'PREPARING', 'TESTING', 'ANALYZING', 'REPAIRING', 'VERIFYING'}:
            old.update(state='BLOCKED', error='Proceso interrumpido; volver a ejecutar para nueva evidencia')
            write_json(path, old)
    token = os.environ.get('QUALITY_TOKEN') or secrets.token_urlsafe(32)
    if not os.environ.get('QUALITY_TOKEN'):
        print('Token local de esta sesión: ' + token, flush=True)
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def send(self, status, body, mime='application/json'):
            raw = json.dumps(body, ensure_ascii=False).encode() if mime == 'application/json' else body
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob:; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def authorized(self):
            if not hmac.compare_digest(self.headers.get('Authorization', ''), 'Bearer ' + token):
                self.send(401, {'error': 'Ingresar token local'})
                return False
            return True

        def do_GET(self):
            path = urlparse(self.path).path
            static = {'/': ('dashboard.html', 'text/html; charset=utf-8'),
                      '/dashboard.js': ('dashboard.js', 'text/javascript; charset=utf-8'),
                      '/dashboard.css': ('dashboard.css', 'text/css; charset=utf-8')}
            if path in static:
                name, mime = static[path]
                return self.send(200, Path(__file__).with_name(name).read_bytes(), mime)
            if not self.authorized():
                return
            if path == '/api/projects':
                return self.send(200, [{'id': p['id'], 'name': p['name'], 'base_url': p['base_url']} for p in projects])
            if path == '/api/runs':
                rows = [json.loads(p.read_text()) for p in sorted(data.glob('*/report.json'), reverse=True)[:100]]
                return self.send(200, rows)
            if path.startswith('/api/evidence/'):
                rel = path.removeprefix('/api/evidence/')
                target = (data / rel).resolve()
                # Only explicitly published evidence, never project sources or logs/secrets.
                if not target.is_relative_to(data) or len(Path(rel).parts) != 3 or target.suffix != '.png':
                    return self.send(403, {'error': 'Evidencia no permitida'})
                if target.is_file():
                    return self.send(200, target.read_bytes(), 'image/png')
            return self.send(404, {'error': 'No encontrado'})

        def do_POST(self):
            if not self.authorized():
                return
            if self.headers.get('Origin') and urlparse(self.headers['Origin']).netloc != self.headers.get('Host'):
                return self.send(403, {'error': 'Origen no permitido'})
            if self.path != '/api/runs':
                return self.send(404, {'error': 'No encontrado'})
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size < 4096:
                    raise ValueError('Solicitud demasiado grande o vacía')
                body = json.loads(self.rfile.read(size))
                project = registry[body['project']]
                mode = body['mode']
                if mode not in {'test', 'repair'}:
                    raise ValueError('Modo inválido')
            except (ValueError, KeyError, TypeError) as e:
                return self.send(400, {'error': str(e)})
            if not lock.acquire(blocking=False):
                return self.send(409, {'error': 'Hay una ejecución activa; revisar progreso'})
            run_id = time.strftime('%Y%m%d-%H%M%S') + '-' + secrets.token_hex(4)
            folder = data / run_id
            try:
                write_json(folder / 'report.json', {'id': run_id, 'project': project['id'],
                                                   'mode': mode, 'state': 'QUEUED', 'events': [], 'attempts': []})
                def work():
                    try:
                        ai = Ollama(os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434'),
                                    os.environ['OLLAMA_MODEL'], os.environ.get('OLLAMA_VISION') == '1') if os.environ.get('OLLAMA_MODEL') else None
                        run(project, folder, mode, ai)
                    finally:
                        lock.release()
                threading.Thread(target=work, daemon=True).start()
            except Exception:
                lock.release()
                raise
            return self.send(202, {'id': run_id})

        def log_message(self, *args):
            pass  # Avoid URLs / query data in access logs.

    print(f'ARQUITEKTA Quality: http://{args.host}:{args.port}', flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
