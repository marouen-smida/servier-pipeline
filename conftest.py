"""Pytest configuration to ensure the src/ directory is importable.

This allows tests to import packages using the src/ layout, e.g.::

    from pkg_ex.example import add
"""

from __future__ import annotations

import os
import sys

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
