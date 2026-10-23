import tempfile
import unittest
from pathlib import Path
import subprocess
from arquitekta_quality.core import redact
from arquitekta_quality.runner import run


class PilotPermissionTests(unittest.TestCase):
    def test_redaction_removes_structured_credentials_and_bearer(self):
        self.assertEqual(redact({'token':'secret-value','detail':'Bearer abc.xyz'}),
                         {'token':'[REDACTED]','detail':'Bearer [REDACTED]'})

    def test_readonly_repair_cannot_start_even_without_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['git','init','-q',tmp],check=True)
            r = run({'id':'pilot','name':'Pilot','repo':tmp,'base_url':'http://127.0.0.1:18252/',
                     'attach_readonly':True,'environment':'test','test_data':'synthetic',
                     'permissions':['audit'],'verify':['true'], 'journeys':[{'steps':[{'action':'expect_visible','selector':'body'}]}]}, Path(tmp)/'run', 'repair',None)
            self.assertEqual(r['state'],'BLOCKED')
            self.assertIn('autorización independiente',r['error'])
            self.assertNotIn('repair_commit',r)
