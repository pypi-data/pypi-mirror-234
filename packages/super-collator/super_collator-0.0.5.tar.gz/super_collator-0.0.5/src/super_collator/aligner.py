"""This module implements the aligner."""

import collections
from typing import Tuple, List, Sequence, Optional, Callable


class Data:
    """Private data class for the Needleman-Wunsch+Gotoh sequence aligner."""

    __slots__ = ("score", "m", "p", "q", "prefilled", "backtrack", "backtracked")

    def __init__(self, score: float):
        self.score: float = score
        """The cumulative score up to this square."""
        self.m: float = 0.0
        """The score for this alignment as match."""
        self.p: float = 0.0
        """`P_{m,n}` in [Gotoh1982]_."""
        self.q: float = 0.0
        """`Q_{m,n}` in [Gotoh1982]_."""

        self.backtrack: int | None = 0
        """A copy of the backtracking matrix entry for debugging."""
        self.prefilled: bool = False
        """True if this cell was prefilled."""
        self.backtracked: bool = False
        """True if we actually backtracked through this entry."""

    def arrow(self) -> str:
        """Return the appropriate arrow form."""
        if self.backtrack is None:
            return "⏹"
        if self.backtrack == 0:
            return "↖"
        if self.backtrack < 0:
            return "↑"
        return "←"

    def __str__(self):
        """Return the data as string useful for debugging."""

        return "| {arrow} {self.q: 2.2f} {self.m: 2.2f} {self.p: 2.2f} ".format(
            self=self,
            arrow=self.arrow(),
        )

    def html(self) -> str:
        """Return the data as HTML string useful for debugging."""

        emph = [False, False, False]
        if self.backtrack is not None:
            if self.backtrack == 0:
                emph[0] = True
            elif self.backtrack < 0:
                emph[1] = True
            else:
                emph[2] = True
        klass: List
        cells = []
        for val, klass, em in zip(
            (self.m, self.p, self.q), (["d"], ["p"], ["q"]), emph
        ):  # type: ignore
            klass.append("inner")
            if em:
                klass.append("em")
            kl = " ".join(klass)
            cells.append(f"<td class='{kl}'>{val:2.2f}</td>")
        cells.append(f"<td class='inner arrow'>{self.arrow()}</td>")

        klass = ["outer"]
        if self.prefilled:
            klass.append("prefilled")
        if self.backtracked:
            klass.append("bt")
        kl = " ".join(klass)
        a = [f"<td class='{kl}'><table><tr>"]
        a.extend(cells[:2])
        a.append("</tr><tr>")
        a.extend(cells[2:])
        a.append("</tr></table></td>")
        return "".join(a)

    @staticmethod
    def str_size():
        """Return the size of the string returned by __str__."""
        return len("| ↖ -0.00 -0.00 -0.00 ")


