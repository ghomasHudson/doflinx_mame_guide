---
title: Commands And Actions
layout: default
---

# Commands And Actions

The `[COMMANDS]` section maps a trigger name and state to one or more DOFLinx actions.

## Command Format

```ini
trigger|state|action1|action2|action3
```

Example:

```ini
led0|ON|FF_Button BUT_P1,BA_ON,0,0|FF_DOF E51,1200
led0|OFF|FF_Button BUT_P1,BA_OFF,0,0
```

## Trigger Names

Trigger names in `[COMMANDS]` can come from MAME output messages, DOFLinx key mappings, or named events.

Common MAME output triggers:

```text
led0
led1
coin
player1
player2
pause
reset
cheat
cheat_status
```

Custom trigger names are also useful with `KEY_TO_COMMAND`.

Example:

```ini
[STARTUP]
KEY_TO_COMMAND=BUT_B1,fire

[COMMANDS]
fire|ON|FF_DOF E216,-1
```

## States

Common states:

```text
ON
OFF
```

For MAME output messages, `ON` normally means the output value became active and `OFF` means inactive.

## Multiple Actions

Separate actions with `|`:

```ini
fire|ON|FF_DOF E216,-1|FF_DOF E217,-1|FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1
```

## Common Action Types

```text
FF_DOF
FF_Button
FF_Colour
FF_Flasher
FF_Dev
FF_PC
FF_DMD
FF_MSG
FF_SSF
FF_RUN
```

Examples:

```ini
FF_DOF E223,-1
FF_Button BUT_P1,BA_ON,0,0
FF_Colour Blue,RGB_TT,1500
FF_Flasher DV_FLCN,FL_TT,1,300,100,Random
FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1
FF_DMD,U,display/picture?path=ingame/explosion1
```

## Command Cleanup

If a shared file defines commands you do not want for a specific game, use `[CLEAR COMMANDS]`:

```ini
[CLEAR COMMANDS]
led0
led1
```
