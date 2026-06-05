---
title: Custom A-Series Values
layout: default
---

# Custom A-Series Values

The A-series is for arbitrary custom memory values that do not fit the older fixed score/lives/round/hits/shots slots.

The parser supports:

```text
A
AM
AC
AT
AE
AV
```

In practice, use indexed keys:

```ini
A1=...
AM1=...
A2=...
AM2=...
```

DOFLinx extracts the number from the key, so `A1` is parsed as A-series slot 1 and `AM1` as the parser for slot 1.

## Basic Pattern

```ini
A1=:maincpu|main|program|ADDRESS|LENGTH
AM1=,,,1,HEX,FORWARD,Label
```

Example:

```ini
A1=:maincpu|main|program|9820|1
AM1=,,,1,HEX,REVERSE,ShipState
```

This reads one byte at `0x9820`, parses it as hex, and labels it `ShipState`.

## Multiple Custom Values

```ini
A1=:maincpu|main|program|E123|1
AM1=,,,1,HEX,FORWARD,Weapon

A2=:maincpu|main|program|E140|1
AM2=,,,1,NUMBER,FORWARD,Enemies
```

## A-Series Triggers

The parser supports:

| Key | Use |
|---|---|
| `AC` | Custom value changed in range |
| `AT` | Custom value reached threshold |
| `AE` | Custom value event with repeat/step |
| `AV` | Custom value/direct value trigger |

The exact argument shapes are inferred from the parser family and should be tested with logging enabled.

Recommended starting forms:

```ini
AC=index:min:max:actions
AT=index:threshold:actions
AE=index:min:max:step:actions
AV=index:value:actions
```

Example:

```ini
# Monitor weapon byte
A1=:maincpu|main|program|E123|1
AM1=,,,1,HEX,FORWARD,Weapon

# Monitor enemy count
A2=:maincpu|main|program|E140|1
AM2=,,,1,NUMBER,FORWARD,Enemies

# Trigger when weapon value reaches 3
AT=1:3:FF_Flasher DV_FLCN,FL_TT,1,300,100,Blue|FF_DOF E223,300

# Trigger when enemy count changes by 1 through 5
AC=2:1:5:FF_DOF E514,500
```

## When To Use A-Series

Use A-series for game-specific state such as:

```text
weapon selected
enemy count
boss health
bonus mode active
current room
power-up state
timer value
mission objective
```

Use the older fixed keys when the value already has a known role:

| Goal | Prefer |
|---|---|
| Score | `S1`/`M1`, `S2`/`M2` |
| Lives | `L1`/`LM1`, `L2`/`LM2` |
| Round/stage | `R1`/`RM1`, `R2`/`RM2` |
| Hits | `H1`/`HM1`, `H2`/`HM2` |
| Shots | `T1`/`TM1`, `T2`/`TM2` |
| Credits | `DK`/`DKM` and `DC` |
| Anything else | `A#`/`AM#` and `AC`/`AT`/`AE`/`AV` |

## Finding Addresses

Use MAME debugger, Lua console, cheat search tools, or RAM watches to find stable addresses.

Then validate in small steps:

1. Add one `A#` read.
2. Add one `AM#` parser.
3. Add one simple `AT` or `AC` action.
4. Enable DOFLinx logging.
5. Confirm the value changes when expected.
