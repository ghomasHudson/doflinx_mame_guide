---
title: API Reference
nav_order: 2
layout: default
---

# API Reference

This is a lookup reference for DOFLinx `.MAME` files. Use it alongside the task-based documentation when you know which section, key, trigger, parser, or action you need.

## File-Level Directives

| Directive | Format | Purpose |
|---|---|---|
| `USES` | `USES=<rom>` | Process another ROM's `.MAME` file instead of duplicating configuration. Commonly used by clone ROMs. |
| `MAME_FBNEO_OFFSET` | `MAME_FBNEO_OFFSET=<enabled>,<offset>,<from>,<to>[,<from>,<to>,<base>]` | Translate address ranges for FBNeo-style memory layout differences. |

## Sections

| Section | Purpose | Typical Contents |
|---|---|---|
| `[STARTUP]` | Runs when the game starts. | Button colours, lit-button changes, key mappings, startup effects. |
| `[SHUTDOWN]` | Runs when the game stops. | Cleanup for mappings, lights, and game-specific setup. |
| `[COMMANDS]` | Maps discrete MAME outputs or command names to actions. | `trigger\|state\|action` lines. |
| `[CLEAR COMMANDS]` | Removes command mappings loaded earlier. | One trigger name per line. |
| `[SCORE]` | Defines memory reads, parser rules, and value triggers. | `S1`, `M1`, `CK`, `CKM`, `SC`, `ST`, `A1`, `AM1`, etc. |

## Startup And Shutdown Keys

| Key | Format | Purpose |
|---|---|---|
| `BUTTON_COLOUR_CHANGE` | `BUTTON_COLOUR_CHANGE=<button>,<colour>[,<button>,<colour>...]` | Changes cabinet button colours for this game. |
| `COLOUR_PALETTE` | `COLOUR_PALETTE=<colour>[,<colour>...]` | Defines colours available to random colour effects. |
| `KEY_TO_COMMAND` | `KEY_TO_COMMAND=<button>,<command>` | Emits a named command when a cabinet button changes state. Use an empty value to clear mappings. |
| `FF_DOF` | `FF_DOF=<event>,<duration>` | Fires a DOF event immediately during startup or shutdown. |
| `BUTTONS_LIT_ADDED` | `BUTTONS_LIT_ADDED=<button>[,<button>...]` | Adds buttons to the lit-button set. |
| `BUTTONS_LIT_DELETED` | `BUTTONS_LIT_DELETED=<button>[,<button>...]` | Removes buttons from the lit-button set. |

## Command Lines

```ini
trigger|state|action1|action2|action3
```

| Field | Meaning |
|---|---|
| `trigger` | MAME output name, DOFLinx command name, or custom event name. |
| `state` | Required state/value before actions run, such as `ON` or `OFF`. |
| `action` | One or more DOFLinx actions, evaluated left to right. |

Example:

```ini
led0|ON|FF_Button BUT_P1,BA_ON,0,0|FF_DOF E51,1200
led0|OFF|FF_Button BUT_P1,BA_OFF,0,0
```

## Common Command Triggers

| Trigger | Typical Meaning |
|---|---|
| `led0`, `led1` | MAME lamp or LED output. |
| `coin` | Coin counter/output. |
| `player1`, `player2` | Player state or start output. |
| `pause` | Pause state. |
| `reset` | Reset state. |
| `cheat`, `cheat_status` | Cheat/debug-related output. |
| Custom name | A command emitted by `KEY_TO_COMMAND`, such as `fire`. |

## Actions

Actions use this shape:

```ini
ACTION_NAME parameter1,parameter2,parameter3
```

