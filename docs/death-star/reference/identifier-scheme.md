---
title: Identifier Scheme
---

<div class="doc-control" markdown>

| Document ID | Classification | System | Document Owner | Status |
|---|---|---|---|---|
| `DS1-REF-020` | IMPERIAL RESTRICTED | DS-1 Orbital Battle Station | Imperial Engineering Directorate — Documentation Systems Section | Operational / Controlled Document |

ACCESS: AUTHORIZED ENGINEERING PERSONNEL ONLY &middot; Unauthorized access will be logged and escalated to Sector Security Command.
</div>

# Identifier Scheme

Every identifier used across this library, in one place. Identifiers are
permanent; a superseded document keeps its identifier and gains a status of
`Superseded`.

## 1. Document Identifiers

```
DS1 - ARCH - 007
 |      |      |
 |      |      +-- Sequence, three digits, allocated by Documentation Systems
 |      +--------- Volume code
 +---------------- Platform code, fixed
```

| Code | Volume | Allocated range | In use |
|---|---|---|---|
| `ARCH` | Architecture | 000–099 | 000–011 |
| `ENG` | System engineering | 000–199 | 001, 010–011, 020–021, 030–031, 040, 050, 060, 070, 080–081, 090, 100, 110, 120 |
| `OPS` | Operations | 000–099 | 001–002, 010, 020, 030, 040, 050, 060 |
| `SEC` | Security | 000–099 | 001–002, 010, 020, 030, 040 |
| `ADR` | Architecture Decision Records | 000–999 | 000–008 |
| `RSK` | Risk and debt registers | 000–099 | 000–001, 010 |
| `REF` | Reference | 000–099 | 000–001, 010–040, 090 |
| `DRG` | Controlled engineering drawings | 000–999 | 001–005 |

## 2. Location Designations

<div class="visual-callout" markdown>

**Read an address**

```mermaid
flowchart LR
    Z["Z1 / zone"] --> S["N2-090 / sector"] --> I["PL-04 / local item"]
```

Each field narrows the physical target; matching the item name alone is insufficient.

</div>


```
Z1 / N2-090 / PL-04
|      |        |
|      |        +-- Local item reference
|      +----------- Surface sector
+------------------ Zone
```

### Zones

| Code | Zone |
|---|---|
| `Z0` | Reactor containment |
| `Z1` | Critical systems |
| `Z2` | Command and sector control |
| `Z3` | Operational and habitation |
| `Z4` | Perimeter and hangar belt |

### Surface Sectors

`<BAND>-<MERIDIAN>` where band is `N3` `N2` `N1` `S1` `S2` `S3` and meridian is
`000` to `330` in 030 steps. 72 sectors. See
[DS1-DRG-003](../architecture/zone-and-sector-architecture.md#2-the-sector-model).

### Local Item References

| Prefix | Item |
|---|---|
| `PL-nn` | Plant room |
| `LB-nn` | Lift bank |
| `BY-nn` | Hangar bay |
| `SN-nn` | Sector control node |
| `BC-o-i` | Boundary control point, outer zone to inner zone |
| `SD-nn` | Sector distribution board |
| `FL-nnX` | Freight lift |
| `BTC-nn` | Bay traffic control |

## 3. System and Infrastructure Designations

| Pattern | Meaning | Example |
|---|---|---|
| `MTB-A` / `MTB-B` | Main trunk bus | Two only |
| `QRB-I` … `QRB-IV` | Quadrant ring bus | Roman numerals, four |
| `EB-A` / `EB-B` | Essential bus | Two only |
| `NEB` | Non-essential bus | One |
| `SG-1` … `SG-8` | Standby generation set | Eight |
| `PCH-A` / `PCH-B` | Primary conversion hall | Two only |
| `QCP-I` … `QCP-IV` | Quadrant command post | Four |
| `ENC-<name>` | Network enclave | `ENC-CORE`, `ENC-CTRL`, `ENC-OPS`, `ENC-LOG` |
| `GW-<from><to>` | Enclave gateway | `GW-OC` = `ENC-OPS` → `ENC-CTRL` |
| `DIODE-IN` / `DIODE-OUT` | Core data diodes | Two only, one per direction |

## 4. Reference Identifiers

| Prefix | Meaning | Held in |
|---|---|---|
| `FR-nn` | Functional requirement | [Introduction and Goals](../architecture/introduction-and-goals.md) |
| `C-M-nn` | Mandated constraint | [Constraints](../architecture/constraints.md) |
| `C-T-nn` | Technical constraint | [Constraints](../architecture/constraints.md) |
| `C-O-nn` | Organisational constraint | [Constraints](../architecture/constraints.md) |
| `C-C-nn` | Convention | [Constraints](../architecture/constraints.md) |
| `S-n` | Solution strategy | [Solution Strategy](../architecture/solution-strategy.md) |
| `CC-n` | Cross-cutting concept | [Cross-Cutting Concepts](../architecture/crosscutting-concepts.md) |
| `QS-nn` | Quality scenario | [Quality Requirements](../architecture/quality-requirements.md) |
| `RV-n` | Runtime view scenario | [Runtime View](../architecture/runtime-view.md) |
| `R-nn` | Risk | [Risk Register](../risks/risk-register.md) |
| `TD-nn` | Technical debt item | [Technical Debt Register](../risks/technical-debt.md) |
| `T-n` | Threat actor | [Security Volume](../security/index.md#threat-model) |
| `IF-nn` | External interface | [Interface Register](interface-register.md) |
| `IX-<name>` | Internal interface | [Interface Register](interface-register.md) |
| `IMP-n` | Clearance level | [Access Control Model](../security/access-control-model.md) |
| `ORL-n` | Operational readiness level | [Operating Model](../operations/operating-model.md) |
| `P0` … `P4` | Load priority class | [Power Distribution](../systems/power-distribution.md) |
| `LSD-n` | Load shed directive | [Power Distribution](../systems/power-distribution.md) |
| `W-<class>` | Maintenance window class | [Maintenance and Windows](../operations/maintenance.md) |

## 5. Allocation

New identifiers are allocated by the Documentation Systems Section on request
through a System Authority. Self-allocation is not permitted: it produces
collisions, and a collision in a location designation misroutes an isolation.

Retired identifiers are **not** reused.
