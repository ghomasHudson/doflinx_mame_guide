---
title: Add A New Game
nav_order: 8
layout: default
---

# Add A New Game

This guide walks through creating a new `.MAME` file from scratch for a ROM that does not already have DOFLinx effects.

## 1. Create The Game File

Create a file named after the MAME ROM name:

```text
MAME/<rom>.MAME
```

Examples:

```text
MAME/galaga.MAME
MAME/frogger.MAME
MAME/robotron.MAME
```

Use the exact ROM name that MAME launches. Clone ROMs can either have their own file or redirect to a parent file with `USES=`.

```ini
USES=galaga
```

## 2. Start With The Basic Sections

A minimal game file usually starts with these sections:

```ini
[STARTUP]

[SHUTDOWN]

[COMMANDS]

[CLEAR COMMANDS]

[SCORE]
```

`[STARTUP]` sets up game-specific lighting, button mappings, and long-running effects. `[SHUTDOWN]` should undo anything that should not carry into the next game.

Use `[CLEAR COMMANDS]` only when this game needs to remove command mappings loaded earlier, such as generic mappings from `All_Pre.MAME` that are wrong for this ROM.

```ini
[STARTUP]
BUTTONS_LIT_ADDED=BUT_J1,BUT_B1
KEY_TO_COMMAND=BUT_B1,fire

[SHUTDOWN]
KEY_TO_COMMAND=
BUTTONS_LIT_DELETED=BUT_J1,BUT_B1
```

## 3. Add Output Commands

If the game exposes MAME outputs such as lamps, LEDs, or coin counters, map them in `[COMMANDS]`.

```ini
[COMMANDS]
led0|ON|FF_Button BUT_P1,BA_ON,0,0
led0|OFF|FF_Button BUT_P1,BA_OFF,0,0
fire|ON|FF_DOF E212,-1
fire|OFF|FF_DOF E212,0
```

Use `KEY_TO_COMMAND` in `[STARTUP]` when you want a cabinet button to trigger a named command such as `fire`.

If a shared file defines a command that should not apply to this game, remove it in `[CLEAR COMMANDS]` before adding any replacement behavior:

```ini
[CLEAR COMMANDS]
led0
led1
```

## 4. Find Memory Values

Use the `[SCORE]` section for memory-backed values. Despite the name, this can include scores, credits, lives, rounds, hits, shots, player state, and custom values.

Launch MAME with the debugger enabled:

```sh
mame 1941 -debug
```

Replace `1941` with the ROM you are working on. The game starts with the debugger window open, which lets you inspect memory while the game is running.

Use debugger cheat searches to identify values that change during gameplay. The cheat search works by saving memory values, then filtering candidate locations as those values change.

For credits, start the game, open the debugger, and initialize an unsigned 8-bit search:

```text
cheatinit ub
```

`ub` means unsigned byte, which is a good first search type for small counters such as credits. If the game already has 0 credits, insert one credit, break back into the debugger, and filter candidates to locations now equal to 1:

```text
cheatnext equal,1
```

Insert another credit and filter the remaining candidates to locations now equal to 2:

```text
cheatnext equal,2
```

Repeat with each visible credit change:

```text
cheatnext equal,3
cheatnext equal,4
```

When only a few matches remain, list them:

```text
cheatlist
```

If you filter out the correct address by mistake, undo the last filter:

```text
cheatundo
```

The main cheat debugger commands are:

| Command | Purpose |
|---|---|
| `cheatinit` | Initialize the cheat search over writable RAM. |
| `cheatrange` | Add a selected memory range to the current cheat search. |
| `cheatnext` | Filter candidates by comparing against the previous values. |
| `cheatnextf` | Filter candidates by comparing against the initial values. |
| `cheatlist` | Show current matches or save them to a file. |
| `cheatundo` | Undo the most recent cheat search filter. |

See the MAME cheat debugger reference for the full syntax: [MAME Cheat Debugger Commands](https://docs.mamedev.org/debugger/cheats.html#debugger-command-cheatinit).

Once you identify a candidate address, test it by adding a read line in DOFLinx. The address, device, tag, address space, and length become the memory read fields:

```ini
DK=:maincpu|main|program|99B5|1
```

If the value changes correctly in DOFLinx when the game value changes, keep the mapping. If it is noisy or only works on some screens, keep searching for a more stable location.

Start with one value at a time. A score mapping has a memory read key and a parser key:

```ini
[SCORE]
S1=:maincpu|main|program|83f8|8
M1=,,24,1,NUMBER,REVERSE
```

For non-score values, use the matching key pair:

```ini
DK=:maincpu|main|program|99B5|1
DKM=,,,1,NUMBER,FORWARD,CREDITS

L1=:maincpu|main|program|9820|1
LM1=,,,+1,HEX,REVERSE,SHIPS

A1=:maincpu|main|program|9000|1
AM1=,,,1,HEX,FORWARD,MODE
```

See [Memory Mapping](documentation/03-score-memory-mapping.md) for the read key and parser formats.

## 5. Add Triggers

After a value is being read correctly, add triggers for gameplay events.

```ini
# Small score increase
SC=50:160:FF_DOF E223,-1

# Extra life at 30000
ST=30000:FF_DOF E773,1800

# Credit added
DC=1:1:FF_DOF E700,500

# Player 1 lives changed
LC1=-1:-1:FF_DOF E701,700
```

Start with simple effects and narrow ranges. Once the trigger fires at the right time, add more actions.

See [Score And Value Triggers](documentation/04-score-and-value-triggers.md) for the available trigger types.

## 6. Test In Small Steps

Build the file incrementally:

1. Confirm the game-specific `.MAME` file loads.
2. Add one `[STARTUP]` effect and confirm it appears.
3. Add one `[COMMANDS]` mapping and confirm the output or button command fires.
4. Add one memory read and parser pair.
5. Add one trigger for that value.
6. Repeat for the next value.

If an effect does not fire, simplify the file until only the relevant command, read, parser, and trigger remain.

## 7. Clean Up The Finished File

Before sharing or committing the file:

1. Remove temporary test effects.
2. Keep comments only where they explain useful game behavior.
3. Move shared behavior into `All_Pre.MAME` or `All_Post.MAME` if it applies to multiple games.
4. Use `USES=` for clone ROMs that should share the same configuration.
5. Confirm `[SHUTDOWN]` resets any game-specific button mappings or lighting changes.

Please submit new or improved `.MAME` files to the DOFLinx GitHub repository so the community has one shared set of MAME files: [DOFLinx MAMEV3](https://github.com/DOFLinx/DOFLinx/tree/main/MAMEV3).
