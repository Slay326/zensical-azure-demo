---
title: 6. Runtime View
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-ARCH-007` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Architecture Authority | Operational / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# 6. Runtime View

Behavioural scenarios that exercise the architecture. Each names its trigger, its
participating blocks, its failure handling and the quality scenario it verifies.
Nominal-path scenarios are given first; degradation and incident paths follow.

| # | Scenario | Verifies |
|---|---|---|
| [RV-1](#rv-1-operational-request-flow) | Operational request from tasking to execution | Controllability |
| [RV-2](#rv-2-authentication-and-authorization-at-a-zone-boundary) | Personnel transit across a zone boundary | Controllability |
| [RV-3](#rv-3-hyperspace-transit-preparation-and-execution) | Hyperspace transit | Sustainability |
| [RV-4](#rv-4-craft-recovery-cycle) | Craft recovery into a hangar bay | Sustainability |
| [RV-5](#rv-5-sector-link-loss-and-autonomous-degradation) | Loss of a sector's command link | Survivability |
| [RV-6](#rv-6-hull-breach-and-incident-escalation) | Hull breach in an occupied sector | Survivability |
| [RV-7](#rv-7-primary-armament-authorization-interlock-chain) | Armament authorization interlocks | Controllability |

---

## RV-1 — Operational Request Flow

**Trigger.** Fleet Command issues an operational directive over `IF-01`.

**Principle under test.** Intent arrives from outside; *authority* is always
exercised inside. No external actor can actuate anything.

```mermaid
sequenceDiagram
    autonumber
    participant FC as Fleet Command<br/>(external)
    participant CS as Comms Suite<br/>IF-01
    participant OB as Overbridge
    participant AS as Authorization Service
    participant CL as Command Log
    participant QCP as Quadrant Command Post
    participant SCN as Sector Control Node
    participant PL as Plant / Actuator

    FC->>CS: Operational directive (signed, encrypted)
    CS->>CS: Decrypt, verify origin signature
    CS->>OB: Directive presented as INTENT (no execution authority)
    OB->>AS: Request authorization<br/>(directive, commander identity, platform state)
    AS->>AS: Evaluate policy: authority, readiness level,<br/>zone state, interlocks, standing prohibitions
    alt Authorized
        AS-->>OB: PERMIT + authorization token (scoped, time-boxed)
        OB->>CL: Record directive, decision, token scope
        OB->>QCP: Authorized directive + token
        QCP->>SCN: Sector tasking + derived token
        SCN->>SCN: Validate token scope against local sector state
        SCN->>PL: Actuate
        PL-->>SCN: State change confirmed
        SCN-->>QCP: Execution report
        QCP-->>OB: Aggregated execution report
        OB->>CL: Record outcome
        OB-->>CS: Acknowledgement to Fleet Command
    else Refused
        AS-->>OB: DENY + reason code
        OB->>CL: Record directive and refusal reason
        OB-->>CS: Refusal with reason to Fleet Command
    end