| Action | Common Format | Purpose |
|---|---|---|
| `FF_DOF` | `FF_DOF E223,-1` | Fires a DOF event. The second value is usually duration in milliseconds; `-1` means default pulse behavior and `0` commonly turns an event off. |
| `FF_Button` | `FF_Button BUT_P1,BA_ON,0,0` | Changes a cabinet button light state. |
| `FF_Colour` | `FF_Colour Blue,RGB_TT,1500` | Sets a named RGB device/toy to a colour. |
| `FF_Flasher` | `FF_Flasher DV_FLCN,FL_TT,1,300,100,Random` | Runs a flasher effect on a configured device. |
| `FF_Dev` | `FF_Dev DV_KN,-1` | Sends a command to a configured output device. |
| `FF_PC` | `FF_PC,U,E,animation/overlay/mameoutput/generic_explosion1` | Triggers PinUP Player or Pixelcade content. |
| `FF_DMD` | `FF_DMD,U,display/picture?path=ingame/explosion1` | Shows media on a DMD/display target. |
| `FF_MSG` | `FF_MSG <message>` | Sends a text message through DOFLinx. |
| `FF_SSF` | `FF_SSF <sound>` | Plays an SSF sound effect. |
| `FF_RUN` | `FF_RUN <command>` | Runs an external command or program. |

## Memory Read Keys

Memory reads use this shape:

```ini
KEY=device|tag|address_space|address|length
```

Example:

```ini
S1=:maincpu|main|program|83f8|8
```

| Field | Example | Meaning |
|---|---|---|
| `device` | `:maincpu` | MAME device to read from. |
| `tag` | `main` | Device tag/group. |
| `address_space` | `program` | MAME address space. |
| `address` | `83f8` | Hex memory address. |
| `length` | `8` | Number of bytes to read. |

## Read And Parser Key Pairs

| Read Key | Parser Key | Purpose |
|---|---|---|
| `CK` | `CKM` | Game-active/check gate. |
| `DK` | `DKM` | Credits. |
| `PK` | `PKM` | Player/current state. |
| `S1` | `M1` | Player 1 score. |
| `S2` | `M2` | Player 2 score. |
| `L1` | `LM1` | Player 1 lives/ships. |
| `L2` | `LM2` | Player 2 lives/ships. |
| `R1` | `RM1` | Player 1 round/stage/level. |
| `R2` | `RM2` | Player 2 round/stage/level. |
| `H1` | `HM1` | Player 1 hits. |
| `H2` | `HM2` | Player 2 hits. |
| `T1` | `TM1` | Player 1 shots/targets. |
| `T2` | `TM2` | Player 2 shots/targets. |
| `A1`, `A2`, ... | `AM1`, `AM2`, ... | Custom arbitrary values. |

## Check Gate

The check gate prevents score/value processing until a memory value indicates the game is ready.

```ini
CK=:maincpu|main|program|98F2|1
CKM=EQ,01
```

| Check Parser | Meaning |
|---|---|
| `CKM=EQ,<value>` | Process values only when the check value equals `<value>`. |
| `CKM=NEQ,<value>` | Process values only when the check value does not equal `<value>`. |

## Parser Rules

Parser rules normalize raw memory bytes into values that triggers can compare.

```ini
PARSER_KEY=filler,unknown,offset,multiplier,type,direction,label,operator,operator_arg
```

| Field | Example | Meaning |
|---|---|---|
| `filler` | empty | Usually unused. |
| `unknown` | empty | Usually unused. |
| `offset` | `24` | Optional offset/adjustment used by some value formats. |
| `multiplier` | `1`, `10`, `+1` | Multiplies or adjusts the parsed value. |
| `type` | `NUMBER`, `HEX`, `STRING`, `ASCII` | Conversion mode for raw bytes. |
| `direction` | `FORWARD`, `REVERSE` | Byte read order. |
| `label` | `SHIPS`, `CREDITS`, `Hits` | Optional display/substitution label. |
| `operator` | `ADD3COMP` | Optional post-processing operator. |
| `operator_arg` | `50`, `100`, `2` | Optional argument for the operator or parser. |

Common parser values:

