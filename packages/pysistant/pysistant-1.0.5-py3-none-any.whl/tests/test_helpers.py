"""
Tests for pysistant/helpers.py
"""

import os

from pysistant.helpers import Timer

def test_timer():
    timer = Timer(granularity='h')

    assert timer.granularity == 'h'