```

**Failure handling.**

| Failure | Behaviour |
|---|---|
| Signature verification fails | Directive discarded at `IF-01`; security event Class 2 raised; no presentation to the Overbridge |
| Authorization Service unreachable | **Refuse.** There is no fail-open path. The Overbridge may invoke the two-officer manual authority procedure, which is itself logged |
| Token expires mid-execution | Sector Control Node halts at the next safe point and reports; it does not complete on a stale token |
| Sector Control Node unreachable | Quadrant Command Post reports partial execution; the directive is *not* silently marked complete |

---

## RV-2 — Authentication and Authorization at a Zone Boundary

**Trigger.** A rating attempts to transit from `Z3` into `Z2` at a Boundary
Control Point.

```mermaid
sequenceDiagram
    autonumber
    participant P as Personnel
    participant BCP as Boundary Control Point<br/>(policy enforcement point)
    participant IDG as Identity Federation Gateway<br/>IF-04
    participant PDP as Authorization Service<br/>(policy decision point)
    participant AUD as Security Audit Store
    participant GAR as Garrison Response

    P->>BCP: Present credential + biometric
    BCP->>BCP: Verify credential integrity locally
    BCP->>PDP: Authorization request<br/>(identity, target zone, time, current zone, task reference)
    PDP->>IDG: Resolve clearance assertion
    alt Assertion cached and valid
        IDG-->>PDP: Clearance level, attributes, expiry
    else Cache stale and IF-04 unavailable
        IDG-->>PDP: Cached assertion past refresh, within grace
        PDP->>AUD: Record degraded-assertion decision
    end
    PDP->>PDP: Evaluate:<br/>clearance >= zone minimum?<br/>adjacent zone only?<br/>active task reference?<br/>escort required?<br/>zone in lockdown?
    alt All conditions met
        PDP-->>BCP: PERMIT (single transit, time-boxed)
        BCP->>P: Boundary opens
        BCP->>AUD: Record transit
    else Any condition fails
        PDP-->>BCP: DENY + reason code
        BCP->>P: Boundary holds closed
        BCP->>AUD: Record refusal
        opt Non-adjacent zone attempted, or clearance shortfall > 1 level
            AUD->>GAR: Class-2 security event — dispatch
        end
    end
```

**Design notes.**

- The Boundary Control Point is an *enforcement* point only. It holds no policy
  and cannot be reconfigured locally. A compromised BCP cannot grant access.
- Transit is single-use and time-boxed. Holding a door for a colleague produces
  one authorized and one unauthorized transit; the second is detected.
- `IF-04` unavailability degrades to cached assertions within a grace window,
  then to local fallback authority. It never degrades to open. See
  [ADR-007](../decisions/adr-007-identity-federation.md).

---

## RV-3 — Hyperspace Transit Preparation and Execution

**Trigger.** Authorized reposition directive. Transit is an *operating mode*
with its own readiness level, not a background activity (`C-T-05`).

```mermaid
stateDiagram-v2
    [*] --> ORL3: Operational, restricted

    ORL3 --> PREP: Transit directive authorized
    PREP: Transit Preparation
    PREP: - Navigation solution computed and cross-checked
    PREP: - Mass distribution and structural survey
    PREP: - All hangar bays closed and sealed
    PREP: - External craft recovered or released
    PREP: - Armament charge state driven to zero and interlocked

    PREP --> QUIESCE: All preparation gates passed
    PREP --> ORL3: Any gate fails — directive returned to Overbridge

    QUIESCE: Electrical and Structural Quiescence
    QUIESCE: - Non-essential bus shed to P3
    QUIESCE: - Sector nodes commanded to TRANSIT configuration
    QUIESCE: - Pressure boundaries verified closed
    QUIESCE: - Gravity plating phase-locked

    QUIESCE --> TRANSIT: Quiescence confirmed by all 72 sectors
    QUIESCE --> ABORT: Any sector reports non-quiescent

    TRANSIT: Hyperspace Transit
    TRANSIT: - Sensors in passive-only mode
    TRANSIT: - External interfaces IF-01, IF-03, IF-06 suspended
    TRANSIT: - Sector nodes in DETACHED, pre-authorized envelope only

    TRANSIT --> REVERT: Transit complete
    TRANSIT --> EMERGENCY: Structural or containment alarm

    REVERT: Reversion and Restoration
    REVERT: - Position fix acquired and confirmed against IF-02
    REVERT: - Sensors to active, threat assessment
    REVERT: - Interfaces restored, sector nodes to LINKED
    REVERT: - Load restored in priority order P0 to P4

    REVERT --> ORL3: Restoration complete
    ABORT --> ORL3: Directive returned, cause recorded
    EMERGENCY --> REVERT: Emergency reversion to realspace
