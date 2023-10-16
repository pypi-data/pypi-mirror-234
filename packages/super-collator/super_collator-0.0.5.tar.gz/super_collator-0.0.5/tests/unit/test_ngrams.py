""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.aligner import Aligner
from super_collator.ngrams import NGrams

N = [1, 2, 3]


class TestNGrams:
    @pytest.mark.parametrize("n", N)
    def test_ngrams_1(self, n):
        a = NGrams().load("hello", n)
        b = NGrams().load("world", n)
        c = NGrams().load("cacao", n)
        if n == 1:
            assert len(a.ngrams) == 4
            assert len(b.ngrams) == 5
            assert len(c.ngrams) == 3
        if n == 2:
            assert len(a.ngrams) == 6
            assert len(b.ngrams) == 6
            assert len(c.ngrams) == 5
        if n == 3:
            assert len(a.ngrams) == 7
            assert len(b.ngrams) == 7
            assert len(c.ngrams) == 7

    @pytest.mark.parametrize(
        "o",
        [("hello", "hello", 1.0), ("hello", "kitty", 0.0), ("hello", "worlo", 4 / 12)],
    )
    def test_ngrams_2(self, o):
        a = NGrams().load(o[0], 2)
        b = NGrams().load(o[1], 2)
        assert NGrams.similarity(a, b) == o[2]

    @pytest.mark.parametrize("n", N)
    def test_ngrams_3(self, n):
        a = NGrams()
        b = NGrams()
        assert NGrams.similarity(a, b) == 0.0
