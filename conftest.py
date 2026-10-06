"""Shared pytest fixtures for lab validation.

Each lab folder has a test_lab.py. Tests receive:
  lab    - the imported implementation (starter by default; LAB_IMPL=solution for the reference)
  result - the dict returned by lab.main(), computed once per lab
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from labkit import runner


def _lab_id(request) -> str:
    return Path(request.module.__file__).parent.name[:2]


@pytest.fixture(scope="module")
def lab(request):
    lab_id = _lab_id(request)
    hints = runner.missing_requirements(lab_id)
    if hints:
        pytest.skip("; ".join(hints))
    return runner.load(lab_id, os.environ.get("LAB_IMPL", "starter"))


@pytest.fixture(scope="module")
def result(lab):
    out = lab.main()
    assert isinstance(out, dict), "main() must return a dict of results"
    return out
