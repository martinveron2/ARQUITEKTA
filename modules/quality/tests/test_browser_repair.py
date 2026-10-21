"""Real Chromium E2E, deterministic inference double; never claims a real Ollama run."""
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest

from arquitekta_quality.core import command, git
from arquitekta_quality.runner import run


class BrowserRepairTests(unittest.TestCase):
    def test_broken_button_and_mobile_overflow_are_repaired_in_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'app'; repo.mkdir()
            original = '''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0}.card{width:900px}</style><div class="card"><button id="save">Guardar</button><p id="result">Pendiente</p></div>
<script>document.querySelector('#save').onclick=()=>{document.querySelector('#result').textContent='ERROR'}</script>'''
            (repo / 'index.html').write_text(original)
            command(['git', 'init', '-b', 'main'], repo)
            git(repo, 'add', '.')
            git(repo, '-c', 'user.name=Test', '-c', 'user.email=test@localhost', 'commit', '-m', 'fixture')
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
            project = {'id': 'fixture', 'name': 'Fixture', 'repo': str(repo),
                       'base_url': f'http://127.0.0.1:{port}/',
                       'start': [sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'],
                       'verify': [sys.executable, '-c', 'print("project validation")'],
                       'editable_files': ['index.html'], 'max_attempts': 1,
                       'journeys': [{'name': 'Guardar', 'steps': [
                           {'action': 'goto', 'path': '/'}, {'action': 'click', 'selector': '#save'},
                           {'action': 'expect_text', 'selector': '#result', 'value': 'Guardado'}]}]}
            class InferenceDouble:
                def propose(self, evidence, sources, images):
                    self.evidence = evidence
                    return {'summary': 'Reparar ancho y acción de guardar (modelo simulado de prueba)',
                            'edits': [{'path': 'index.html', 'before': sources['index.html'],
                                       'after': sources['index.html'].replace('width:900px', 'width:100%').replace("='ERROR'", "='Guardado'")}]}
            report = run(project, Path(tmp) / 'runs' / 'test', 'repair', InferenceDouble())
            self.assertEqual(report['state'], 'REPAIRED_CONFIGURED_CHECKS', json.dumps(report))
            self.assertTrue(any(f['kind'] == 'horizontal-overflow' for f in report['before']['findings']))
            self.assertTrue(any(f['kind'] == 'journey-failed' for f in report['before']['findings']))
            self.assertEqual(report['after']['findings'], [])
            self.assertEqual((repo / 'index.html').read_text(), original)
            self.assertEqual(git(repo, 'status', '--porcelain'), '')
            self.assertTrue((Path(tmp) / 'runs/test/before/mobile-0.png').exists())
            self.assertTrue((Path(tmp) / 'runs/test/repair.patch').exists())


if __name__ == '__main__': unittest.main()
