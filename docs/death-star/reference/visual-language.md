---
title: Engineering Drawing Register
---

# Engineering Drawing Register

The plates describe relationships already defined by the system authorities.
They are schematic views of a fictional platform, not construction drawings.
Each drawing has a document ID, revision, grid coordinates and a text equivalent
in its SVG description and in the surrounding documentation.

## Line conventions

| Mark | Meaning |
|---|---|
| Fine blue grid | Drawing coordinates only; not a dimensional scale |
| Solid thin line with arrow | Directed flow, delegation or movement, as identified in the caption |
| Dashed line with arrow | Secondary channel, telemetry or conditional transfer; caption specifies which |
| Dashed enclosure | System or trust boundary |
| Muted amber line | Isolation, inhibit or critical boundary |
| Open contact | Disconnected path; not an available route |

Directions and labels carry meaning independently of color. Open any plate to
inspect its labels at full resolution. On small screens, figures scroll
horizontally while the caption remains readable.

## Subsystem plates

| Drawing | Subject |
|---|---|
| [DS1-DRG-101](../assets/blueprints/ds1-station-section.svg) | Station section & sector addressing |
| [DS1-DRG-102](../assets/blueprints/ds1-command-hierarchy.svg) | Command authority & delegation |
| [DS1-DRG-103](../assets/blueprints/ds1-power-topology.svg) | Power topology & failure separation |
| [DS1-DRG-104](../assets/blueprints/ds1-hangar-logistics.svg) | Hangar logistics / separated routes |
| [DS1-DRG-105](../assets/blueprints/ds1-security-boundaries.svg) | Security zones / inward gates |
| [DS1-DRG-106](../assets/blueprints/ds1-network-enclaves.svg) | Network enclaves / explicit interfaces |
| [DS1-DRG-107](../assets/blueprints/ds1-maintenance-layers.svg) | Maintenance access / layers of evidence |
| [DS1-DRG-108](../assets/blueprints/ds1-reactor-containment.svg) | Reactor containment / system boundaries |
| [DS1-DRG-109](../assets/blueprints/ds1-superlaser-interfaces.svg) | Superlaser / architectural couplings |
| [DS1-DRG-110](../assets/blueprints/ds1-emergency-routing.svg) | Emergency routing / local evacuation |
| [DS1-DRG-111](../assets/blueprints/ds1-construction-phases.svg) | Construction / progressive deployment |

## Reading a plate

```mermaid
flowchart LR
    I["Match drawing ID"] --> B["Locate boundary"] --> F["Trace labeled flow"] --> R["Read residual / exception"]
```

## Authoring rules

Keep SVG files and any diagram-specific CSS under `docs/death-star/assets/`.
Use relative image links from the owning page, meaningful alt text, and a
caption that states the drawing ID and interpretation. Keep labels outside
crossing lines, use orthogonal connectors for logical flows, and state where
geometry or sequencing is schematic.

Use Mermaid for state, authority, trust and process relationships. Use SVG for
spatial views, physical separation and larger subsystem plates. Small callouts
should explain a local decision or failure path, rather than repeat an entire
system decomposition.

The deployment build checks generated asset references under `/death-star/`
and rejects local asset URLs that escape that prefix or point to missing files.
