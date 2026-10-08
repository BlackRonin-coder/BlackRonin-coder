"""Reproducible finite-scope evaluation of the PUBLIC mock controller.

Uses only fictional demo:// targets and standard-library Python. This is an
author-authored evaluation, NOT an independent assessment of a private system.
"""
from __future__ import annotations

import itertools
import json

from control_demo import Context, Observation, Proposal, SyntheticController


# Independent-as-code TEST EXPECTATION. Still author-authored, not external.
# These two tuples intentionally correspond to a tiny, public, fixed allowlist.
EXPECTED_ALLOWED = frozenset(
    {
        ("reviewer-1", "draft_report", "demo://report"),
        ("reviewer-1", "read_summary", "demo://summary"),
    }
)


def reference_expectation(subject: object, action: object, target: object,
                          epoch: object, identity_checked: object) -> bool:
    """Declarative public test contract, not a secure identity oracle."""
    return (
        type(subject) is str
        and type(action) is str
        and type(target) is str
        and (subject, action, target) in EXPECTED_ALLOWED
        and type(epoch) is int
        and epoch == 3
        and identity_checked is True
        and type(identity_checked) is bool
    )


def evaluate_fixed_grid() -> dict[str, int]:
    """Enumerate a deterministic input grid; each request gets fresh state."""
    fields = itertools.product(
        ("reviewer-1", "reviewer-2", "agent-self-claim", ""),
        ("draft_report", "read_summary", "delete_records", ""),
        ("demo://report", "demo://summary", "demo://outside", ""),
        (2, 3, 4, "3"),
        (True, False),
    )
    result = {
        "cases": 0,
        "expected_admit": 0,
        "observed_admit": 0,
        "false_admit": 0,
        "false_reject": 0,
    }
    for index, (subject, action, target, epoch, checked) in enumerate(fields):
        expected = reference_expectation(subject, action, target, epoch, checked)
        # Fresh controller means no accidental cross-case state coupling.
        actual = SyntheticController().submit(
            Proposal(f"case-{index}", action, target),
            Context(subject, epoch, checked),
        ).status == "SIMULATED_DISPATCH"
        result["cases"] += 1
        result["expected_admit"] += int(expected)
        result["observed_admit"] += int(actual)
        result["false_admit"] += int(actual and not expected)
        result["false_reject"] += int(expected and not actual)
    return result


def demonstrate_known_gaps() -> dict[str, bool]:
    """Explicitly exhibit flaws of the toy trust boundary; do not disguise them."""
    spoofed_context = SyntheticController()
    can_forge_mock_identity = (
        spoofed_context.submit(
            Proposal("forged-context", "draft_report", "demo://report"),
            # A real attacker could manufacture this caller-controlled fixture.
            Context("reviewer-1", 3, True),
        ).status == "SIMULATED_DISPATCH"
    )

    spoofed_observation = SyntheticController()
    spoofed_observation.submit(
        Proposal("forged-receipt", "draft_report", "demo://report"),
        Context("reviewer-1", 3, True),
    )
    can_forge_mock_observer = (
        spoofed_observation.reconcile(
            Observation("forged-receipt", "mock-independent-observer", True),
        ).status == "MOCK_VERIFIED_COMPLETE"
    )

    reused_semantic_action = SyntheticController()
    ctx = Context("reviewer-1", 3, True)
    first = reused_semantic_action.submit(
        Proposal("id-one", "draft_report", "demo://report"), ctx
    )
    second = reused_semantic_action.submit(
        Proposal("id-two", "draft_report", "demo://report"), ctx
    )
    different_id_same_action_admitted = (
        first.status == "SIMULATED_DISPATCH"
        and second.status == "SIMULATED_DISPATCH"
        and len(reused_semantic_action.effects) == 2
    )
    return {
        "fixture_identity_can_be_forged": can_forge_mock_identity,
        "fixture_observer_label_can_be_forged": can_forge_mock_observer,
        "new_id_can_repeat_same_semantic_action": different_id_same_action_admitted,
    }


def evaluate() -> dict[str, object]:
    return {
        "evaluation": "public_mock_finite_grid_v1",
        "nature": "synthetic_author_authored_not_independent",
        "grid": evaluate_fixed_grid(),
        "known_gaps_reproduced": demonstrate_known_gaps(),
        "external_effects": 0,
    }


def main() -> None:
    print(json.dumps(evaluate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
