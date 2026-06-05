# DOFLinx MAME File Documentation

This documentation explains how to write and maintain DOFLinx `.MAME` files.

The `.MAME` files in this DOFLinx package configure what happens when a MAME game starts, stops, sends output messages, or changes memory-backed values such as score, lives, rounds, hits, shots, credits, and custom values.

## Files

- [01 - File Structure](docs/documentation/01-file-structure.md)
- [02 - Commands And Actions](docs/documentation/02-commands-and-actions.md)
- [03 - Memory Mapping](docs/documentation/03-score-memory-mapping.md)
- [04 - Score And Value Triggers](docs/documentation/04-score-and-value-triggers.md)
- [05 - Custom A-Series Values](docs/documentation/05-custom-a-series-values.md)
- [06 - Encoded Lines](docs/documentation/06-encoded-lines.md)
- [07 - Worked Examples](docs/documentation/07-worked-examples.md)
- [API Reference](docs/api-reference.md)
- [08 - Add A New Game](docs/08-add-a-new-game.md)

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
