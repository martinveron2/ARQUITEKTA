import json
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from arquitekta_quality.core import Blocked, apply_edits, command, git, safe_source
from arquitekta_quality.ollama import Ollama


class EngineTests(unittest.TestCase):
    def test_path_escape_symlink_and_protected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'app.js').write_text('hello')
            (root / 'linked.js').symlink_to('/etc/passwd')
            (root / 'inside').mkdir()
            (root / 'inside' / 'app.js').write_text('hello')
            (root / 'alias').symlink_to(root / 'inside', target_is_directory=True)
            for path in ['../app.js', '.env', 'tests/foo.py', 'app.test.js', 'linked.js', 'alias/app.js']:
                with self.assertRaises(Blocked):
                    safe_source(root, path, [path])
            self.assertEqual(safe_source(root, 'app.js', ['app.js']).read_text(), 'hello')

    def test_atomic_validation_rejects_partial_proposals(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'app.js'
            p.write_text('one two')
            proposal = {'edits': [{'path': 'app.js', 'before': 'one', 'after': 'three'},
                                  {'path': '../oops.js', 'before': 'x', 'after': 'y'}]}
            with self.assertRaises(Blocked):
                apply_edits(tmp, proposal, ['app.js'])
            self.assertEqual(p.read_text(), 'one two')
            apply_edits(tmp, {'edits': [proposal['edits'][0]]}, ['app.js'])
            self.assertEqual(p.read_text(), 'three two')

    def test_ambiguous_match_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'app.js').write_text('x x')
            with self.assertRaises(Blocked):
                apply_edits(tmp, {'edits': [{'path': 'app.js', 'before': 'x', 'after': 'y'}]}, ['app.js'])

    def test_ollama_protocol_uses_schema_no_stream(self):
        captured = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                captured.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                body = json.dumps({'done': True, 'message': {'content': json.dumps({'summary': 'fix', 'edits': []})}}).encode()
                self.send_response(200); self.end_headers(); self.wfile.write(body)
            def log_message(self, *args): pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            result = Ollama(f'http://127.0.0.1:{server.server_port}', 'local-model').propose({'findings': []}, {})
            self.assertEqual(result['summary'], 'fix')
            self.assertFalse(captured[0]['stream'])
            self.assertEqual(captured[0]['format']['type'], 'object')
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == '__main__':
    unittest.main()
