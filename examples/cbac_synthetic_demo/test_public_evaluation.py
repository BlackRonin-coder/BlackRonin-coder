"""Checks for the deliberately bounded, public-only evaluation."""
import json
import unittest

from control_demo import Context, Observation, Proposal, SyntheticController
from public_evaluation import (
    demonstrate_known_gaps,
    evaluate,
    evaluate_fixed_grid,
    reference_expectation,
)


class PublicEvaluationTests(unittest.TestCase):
    def test_cartesian_enumeration_is_complete(self):
        summary = evaluate_fixed_grid()
        self.assertEqual(summary["cases"], 4 * 4 * 4 * 4 * 2)
        self.assertEqual(summary["expected_admit"], 2)
        self.assertEqual(summary["observed_admit"], 2)

    def test_no_contract_disagreement_in_finite_grid(self):
        data = evaluate_fixed_grid()
        self.assertEqual(data["false_admit"], 0)
        self.assertEqual(data["false_reject"], 0)

    def test_contract_rejects_stale_or_forged_strings(self):
        self.assertTrue(reference_expectation(
            "reviewer-1", "draft_report", "demo://report", 3, True
        ))
        self.assertFalse(reference_expectation(
            "reviewer-1", "draft_report", "demo://report", "3", True
        ))
        self.assertFalse(reference_expectation(
            "reviewer-1", "draft_report", "demo://report", 3, "True"
        ))
        self.assertFalse(reference_expectation(
            "reviewer-1", "delete_records", "demo://report", 3, True
        ))

    def test_known_gaps_are_visible_not_reported_as_successful_controls(self):
        self.assertEqual(demonstrate_known_gaps(), {
            "fixture_identity_can_be_forged": True,
            "fixture_observer_label_can_be_forged": True,
            "new_id_can_repeat_same_semantic_action": True,
        })

    def test_mock_evaluation_has_zero_external_effects(self):
        report = evaluate()
        self.assertEqual(report["external_effects"], 0)
        self.assertEqual(
            report["nature"], "synthetic_author_authored_not_independent"
        )

    def test_report_has_stable_json_shape(self):
        report = evaluate()
        rendered = json.dumps(report, sort_keys=True)
        self.assertEqual(json.loads(rendered), report)
        self.assertIn("known_gaps_reproduced", report)

    def test_exact_identifier_duplicate_blocks_only_second(self):
        controller = SyntheticController()
        ctx = Context("reviewer-1", 3, True)
        p = Proposal("id", "draft_report", "demo://report")
        self.assertEqual(controller.submit(p, ctx).status, "SIMULATED_DISPATCH")
        self.assertEqual(controller.submit(p, ctx).status, "BLOCKED")
        self.assertEqual(len(controller.effects), 1)

    def test_agent_completion_claim_does_not_verify(self):
        controller = SyntheticController()
        ctx = Context("reviewer-1", 3, True)
        p = Proposal("id", "draft_report", "demo://report", True)
        controller.submit(p, ctx)
        self.assertFalse(controller.verified)
        self.assertEqual(
            controller.reconcile(Observation("id", "agent-self-report", True)).status,
            "NOT_VERIFIED",
        )


if __name__ == "__main__":
    unittest.main()
