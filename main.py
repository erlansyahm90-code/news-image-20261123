#!/usr/bin/env python3
"""news-image-20261123: one poster summing up Monday 23 November 2026.

The poster itself (entry.png, shipped in this repo) was rendered offline
from news verified as having happened or first been reported on
23 November 2026: 39 stories, a UTC timeline strip, a world map with
numbered pins, and a DATE CHECK box naming the previous days' big
stories that were deliberately left out.

This program does no rendering at all: it only copies the bundled image
to the output directory, byte for byte, so repeated runs are identical.
Standard library only; no network, no fonts, no image libraries.
"""

import os
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"


def output_dir():
    """Where the harness wants the entry: env override, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(chosen) if chosen else Path("/output")


def main():
    destination = output_dir()
    destination.mkdir(parents=True, exist_ok=True)
    payload = ENTRY.read_bytes()
    (destination / "entry.png").write_bytes(payload)


if __name__ == "__main__":
    main()
