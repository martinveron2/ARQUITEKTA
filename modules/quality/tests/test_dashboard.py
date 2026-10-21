import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request


class DashboardTests(unittest.TestCase):
    def test_dashboard_connects_without_overflow_on_mobile_and_desktop(self):
        from playwright.sync_api import sync_playwright, expect
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'projects.json'
            config.write_text(json.dumps({'projects': []}))
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
            url = f'http://127.0.0.1:{port}'
            env = dict(os.environ, QUALITY_TOKEN='local-test-token-not-a-secret')
            process = subprocess.Popen([sys.executable, '-m', 'arquitekta_quality.server', '--projects', str(config),
                                        '--data', str(Path(tmp) / 'data'), '--port', str(port)], env=env,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                for _ in range(50):
                    try:
                        urllib.request.urlopen(url, timeout=1).close(); break
                    except OSError: time.sleep(.1)
                else: self.fail('Dashboard no inició')
                try:
                    urllib.request.urlopen(url + '/api/projects')
                    self.fail('La API permitió acceso sin token')
                except urllib.error.HTTPError as error:
                    self.assertEqual(error.code, 401)
                with sync_playwright() as pw:
                    browser = pw.chromium.launch()
                    try:
                        for width in [320, 390, 1440]:
                            page = browser.new_page(viewport={'width': width, 'height': 900})
                            page.goto(url)
                            page.locator('#token').fill(env['QUALITY_TOKEN'])
                            page.locator('#connect').click()
                            expect(page.locator('#message')).to_contain_text('Sin proyectos')
                            expect(page.locator('#test')).to_be_disabled()
                            page.locator('#refresh').click()
                            expect(page.locator('#runs')).to_contain_text('Todavía no ejecutaste pruebas')
                            self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'))
                            if os.environ.get('QUALITY_TEST_EVIDENCE'):
                                target = Path(os.environ['QUALITY_TEST_EVIDENCE'])
                                target.mkdir(parents=True, exist_ok=True)
                                page.screenshot(path=str(target / f'dashboard-{width}.png'), full_page=True)
                            page.close()
                    finally: browser.close()
            finally:
                process.terminate()
                process.wait(timeout=5)
