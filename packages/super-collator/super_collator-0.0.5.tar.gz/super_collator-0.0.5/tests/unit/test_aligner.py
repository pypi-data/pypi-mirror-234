""" Simple test. """

# pylint: disable=missing-docstring

import pytest

import super_collator.aligner
from super_collator.aligner import Aligner
from super_collator.ngrams import NGrams
from super_collator.super_collator import (
    to_table,
    to_table_html,
    html_style,
    build_debug_matrix,
    build_debug_matrix_html,
)


@pytest.fixture
def the_fox():
    return "the quick brown fox jumps over the lazy dog"


STRATEGIES = [2, 3]


def to_string(seq, strategy):
    """Convert a sequence of tokens into a string.

    This function calls str() on each token.
    """
    return " ".join([strategy.postprocess(t) or "-" for t in seq])


class TestAlignStrings:
    @staticmethod
    def to_string(aligned):
        return " ".join([str(t or "-") for t in aligned])

    def test_align_1(self, the_fox):
        aligner = Aligner()
        a = the_fox.split()
        b = "the brown dog".split()
        a, b, score = aligner.align(a, b, str.__eq__, lambda: "-")
        assert " ".join(b) == "the - brown - - - - - dog"


@pytest.mark.parametrize("n", STRATEGIES)
class TestAlign:
    @staticmethod
    def preprocess(seq, n):
        return [NGrams(s).load(s, n) for s in seq]

    @staticmethod
    def gap():
        return NGrams("-")

    @staticmethod
    def to_string(seq):
        return " ".join([str(t) for t in seq])

    def test_align_1(self, n, the_fox):
        aligner = Aligner()
        a = self.preprocess(the_fox.split(), n)
        b = self.preprocess("rumps".split(), n)
        a, b, score = aligner.align(a, b, NGrams.similarity, self.gap)
        assert self.to_string(b) == "- - - - rumps - - - -"

    def test_align_2(self, n, the_fox):
        aligner = Aligner()
        a = self.preprocess(the_fox.split(), n)
        b = self.preprocess("the brown dog".split(), n)
        a, b, score = aligner.align(a, b, NGrams.similarity, self.gap)
        assert self.to_string(b) == "the - brown - - - - - dog"

    def test_align_3(self, n, the_fox):
        aligner = Aligner(
            0, 0, 0
        )  # the gap penalties would overwhelm the small similarities
        a = self.preprocess(the_fox.split(), n)
        b = self.preprocess("that ox is crazy".split(), n)
        a, b, score, matrix = aligner.align_debug(
            a, b, NGrams.similarity, self.gap, self.gap, True
        )
        assert self.to_string(b) == "that - - ox is - - crazy -"

        # go for full coverage
        to_table((a, b))
        to_table_html("FakeId", (a, b))
        html_style()
        build_debug_matrix_html(matrix, a, b, "FakeId")
        build_debug_matrix(matrix, a, b)
