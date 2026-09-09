---
title: 7. Deployment View
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-ARCH-008` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Architecture Authority | Operational / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# 7. Deployment View

Allocation of logical building blocks to physical infrastructure. On a platform
that cannot be taken out of service (`C-T-07`), the deployment view also has to
describe how software and configuration reach a live, occupied, armed station —
which is the second half of this chapter.

## 7.1 Physical Allocation

<figure class="blueprint" markdown>

[![Concentric zones surround a single core. Six latitude bands and twelve meridians define 72 sectors. Zones and sectors are independent coordinates.](../assets/blueprints/ds1-station-section.svg)](../assets/blueprints/ds1-station-section.svg)

<figcaption>DS1-DRG-101 · Station section & sector addressing · Rev 01 · Schematic, not to scale</figcaption>
</figure>

Use the zone coordinate for physical placement and the sector coordinate for failure-domain assignment.


```mermaid
flowchart TB
    subgraph Z0["Zone Z0 — Reactor Containment"]
        N_CORE["Containment Control Cabinets<br/><i>2N, air-gapped</i><br/><code>Z0/core</code>"]
    end

    subgraph Z1["Zone Z1 — Critical Systems"]
        N_PWR["Power Control Cabinets<br/><i>2N per quadrant</i>"]
        N_LS["Life Support Plant Controllers<br/><i>2N per life support group</i>"]
        N_PROP["Drive Control Cabinets<br/><i>N+1</i>"]
        N_DIODE["Core Data Diodes<br/><i>one inbound, one outbound</i>"]
    end

    subgraph Z2["Zone Z2 — Command and Control"]
        N_OB["Overbridge Compute Halls<br/><i>2N, northern polar</i><br/><code>Z2/N3-000</code>"]
        N_AOB["Alternate Overbridge<br/><i>southern polar, warm standby</i><br/><code>Z2/S3-180</code>"]
        N_QCP["Quadrant Command Posts<br/><i>4 &times; 2N</i>"]
        N_SCN["Sector Control Nodes<br/><i>72 &times; N+1</i>"]
        N_FUS["Sensor Fusion Cluster<br/><i>N+1 per quadrant</i>"]
        N_AUTH["Authorization Service<br/><i>2N, split across poles</i>"]
        N_LOG["Command Log Store<br/><i>append-only, 4-way replicated</i>"]
    end

    subgraph Z3["Zone Z3 — Operational"]
        N_OPS["Operational Compute<br/><i>maintenance, logistics, medical, personnel</i>"]
        N_ENG["Engineering Environments<br/><i>see 7.2</i>"]
    end

    subgraph Z4["Zone Z4 — Perimeter"]
        N_BTC["Bay Traffic Control<br/><i>72 &times; N+1</i>"]
        N_EDGE["External Interface Layer<br/><i>IF-01 to IF-06</i>"]
        N_SENS["Sensor Front Ends<br/><i>24 apertures</i>"]
    end

    N_CORE <-->|"physically distinct paths"| N_DIODE
    N_DIODE --> N_PWR
    N_DIODE --> N_OB
    N_PWR --> N_SCN
    N_LS --> N_SCN
    N_PROP --> N_QCP
    N_OB <--> N_AUTH
    N_OB --> N_QCP
    N_AOB -.->|"declared handover only"| N_QCP
    N_QCP --> N_SCN
    N_SCN --> N_BTC
    N_SENS --> N_FUS --> N_OB
    N_EDGE --> N_OB
    N_EDGE --> N_OPS
    N_OB --> N_LOG
    N_QCP --> N_LOG
    N_AUTH --> N_LOG
    N_OPS --> N_SCN
    N_ENG -.->|"promotion path only,<br/>see 7.2"| N_SCN
```

### Allocation Rules

| Rule | Rationale |
|---|---|
| No compute node serves two zones. | Zone invariant 4: no shared failure domain across a boundary. |
| Redundant pairs are separated by at least one quadrant and are supplied from different ring buses. | A single structural event may not take both halves of a 2N pair. |
| The Overbridge and the Alternate Overbridge are at opposite poles. | Maximum physical separation available within the hull. |
| The Authorization Service is split across both poles, not co-located with either bridge. | Loss of a bridge must not remove the ability to authorize. |
| The Command Log is replicated to all four Quadrant Command Posts. | An incident that destroys the Overbridge must not destroy the record of what it ordered. |
| `Z0` control cabinets have no network path out except the outbound diode. | Zone invariant 5. |

## 7.2 Engineering Environments on a Live Platform

There is no separate test platform. There is one hull, and it is occupied and
operational. Environment separation is therefore **logical, enforced, and
explicitly bounded** — and the boundaries are where the residual risk sits.

| Environment | Location | What it may reach | What it may never reach |
|---|---|---|---|
| `DEV` | `Z3`, isolated segment of `ENC-OPS` | Simulated plant models only | Any real actuator, any real telemetry, `ENC-CTRL`, `ENC-CORE` |
| `INT` | `Z3`, isolated segment of `ENC-OPS` | Hardware-in-the-loop rigs replicating one sector | Real sectors, `ENC-CTRL`, `ENC-CORE` |
| `PREPROD` | `Z2`, one designated reference sector node held out of the operational set | Real hardware of that one node, real telemetry read-only | Actuation outside its own node; `ENC-CORE` |
| `PROD` | `Z2` / `Z1` / `Z0` operational nodes | Everything within its zone allocation | `DEV` and `INT` segments — the path is one-way |

```mermaid
flowchart LR
    DEV["DEV<br/>Z3 / ENC-OPS isolated<br/><i>simulation only</i>"]
    INT["INT<br/>Z3 / ENC-OPS isolated<br/><i>hardware in the loop</i>"]
    PRE["PREPROD<br/>Z2 reference node<br/><i>real hardware, held out</i>"]
    PROD["PROD<br/>Z2 / Z1 / Z0<br/><i>72 operational nodes</i>"]

    G1["Promotion Gate 1<br/>Directorate technical review"]
    G2["Promotion Gate 2<br/>Architecture Review Board<br/>+ Ordnance concurrence if armament-adjacent"]
    G3["Promotion Gate 3<br/>Station Commander release<br/>within a declared maintenance window"]

    DEV --> G1 --> INT
    INT --> G2 --> PRE
    PRE --> G3 --> PROD

    PROD -.->|"telemetry export,<br/>one-way, sanitised"| INT
    PROD -.->|"telemetry export,<br/>one-way, sanitised"| DEV
