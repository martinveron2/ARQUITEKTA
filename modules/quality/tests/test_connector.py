import json
from pathlib import Path
import tempfile
import unittest
from arquitekta_quality.connector import connect, dashboard_link
from arquitekta_quality.core import Blocked


class ConnectorTests(unittest.TestCase):
    def test_persist_idempotent_connection_and_reject_unknown_or_production(self):
        p = dict(id='pilot', name='Pilot', environment='test', test_data='synthetic', permissions=['audit'])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'connections.json'
            connect({'pilot': p}, 'pilot', target)
            connect({'pilot': p}, 'pilot', target)
            self.assertEqual(list(json.loads(target.read_text())), ['pilot'])
            with self.assertRaises(Blocked):
                connect({'pilot': p}, 'unknown', target)
            with self.assertRaises(Blocked):
                connect({'pilot': dict(p, environment='production')}, 'pilot', target)
            self.assertEqual(len(json.loads(target.read_text())), 1)

    def test_dashboard_link_carries_id_without_credentials(self):
        self.assertEqual(dashboard_link('http://127.0.0.1:18787', 'pilot'),
                         'http://127.0.0.1:18787/?project=pilot')
        with self.assertRaises(Blocked):
            dashboard_link('https://user:password@example.test', 'pilot')
