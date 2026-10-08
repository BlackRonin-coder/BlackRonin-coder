"""Public educational example: simulated action admission and evidence reconciliation.

This file was authored separately for public demonstration; it is not the private engineering programme
source and is not a production security control. There is no external adapter.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Proposal:
    """Untrusted request originating from a hypothetical agent."""

    request_id: str
    action: str
    target: str
    claimed_complete: bool = False


@dataclass(frozen=True)
class Context:
    """Simulated trusted input from outside the agent.

    IMPORTANT: 'identity_checked' is test-fixture data, not real authentication.
    An actual deployment requires a genuine independent authenticated source.
    """

    subject: str
    authority_epoch: int
    identity_checked: bool


@dataclass(frozen=True)
class Observation:
    """Mock independent observer receipt; the producer label is NOT authenticated."""

    request_id: str
    producer: str
    completed: bool


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str


class SyntheticController:
    """A tiny in-memory state machine; never performs real external actions."""

    def __init__(self) -> None:
        self.epoch = 3
        self._allowed = frozenset({
            ("reviewer-1", "draft_report", "demo://report"),
            ("reviewer-1", "read_summary", "demo://summary"),
        })
        self._seen: set[str] = set()
        self.effects: list[tuple[str, str, str]] = []
        self.verified: set[str] = set()

    def submit(self, proposal: Proposal, context: Context) -> Decision:
        if type(proposal) is not Proposal or type(context) is not Context:
            return Decision("BLOCKED", "malformed request or context")
        if not all(
            type(field) is str and 0 < len(field) <= 100
            for field in (
                proposal.request_id, proposal.action, proposal.target, context.subject
            )
        ):
            return Decision("BLOCKED", "invalid request fields")
        if type(proposal.claimed_complete) is not bool:
            return Decision("BLOCKED", "invalid completion claim")
        if type(context.identity_checked) is not bool or context.identity_checked is not True:
            return Decision("BLOCKED", "identity not established")
        if type(context.authority_epoch) is not int or context.authority_epoch != self.epoch:
            return Decision("BLOCKED", "stale, future, or invalid authority epoch")
        if (context.subject, proposal.action, proposal.target) not in self._allowed:
            return Decision("BLOCKED", "request is outside the allowed scope")
        if proposal.request_id in self._seen:
            return Decision("BLOCKED", "duplicate request identifier")

        # No real dispatch: record a synthetic effect only after all checks.
        self._seen.add(proposal.request_id)
        self.effects.append((proposal.request_id, proposal.action, proposal.target))
        # A claim of completion from the agent is intentionally ignored.
        return Decision("SIMULATED_DISPATCH", "awaiting separate observation")

    def reconcile(self, receipt: Observation) -> Decision:
        if type(receipt) is not Observation:
            return Decision("NOT_VERIFIED", "invalid observation")
        if type(receipt.request_id) is not str or not receipt.request_id:
            return Decision("NOT_VERIFIED", "invalid observation identity")
        if receipt.request_id not in self._seen:
            return Decision("NOT_VERIFIED", "no matching simulated dispatch")
        if receipt.producer != "mock-independent-observer":
            return Decision("NOT_VERIFIED", "wrong mock producer")
        if receipt.completed is not True or type(receipt.completed) is not bool:
            return Decision("NOT_VERIFIED", "no affirmative mock completion observation")
        self.verified.add(receipt.request_id)
        return Decision("MOCK_VERIFIED_COMPLETE", "synthetic observation matched")


def main() -> None:
    controller = SyntheticController()
    context = Context("reviewer-1", authority_epoch=3, identity_checked=True)
    valid = Proposal("request-1", "draft_report", "demo://report", claimed_complete=True)
    invalid = Proposal("request-2", "delete_records", "demo://report")
    print("Valid request:", controller.submit(valid, context))
    print("Unsupported action:", controller.submit(invalid, context))
    print("Agent completion claim:", "not accepted as verified completion")
    print("Mock observation:", controller.reconcile(
        Observation("request-1", "mock-independent-observer", True)
    ))
    print("Synthetic effects:", controller.effects)
    print("No network, filesystem writes or real-world effects were performed.")


if __name__ == "__main__":
    main()