class Aligner:
    r"""A generic Needleman-Wunsch+Gotoh sequence aligner.

    This implementation uses Gotoh's improvements to get `\mathcal{O}(mn)` running time
    and reduce memory requirements to essentially the backtracking matrix only.  In
    Gotoh's technique the gap weight formula must be of the special form `w_k = uk + v`
    (affine gap).  `k` is the gap size, `v` is the gap opening score and `u` the gap
    extension score.

    The aligner is type-agnostic.  When the aligner wants to compare two objects, it
    calls the method :func:`similarity` with both objects as arguments.  This method
    should return the score of the alignment.  The score should increase with the
    desirability of the alignment, but otherwise there are no fixed rules.

    The score must harmonize with the penalties for inserting gaps. If the score for
    opening a gap is -1.0 (the default) then a satisfactory match should return a score
    > 1.0.

    The :func:`similarity` function may consult a PAM or BLOSUM matrix, or compute a
    hamming distance between the arguments.  It may also use auxiliary data like
    Part-of-Speech tags.  In this case the data type aligned could be a dict containing
    the word and the POS-tag.

    .. seealso::

       [NeedlemanWunsch1970]_

       [Gotoh1982]_
    """

    __slots__ = ("open_score", "extend_score", "start_score")

    def __init__(
        self,
        start_score: float = -1.0,
        open_score: float = -1.0,
        extend_score: float = -0.5,
    ):
        self.start_score: float = start_score
        """The gap opening score at the start of the string.
        Set this to 0 to find local alignments."""
        self.open_score: float = open_score
        """The gap opening score `v`."""
        self.extend_score: float = extend_score
        """The gap extension score `u`."""

    def align(
        self,
        seq_a: Sequence[object],
        seq_b: Sequence[object],
        similarity: Callable[[object, object], float],
        gap_a: Optional[Callable[[], object]] = None,
        gap_b: Optional[Callable[[], object]] = None,
    ) -> Tuple[Sequence[object], Sequence[object], float]:
        """Align two sequences.

        :param seq_a: the first sequence to align
        :param seq_b: the second sequence to align
        :param similarity: a callable that returns the similarity of two members
            of seq_a and seq_b
        :param gap_a: insert gap_a() for a gap in sequence a. None inserts None.
        :param gap_b: insert gap_b() for a gap in sequence b. None inserts gap_a().
        :return: the aligned sequences and the score
        """
        return self.align_debug(seq_a, seq_b, similarity, gap_a, gap_b, False)[:3]

    def align_debug(
        self,
        seq_a: Sequence[object],
        seq_b: Sequence[object],
        similarity: Callable[[object, object], float],
        gap_a: Optional[Callable[[], object]] = None,
        gap_b: Optional[Callable[[], object]] = None,
        debug=False,
    ) -> Tuple[Sequence[object], Sequence[object], float, List[List[Data]]]:
        """Align two sequences and return debug information.

        :param seq_a: the first sequence to align
        :param seq_b: the second sequence to align
        :param similarity: a callable that returns the similarity of two members
            of seq_a and seq_b
        :param gap_a: insert gap_a() for a gap in sequence a. None inserts None.
        :param gap_b: insert gap_b() for a gap in sequence b. None inserts gap_a().
        :param debug: calculate debug information if True, debug info wastes memory
        :return: the aligned sequences, the score, and the debug matrix
        """
        gap_b = gap_b or gap_a

        len_a = len(seq_a)
        len_b = len(seq_b)

        back_matrix: List[List[int]] = []  # list[len_a + 1]
        """The backtracking matrix.  0 stands for a match.  A negative integer
        represents a DEL TOP operation.  A positive integer represent an INS LEFT
        operation.  The abs() of the integer is the size of the gap.
        """
        matrix: List[List[Data]] = []
        """The scoring matrix. We need only the last row of the scoring matrix for our
        calculations, so we build the full scoring matrix only while debugging.
        """
        this_back_row: List[int] = []  # list[len_b + 1]
        """The current row of the backtracking matrix."""
        this_row: List[Data] = []  # list[len_b + 1]
        """The current row of the scoring matrix."""

        back_matrix.append(this_back_row)

        # Initialize the first row of the matrix with start and extend scores
        data = Data(0.0)
        data.backtrack = None
        data.prefilled = True
        this_row.append(data)
        this_back_row.append(0)

        for j in range(1, len_b + 1):
            data = Data(self.start_score + (j - 1) * self.extend_score)
            data.p = data.m = data.q = data.score
            data.backtrack = 1
            data.prefilled = True
            this_row.append(data)
            this_back_row.append(j)  # INS LEFT

        if __debug__ and debug:
            matrix = []
            matrix.append(this_row[:])

        # Score the matrix
        for i, a in enumerate(seq_a, start=1):
            # add new back_row to back_matrix
            this_back_row = []
            back_matrix.append(this_back_row)
            this_back_row.append(-i)  # DEL TOP

            diag = this_row[0]
            left = Data(self.start_score + (i - 1) * self.extend_score)
            left.m = left.p = left.q = left.score
            left.backtrack = -1
            left.prefilled = True

            for j, b in enumerate(seq_b, start=1):
                top = this_row[j]
                curr = Data(0.0)

                curr.p = top.score + self.open_score
                if curr.p < top.p + self.extend_score:
                    curr.p = top.p + self.extend_score

                curr.q = left.score + self.open_score
                if curr.q < left.q + self.extend_score:
                    curr.q = left.q + self.extend_score

                curr.m = diag.score + similarity(a, b)

                # Decide which operation is optimal and perform it
                if (curr.m > curr.p) and (curr.m > curr.q):
                    curr.score = curr.m
                    curr.backtrack = 0  # SUBST
                elif curr.q > curr.p:
                    curr.score = curr.q
                    curr.backtrack = 1  # INS LEFT
                else:
                    curr.score = curr.p
                    curr.backtrack = -1  # DEL TOP
                this_back_row.append(curr.backtrack)

                # Advance to next column
                this_row[j - 1] = left
                this_row[j] = curr
                diag = top
                left = curr

            if __debug__ and debug:
                matrix.append(this_row[:])

        # Backtrack and output alignments.

        aligned_a: collections.deque[object] = collections.deque()
        aligned_b: collections.deque[object] = collections.deque()

        i = len_a
        j = len_b
        while (i > 0) or (j > 0):
            if __debug__ and debug:
                matrix[i][j].backtracked = True
            back_m = back_matrix[i][j]
            assert back_m is not None
            if back_m == 0:
                aligned_a.appendleft(seq_a[i - 1])
                aligned_b.appendleft(seq_b[j - 1])
                i -= 1
                j -= 1
            else:
                if back_m < 0:
                    aligned_a.appendleft(seq_a[i - 1])
                    aligned_b.appendleft(gap_b() if gap_b else None)
                    i -= 1
                else:
                    aligned_a.appendleft(gap_a() if gap_a else None)
                    aligned_b.appendleft(seq_b[j - 1])
                    j -= 1

        return aligned_a, aligned_b, this_row[-1].score, matrix
