---
title: ADR-006 Hyperdrive Cluster
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-ADR-006` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Architecture Authority | Accepted / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# ADR-006 — Distributed Hyperdrive Cluster, 5-of-7

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Ruling authority** | Architecture Review Board |
| **Date of ruling** | Programme Phase 6 |
| **Proposed again since** | 1 time |

## Context

The platform must transit between systems (`FR-02`). At this mass, no single
hyperdrive unit of buildable size is sufficient. Multiple units are required, and
they must operate in phase (`C-T-05`).

The decision is how many units, and what fraction must be available.

## Options Considered

| Option | Units | Required | Assessment |
|---|---|---|---|
| A | 5 | 5 of 5 | Minimum mass and volume. **Any single unit loss removes mobility.** No maintenance without losing transit capability. Rejected. |
| B | 7 | 5 of 7 | Two units may be lost or under maintenance with transit retained. **Selected.** |
| C | 9 | 5 of 9 | Four-unit margin. Mass, volume and synchronisation complexity rise; the ninth unit adds margin against a scenario already assessed as remote. Refused on mass budget. |
| D | 7 | 4 of 7 | Three-unit margin, but transit at 4 units requires field parameters outside the Propulsion Systems Authority's verified envelope. Rejected on safety, not on architecture. |

## Ruling

<div class="visual-callout" markdown>

**Availability threshold**

```mermaid
flowchart LR
    A["7 available"] --> B["6 available"] --> C["5 available"]
    C -->|third loss| D["4 available / no transit"]
```

The third unavailable unit removes transit capability; other station functions can continue.

</div>


Seven hyperdrive units in the ventral bay, **five required for transit**,
arranged in two groups of three and one single.

Field synchronisation is 2N; loss of both channels aborts transit regardless of
unit availability.

## Consequences

### Accepted

| Consequence | Detail |
|---|---|
| Two-unit margin | One under maintenance plus one failed still permits transit |
| Maintenance is possible without losing mobility | The principal reason for Option B over A |
| **A third loss removes mobility entirely** | No automatic mitigation exists |
| Mobility loss leaves the platform otherwise fully functional | A fully capable station that cannot leave |
| Unit repair requires a down-state | Cannot be done in service |

### The Third-Loss Scenario

With five of seven required, the loss of three units removes transit. The platform
remains fully operational in every other respect and cannot reposition.

Recovery requires either a hyperdrive down-state — which the platform cannot
enter while deployed — or external assistance, which is an external dependency
the architecture otherwise refuses (`FR-01`).

**This scenario is not exercised**, because exercising it would require
deliberately disabling three units. It is carried in
[Disaster Recovery §5.2](../operations/disaster-recovery.md#52-loss-of-mobility)
as a stated non-recoverable condition.

### Realised Deficiencies

| Ref | Deficiency |
|---|---|
| `TD-14` | Unit 4 has operated on a temporary mounting since commissioning ([ADR-008](adr-008-live-commissioning.md)). It carries a reduced structural allowance and is first to de-rate under load — which effectively makes the arrangement 5-of-6.5 rather than 5-of-7. |

`TD-14` materially erodes the margin this decision was made to provide. It is the
strongest argument for the Option C proposal that was refused, and is noted as
such at each review.

## Revisit Conditions

Revisited if:

1. `TD-14` cannot be closed within the current programme horizon, in which case
   the effective margin is below the ruling's intent; or
2. The Propulsion Systems Authority extends the verified field envelope to permit
   transit at four units, which would convert this to a 4-of-7 arrangement
   without additional mass.

One proposal has sought Option C (nine units). It was refused on mass budget, and
the refusal noted that closing `TD-14` would restore the intended margin at no
mass cost — which remains the Directorate's preferred route.
