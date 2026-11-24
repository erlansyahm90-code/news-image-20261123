"""Entry program for the news-image-20261123 v2 poster.

The poster itself (entry.png) is rendered offline by build_image.py and
shipped in this repository. This program only finds that file next to
itself and copies it into the harness output directory, so both graded
runs produce byte-identical output. Standard library only, no network.
"""

import os
import shutil
import sys


def _output_dir():
    """Harness output dir: MAKEFUN_OUTPUT_DIR, else /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return configured
    return "/output"


def _entry_path():
    """Path of entry.png sitting beside this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def main():
    source = _entry_path()
    if not os.path.isfile(source):
        print("entry.png missing next to main.py: %s" % source,
              file=sys.stderr)
        return 1
    target_dir = _output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    print("Wrote %s" % target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
