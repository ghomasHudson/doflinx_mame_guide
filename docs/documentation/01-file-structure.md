---
title: File Structure
nav_order: 1
parent: Documentation
layout: default
---

# File Structure

DOFLinx loads `.MAME` files when a MAME game starts. The main file is named after the ROM, for example:

```text
MAME/galaga.MAME
MAME/frogger.MAME
MAME/robotron.MAME
```

## Load Order

For a game-specific file, DOFLinx loads these in order:

```text
All_Pre.MAME
<rom>.MAME
All_Post.MAME
```

If no game-specific file exists, DOFLinx can load:

```text
All_Pre.MAME
Default.MAME
All_Post.MAME
```

## Redirect Files

Clone ROMs commonly use another ROM's file via `USES=`:

```ini
USES=galaga
```

This tells DOFLinx to process `galaga.MAME` instead of duplicating the same configuration.

## Sections

Game files commonly contain these sections:

```ini
[STARTUP]
[SHUTDOWN]
[COMMANDS]
[CLEAR COMMANDS]
[SCORE]
```

## `[STARTUP]`

Runs when the game starts. It can contain many normal DOFLinx parameters, plus immediate setup actions.

Example:

```ini
[STARTUP]
BUTTON_COLOUR_CHANGE=BUT_EX,Dodger_Blue,BUT_P1,Orchid,BUT_P2,Pale_Green
COLOUR_PALETTE=White,Red,Blue,Green         # Used for random color requences
KEY_TO_COMMAND=BUT_B1,fire
FF_DOF=E63,-1
BUTTONS_LIT_ADDED=BUT_J1,BUT_B1,BUT_B9
BUTTONS_LIT_DELETED=BUT_P1,BUT_P2
```

## `[SHUTDOWN]`

Runs when the game stops. Use it to undo game-specific button mappings and lighting changes.

Example:

```ini
[SHUTDOWN]
KEY_TO_COMMAND=
BUTTONS_LIT_ADDED=BUT_P1,BUT_P2
BUTTONS_LIT_DELETED=BUT_J1,BUT_B1,BUT_B9
```

## `[COMMANDS]`

Maps MAME output messages or DOFLinx key commands to actions.

Example:

```ini
[COMMANDS]
led0|ON|FF_Button BUT_P1,BA_ON,0,0
led0|OFF|FF_Button BUT_P1,BA_OFF,0,0
fire|ON|FF_DOF E212,-1|FF_DOF E213,-1
```

## `[CLEAR COMMANDS]`

Removes commands that were loaded earlier, usually from `All_Pre.MAME` or another shared file.

Example:

```ini
[CLEAR COMMANDS]
led0
led1
```

## `[SCORE]`

Defines memory reads, value parsers, and triggers based on score or other game state.

Example:

```ini
[SCORE]
S1=:maincpu|main|program|83f8|8
M1=,,24,1,NUMBER,REVERSE
SC=50:160:FF_DOF E223,-1
```

This is the most game-specific section and is covered in detail in the later files.
