---
title: Encoded Lines
layout: default
---

# Encoded Lines

Many shipped `.MAME` files contain lines beginning with:

```text
FE=
FD=
FC=
```

These are obfuscated plaintext lines. They are not required. DOFLinx decodes them, then processes the resulting line normally.

This encoded line:

```ini
FE=054140584A464C4B213741373C585C65
```

decodes to:

```ini
FF_ROM=DOFLinx
```

This encoded line:

```ini
FE=03404D4C27336B6C587161545B5F6C526D715A6D69595A5B712D2B38236C20
```

decodes to:

```ini
CK=:maincpu|main|program|98F2|1
```

## Plaintext Is Allowed

You can write the decoded lines directly:

```ini
CK=:maincpu|main|program|98F2|1
CKM=EQ,01
S1=:maincpu|main|program|83f8|8
M1=,,24,1,NUMBER,REVERSE
```

This is usually easier to maintain than encoded lines.

## Codec Script

This package includes a helper script created for this documentation:

```text
doflinx_mame_codec.py
```

Decode a file:

```bash
python3 doflinx_mame_codec.py decode MAME/galaga.MAME galaga.decoded.MAME
```

Encode a file:

```bash
python3 doflinx_mame_codec.py encode galaga.decoded.MAME galaga.encoded.MAME
```

Encode using a specific kind and seed:

```bash
python3 doflinx_mame_codec.py encode galaga.decoded.MAME galaga.encoded.MAME --kind FE --seed 0x03
```

## Decoder Algorithm

The first byte after `FE=`, `FD=`, or `FC=` is a seed. Every following byte is transformed into one character.

Simplified Python decoder:

```python
def decode_f_line(line):
    kind = line[:2]
    hex_data = line[3:]
    seed = int(hex_data[:2], 16)
    out = []

    for i, pos in enumerate(range(2, len(hex_data), 2)):
        value = int(hex_data[pos:pos + 2], 16)

        if kind == "FE":
            char_code = value + seed + (i % 15)
        elif kind == "FD":
            char_code = value - seed - (i % 15)
        elif kind == "FC":
            char_code = value - seed + (i % 15)

        out.append(chr(char_code))

    decoded = "".join(out)

    replacements = {
        "QQ-": "K=",
        "VV-": "M=",
        "FF-": "1=",
        "JJ-": "2=",
        "ZZ+": "0",
        "YY+": "1",
        "XX+": "2",
        "WW+": "3",
        "AA+": "4",
        ":sub": ":maincpu",
        "cpu_space": "program",
    }

    for old, new in replacements.items():
        decoded = decoded.replace(old, new)

    return decoded
```

## Why Keep Encoded Lines?

There is no technical need to keep them encoded for normal use. Encoding may have been used to package or hide internal mappings. For maintainability, plaintext is better.
