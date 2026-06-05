---
title: DOFLinx MAME File Guide
layout: default
---

# DOFLinx MAME File Guide

This site explains how to write and maintain DOFLinx `.MAME` files for MAME force feedback, cabinet toys, Pixelcade, DMD output, score monitoring, and custom memory-based triggers.

## Contents

1. [File Structure](01-file-structure.md)
2. [Commands And Actions](02-commands-and-actions.md)
3. [Score Memory Mapping](03-score-memory-mapping.md)
4. [Score And Value Triggers](04-score-and-value-triggers.md)
5. [Custom A-Series Values](05-custom-a-series-values.md)
6. [Encoded Lines](06-encoded-lines.md)
7. [Worked Examples](07-worked-examples.md)

## Quick Example

```ini
[SCORE]
S1=:maincpu|main|program|83f8|8
M1=,,24,1,NUMBER,REVERSE

L1=:maincpu|main|program|9820|1
LM1=,,,+1,HEX,REVERSE,SHIPS

SC=50:160:FF_DOF E223,-1
ST=30000:FF_DOF E773,1800
```

This reads player score and ship count from MAME memory, then triggers DOFLinx actions when score changes match configured values.

## Hosting On GitHub Pages

This directory is ready to host with GitHub Pages using the built-in Jekyll renderer.

In your repository settings:

1. Open `Settings`.
2. Open `Pages`.
3. Set `Source` to `Deploy from a branch`.
4. Select your branch.
5. Set the folder to `/docs`.
6. Save.
