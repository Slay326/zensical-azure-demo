---
title: ADR-002 Sector Autonomy
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-ADR-002` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Architecture Authority | Accepted / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# ADR-002 — Sector Autonomy with Bounded Envelopes

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Ruling authority** | Architecture Review Board |
| **Date of ruling** | Programme Phase 5 |
| **Proposed again since** | 2 times (both proposing wider autonomy) |

## Context

Constraint `C-T-03`: signal latency across a 160 km hull is operationally
significant. Closed-loop control from a single point cannot meet the response
times that life-safety functions require — a bulkhead that must seal in 8 seconds
cannot wait on a round trip to the Overbridge and back under a degraded network.

At the same time, the platform must have a single accountable command authority
(`C-M-01`). Distributing execution must not distribute authority.

## Options Considered

### Option A — Centralised control

All actuation commanded from the Overbridge.

Rejected. Fails life-safety response times under any network degradation, and
makes every sector dependent on a single link.

### Option B — Full sector autonomy

Each sector node holds full local authority and acts as it judges best.

Rejected on two grounds. It violates `C-M-01` — 72 independent authorities is not
a single accountable command. And it creates a privilege escalation path: a node
that loses its link would *gain* authority, making link loss attractive to an
adversary.

### Option C — Bounded autonomy within a pre-authorized envelope

Nodes execute normally under quadrant direction. On link loss they hold the last
authorized configuration and may act only within an envelope that was authorized
in advance, refusing anything outside it.

**Selected.**

## Ruling

<div class="visual-callout" markdown>

**Bounded autonomy**

```mermaid
flowchart LR
    L["LINKED"] -->|link lost| D["DETACHED"]
    D -->|envelope exceeded| S["SAFE"]
    D -->|reconcile restored link| L
```

A detached sector retains only its pre-authorized envelope.

</div>


Sector Control Nodes operate in three modes — `LINKED`, `DETACHED`, `SAFE` — as
specified in [RV-5](../architecture/runtime-view.md#rv-5-sector-link-loss-and-autonomous-degradation).

Four invariants are binding:

1. **Degradation never increases authority.** `DETACHED` is strictly less capable
   than `LINKED`.
2. **Peer commanding is forbidden**, in policy and in network topology
   ([Network Segmentation §4](../security/network-segmentation.md#4-within-enclave-segmentation)).
3. **Local logging continues in all modes** and is replayed on reconciliation. A
   gap in the log is an incident.
4. **`SAFE` is not self-exiting.** Recovery is an authorized human action.

## Consequences

### Accepted

| Consequence | Detail |
|---|---|
| Life-safety response times are met without network dependency | The decision's purpose |
| Command authority remains singular | `C-M-01` satisfied |
| Link loss is not an escalation vector | Invariant 1 |
| **The envelope must be defined and maintained for all 72 nodes** | Expensive; the origin of `TD-08` |
| Reconciliation after long detachment is complex | `TD-03` |

### Realised Deficiencies

| Ref | Deficiency |
|---|---|
| `TD-03` | Reconciliation is slow and occasionally rejected, forcing unnecessary `SAFE` transitions and contributing to the 22 per cent transit abort rate (`TD-13`) |
| `TD-08` | Envelopes are maintained manually per node and have drifted between quadrants; a `Q-III` node may refuse what a `Q-I` node permits |

Both are consequences of the ruling, not of its implementation, and both were
predicted at the Board. The envelope maintenance cost was the principal argument
against Option C and it has proved accurate.

## Revisit Conditions

Revisited if envelope maintenance cost becomes unsustainable — measured as
envelope drift beyond a declared tolerance across quadrants. `TD-08` is the
current indicator and is approaching, but has not crossed, that tolerance.

Both subsequent proposals sought *wider* envelopes to reduce the refusal rate in
`DETACHED`. Both were refused: a wider envelope reduces the difference between
`LINKED` and `DETACHED`, which erodes invariant 1.
