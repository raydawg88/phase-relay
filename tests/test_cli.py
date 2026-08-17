from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, home: Path | None = None) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        command = [sys.executable, "-m", "phaserelay"]
        if home is not None:
            command.extend(["--home", str(home)])
        command.extend(args)
        return subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)

    def test_route_json(self) -> None:
        result = self.run_cli("route", "--workflow", "Finance/accounting", "--subtask", "spreadsheet/account analysis", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("Python/spreadsheet", payload["primary_route"])

    def test_end_to_end_local_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "state"
            self.assertEqual(self.run_cli("init", home=home).returncode, 0)
            self.assertEqual(self.run_cli("validate", "--json", home=home).returncode, 0)
            self.assertEqual(self.run_cli(
                "observe", "--workflow", "Coding", "--subtask", "review",
                "--provider", "Example", "--model", "example", "--outcome", "success",
                "--surface", "test", "--notes", "synthetic",
                home=home,
            ).returncode, 0)
            self.assertEqual(self.run_cli(
                "usage", "--provider", "Example", "--model", "example",
                "--workflow", "Coding", "--subtask", "review", "--input", "10", "--output", "5",
                home=home,
            ).returncode, 0)
            report = self.run_cli("report", "--json", home=home)
            self.assertEqual(report.returncode, 0, report.stderr)
            self.assertEqual(json.loads(report.stdout)["total_tokens"], 15)

    def test_recorded_failures_change_the_next_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "state"
            self.assertEqual(self.run_cli("init", home=home).returncode, 0)
            for _ in range(3):
                result = self.run_cli(
                    "observe", "--workflow", "Video analysis",
                    "--subtask", "native first-pass visual/audio understanding",
                    "--provider", "Google", "--model", "Gemini", "--outcome", "failure",
                    "--score-delta", "-10", "--route-role", "primary", home=home,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            routed = self.run_cli(
                "route", "--workflow", "Video analysis",
                "--subtask", "native first-pass visual/audio understanding", "--json", home=home,
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            payload = json.loads(routed.stdout)
            self.assertEqual(payload["decision"], "primary_suspended_after_three_failures")
            self.assertEqual(payload["primary_route"], "GPT multimodal if short clip")


if __name__ == "__main__":
    unittest.main()
