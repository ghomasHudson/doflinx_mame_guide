---
title: Commands
nav_order: 2
parent: Documentation
layout: default
---

# Commands And Actions

The `[COMMANDS]` section maps a trigger name and state to one or more DOFLinx actions. Use it for immediate events such as button presses, MAME lamp or LED outputs, coin counters, and other simple on/off signals.

## Command Format

```ini
trigger|state|action1|action2|action3
```

Each command line is split with pipe characters (`|`):

| Field | Meaning |
|---|---|
| `trigger` | The MAME output name or DOFLinx command name to listen for. |
| `state` | The value/state that must be received before the actions run. |
| `action1`, `action2`, ... | One or more DOFLinx actions to run, in order, when the trigger and state match. |

The trigger and state are the matching part. The actions are the effect part. If the trigger changes to a different state, that line is skipped and another matching line can handle it.

Example:

```ini
led0|ON|FF_Button BUT_P1,BA_ON,0,0|FF_DOF E51,1200
led0|OFF|FF_Button BUT_P1,BA_OFF,0,0
```

In this example, `led0|ON` turns on the player 1 button light and pulses DOF event `E51` for 1200 ms. `led0|OFF` turns the player 1 button light back off.

## Trigger Names

Trigger names in `[COMMANDS]` can come from MAME output messages, DOFLinx key mappings, or named events.

MAME output triggers are the names emitted by the running game. They are often outputs that originally controlled cabinet lamps, start buttons, counters, or status LEDs. If the game reports `led0` changing to `ON`, DOFLinx looks for a command line that starts with `led0|ON|`.

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

Many games don't have triggers to easily hook into. For them you'll need [Memory Mapping](03-score-memory-mapping).

Custom trigger names are also useful with `KEY_TO_COMMAND`. This lets a cabinet button behave like a named trigger even when the game does not expose a matching MAME output.

Example:

```ini
[STARTUP]
KEY_TO_COMMAND=BUT_B1,fire

[COMMANDS]
fire|ON|FF_DOF E216,-1
```

Here, pressing `BUT_B1` creates the `fire` command. The `[COMMANDS]` line then maps `fire|ON` to DOF event `E216`. Releasing the button would be `fire|OFF` if you need a separate off action.

## Multiple Actions

Separate actions with `|`:

```ini
fire|ON|FF_DOF E216,-1|FF_DOF E217,-1|FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1
```

Actions run from left to right. This is useful when one event should produce several effects at the same time, such as a solenoid pulse, a flasher, and a Pixelcade animation.

Keep the trigger and state only once at the start of the line. Every field after that is an action.

## Common Action Types

| Action | Typical Use |
|---|---|
| `FF_DOF` | Fire a DOF event, such as a contactor, shaker, knocker, beacon, or custom DOF output. |
| `FF_Button` | Change a cabinet button light state. |
| `FF_Colour` | Set a named RGB device or toy to a colour for a duration. |
| `FF_Flasher` | Run a flasher effect on a configured device. |
| `FF_Dev` | Send a command to a specific configured output device. |
| `FF_PC` | Trigger Pixelcade content. |
| `FF_PUP` | Trigger PinUP Player content, commonly overlays or videos. |
| `FF_DMD` | Show media or content on a DMD/display target. |
| `FF_MSG` | Send a text message through DOFLinx. |
| `FF_SSF` | Play an SSF sound effect. |
| `FF_RUN` | Run an external command or program. |

The action name is followed by a space and then that action's parameters. Parameters are comma-separated. For example, `FF_DOF E223,-1` means action `FF_DOF` with parameters `E223` and `-1`.

For many DOF actions, the second parameter is a duration in milliseconds. A value of `-1` commonly means the normal/default DOF pulse behavior for that event, while `0` is commonly used to turn an event off.

Examples:

```ini
FF_DOF E223,-1
FF_Button BUT_P1,BA_ON,0,0
FF_Colour Blue,RGB_TT,1500
FF_Flasher DV_FLCN,FL_TT,1,300,100,Random
FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1
FF_PUP,U,E,animation/overlay/mameoutput/generic_explosion1
FF_DMD,U,display/picture?path=ingame/explosion1
```

What those examples do:

| Example | Effect |
|---|---|
| `FF_DOF E223,-1` | Fires DOF event `E223` using its default behavior. |
| `FF_Button BUT_P1,BA_ON,0,0` | Turns the player 1 button light on. |
| `FF_Colour Blue,RGB_TT,1500` | Sets the `RGB_TT` device to blue for 1500 ms. |
| `FF_Flasher DV_FLCN,FL_TT,1,300,100,Random` | Runs a flasher effect using the configured flasher device and timing values. |
| `FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1` | Plays an explosion on a Pixelcade LED. |
| `FF_PUP,U,E,animation/overlay/mameoutput/generic_explosion1` | Triggers PinUP Player content. |
| `FF_DMD,U,display/picture?path=ingame/explosion1` | Displays the named picture content on the DMD/display target. |

## Choosing Commands Or Score Triggers

Use `[COMMANDS]` when the game or cabinet already gives you a discrete event, such as `led0` turning on or a mapped button being pressed.

Use `[SCORE]` triggers when you need to watch memory values, such as score increases, lives changing, credits changing, boss health, or game mode values. See [Score And Value Triggers](04-score-and-value-triggers.md).

## Command Cleanup

If a shared file defines commands you do not want for a specific game, use `[CLEAR COMMANDS]`:

```ini
[CLEAR COMMANDS]
led0
led1
```

This removes earlier command mappings for `led0` and `led1` before the current game file adds its own behavior. It is most useful when a shared file has generic mappings that are wrong for one specific game.
