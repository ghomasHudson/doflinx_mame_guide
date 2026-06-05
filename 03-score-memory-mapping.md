---
title: Score Memory Mapping
layout: default
---

# Score Memory Mapping

The `[SCORE]` section lets DOFLinx poll MAME memory through the DOFLinx MAME Lua plugin.

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

## Memory Read Keys

Memory read keys are paired with parser keys.

| Read Key | Parser Key | Purpose |
|---|---|---|
| `CK` | `CKM` | Game-active/check value |
| `DK` | `DKM` | Credits |
| `PK` | `PKM` | Player/current state |
| `S1` | `M1` | Player 1 score |
| `S2` | `M2` | Player 2 score |
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

Parser rules are comma-separated. The exact fields vary by parser type, but shipped files commonly use this shape:

```ini
M1=filler,unknown,offset,multiplier,type,direction,label,operator,operator_arg
```

Examples:

```ini
M1=,,24,1,NUMBER,REVERSE
LM1=,,,+1,HEX,REVERSE,SHIPS
HM1=,,,1,HEX,REVERSE,Hits,,50
TM1=,,,1,STRING,FORWARD,Shots,ADD3COMP,2
```

Useful parser fields seen in the executable and shipped files:

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

## Check Keys

`CK` and `CKM` gate score processing. They are commonly used to ensure the game is active before processing score values.

Example:

```ini
CK=:maincpu|main|program|98F2|1
CKM=EQ,01
```

This says score processing should proceed when memory at `0x98F2` equals `0x01`.

Seen check operators:

```text
EQ
NEQ
```

## Credits

Credits normally use `DK` and `DKM`, then `DC` triggers.

Example:

```ini
DK=:maincpu|main|program|99B5|1
DKM=,,,1,NUMBER,FORWARD,CREDITS
DC=-2:1:FF_PC,U,M,ministats?label=!PREFIX_C!&value=!CREDITS!
```

## MAME FBNeo Offset

Some files define offset translation for FBNeo-style address differences:

```ini
MAME_FBNEO_OFFSET=1,0,EFFF,E000
```

or:

```ini
MAME_FBNEO_OFFSET=1,0,8FFF,8000,9800,9FFF,8800
```

Use existing files for the target game or driver family as a guide.
