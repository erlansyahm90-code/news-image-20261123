"""Produce the competition entry image.

The artwork itself (entry.png) is generated separately by
build_image.py. This script only locates that file next to itself
and places a copy in the output directory expected by the harness,
so the submitted artifact is exactly the generated poster.
No image bytes are created or altered here; it is a plain copy.
"""

import os
import shutil
import sys


def output_dir():
    """Return the harness output directory, falling back to /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return configured
    return "/output"


def locate_entry():
    """Return the path of entry.png sitting next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def main():
    source = locate_entry()
    if not os.path.isfile(source):
        print("entry.png not found next to main.py: %s" % source,
              file=sys.stderr)
        return 1
    destination_dir = output_dir()
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "entry.png")
    shutil.copyfile(source, destination)
    print("Wrote %s" % destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
