from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from phaserelay.telemetry import append_observation, append_usage, initialize_home, report
from phaserelay.validation import validate_home


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "src" / "phaserelay" / "defaults"


class TelemetryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        initialize_home(self.home, DEFAULTS)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_initialized_home_validates(self) -> None:
        self.assertEqual(validate_home(self.home), [])

    def test_observation_is_valid_jsonl(self) -> None:
        path = self.home / "telemetry" / "routing-observations.jsonl"
        append_observation(path, {
            "workflow": "Coding", "subtask": "review", "chosen_provider": "Example",
            "chosen_model_or_tool": "example-model", "outcome": "failure", "score_delta": -10,
        })
        records = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(records[-1]["score_delta"], -10)
        self.assertEqual(records[-1]["outcome"], "failure")

    def test_usage_total_and_report(self) -> None:
        path = self.home / "telemetry" / "token-usage.csv"
        append_usage(path, {
            "provider": "Example", "model_or_tool": "small", "workflow": "Coding",
            "subtask": "extraction", "input_tokens": 100, "output_tokens": 20,
            "reasoning_tokens": 5, "estimated_cost_usd": 0.01,
        })
        summary = report(self.home)
        self.assertEqual(summary["total_tokens"], 125)
        self.assertEqual(summary["tokens_by_provider"], {"Example": 125})
        with path.open(newline="") as handle:
            row = list(csv.DictReader(handle))[0]
        self.assertEqual(row["total_tokens"], "125")

    def test_malformed_matrix_is_rejected(self) -> None:
        matrix = self.home / "task-matrix.csv"
        matrix.write_text(matrix.read_text() + "broken,row\n", encoding="utf-8")
        errors = validate_home(self.home)
        self.assertTrue(any("expected 9 columns" in error for error in errors))

    def test_deprecated_model_reference_is_rejected(self) -> None:
        matrix = self.home / "task-matrix.csv"
        text = matrix.read_text(encoding="utf-8").replace(
            "Perplexity,ChatGPT/Gemini web search", "sora-2,ChatGPT/Gemini web search", 1
        )
        matrix.write_text(text, encoding="utf-8")
        errors = validate_home(self.home)
        self.assertTrue(any("deprecated model referenced: sora-2" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