```

**Failure handling.** A single sector that cannot confirm quiescence aborts the
transit for the whole platform. This is deliberate: a partial-quiescence transit
is a structural risk, and 72 independent confirmations is the only honest way to
establish the platform's state. Aborts are common; they are recorded and trended
rather than treated as exceptional.

---

## RV-4 — Craft Recovery Cycle

**Trigger.** Inbound craft requests recovery on `IF-06`.

```mermaid
sequenceDiagram
    autonumber
    participant CR as Inbound Craft
    participant TC as Traffic Control<br/>IF-06
    participant BTC as Bay Traffic Control<br/>BTC-nn
    participant CF as Containment Field Plant
    participant BD as Blast Door Assembly
    participant BCP as BCP-4/3
    participant LOG as Internal Logistics

    CR->>TC: Approach request + transponder identity
    TC->>TC: Challenge transponder, cross-check against<br/>expected returns and tactical picture
    alt Identity not confirmed
        TC-->>CR: Approach refused, hold at standoff
        TC->>BTC: Bay held closed
    else Identity confirmed
        TC->>BTC: Assign bay, pad, inbound lane
        BTC->>CF: Confirm containment field integrity
        CF-->>BTC: Field nominal
        BTC->>BD: Open blast doors
        BD-->>BTC: Doors open and locked
        BTC-->>CR: Cleared, inbound lane A, pad 07
        CR->>BTC: On pad, clamps engaged
        BTC->>BD: Close blast doors
        BTC->>LOG: Cargo manifest handover request
        LOG->>BCP: Personnel egress requests presented individually
        Note over BCP: Each crew member is authorized<br/>separately per RV-2.<br/>Craft clearance is not crew clearance.
        BCP-->>LOG: Per-person permit or deny
    end
```

**Design note.** Craft identity and crew identity are separate decisions. A
confirmed craft carrying an unconfirmed person results in a berthed craft and a
person who does not leave `Z4`. This separation is the primary control against
the infiltration path modelled in [R-04](../risks/risk-register.md).

---

## RV-5 — Sector Link Loss and Autonomous Degradation

**Trigger.** A Sector Control Node loses its link to its Quadrant Command Post.

```mermaid
stateDiagram-v2
    [*] --> LINKED

    LINKED: LINKED
    LINKED: Executes authorized directives
    LINKED: Reports state continuously

    DETACHED: DETACHED
    DETACHED: Holds last authorized configuration
    DETACHED: Acts only within pre-authorized envelope
    DETACHED: Refuses anything outside it
    DETACHED: Continues to log locally

    SAFE: SAFE
    SAFE: Sheds load to P0/P1
    SAFE: Seals sector boundary
    SAFE: Preserves life support
    SAFE: Accepts no directive but recovery

    RECOVER: RECOVERING
    RECOVER: Link restored, state reconciled
    RECOVER: Local log replayed to Command Log
    RECOVER: Divergence reported

    LINKED --> DETACHED: Link lost > 4 s
    DETACHED --> LINKED: Link restored, no local fault
    DETACHED --> SAFE: Local fault while detached
    LINKED --> SAFE: Life-safety alarm, any link state
    SAFE --> RECOVER: Link restored and fault cleared
    DETACHED --> RECOVER: Link restored after > 300 s
    RECOVER --> LINKED: Reconciliation accepted by QCP
    RECOVER --> SAFE: Reconciliation rejected — divergence too large
