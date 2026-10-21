from __future__ import annotations

import contextlib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import time
import urllib.request
from urllib.parse import urlparse


class Blocked(RuntimeError):
    pass


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def command(argv, cwd, timeout=180):
    """Only operator-supplied argv, never model-generated shell commands."""
    if not isinstance(argv, list) or not argv or not all(isinstance(s, str) for s in argv):
        raise Blocked('El comando debe ser un array de argumentos')
    proc = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            start_new_session=True)
    try:
        output, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        raise Blocked('Tiempo agotado en comando configurado')
    return proc.returncode, output.decode(errors='replace')[-12000:]


def git(repo, *args):
    code, output = command(['git', *args], repo)
    if code:
        raise Blocked('Git: ' + output)
    return output.strip()


def safe_source(root, name, allowed):
    p = PurePosixPath(name)
    denied = {'.git', '.github', 'node_modules', 'tests', 'test', '__tests__', 'secrets'}
    if (not isinstance(name, str) or name not in allowed or p.is_absolute() or '..' in p.parts
            or any(s in denied or s.startswith('.env') for s in p.parts)
            or any(s in p.name.lower() for s in ('test.', '.spec.', 'lock.', 'credential', 'secret'))
            or p.suffix.lower() not in {'.html', '.css', '.js', '.jsx', '.ts', '.tsx', '.py', '.vue', '.svelte'}):
        raise Blocked('Archivo fuera del alcance de reparación: ' + str(name))
    root = Path(root).resolve()
    candidate = root.joinpath(*p.parts)
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
        raise Blocked('Symlink o ruta fuera del proyecto')
    if not candidate.is_file() or candidate.stat().st_size > 80000:
        raise Blocked('Archivo ausente o demasiado grande: ' + name)
    return candidate


def validate_project(p):
    if not p.get('id') or not p.get('name'):
        raise Blocked('Falta id o nombre del proyecto')
    repo = Path(p['repo']).resolve()
    if not (repo / '.git').exists():
        raise Blocked('Se requiere un checkout Git local')
    u = urlparse(p['base_url'])
    # Repairs always exercise a disposable LOCAL app instance, never production.
    if u.scheme != 'http' or u.hostname not in {'localhost', '127.0.0.1'} or not u.port:
        raise Blocked('base_url debe ser http://127.0.0.1:PUERTO de una copia de prueba')
    if not p.get('start') or not p.get('verify') or not p.get('journeys'):
        raise Blocked('Configurar start, verify y recorridos con aserciones')
    if not all(any(s.get('action', '').startswith('expect_') for s in j.get('steps', [])) for j in p['journeys']):
        raise Blocked('Cada recorrido necesita un resultado esperado comprobable')
    for name in p.get('editable_files', []):
        safe_source(repo, name, p['editable_files'])
    if len(p.get('editable_files', [])) > 30:
        raise Blocked('Dividir el contexto en módulos de hasta 30 archivos')
    return repo


@contextlib.contextmanager
def app_server(project, workspace, output):
    """A port already in use must not accidentally verify an unrelated app."""
    import socket
    u = urlparse(project['base_url'])
    with socket.socket() as sock:
        if sock.connect_ex(('127.0.0.1', u.port)) == 0:
            raise Blocked('Puerto de pruebas ocupado; detener esa instancia o elegir otro puerto')
    if project.get('prepare'):
        code, log = command(project['prepare'], workspace, 600)
        (output / 'prepare.log').write_text(log)
        if code:
            raise Blocked('Falló la preparación del proyecto; ver prepare.log')
    with (output / 'server.log').open('w') as log:
        proc = subprocess.Popen(project['start'], cwd=workspace, stdout=log, stderr=log,
                                start_new_session=True)
        try:
            deadline = time.monotonic() + project.get('startup_timeout', 60)
            while time.monotonic() < deadline:
                if proc.poll() is not None:
                    raise Blocked('La app terminó durante el inicio; ver server.log')
                try:
                    with urllib.request.urlopen(project['base_url'], timeout=1) as r:
                        if r.status < 400:
                            break
                except Exception:
                    time.sleep(.2)
            else:
                raise Blocked('La copia de prueba no inició a tiempo')
            yield
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()


def apply_edits(root, proposal, allowed):
    edits = proposal.get('edits')
    if not isinstance(edits, list) or not 1 <= len(edits) <= 6:
        raise Blocked('Ollama no devolvió entre 1 y 6 cambios válidos')
    prepared = []
    seen = set()
    for edit in edits:
        path = safe_source(root, edit.get('path', ''), allowed)
        if path in seen:
            raise Blocked('Archivo duplicado en la propuesta')
        seen.add(path)
        before, after = edit.get('before'), edit.get('after')
        content = path.read_text()
        if not isinstance(before, str) or not before or content.count(before) != 1:
            raise Blocked('El texto original no coincide exactamente una vez')
        if not isinstance(after, str) or len(after) > 40000 or before == after:
            raise Blocked('Reemplazo vacío, excesivo o sin cambios')
        prepared.append((path, content.replace(before, after, 1)))
    for path, content in prepared:
        path.write_text(content)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