| Value | Meaning |
|---|---|
| `NUMBER` | Convert memory bytes as numeric digits. |
| `HEX` | Convert as a hex-coded value. |
| `STRING` | Convert as string-like score bytes. |
| `ASCII` | ASCII conversion mode. |
| `FORWARD` | Read in forward order. |
| `REVERSE` | Read in reverse order. |
| `REVERSE4` | Reverse in 4-byte groups. |
| `EDREVERSE4` | Extended/double reverse 4-byte mode. |
| `2NDEVEN` | Use second/even bytes. |
| `2NDODD` | Use second/odd bytes. |
| `NUMHEX-1` | Numeric hex minus one mode. |
| `ADD3COMP` | Add/compact operator used by some counters. |

## Trigger Families

Most value triggers use one of these suffixes:

| Suffix | Format | Meaning |
|---|---|---|
| `C` | `<prefix>C=min:max:actions` | Runs when the value changes by an amount between `min` and `max`. |
| `T` | `<prefix>T=threshold:actions` | Runs when the value reaches `threshold`. |
| `E` | `<prefix>E=min:max:step:actions` | Runs for a matching event range, with `step` controlling repeated events. |

Examples:

```ini
SC=50:160:FF_DOF E223,-1
ST=30000:FF_DOF E773,1800
SE=80000:80000:10:FF_DOF E781,1800
```

## Trigger Keys

| Trigger | Format | Meaning |
|---|---|---|
| `SC` | `SC=min:max:actions` | Score changed in range. |
| `ST` | `ST=threshold:actions` | Score threshold reached. |
| `SE` | `SE=min:max:step:actions` | Score event with repeat step. |
| `SD` | `SD=delay_ms:actions` | Runs after score activity has been idle for the configured delay. |
| `DC` | `DC=min:max:actions` | Credits changed in range. |
| `DT` | `DT=threshold:actions` | Credits threshold reached. |
| `DE` | `DE=min:max:step:actions` | Credits event with repeat step. |
| `LC1`, `LC2` | `LC#=min:max:actions` | Player lives changed in range. |
| `HC` | `HC=min:max:actions` | Hits changed in range. |
| `HT` | `HT=threshold:actions` | Hits threshold reached. |
| `HE` | `HE=min:max:step:actions` | Hits event with repeat step. |
| `RC` | `RC=min:max:actions` | Round/stage changed in range. |
| `RT` | `RT=threshold:actions` | Round/stage threshold reached. |
| `RE` | `RE=min:max:step:actions` | Round/stage event with repeat step or delay. |
| `TC` | `TC=min:max:actions` | Shots/targets changed in range. |
| `TT` | `TT=threshold:actions` | Shots/targets threshold reached. |
| `TE` | `TE=min:max:step:actions` | Shots/targets event with repeat step. |
| `AC` | `AC=index:min:max:actions` | Custom A-series value changed in range. |
| `AT` | `AT=index:threshold:actions` | Custom A-series value threshold reached. |
| `AE` | `AE=index:min:max:step:actions` | Custom A-series value event with repeat step. |
| `AV` | `AV=index:value:actions` | Custom A-series direct value trigger. |

## Substitutions

Actions can include live value substitutions.

| Token | Meaning |
|---|---|
| `!ROM!` | Current ROM name. |
| `!SHOTS!` | Current shots/targets value. |
| `!HITS!` | Current hits value. |
| `!RATIO!` | Hit/shot ratio. |
| `!ROUND!` | Current round/stage value. |
| `!LIVES!` | Current lives value. |
| `!CREDITS!` | Current credits value. |
| `!PULSE_RES!` | Pulse/result value. |
| `!PREFIX_R!` | Round label prefix. |
| `!PREFIX_L!` | Lives label prefix. |
| `!PREFIX_C!` | Credits label prefix. |
| `!LED_R!` | Current red LED value. |
| `!LED_G!` | Current green LED value. |
| `!LED_B!` | Current blue LED value. |

## Encoded Lines

| Prefix | Meaning |
|---|---|
| `FE=` | Encoded plaintext line decoded before processing. |
| `FD=` | Encoded plaintext line decoded before processing. |
| `FC=` | Encoded plaintext line decoded before processing. |

Plaintext lines are allowed and are usually easier to maintain. See [Encoded Lines](documentation/06-encoded-lines.md) for the decoder algorithm and helper tool.
