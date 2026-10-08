# Public Synthetic Control Evaluation — V1

**Leon Maurice Browne | 8 October 2026**
**Reproducibility:** Python 3.10+ standard library only
**Maturity:** Author-authored finite-scope demonstration; **not** third-party validation
**Scope:** Standalone fictional `demo://` actions. No model, real credentials, network, filesystem modification, real tools or external effects.

## Executive result

This public case study demonstrates an elementary but falsifiable engineering pattern: define intended action-admission behaviour *before* evaluating an implementation, enumerate input combinations, compare observed decisions to expected decisions and **publish bypasses rather than obscuring them**.

| Measured quantity | Reproducible result | Meaning |
| --- | ---: | --- |
| Synthetic grid combinations | **512** | Finite cartesian input space described below |
| Cases expected to admit | **2** | Fixed, permitted cases in that grid |
| Cases observed to admit | **2** | Observed in-memory simulated dispatches |
| False admits vs public contract | **0** | No mismatch within the grid |
| False rejects vs public contract | **0** | No mismatch within the grid |
| Deliberately reproduced limitations | **3** | See explicit known-gap demonstrations |
| Real-world external effects | **0** | No executor or effectful adapter exists |

**Critical interpretation:** Zero mismatches in a 512-case *author-chosen synthetic grid* is not a false-accept-rate estimate for real adversaries, nor a proof of complete mediation, identity security, deployed correctness or private-system safety.

## Reproduce the result yourself

Clone the [public profile repository](https://github.com/BlackRonin-coder/BlackRonin-coder), enter its root and run:

```bash
python3 -B -m unittest discover -s examples/cbac_synthetic_demo -p 'test_*.py' -v
python3 -B examples/cbac_synthetic_demo/public_evaluation.py
```

The first command runs both the original unit tests and the new finite-grid/known-gap tests. The second emits deterministic, human-readable JSON summarising the trial.

All commands run with the Python standard library. They do not require credentials, secrets, an account or access to any private repository.

For ongoing regression results, inspect the [public GitHub Actions runs](https://github.com/BlackRonin-coder/BlackRonin-coder/actions). A green job means the **published mock suite** passed on the tested commit—not that a private AI control programme passed external evaluation.

## Specification and finite case construction

The toy policy permits only:

- `reviewer-1 / draft_report / demo://report`
- `reviewer-1 / read_summary / demo://summary`

The *synthetic* context must claim an established identity and have authority epoch `3`. The action identifier must be non-empty and not previously seen.

The grid systematically enumerates:

| Input dimension | Count | Values |
| --- | ---: | --- |
| Subject | 4 | `reviewer-1`, `reviewer-2`, `agent-self-claim`, empty |
| Action | 4 | `draft_report`, `read_summary`, `delete_records`, empty |
| Target | 4 | `demo://report`, `demo://summary`, `demo://outside`, empty |
| Epoch | 4 | `2`, `3`, `4`, string `"3"` |
| Identity-checked fixture flag | 2 | Boolean true or false |

`4 × 4 × 4 × 4 × 2 = 512` cases. Each case starts with a fresh controller to prevent cross-case state from changing the expected admission decision.

An *author-authored* declarative expectation function defines the allowed set. It is written as a separate function and compared against the implementation decision; this is **not** independent verification by a different research team. The two components can share mistakes because they were developed together.

## Known-gap adversarial probes: three reproduced weaknesses

### 1. Caller-forged identity fixture

Passing `Context("reviewer-1", 3, True)` causes the demo to admit an allowed synthetic action.

**Limitation:** `True` is caller-supplied; it is not independently authenticated. An attacker controlling this argument can forge the supposed identity check.

**Real-world requirement:** an independently authenticated identity and tamper-resistant binding to the action and purpose.

### 2. Caller-forged observer receipt

Passing `Observation(request_id, "mock-independent-observer", True)` causes the demo to report mock verified completion.

**Limitation:** the producer name is an arbitrary caller-supplied string, not attested evidence. Forging it trivially defeats the mock check.

**Real-world requirement:** authentic external observation with trusted provenance and binding to a specific executed operation.

### 3. Semantic repetition under a different identifier

Submitting the same synthetic action with `id-one` and `id-two` results in two simulated dispatches.

**Limitation:** the example rejects duplicate identifiers but does not decide whether differently identified requests represent the same real-world effect. It cannot guarantee semantic idempotency.

**Real-world requirement:** operation-specific duplicate semantics, durable effect tracking, cancellation/reconciliation rules and an independent determination of actual completion.

**These are disclosed vulnerabilities or incompletenesses of the illustration, not test failures to hide or features claimed for a protected system.**

## Threat model and trust boundaries

| Threat/control question | Coverage here | Needed before real use |
| --- | --- | --- |
| Unsupported action or resource | Simulated static allowlist | Independently enforced per-operation authorisation |
| Stale or malformed epoch | Checked against fixed integer `3` | Revocation, clock/state semantics and durable authority |
| Identical request ID repeated in one process | Blocked in memory | Durable, distributed replay control |
| Unauthenticated actor | **Not protected** | Trustworthy identity proof, independent binding |
| Forged completion receipt | **Not protected** | Independent evidence provenance |
| Alternate execution channel | **Not protected** | Complete effect-path mediation |
| Partial external execution and crashes | **Not tested** | Durable execution and independently verified reconciliation |
| Compound actions or cross-agent authority | **Not tested** | Compositional control and adversarial host integration |
| Agent misuse of real tools | **Not tested** | Real agent/tool sandbox with external observation |

The evaluation intentionally provides no operational attack utilities, secrets, real infrastructure access or proprietary algorithm.

## How to falsify this public demonstration

Reviewers can examine the [Python implementation](../examples/cbac_synthetic_demo/control_demo.py), [test contract](../examples/cbac_synthetic_demo/public_evaluation.py) and [tests](../examples/cbac_synthetic_demo/test_public_evaluation.py) to find:

1. An input within the declared finite grid where the observed decision disagrees with the declared expectation.
2. An undocumented mock-effect side effect.
3. A repeatable failure of the test harness itself.
4. A narrower limit that the paper mistakenly describes as generally secure.

Independent reproductions and valid counterexamples would strengthen the evidence. A contradiction should cause a corrected document and test—not a broader claim of success.

## Engineering significance

This demonstrates a disciplined workflow that transfers from safety-critical engineering into software assurance:

**Declare the requirement → create explicit test expectations → execute negative-path trials → inspect the result → publish limitations → verify changes in CI.**

It is **not** a private-system implementation, proof of AI safety, statistically estimated success probability, external validation, or evidence of production deployment.

### Intellectual-property boundary

All code was written independently for this public illustration. No private constitutional logic, runtime implementation, proprietary conformance corpus or protected evidence is disclosed. The repository has no general open-source licence; GitHub visibility and technical reproducibility do not convey commercial redistribution rights.

See the [public evidence register](PUBLIC_EVIDENCE_REGISTER.md) for evidence maturity and the [CBAC research note](CBAC_Public_Research_Note_2026.md) for research context.