```

!!! danger "The reference-node compromise"

    `PREPROD` is a real operational sector node, temporarily removed from the
    operational set. While it is held out, that sector runs on its `N+1`
    partner with no further margin. The reference node is therefore rotated
    across sectors and may not be held out during a declared alert state.

    This is a genuine compromise forced by `C-T-07`, not a good arrangement. It
    is recorded as `TD-04` and reviewed at each Architecture Review Board.

## 7.3 Change Propagation to Production

Changes reach production only inside a declared maintenance window
([DS1-OPS-030](../operations/maintenance.md)), and only in the order below.

```mermaid
sequenceDiagram
    autonumber
    participant ARB as Architecture Review Board
    participant SC as Station Commander
    participant MW as Maintenance Window Authority
    participant QCP as Quadrant Command Post
    participant SCN as Sector Control Node
    participant CL as Command Log

    ARB->>SC: Change package, verified at PREPROD
    SC->>MW: Release into declared window W-nnnn
    MW->>MW: Confirm readiness impact published<br/>and accepted by Fleet Command
    MW->>QCP: Authorize canary application — one sector
    QCP->>SCN: Apply to canary sector
    SCN-->>QCP: Applied — soak period begins
    Note over SCN,QCP: Soak: one full watch cycle.<br/>No further sectors during soak.
    alt Soak clean
        QCP->>SCN: Apply per quadrant, one quadrant at a time
        SCN-->>QCP: Applied and confirmed
        QCP->>CL: Record completion per sector
    else Any anomaly during soak
        QCP->>SCN: Revert canary to previous configuration
        SCN-->>QCP: Reverted and confirmed
        QCP->>CL: Record reversion and cause
        QCP->>ARB: Change package returned
    end
```

**Constraints on propagation.**

- One quadrant at a time. Never two. A change that has degraded two quadrants
  has degraded the platform.
- Every node must be able to revert to its previous configuration without an
  external dependency, including without the Overbridge.
- `Z0` containment control is **excluded from this path entirely.** It is changed
  only during a full reactor down-state, which has occurred twice since
  commissioning and requires Imperial Engineering Command approval in each case.

## 7.4 Infrastructure Register

| Infrastructure | Count | Zone | Redundancy | Supplied from |
|---|---|---|---|---|
| Overbridge compute halls | 2 | Z2 | 2N | `MTB-A` / `MTB-B` via `EB-A` / `EB-B` |
| Alternate Overbridge | 1 | Z2 | Warm standby | `EB-B` |
| Quadrant Command Posts | 4 | Z2 | 2N each | Own quadrant ring bus + cross-feed |
| Sector Control Nodes | 72 | Z2 | N+1 each | Own sector distribution board |
| Authorization Service instances | 2 | Z2 | 2N, pole-split | `EB-A` / `EB-B` |
| Command Log replicas | 4 | Z2 | 4-way | One per quadrant |
| Sensor fusion clusters | 4 | Z2 | N+1 each | Own quadrant ring bus |
| Core data diodes | 2 | Z1 | One per direction, no redundancy by design | `EB-A` (in), `EB-B` (out) |
| Bay traffic control units | 72 | Z4 | N+1 each | Own sector distribution board |
| External interface gateways | 6 &times; 2 | Z4 | 2N per interface | `QRB` per quadrant |
| Sensor apertures | 24 | Z4 | N+1 coverage overlap | Own sector distribution board |

!!! note "On the diodes having no redundancy"

    A redundant data diode is a second path, and a second path into `Z0` is
    exactly what the diode exists to prevent. Loss of the inbound diode means
    reactor setpoints cannot be changed remotely; the reactor continues at its
    last commanded setpoint and local `Z0` control assumes authority under the
    two-person rule. This is the intended behaviour, not a gap.
