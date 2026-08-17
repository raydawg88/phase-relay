#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "phase-relay"


def install(target_root: Path) -> Path:
    target = target_root.expanduser() / "phase-relay"
    target_root.expanduser().mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    shutil.copytree(SOURCE, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the PhaseRelay skill for Codex and/or Claude Code.")
    parser.add_argument("--codex-dir", type=Path, default=Path.home() / ".codex" / "skills")
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude" / "skills")
    parser.add_argument("--codex-only", action="store_true")
    parser.add_argument("--claude-only", action="store_true")
    args = parser.parse_args()
    if args.codex_only and args.claude_only:
        parser.error("choose at most one of --codex-only or --claude-only")

    targets = []
    if not args.claude_only:
        targets.append(install(args.codex_dir))
    if not args.codex_only:
        targets.append(install(args.claude_dir))
    for target in targets:
        print(f"Installed: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

