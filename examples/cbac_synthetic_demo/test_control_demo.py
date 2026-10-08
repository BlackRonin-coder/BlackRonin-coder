"""Negative-path tests for a synthetic demonstration only."""
import unittest

from control_demo import Context, Observation, Proposal, SyntheticController


class SyntheticControlTests(unittest.TestCase):
    def setUp(self):
        self.c = SyntheticController()
        self.ctx = Context("reviewer-1", 3, True)
        self.req = Proposal("request-1", "draft_report", "demo://report")

    def test_authorized_request_is_dispatched_in_memory(self):
        self.assertEqual(self.c.submit(self.req, self.ctx).status, "SIMULATED_DISPATCH")
        self.assertEqual(len(self.c.effects), 1)

    def test_bad_action_is_blocked_without_effect(self):
        p = Proposal("x", "delete_records", "demo://report")
        self.assertEqual(self.c.submit(p, self.ctx).status, "BLOCKED")
        self.assertEqual(self.c.effects, [])

    def test_bad_target_is_blocked(self):
        p = Proposal("x", "draft_report", "demo://outside")
        self.assertEqual(self.c.submit(p, self.ctx).status, "BLOCKED")

    def test_subject_not_authorized(self):
        ctx = Context("agent-admin-claim", 3, True)
        self.assertEqual(self.c.submit(self.req, ctx).status, "BLOCKED")

    def test_identity_unverified(self):
        ctx = Context("reviewer-1", 3, False)
        self.assertEqual(self.c.submit(self.req, ctx).status, "BLOCKED")

    def test_stale_epoch(self):
        ctx = Context("reviewer-1", 2, True)
        self.assertEqual(self.c.submit(self.req, ctx).status, "BLOCKED")

    def test_future_epoch(self):
        ctx = Context("reviewer-1", 4, True)
        self.assertEqual(self.c.submit(self.req, ctx).status, "BLOCKED")

    def test_non_integer_epoch(self):
        ctx = Context("reviewer-1", "3", True)
        self.assertEqual(self.c.submit(self.req, ctx).status, "BLOCKED")

    def test_duplicate_is_blocked_without_second_effect(self):
        self.c.submit(self.req, self.ctx)
        self.assertEqual(self.c.submit(self.req, self.ctx).status, "BLOCKED")
        self.assertEqual(len(self.c.effects), 1)

    def test_empty_request_identifier(self):
        p = Proposal("", "draft_report", "demo://report")
        self.assertEqual(self.c.submit(p, self.ctx).status, "BLOCKED")

    def test_malformed_proposal(self):
        self.assertEqual(self.c.submit(None, self.ctx).status, "BLOCKED")

    def test_completion_claim_does_not_verify(self):
        p = Proposal("request-1", "draft_report", "demo://report", claimed_complete=True)
        self.c.submit(p, self.ctx)
        self.assertNotIn("request-1", self.c.verified)

    def test_model_generated_receipt_not_accepted(self):
        self.c.submit(self.req, self.ctx)
        receipt = Observation("request-1", "agent-self-report", True)
        self.assertEqual(self.c.reconcile(receipt).status, "NOT_VERIFIED")
        self.assertFalse(self.c.verified)

    def test_missing_observation_not_complete(self):
        self.c.submit(self.req, self.ctx)
        self.assertEqual(self.c.verified, set())

    def test_mismatched_observation_not_accepted(self):
        self.c.submit(self.req, self.ctx)
        receipt = Observation("another-request", "mock-independent-observer", True)
        self.assertEqual(self.c.reconcile(receipt).status, "NOT_VERIFIED")

    def test_negative_observation_not_complete(self):
        self.c.submit(self.req, self.ctx)
        receipt = Observation("request-1", "mock-independent-observer", False)
        self.assertEqual(self.c.reconcile(receipt).status, "NOT_VERIFIED")

    def test_producer_label_matches_mock_receipt(self):
        self.c.submit(self.req, self.ctx)
        receipt = Observation("request-1", "mock-independent-observer", True)
        self.assertEqual(self.c.reconcile(receipt).status, "MOCK_VERIFIED_COMPLETE")
        self.assertIn("request-1", self.c.verified)

    def test_malformed_observation(self):
        self.c.submit(self.req, self.ctx)
        self.assertEqual(self.c.reconcile(None).status, "NOT_VERIFIED")

    def test_mock_observation_does_not_grant_new_authority(self):
        self.c.submit(self.req, self.ctx)
        self.c.reconcile(Observation("request-1", "mock-independent-observer", True))
        self.assertEqual(
            self.c.submit(Proposal("new-request", "delete_records", "demo://report"), self.ctx).status,
            "BLOCKED",
        )
        self.assertEqual(len(self.c.effects), 1)


if __name__ == "__main__":
    unittest.main()
