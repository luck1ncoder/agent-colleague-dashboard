import unittest
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
TEMPLATES = ROOT / 'templates'
SAMPLES = ROOT / 'samples'


class TestRenderCLI(unittest.TestCase):
    def test_render_focus_mode(self):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
            out_path = f.name
        try:
            result = subprocess.run([
                'python3', str(SCRIPTS / 'render.py'),
                '--json', str(SAMPLES / 'code-reviewer.json'),
                '--template', str(TEMPLATES / 'agent-profile.html'),
                '--out', out_path,
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            html = Path(out_path).read_text()
            self.assertIn('柯瑞', html)
            self.assertIn('#完美主义晚期', html)
            self.assertIn('width:95%', html)
            self.assertIn('🛡️', html)
            self.assertNotIn('{{', html, msg="Template directives should all be rendered")
        finally:
            os.unlink(out_path)


class TestRenderTeam(unittest.TestCase):
    def test_render_team_mode(self):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
            out_path = f.name
        try:
            result = subprocess.run([
                'python3', str(SCRIPTS / 'render.py'),
                '--json', str(SAMPLES / 'team.json'),
                '--template', str(TEMPLATES / 'team-dashboard.html'),
                '--out', out_path,
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            html = Path(out_path).read_text()
            self.assertIn('柯瑞', html)
            self.assertIn('阿V', html)
            self.assertIn('🧐', html)
            self.assertIn('🤙', html)
            self.assertIn('先想再写', html)
            self.assertNotIn('{{', html)
        finally:
            os.unlink(out_path)


class TestRenderCharter(unittest.TestCase):
    def test_render_charter_mode(self):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
            out_path = f.name
        try:
            result = subprocess.run([
                'python3', str(SCRIPTS / 'render.py'),
                '--json', str(SAMPLES / 'claude-md.json'),
                '--template', str(TEMPLATES / 'claude-charter.html'),
                '--out', out_path,
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            html = Path(out_path).read_text()
            self.assertIn('项目宪章', html)
            self.assertIn('先想再写', html)
            self.assertIn('阿V 服从度仅 28', html)
            self.assertNotIn('{{', html)
        finally:
            os.unlink(out_path)


if __name__ == '__main__':
    unittest.main()
