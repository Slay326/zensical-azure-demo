---
title: arc42 Conformance Matrix
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-REF-040` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Architecture Authority | Operational / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# arc42 Conformance Matrix

<div class="visual-callout" markdown>

**Trace a claim to evidence**

```mermaid
flowchart LR
    A["arc42 concern"] --> D["Defining document"] --> Q["Quality scenario / evidence"]
```

Use the matrix to move from an architecture concern to its defining document and verification evidence.

</div>


This library follows the arc42 template for its architectural core. Where the
template's chapter structure did not suit a platform of this scale, content was
relocated rather than omitted. This matrix records where each chapter is held so
that the library can be audited against the template.

| arc42 chapter | Held in | ID | Deviation |
|---|---|---|---|
| 1. Introduction and Goals | [Introduction and Goals](../architecture/introduction-and-goals.md) | `DS1-ARCH-002` | None |
| 2. Architecture Constraints | [Architecture Constraints](../architecture/constraints.md) | `DS1-ARCH-003` | Constraints are typed (`C-M`/`C-T`/`C-O`/`C-C`) and each names its conformance check |
| 3. Context and Scope | [Context and Scope](../architecture/context-and-scope.md) | `DS1-ARCH-004` | None |
| 4. Solution Strategy | [Solution Strategy](../architecture/solution-strategy.md) | `DS1-ARCH-005` | Strategies are numbered `S-1`…`S-5` and traced to constraints, ADRs and residual risks |
| 5. Building Block View | [Building Block View](../architecture/building-block-view.md) | `DS1-ARCH-006` | Levels 1–2 held here; level 3 devolved to the [Systems volume](../systems/index.md) |
| 6. Runtime View | [Runtime View](../architecture/runtime-view.md) | `DS1-ARCH-007` | Seven scenarios, each traced to a quality goal |
| 7. Deployment View | [Deployment View](../architecture/deployment-view.md) | `DS1-ARCH-008` | Extended with the change propagation model, required by `C-T-07` |
| 8. Cross-Cutting Concepts | [Cross-Cutting Concepts](../architecture/crosscutting-concepts.md) | `DS1-ARCH-009` | Each concept states its verification method and violation consequence; coverage matrix added |
| 9. Architecture Decisions | [Decisions volume](../decisions/index.md) | `DS1-ADR-000` … `008` | **Relocated to its own volume.** Eight records, individually addressable |
| 10. Quality Requirements | [Quality Requirements](../architecture/quality-requirements.md) | `DS1-ARCH-010` | Every scenario carries a measure and a current measured status, not a design claim |
| 11. Risks and Technical Debt | [Risks volume](../risks/index.md) | `DS1-RSK-000` … `010` | **Relocated and split** into a risk register (possibilities) and a debt register (present conditions) |
| 12. Glossary | [Glossary](glossary.md) | `DS1-REF-010` | Every term names the document that defines it |

## Extensions Beyond arc42

Added because a platform of this scale is not adequately described by the
template alone.

| Extension | ID | Why |
|---|---|---|
| [Zone and Sector Architecture](../architecture/zone-and-sector-architecture.md) | `DS1-ARCH-011` | The spatial addressing model underlies every other document; it is not a building block and does not fit chapter 5 |
| [Systems volume](../systems/index.md) | `DS1-ENG-*` | 13 system descriptions at a depth chapter 5 cannot carry |
| [Operations volume](../operations/index.md) | `DS1-OPS-*` | arc42 describes architecture, not operation. `C-T-07` makes operation architecturally significant |
| [Security volume](../security/index.md) | `DS1-SEC-*` | Security is a cross-cutting concept in arc42; at this scale it requires its own volume with its own threat model |
| [Interface Register](interface-register.md) | `DS1-REF-030` | Normative rather than descriptive; it defines what is permitted, which chapter 3 does not do |
| [Identifier Scheme](identifier-scheme.md) | `DS1-REF-020` | `C-C-01` makes addressing mandatory and mechanically enforced |
| Controlled drawings | `DS1-DRG-*` | Geometric content that no diagram-as-text notation renders adequately |

## Deliberate Omissions

| Not held | Why | Held by |
|---|---|---|
| Reactor constructional detail | `C-M-06` compartmentation | Reactor Systems Authority |
| Armament design, effects, targeting, sequencing | `C-M-06` compartmentation | Ordnance Systems Authority |
| Force disposition and operational tasking | Not an architectural concern | Fleet Command |
| Personnel records and vetting outcomes | Not an architectural concern | Sector Security Command |
| Programme cost and schedule | Not an architectural concern | Imperial Engineering Command |

Omissions are recorded rather than left implicit, so that a reader can tell the
difference between material this library does not hold and material that does not
exist.
