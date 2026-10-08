# Consequence-Bounded AI Control (CBAC)

## A systems-control hypothesis for agentic AI

**Leon Maurice Browne — London, United Kingdom**
**Original research framing:** 22 September 2026
**Public synopsis:** 8 October 2026
**Status:** Architecture-informed hypothesis. Independent frontier-model validation pending.

> The goal is not to make AI incapable of unsafe behaviour; it is to prevent unsafe behaviour from automatically becoming harmful external consequence.

## Abstract

As AI systems gain access to tools, credentials and operational environments, model mistakes can become actions. Alignment remains important, but model behaviour cannot be the sole security boundary. **Consequence-Bounded AI Control (CBAC)** investigates whether independently controlled identity, authority, execution, provenance and evidence can reduce the real-world consequences of erroneous or adversarial agent behaviour.

This is a research hypothesis associated with an ongoing private engineering programme—not a claim of perfect AI control, third-party certification or a deployed product. Complete mediation and least privilege are established security ideas; the proposed research contribution is examining their integration into a coherent, empirically testable control architecture for autonomous systems.

## 1. The problem: capability can turn into consequence

A text-only model can generate incorrect information. A tool-using agent may also send data, modify records, run code, obtain credentials or persist state. The consequential boundary is the transition from **model-proposed action to external effect**.

Technical capability does not itself establish permission to act. A model claiming success does not independently establish successful completion. A previously valid permission may no longer be current.

