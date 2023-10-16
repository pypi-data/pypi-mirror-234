""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.aligner import Aligner
from super_collator.ngrams import NGrams
from super_collator.super_collator import to_table


@pytest.fixture
def the_fox():
    return "the quick brown fox jumps over the lazy dog"


class TestMultipleAlign:
    @staticmethod
    def similarity(aa, bb):
        sim = float("-inf")
        for a in aa:
            for b in bb:
                score = NGrams.similarity(a, b)
                if score > sim:
                    sim = score
        return sim

    @staticmethod
    def preprocess(seq):
        return [[NGrams(t).load(t, 3)] for t in seq]

    @staticmethod
    def gap(n: int = 1):
        return [NGrams("-")] * n

    @staticmethod
    def merge(aa, bb):
        return [a + b for a, b in zip(aa, bb)]

    @staticmethod
    def to_string(aligned, n):
        return " ".join(t[n].user_data for t in aligned)

    def test_multiple_align_1(self, the_fox):
        aligner = Aligner()
        aligner.open_score = -0.5
        aligner.start_score = -0.5
        a = self.preprocess(the_fox.split())
        b = self.preprocess("the quick dog".split())
        c = self.preprocess("rumps".split())
        d = self.preprocess("lady".split())

        assert self.to_string(a, 0) == the_fox

        a, b, score = aligner.align(
            a, b, self.similarity, lambda: self.gap(1), lambda: self.gap(1)
        )
        ab = self.merge(a, b)

        assert self.to_string(ab, 0) == the_fox
        assert self.to_string(ab, 1) == "the quick - - - - - - dog"

        ab, c, score = aligner.align(
            ab, c, self.similarity, lambda: self.gap(2), lambda: self.gap(1)
        )
        abc = self.merge(ab, c)

        assert self.to_string(abc, 0) == the_fox
        assert self.to_string(abc, 1) == "the quick - - - - - - dog"
        assert self.to_string(abc, 2) == "- - - - rumps - - - -"

        abc, d, score = aligner.align(
            abc, d, self.similarity, lambda: self.gap(3), lambda: self.gap(1)
        )
        abcd = self.merge(abc, d)

        assert self.to_string(abcd, 0) == the_fox
        assert self.to_string(abcd, 1) == "the quick - - - - - - dog"
        assert self.to_string(abcd, 2) == "- - - - rumps - - - -"
        assert self.to_string(abcd, 3) == "- - - - - - - lady -"
