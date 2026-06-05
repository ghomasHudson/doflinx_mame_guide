#!/usr/bin/env python3
"""Encode/decode DOFLinx MAME obfuscated F-lines.

Examples:
  Decode a file:
    python3 doflinx_mame_codec.py decode MAME/galaga.MAME galaga.decoded.MAME

  Encode plaintext config lines:
    python3 doflinx_mame_codec.py encode galaga.decoded.MAME galaga.encoded.MAME

"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


F_LINE_RE = re.compile(r"^(F[CED])=([0-9A-Fa-f]+)\s*$")

DECODE_REPLACEMENTS = (
    ("QQ-", "K="),
    ("VV-", "M="),
    ("FF-", "1="),
    ("JJ-", "2="),
    ("ZZ+", "0"),
    ("YY+", "1"),
    ("XX+", "2"),
    ("WW+", "3"),
    ("AA+", "4"),
    (":sub", ":maincpu"),
    ("cpu_space", "program"),
)


def decode_line(line: str) -> str:
    """Decode a single FC/FD/FE line, returning plaintext plus newline if present."""
    newline = "\n" if line.endswith("\n") else ""
    raw = line[:-1] if newline else line
    match = F_LINE_RE.match(raw)
    if not match:
        return line

    kind, hex_data = match.groups()
    if len(hex_data) < 2 or len(hex_data) % 2:
        raise ValueError(f"Invalid encoded line: {raw}")

    seed = int(hex_data[:2], 16)
    chars: list[str] = []

    for i, pos in enumerate(range(2, len(hex_data), 2)):
        value = int(hex_data[pos : pos + 2], 16)

        if kind == "FE":
            decoded = value + seed + (i % 15)
        elif kind == "FD":
            decoded = value - seed - (i % 15)
        elif kind == "FC":
            decoded = value - seed + (i % 15)
        else:
            raise ValueError(f"Unsupported encoded kind: {kind}")

        if not 0 <= decoded <= 0x10FFFF:
            raise ValueError(f"Decoded character out of range in line: {raw}")
        chars.append(chr(decoded))

    decoded_line = "".join(chars)
    for old, new in DECODE_REPLACEMENTS:
        decoded_line = decoded_line.replace(old, new)

    return decoded_line + newline


def encode_line(line: str, kind: str = "FE", seed: int = 0) -> str:
    """Encode a single plaintext line as FC/FD/FE."""
    newline = "\n" if line.endswith("\n") else ""
    raw = line[:-1] if newline else line

    if kind not in {"FE", "FD", "FC"}:
        raise ValueError("kind must be FE, FD, or FC")
    if not 0 <= seed <= 255:
        raise ValueError("seed must be 0..255")

    hex_parts = [f"{seed:02X}"]
    for i, char in enumerate(raw):
        value = ord(char)

        if kind == "FE":
            encoded = value - seed - (i % 15)
        elif kind == "FD":
            encoded = value + seed + (i % 15)
        else:  # FC
            encoded = value + seed - (i % 15)

        if not 0 <= encoded <= 255:
            raise ValueError(
                f"Character {char!r} cannot be encoded with {kind} seed {seed}: {raw}"
            )
        hex_parts.append(f"{encoded:02X}")

    return f"{kind}={''.join(hex_parts)}{newline}"


def should_encode(line: str, reencode: bool) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    if stripped.startswith("[") and stripped.endswith("]"):
        return False
    if F_LINE_RE.match(stripped):
        return reencode
    return "=" in stripped


def transform_file(
    mode: str,
    input_path: Path,
    output_path: Path | None,
    kind: str,
    seed: int,
    reencode: bool,
) -> None:
    lines = input_path.read_text(encoding="utf-8", errors="surrogateescape").splitlines(
        keepends=True
    )

    transformed: list[str] = []
    for line in lines:
        if mode == "decode":
            transformed.append(decode_line(line))
        elif mode == "encode":
            if should_encode(line, reencode):
                plain = decode_line(line) if F_LINE_RE.match(line.strip()) else line
                transformed.append(encode_line(plain, kind=kind, seed=seed))
            else:
                transformed.append(line)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    text = "".join(transformed)
    if output_path is None:
        sys.stdout.write(text)
    else:
        output_path.write_text(text, encoding="utf-8", errors="surrogateescape")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Encode/decode DOFLinx MAME FC/FD/FE obfuscated lines."
    )
    parser.add_argument("mode", choices=("encode", "decode"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument(
        "--kind",
        choices=("FE", "FD", "FC"),
        default="FE",
        help="Encoded line type to use in encode mode. Default: FE",
    )
    parser.add_argument(
        "--seed",
        type=lambda value: int(value, 0),
        default=0,
        help="Seed byte for encode mode, decimal or 0xNN. Default: 0",
    )
    parser.add_argument(
        "--reencode",
        action="store_true",
        help="In encode mode, decode and re-encode existing FC/FD/FE lines too.",
    )
    args = parser.parse_args(argv)

    try:
        transform_file(
            args.mode,
            args.input,
            args.output,
            kind=args.kind,
            seed=args.seed,
            reencode=args.reencode,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
