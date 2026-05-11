"""Scan agent directories and pick a smart-default render mode."""
from pathlib import Path


def scan_agents(dirs):
    """Walk each dir for *.md files. Earlier dirs take precedence on name conflict.

    Returns deduplicated list of Path objects (in order of first appearance).
    """
    seen_names = set()
    result = []
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            continue
        for path in sorted(d.glob('*.md')):
            if path.stem in seen_names:
                continue
            seen_names.add(path.stem)
            result.append(path)
    return result


def pick_mode(agent_count):
    if agent_count == 0:
        return 'claude'
    if agent_count == 1:
        return 'focus'
    return 'team'


def default_search_dirs(project_root, home):
    """Standard search locations: project-level then user-level."""
    return [
        Path(project_root) / '.claude' / 'agents',
        Path(home) / '.claude' / 'agents',
    ]


if __name__ == '__main__':
    import sys, os
    home = os.environ.get('HOME', '/Users')
    cwd = os.getcwd()
    dirs = default_search_dirs(cwd, home)
    agents = scan_agents(dirs)
    print(f"agents={len(agents)}")
    print(f"mode={pick_mode(len(agents))}")
    for a in agents:
        print(f"  {a}")
