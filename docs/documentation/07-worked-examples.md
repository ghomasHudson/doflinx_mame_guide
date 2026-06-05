---
title: Worked Examples
nav_order: 7
parent: Documentation
layout: default
---

# Worked Examples

## Galaga Score Mapping

Decoded from `MAME/galaga.MAME`:

```ini
[SCORE]
CK=:maincpu|main|program|98F2|1
CKM=EQ,01

DK=:maincpu|main|program|99B5|1
DKM=,,,1,NUMBER,FORWARD,CREDITS

PK=:maincpu|main|program|9840|1
PKM=,,,1,HEX,FORWARD

S1=:maincpu|main|program|83f8|8
M1=,,24,1,NUMBER,REVERSE

S2=:maincpu|main|program|83e3|8
M2=,,24,1,NUMBER,REVERSE

L1=:maincpu|main|program|9820|1
LM1=,,,+1,HEX,REVERSE,SHIPS

R1=:maincpu|main|program|9821|1
RM1=,,,1,HEX,REVERSE,STAGE

H1=:maincpu|main|program|9844|2
HM1=,,,1,HEX,REVERSE,Hits,,50

T1=:maincpu|main|program|9846|2
TM1=,,,1,HEX,REVERSE,Shots,,100

DELAY=5000
```

Triggers:

```ini
# A single ship stationary or in flight
SC=50:160:FF_DOF E223,-1

# Boss Ship in flight
SC=400:400:FF_DOF E514,800|FF_DOF E518,800

# Challenge Stage Perfect
SC=10000:10000:FF_Dev DV_KN,-1|FF_DOF E786,1500

# First New Ship
ST=30000:FF_Dev DV_MC,-1|FF_DOF E773,1800

# Subsequent New Ships
SE=80000:80000:10:FF_Dev DV_MC,-1|FF_DOF E781,1800
```

## Frogger Lives And Score

Decoded from `MAME/frogger.MAME`:

```ini
[SCORE]
CK=:maincpu|main|program|83B3|1
CKM=EQ,01

DK=:maincpu|main|program|83E1|1
DKM=,,,1,NUMBER,FORWARD,CREDITS

S1=:maincpu|main|program|83ED|2
M1=,,24,10,STRING,REVERSE

S2=:maincpu|main|program|83EB|2
M2=,,24,10,STRING,REVERSE

L1=:maincpu|main|program|83E6|1
LM1=,,,1,HEX,REVERSE,FROGS

L2=:maincpu|main|program|83E5|1
LM2=,,,+1,HEX,REVERSE,FROGS
```

Triggers:

```ini
# A forward step
SC=10:10:FF_DOF E462,200|FF_DOF E465,200

# Frog home
SC=200:999:FF_DOF E505,1100|FF_DOF E507,1100

# End level
SC=1000:3000:FF_DOF E695,1000

# Extra frog
SC=20000:20000:FF_DOF E781,1800
```

## 1942 Level, Hits, And Targets

Decoded from `MAME/1942.MAME`:

```ini
[SCORE]
DK=:maincpu|main|program|E010|2
DKM=,,,1,NUMBER,FORWARD

S1=:maincpu|main|program|E048|8
M1=,,,1,NUMBER,FORWARD

S2=:maincpu|main|program|E050|8
M2=,,,1,NUMBER,FORWARD

L1=:maincpu|main|program|E101|1
LM1=,,,1,HEX,FORWARD,Planes

R1=:maincpu|main|program|E105|1
RM1=,,,+1,HEX,FORWARD,Level

T1=:maincpu|main|program|E15D|3
TM1=,,,1,HEX,REVERSE,Targets

H1=:maincpu|main|program|E14D|3
HM1=,,,1,HEX,REVERSE,Hits
```

Triggers:

```ini
# Planes are 30, 50, 70, 100 and 200
SC=30:30:FF_DOF E225,-1
SC=50:50:FF_DOF E514,800|FF_DOF E518,800
SC=70:70:FF_DOF E510,1000|FF_DOF E512,1000
SC=100:100:FF_DOF E725,1000
SC=200:200:FF_DOF E464,1400

# Bonus points
SC=1000:1500:FF_DOF E574,2000

# Challenge stage bonus
SC=20000:50000:FF_DOF E786,2500
```

## Custom A-Series Example

This is a template for a custom value such as a weapon selector or boss health byte.

```ini
[SCORE]
# Game active check
CK=:maincpu|main|program|98F2|1
CKM=EQ,01

# Custom value 1: weapon selected
A1=:maincpu|main|program|E123|1
AM1=,,,1,HEX,FORWARD,Weapon

# Custom value 2: enemy count
A2=:maincpu|main|program|E140|1
AM2=,,,1,NUMBER,FORWARD,Enemies

# Trigger when weapon reaches value 3
AT=1:3:FF_Flasher DV_FLCN,FL_TT,1,300,100,Blue|FF_DOF E223,300

# Trigger when enemy count changes by 1 through 5
AC=2:1:5:FF_DOF E514,500
```

When building a new file, start with a known working game from the same hardware family, decode it if needed, then change one memory read at a time.
