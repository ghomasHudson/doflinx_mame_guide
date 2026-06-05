---
title: Score And Value Triggers
layout: default
---

# Score And Value Triggers

Score/value triggers live in the `[SCORE]` section and run actions when monitored values change, reach thresholds, or remain idle.

## Score Triggers

### `SC` - Score Changed In Range

```ini
SC=min:max:actions
```

Runs when a score change is between `min` and `max`.

Example:

```ini
SC=50:160:FF_DOF E223,-1
```

In Galaga this range represents a single ship kill.

### `ST` - Score Threshold Reached

```ini
ST=threshold:actions
```

Runs when the score reaches a threshold.

Example:

```ini
ST=30000:FF_DOF E773,1800
```

### `SE` - Score Event With Repeat Step

```ini
SE=min:max:step:actions
```

Used for events where repeated score thresholds should be controlled by a step value.

Example:

```ini
SE=80000:80000:10:FF_DOF E781,1800
```

### `SD` - Score Delay

```ini
SD=delay_ms:actions
```

Runs after score activity has been idle for the delay.

Example:

```ini
SD=5000:FF_PC,U,E,arcade/stream/mame/!ROM!?nogif&nomini&nostrip&event=InGame
```

## Credits Triggers

### `DC` - Credits Changed

```ini
DC=min:max:actions
```

Runs when credits change by a matching amount or range.

Example:

```ini
DC=-2:1:FF_PC,U,M,ministats?label=!PREFIX_C!&value=!CREDITS!
```

### `DT` and `DE`

The executable parser includes `DT` and `DE`, mirroring the `ST` and `SE` trigger families for credits. They are not commonly used in the shipped files.

Likely forms:

```ini
DT=threshold:actions
DE=min:max:step:actions
```

## Hits Triggers

The parser includes these keys:

```text
HC
HT
HE
```

They mirror the score trigger families for hits:

```ini
HC=min:max:actions
HT=threshold:actions
HE=min:max:step:actions
```

## Round Triggers

The parser includes these keys:

```text
RC
RT
RE
```

Known shipped example:

```ini
RE=1:1:200:FF_PC,S,C,!PREFIX_R!%20!ROUND!
```

Likely forms:

```ini
RC=min:max:actions
RT=threshold:actions
RE=min:max:delay_or_step:actions
```

## Shots/Targets Triggers

The parser includes these keys:

```text
TC
TT
TE
```

They mirror the score trigger families for shots/targets:

```ini
TC=min:max:actions
TT=threshold:actions
TE=min:max:step:actions
```

## A-Series Custom Value Triggers

The parser includes these keys:

```text
AC
AT
AE
AV
```

These are for custom `A#` values. See [05 - Custom A-Series Values](05-custom-a-series-values.md).

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
