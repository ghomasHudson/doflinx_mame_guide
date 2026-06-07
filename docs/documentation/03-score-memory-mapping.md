---
title: Memory Mapping
nav_order: 3
parent: Documentation
layout: default
---

# Memory Mapping

The `[SCORE]` section lets DOFLinx poll MAME memory through the DOFLinx MAME Lua plugin. Despite the section name, these mappings are not limited to scores; they also cover credits, player state, lives, rounds, hits, shots, targets, and custom values.

The plugin reads memory from MAME using fields supplied by DOFLinx:

```text
device | tag | address space | address | length
```

Example:

```ini
S1=:maincpu|main|program|83f8|8
```

This reads 8 bytes from:

```text
device:        :maincpu
tag/group:     main
address space: program
address:       0x83f8
length:        8
```

This can then be parsed and used to trigger in-game effects.

Memory mapping uses two lines for each tracked value:

1. A **memory read key** tells DOFLinx where to read bytes from MAME memory.
2. A **parser key** tells DOFLinx how to turn those raw bytes into a usable value.

The memory read line defines an address in memory for DOFLinx to read:

```ini
DK=:maincpu|main|program|99B5|1
```

This reads 1 byte from `0x99B5`, but the byte still needs to be interpreted. That is what the paired parser line does.

```ini
DKM=,,,1,NUMBER,FORWARD,CREDITS
```

Together, `DK` and `DKM` mean: read the raw credit byte from MAME memory, parse it as a number, read it in forward order, and label the resulting value as credits.

Many of the keys have predefined meanings within DOFLinx (e.g. for scores, credits, lives, etc).

Memory read keys are paired with parser keys by name. For example, `DK` pairs with `DKM`, `S1` pairs with `M1`, and `L1` pairs with `LM1`.

| Read Key | Parser Key | Purpose |
|---|---|---|
| `CK` | `CKM` | Game-active/check value |
| `DK` | `DKM` | Credits |
| `PK` | `PKM` | Player/current state |
| `S1` | *`M1` | Player 1 score |
| `S2` | *`M2` | Player 2 score |
| `L1` | `LM1` | Player 1 lives/ships |
| `L2` | `LM2` | Player 2 lives/ships |
| `R1` | `RM1` | Player 1 round/stage/level |
| `R2` | `RM2` | Player 2 round/stage/level |
| `H1` | `HM1` | Player 1 hits |
| `H2` | `HM2` | Player 2 hits |
| `T1` | `TM1` | Player 1 shots/targets |
| `T2` | `TM2` | Player 2 shots/targets |
| `A1`, `A2`, etc. | `AM1`, `AM2`, etc. | Custom arbitrary values |

## Parser Rule Format

A parser is needed because arcade games do not all store values in the same format. One game may store credits as a simple byte, another may store score digits across several bytes, and another may store values in reverse order or as hex-coded digits.

The parser tells DOFLinx how to normalize the raw memory bytes into the value that triggers can use. Without the parser, DOFLinx may be reading the correct address but still display or compare the wrong value.

Parser rules are comma-separated. The exact fields vary by parser type, but use this form:

```ini
M1=start_byte,end_byte,filler,multiplier,type,direction,label,operator,max_change
```

The field order is start byte, end byte, filler, multiplier/add/subtract, type, direction, label, operator, then maximum change. `max_change` limits how large a value change can be before the change is ignored.

Examples:

```ini
M1=,,24,1,NUMBER,REVERSE
LM1=,,,+1,HEX,REVERSE,SHIPS
HM1=,,,1,HEX,REVERSE,Hits,,50
TM1=,,,1,STRING,FORWARD,Shots,ADD3COMP,2
```

### Parser Types

| Field Value | Meaning |
|---|---|
| `NUMBER` | Convert memory bytes as numeric digits |
| `HEX` | Convert as hex-coded value |
| `STRING` | Convert as string-like score bytes |
| `ASCII` | ASCII conversion mode |
| `FORWARD` | Read in forward order |
| `REVERSE` | Read in reverse order |
| `REVERSE4` | Reverse in 4-byte groups |
| `EDREVERSE4` | Extended/double reverse 4-byte mode |
| `2NDEVEN` | Use second/even bytes |
| `2NDODD` | Use second/odd bytes |
| `NUMHEX-1` | Numeric hex minus one mode |
| `ADD3COMP` | Add/compact value operator used by some shots/hits counters |

Finding the right one may take some trial and error.

## Check Keys

When a game is first booted, lots of values are overwritten while the game memory is initialised. We need some way of preventing things being triggered until the values have settled.

`CK` and `CKM` are used to gate this processing. 

Example:

```ini
CK=:maincpu|main|program|98F2|1     # Defines the value to monitor
CKM=EQ,01                           # Process scores when this value=01
```

This says score processing only should proceed when memory at `0x98F2` equals `0x01`. You can also use `NEQ` to wait till a value is not equal to something (e.g. wait till a memory location is no longer 0).


## FBNeo Translation

There are sometimes memory differences between MAME and FBneo. We can define an offset translation for FBNeo-style address differences:

```ini
MAME_FBNEO_OFFSET=1,0,EFFF,E000
```

or:

```ini
MAME_FBNEO_OFFSET=1,0,8FFF,8000,9800,9FFF,8800
```

Use existing files for the target game or driver family as a guide.