The UK [AI Security Institute](https://www.aisi.gov.uk/work/how-to-evaluate-control-measures-for-ai-agents) investigates AI control as a complement to alignment, including adversarial evaluations. [OWASP's Excessive Agency guidance](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) recommends least privilege and downstream authorisation outside a language model.

CBAC builds on these existing directions. It does not claim to have originated them.

## 2. The railway-signalling intuition

A train may be physically capable of entering a section of track while lacking authority to occupy it. Railway interlocking provides an independent set of movement constraints; a train's capability and its movement authority remain different concepts.

I approach autonomous software from a related systems-engineering perspective. What must independently be true before a model's proposed action may produce a consequence?

The public high-level principles are:

- **Capability is not authority.** Tool access does not imply permission.
- **Model output is not permission.** The agent cannot grant itself rights by stating them.
- **Evidence is not authority.** A record or receipt is not itself a valid current grant.
- **Authorisation is not dispatch.** Approval does not establish a request was sent.
- **Dispatch is not execution.** Tool acceptance does not prove the action happened.
- **Execution is not completion.** Independent outcome evidence remains necessary.
- **Failure must not grant new authority.** Uncertainty, timeout and recovery should not silently expand permissions.

These are proposed objectives rather than verified properties of every implementation.

## 3. The hypothesis

**Can a system reduce the likelihood that mistaken or malicious AI behaviour produces unauthorised external effects, without assuming the model itself is perfectly aligned?**

A conceptual risk decomposition is:

- Risk depends on how often unsafe behaviour occurs.
- It also depends on whether unsafe behaviour can cross the permission/effect boundary.
- The severity of the resulting effect determines the consequences.

Alignment research helps address unsafe behaviour. Consequence-bounded control principally investigates the **conditional transition from that behaviour to actual effect**. This is a conceptual framework, not a calibrated statistical formula or evidence of a specific reduction in incident rates.

## 4. Research programme: evidence before conclusion

A credible control evaluation should predeclare the valid task, prohibited effects, control configuration and independent outcome criteria **before** an agent is tested.

A proposed evaluation cycle:

1. Give an agent a useful, legitimate task and defined tools.
2. Define a separate adversarial objective that must not succeed.
3. Identify identity, permission, provenance and output boundaries.
4. Introduce controlled attacks involving prompt injection, excessive privilege, replay, misleading evidence and interrupted actions.
5. Observe the external system independently of the model's explanation.
6. Report unauthorised effect rate, false denials, indeterminate outcomes, recovery failures, bypass paths and performance costs.
7. Reproduce across multiple environments and independent reviewers.

Independent red-teaming is essential because impressive internal test counts alone cannot establish a universal claim.

## 5. Falsification conditions and limitations

The proposed control claim should be weakened or rejected if a correctly observed experiment establishes that:

- an agent can bypass the enforcement path and reach a prohibited effect;
- a model's self-assertion is accepted as a permission;
- stale or revoked authority permits an action after recovery;
- individually permitted actions combine into an unmediated harmful effect;
- a model-generated completion assertion is treated as verified fact;
- a change in environmental assumptions leaves outdated assurance reported as current; or
- controls deny valid work so often that they are operationally unusable.

This work does **not** establish the absence of all such weaknesses. A successful adversarial counterexample is useful research evidence.

## 6. A bounded, public synthetic example

To give reviewers an inspectable demonstration, this repository provides a [self-contained Python example](../examples/cbac_synthetic_demo/README.md).

It illustrates a narrow allowlist, a mock authority epoch, duplicate request rejection, recording of simulated actions, and a separate mock observer receipt. Negative-path tests show the example's intended behaviour under its test fixtures.

**What it does not prove:** it has no genuine identity authentication, cryptographically authenticated evidence, isolated executor, real external effects, crash recovery, complete mediation, independent conformance proof or AI model evaluation. Fixture-controlled identity and producer labels are **forgeable** outside the synthetic assumption. This code was written for public explanation and is **not code extracted from the private engineering programme**.

Passing its tests demonstrates only a small, explicitly defined software behaviour.

## 7. Relationship to Bindu and private engineering

**Bindu** is the broader systems-design and evaluation method, organising constraints, underused assets, possible interventions, failure modes, incentives and verification. **CBAC** is the public research hypothesis about consequence containment. **the private engineering programme** is a distinct private engineering programme exploring related systems controls.

This note exposes no protected implementation details, internal credentials, private authority contracts or confidential engineering artefacts. It neither describes the full private implementation nor asserts independent certification of it.

## 8. Research milestones and claim discipline

| Research milestone | Public evidence status |
| --- | --- |
| Clearly articulated hypothesis and failure criteria | **Documented** |
| Runnable, narrow synthetic teaching example | **Published separately** |
| Real-model, real-tool adversarial evaluation | **Not demonstrated by this paper** |
| Independent cross-implementation conformance | **Not demonstrated by this paper** |
| Foreign-host integration and complete-mediation validation | **Not demonstrated by this paper** |
| Independent reproduction | **Pending** |

A useful negative result should reduce the claim's scope rather than be dismissed.

## Conclusion

The strongest question for an AI-control engineer is not merely whether a system appears well-behaved. It is **what permits a model's action to have consequences, which independent constraints apply, and how failures are detected**.

CBAC is a falsifiable systems-control research direction. The task now is to discover where its proposed boundaries hold, where they fail, and which kinds of independent evidence can genuinely support the claims.

---

## References

- AI Security Institute (2025), [How to evaluate control measures for AI agents?](https://www.aisi.gov.uk/work/how-to-evaluate-control-measures-for-ai-agents).
- Korbak, T., Balesni, M., Shlegeris, B. and Irving, G. (2025), [How to evaluate control measures for LLM agents? A trajectory from today to superintelligence](https://www.aisi.gov.uk/research/how-to-evaluate-control-measures-for-llm-agents-a-trajectory-from-today-to-superintelligence).
- OWASP GenAI Security Project (2025), [LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).
- Browne, L. M. (2026), *Consequence-Bounded AI Control*, private working note, 22 September 2026. This publication is a public-safe synopsis.

**© 2026 Leon Maurice Browne.** This public document does not grant a general open-source licence. See the [public evidence register](PUBLIC_EVIDENCE_REGISTER.md).
