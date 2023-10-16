""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.aligner import Aligner
from super_collator.super_collator import to_table


class PosToken:
    def __init__(self, s, pos):
        self.s = s
        self.pos = pos

    def __str__(self):
        return self.s

    @staticmethod
    def similarity(a, b):
        return 1.0 if a.pos == b.pos else 0.0


class TestAlign:
    @staticmethod
    def to_string(aligned):
        return " ".join([str(t) for t in aligned])

    def test_align_pos(self):
        aligner = Aligner()

        a = "it/PRP was/VBD a/DT dark/JJ and/CC stormy/JJ night/NN"
        b = "it/PRP is/VBZ a/DT fine/JJ day/NN"

        a = [PosToken(*s.split("/")) for s in a.split()]
        b = [PosToken(*s.split("/")) for s in b.split()]

        c, d, score = aligner.align(
            a, b, PosToken.similarity, lambda: PosToken("-", "")
        )

        # print(to_table(c))  # only visible on test failure
        assert self.to_string(d) == "it is a fine - - day"
