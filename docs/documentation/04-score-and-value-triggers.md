---
title: Triggers
nav_order: 4
parent: Documentation
layout: default
---

# Triggers

Score/value triggers live in the `[SCORE]` section and run actions when monitored values change, reach thresholds, or remain idle.

## Trigger Families

Most value triggers follow the same three suffixes:

| Suffix | Format | Meaning |
|---|---|---|
| `*C` | `*C=min:max:actions` | Runs when the value changes by an amount between `min` and `max`. |
| `*T` | `*T=threshold:actions` | Runs when the value reaches `threshold`. |
| `*E` | `*E=min:max:step:actions` | Runs for a matching event range, with `step` controlling repeated events. |

The first letter identifies the value being watched. For example, `S` is score, `D` is credits, `H` is hits, `R` is round, `T` is shots or targets, and `A` is a custom A-series value.

Examples:

```ini
# Score changed by 50 to 160 points
SC=50:160:FF_DOF E223,-1

# Score reached 30000
ST=30000:FF_DOF E773,1800

# Repeating score event
SE=80000:80000:10:FF_DOF E781,1800

# Credits changed by -2 to 1
DC=-2:1:FF_PC,U,M,ministats?label=!PREFIX_C!&value=!CREDITS!
```

## Trigger Summary

| Trigger | Meaning |
|---|---|
| `SC` | Score changed in range. |
| `ST` | Score threshold reached. |
| `SE` | Score event with repeat step. |
| `DC` | Credits changed in range. |
| `DT` | Credits threshold reached. |
| `DE` | Credits event with repeat step. |
| `HC` | Hits changed in range. |
| `HT` | Hits threshold reached. |
| `HE` | Hits event with repeat step. |
| `RC` | Round changed in range. |
| `RT` | Round threshold reached. |
| `RE` | Round event with repeat step or delay. |
| `TC` | Shots/targets changed in range. |
| `TT` | Shots/targets threshold reached. |
| `TE` | Shots/targets event with repeat step. |
| `AC` | Custom A-series value changed in range. |
| `AT` | Custom A-series value threshold reached. |
| `AE` | Custom A-series value event with repeat step. |
| `AV` | Custom A-series value trigger. See [05 - Custom A-Series Values](05-custom-a-series-values.md). |

## Other Trigger Forms

`SD` runs after score activity has been idle for the configured delay.

```ini
SD=delay_ms:actions
```

Example:

```ini
SD=5000:FF_PC,U,E,arcade/stream/mame/!ROM!?nogif&nomini&nostrip&event=InGame
```

## Action Substitutions

Actions can use live substitutions:

```text
!ROM!
!SHOTS!
!HITS!
!RATIO!
!ROUND!
!LIVES!
!CREDITS!
!PULSE_RES!
!PREFIX_R!
!PREFIX_L!
!PREFIX_C!
!LED_R!
!LED_G!
!LED_B!
```

Example:

```ini
SD=100:FF_PC,U,M,ministats?label=!PREFIX_R!&value=!ROUND!&shots=!SHOTS!&hits=!HITS!&ratio=!RATIO!
```
