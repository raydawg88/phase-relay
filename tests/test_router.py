from __future__ import annotations

import unittest
from pathlib import Path

from phaserelay.router import DEFAULT_PHASES, build_project_plan, read_matrix, select_route


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "src" / "phaserelay" / "defaults"


class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = read_matrix(DEFAULTS / "task-matrix.csv")

    def test_exact_route(self) -> None:
        route = select_route(self.matrix, "Video analysis", "frame-level forensic critique")
        self.assertEqual(route.match_score, 1.0)
        self.assertIn("ffmpeg", route.primary_route)
        self.assertIn("frame", route.verification.lower())

    def test_case_and_punctuation_do_not_break_exact_match(self) -> None:
        route = select_route(self.matrix, "video analysis", "FRAME LEVEL forensic critique")
        self.assertEqual(route.match_score, 1.0)

    def test_fuzzy_route(self) -> None:
        route = select_route(self.matrix, "coding", "debug architecture")
        self.assertGreater(route.match_score, 0.5)
        self.assertEqual(route.workflow, "Coding")

    def test_unknown_route_fails_closed(self) -> None:
        with self.assertRaises(LookupError):
            select_route(self.matrix, "quantum basket weaving", "nebula tuning")

    def test_project_plan_covers_requested_phases(self) -> None:
        plan = build_project_plan(self.matrix, ["research", "implementation", "qa"])
        self.assertEqual([item["phase"] for item in plan], ["research", "implementation", "qa"])
        self.assertTrue(all(item["route"]["verification"] for item in plan))

    def test_default_plan_covers_complete_project_lifecycle(self) -> None:
        plan = build_project_plan(self.matrix, list(DEFAULT_PHASES))
        self.assertEqual(plan[0]["phase"], "intake")
        self.assertEqual(plan[-1]["phase"], "retrospective")
        self.assertEqual(plan[-1]["route"]["primary_route"], "PhaseRelay CLI plus deterministic telemetry")

    def test_unknown_project_phase_fails(self) -> None:
        with self.assertRaises(ValueError):
            build_project_plan(self.matrix, ["launch-party"])

    def test_three_primary_failures_suspend_default(self) -> None:
        observations = [
            {
                "workflow": "Video analysis",
                "subtask": "native first-pass visual/audio understanding",
                "route_role": "primary",
                "outcome": "failure",
                "score_delta": -10,
            }
            for _ in range(3)
        ]
        route = select_route(
            self.matrix,
            "Video analysis",
            "native first-pass visual/audio understanding",
            observations,
        )
        self.assertEqual(route.decision, "primary_suspended_after_three_failures")
        self.assertEqual(route.primary_route, "GPT multimodal if short clip")
        self.assertEqual(route.secondary_route, "Gemini")

    def test_secondary_can_win_with_comparable_successes(self) -> None:
        observations = [
            {
                "workflow": "Customer research",
                "subtask": "source discovery and citation gathering",
                "route_role": "secondary",
                "outcome": "success",
                "score_delta": 8,
            }
            for _ in range(3)
        ]
        route = select_route(
            self.matrix,
            "Customer research",
            "source discovery and citation gathering",
            observations,
        )
        self.assertEqual(route.decision, "secondary_promoted_by_observed_score")
        self.assertEqual(route.primary_route, "ChatGPT/Gemini web search")


if __name__ == "__main__":
    unittest.main()
