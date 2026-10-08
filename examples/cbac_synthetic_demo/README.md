# Synthetic Consequence-Control Demonstration

A **standalone educational Python example** authored for this public portfolio. **Not private-system code**, not a product and not a security assurance result.

## What it models

A hypothetical agent proposes actions against fictional 'demo://' targets. A controller applies a static allowlist, checks a mock identity context and authority epoch, blocks duplicate requests, and appends permitted requests to an **in-memory list only**. A model's claim of completion is ignored; a separate mocked observer record is required for a mock completed status.

There is **no network access, filesystem mutation, subprocess invocation, external adapter, database, credential, LLM call or real-world effect**.

## Run locally

Requirements: **Python 3.10+**; standard library only.

From the GitHub repository's root directory:

    python3 examples/cbac_synthetic_demo/control_demo.py
    python3 -m unittest discover -s examples/cbac_synthetic_demo -p 'test_*.py' -v

Expected demonstration: one simulated accepted request, one blocked request, a rejected self-completion claim, a mock external receipt, and one synthetic in-memory effect.

## Reproduce the bounded adversarial evaluation

From the repository root, run:

    python3 -B examples/cbac_synthetic_demo/public_evaluation.py

The deterministic 512-case grid compares the mock controller with a separately written, **author-authored** test expectation. It reports zero in-grid mismatches, alongside **three intentionally reproduced weaknesses** involving caller-controlled mock identity, mock receipts and repeated actions under changed identifiers.

**This is a transparent finite-scope demonstration—not independent validation, not an estimate of real-world attack resistance, and not verification of any protected system.**

Read the full [public evaluation and threat model](../../docs/SYNTHETIC_CONTROL_EVALUATION_V1.md).

## What the tests cover

Permitted mock work; denied actions and targets; subject and mock identity checks; stale and future epochs; malformed inputs; duplicate request identifiers; attempted privilege escalation; model-generated completion claims; mismatched or negative observations; mock receipt acceptance.

## Essential limitations

- **No real authentication.** The caller supplies 'identity_checked=True' in a test fixture; a genuine attacker could forge that input.
- **No authenticated evidence.** The mock observer's producer label is an ordinary string, which a caller can forge.
- **No complete-mediation proof.** Another program could bypass this controller entirely.
- **No genuine effects.** Dispatch just appends to a list; neither work nor effects are independently observed.
- **No durable state.** Restart erases the duplicate-detection memory.
- **No operational security guarantee.** Passing unit tests says only that this implementation handles the tested cases as specified.

Do **not** use this example as an authorisation, identity, provenance, audit or safety mechanism in a real system.

A real implementation would require trusted external identity and evidence sources, complete control over execution pathways, fail-safe recovery, durability, independent assurance, threat modelling and rigorous adversarial evaluation.

The Python code here was created independently as a **small public illustration** and is not copied from the private engineering programme.

**Rights:** public visibility permits inspection and ordinary GitHub functions; no general open-source licence is granted for reuse, redistribution or commercialisation.

Read the [CBAC public research note](../../docs/CBAC_Public_Research_Note_2026.md) for the wider research context.
