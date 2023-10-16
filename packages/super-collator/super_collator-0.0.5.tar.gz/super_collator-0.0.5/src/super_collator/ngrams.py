"""This module implements the NGrams class."""


class NGrams:
    """A class that compares two strings using N-Grams."""

    def __init__(self, user_data=None):
        self.ngrams = frozenset()
        self.user_data = user_data

    def load(self, s: str, n: int) -> "NGrams":
        """Split a string into N-Grams.

        :param s: the string to split into N-Grams
        :param n: puts the N in N-Grams
        """
        if n == 1:
            self.ngrams = frozenset(list(s))
        else:
            pad = " " * (n - 1)
            sp = pad + s + pad
            self.ngrams = frozenset([sp[i : i + n] for i in range(len(s) + n - 1)])
        return self

    def __str__(self) -> str:
        return str(self.user_data)

    @staticmethod
    def similarity(a: "NGrams", b: "NGrams") -> float:
        """Return similarity between two NGrams objects.

        The similarity score is 2 times the count of common N-Grams divided by the total
        count of N-Grams.
        """
        total = len(a.ngrams) + len(b.ngrams)
        if total == 0:
            return 0.0
        common = len(a.ngrams & b.ngrams)
        return 2 * common / total
