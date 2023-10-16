""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.super_collator import to_string


class TestToString:
    def test_to_string(self):
        a = "the quick dog".split()
        assert to_string(a) == "the quick dog"
        assert to_string(a, str) == "the quick dog"