```

**Invariants that hold in every state.**

1. A node never gains authority by losing its link. `DETACHED` is strictly less
   capable than `LINKED`.
2. A node in `DETACHED` or `SAFE` cannot be commanded by a peer node.
3. Local logging continues in all states and is replayed on reconciliation. A
   gap in the log is itself an incident.
4. `SAFE` is not automatically exited. Recovery is an authorized action.

**Known weakness.** Reconciliation after a long detachment is slow and, in
sectors with heavy local state, occasionally rejected — forcing an unnecessary
`SAFE` transition. Recorded as `TD-03`.

---

## RV-6 — Hull Breach and Incident Escalation

**Trigger.** Pressure loss detected in an occupied `Z4` sector.

```mermaid
sequenceDiagram
    autonumber
    participant SEN as Sector Pressure Sensing
    participant SCN as Sector Control Node
    participant PRS as Pressure Boundary Control
    participant QCP as Quadrant Command Post
    participant OB as Overbridge
    participant DC as Damage Control Party
    participant MED as Medical
    participant CL as Command Log

    SEN->>SCN: Rate-of-change alarm, sector N1-060
    SCN->>SCN: Classify: breach vs. sensor fault<br/>(cross-check 3 independent sensing paths)
    Note over SCN: Automatic action requires 2 of 3 agreement.<br/>No single sensor closes a bulkhead.
    SCN->>PRS: Seal sector boundary (automatic, pre-authorized)
    PRS-->>SCN: Boundary sealed, 2 compartments isolated
    SCN->>SCN: Shed to P0/P1 in the affected sector
    SCN->>QCP: CLASS-1 INCIDENT declared
    QCP->>OB: Escalation, platform state impact assessed
    OB->>CL: Incident opened, incident commander assigned
    par Response
        OB->>DC: Dispatch damage control to N1-060
        OB->>MED: Casualty reception at Z3 muster point
    end
    DC->>SCN: Request boundary opening for entry
    SCN->>QCP: Boundary opening requires QCP authorization
    QCP-->>SCN: PERMIT, single entry, escorted, logged
    DC->>DC: Containment and repair
    DC-->>OB: Sector stabilised
    OB->>CL: Incident state to RECOVERY
    Note over OB,CL: Incident is not closed at stabilisation.<br/>Closure requires the post-incident review<br/>defined in DS1-OPS-020.
```

**Escalation classes** are defined in [Incident Response](../operations/incident-response.md).
The architectural point here is that **automatic protective action is
pre-authorized and immediate, while intervention is authorized and deliberate.**
Sealing a bulkhead does not wait for a human. Opening one always does.

---

## RV-7 — Primary Armament Authorization Interlock Chain

**Scope limitation.** This scenario describes the *authorization and interlock
architecture* only. It contains no armament design, energy, targeting or
sequencing detail. That material is held by the Ordnance Systems Authority under
separate classification.

```mermaid
flowchart TD
    A["Directive received from<br/>Imperial High Command over IF-01"]
    B{"Capability release held<br/>by High Command?"}
    C{"Station Commander<br/>authorization present?"}
    D{"Second authorizing officer<br/>concurrence present?"}
    E{"Readiness level ORL-4<br/>or above?"}
    F{"Platform state interlocks clear?<br/>hangars sealed, transit inhibited,<br/>thermal margin available,<br/>no open Class-1 incident"}
    G{"Ordnance Systems Authority<br/>local interlock satisfied?"}
    H["Charge feeder released<br/>under continuous two-party hold"]
    R["REFUSED<br/>reason recorded in Command Log,<br/>refusal reported to originator"]

    A --> B
    B -- No --> R
    B -- Yes --> C
    C -- No --> R
    C -- Yes --> D
    D -- No --> R
    D -- Yes --> E
    E -- No --> R
    E -- Yes --> F
    F -- No --> R
    F -- Yes --> G
    G -- No --> R
    G -- Yes --> H

    H -.->|"release of either hold<br/>at any point"| R
```

**Architectural properties.**

- The chain is **conjunctive**: every gate must pass. There is no override, no
  quorum substitution and no emergency bypass. A gate that cannot be evaluated
  counts as failed.
- The charge feeder is held open by *continuous* two-party action, not by a
  single authorizing event. Release of either hold reverts the feeder.
- Interlocks are enforced by the Ordnance Systems Authority's own equipment as
  well as by the Authorization Service. Neither alone is sufficient.
- Every refusal is logged with its reason code and reported back to the
  originator. Refusals are trended; a rising refusal rate at a particular gate is
  treated as a defect indication, not as operator error.
