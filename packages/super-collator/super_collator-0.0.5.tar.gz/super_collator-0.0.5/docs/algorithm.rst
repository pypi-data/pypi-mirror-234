Collation Algorithm
~~~~~~~~~~~~~~~~~~~

The library uses an enhancement of the Needleman-Wunsch algorithm by Gotoh [Gotoh1982]_.
This section provides a very high level overview of the algorithm.


Phase 1 - Build Table
---------------------

In phase 1 the algorithm builds a table.  For example this is the table built for the
two strings: *the quick brown fox jumps over the lazy dog* and *sick fox is crazy.*

.. raw:: html
   :file: _static/super-collator-phase1.html

Every cell in the table contains three values: `D`, `P`, and `Q`, and an arrow, like this:

.. raw:: html
    :align: center

   <table class='super-collator super-collator-debug-matrix' style="margin-left: auto; margin-right: auto">
   <tr><td class='outer'>
   <table>
     <tr><td class='d inner'>D</td><td class='p inner'>P</td></tr>
     <tr><td class='q inner'>Q</td><td class='inner arrow'>↖</td></tr>
   </table>
   </td>
   </tr>
   </table>

We define the score `S` for each cell as:

.. math::

    S = \max(D, P, Q)

The grayed cells in the first row and first column are initialized using the *gap start*
and *gap extension* penalties.  The numbers for each remaining cell are calculated using
only values from the three cells, to the top-left, the top, and the left, of the current
cell:

.. math::

   D = S_↖ + \mbox{similarity}(word_←, word_↑)

.. math::

   P = \max(S_↑ + openingpenalty, P_↑ + extensionpenalty)

.. math::

   Q = \max(S_← + openingpenalty, Q_← + extensionpenalty)

Finally the arrow in the current cell is set to point to that cell which yielded the
highest of the current cell's `D`, `P`, and `Q` values.


Phase 2 - Backtrack
-------------------

When the table is thus completed, two empty sequences are created.  Then the algorithm
starts backtracking from the last (bottom-right) cell following the arrows until it
reaches the first (top-left) cell.  If the arrow points:

↑
   the word in the row header is added to the first sequence, a hyphen is added to the
   second sequence,
↖
   the word in the row header is added to the first sequence, the word in the column
   header is added to the second sequence,
←
   a hyphen is added to the first sequence, the word in the column header is added to the
   second sequence.

.. raw:: html
   :file: _static/super-collator-phase2.html

Finally the two sequences are reversed and printed.

.. raw:: html
   :file: _static/super-collator-result.html


Parameters
----------

The algorithm can be customized by setting:

- a word comparison (similarity) function,
- the starting gap penalty,
- the gap opening penalty,
- and the gap extension penalty.
