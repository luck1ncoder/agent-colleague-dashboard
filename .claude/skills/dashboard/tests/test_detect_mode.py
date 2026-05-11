import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from detect_mode import scan_agents, pick_mode


class TestDetectMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / '.claude' / 'agents').mkdir(parents=True)
        self.user_agents = self.root / 'user-agents'
        self.user_agents.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def _write_agent(self, dir, name):
        (dir / f'{name}.md').write_text(f'---\nname: {name}\n---\nbody')

    def test_no_agents_returns_claude(self):
        agents = scan_agents([self.root / '.claude/agents', self.user_agents])
        self.assertEqual(agents, [])
        self.assertEqual(pick_mode(0), 'claude')

    def test_one_agent_returns_focus(self):
        self._write_agent(self.root / '.claude/agents', 'code-reviewer')
        agents = scan_agents([self.root / '.claude/agents', self.user_agents])
        self.assertEqual(len(agents), 1)
        self.assertEqual(pick_mode(1), 'focus')

    def test_two_agents_returns_team(self):
        self._write_agent(self.root / '.claude/agents', 'code-reviewer')
        self._write_agent(self.user_agents, 'planner')
        agents = scan_agents([self.root / '.claude/agents', self.user_agents])
        self.assertEqual(len(agents), 2)
        self.assertEqual(pick_mode(2), 'team')

    def test_dedup_by_name(self):
        # Same name in two locations — project takes precedence
        self._write_agent(self.root / '.claude/agents', 'code-reviewer')
        self._write_agent(self.user_agents, 'code-reviewer')
        agents = scan_agents([self.root / '.claude/agents', self.user_agents])
        self.assertEqual(len(agents), 1)
        self.assertEqual(str(agents[0]).startswith(str(self.root / '.claude/agents')), True)


if __name__ == '__main__':
    unittest.main()
