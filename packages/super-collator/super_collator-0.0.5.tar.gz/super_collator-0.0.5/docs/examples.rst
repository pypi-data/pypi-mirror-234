Examples
========

Install:

.. code-block:: shell

   $ pip install super-collator


Align two strings with relaxed spelling using N-Grams:

.. code-block:: python

   >>> from super_collator.aligner import Aligner
   >>> from super_collator.ngrams import NGrams
   >>> from super_collator.super_collator import to_table

   >>> aligner = Aligner(-0.5, -0.5, -0.5)
   >>> a = "Lorem ipsum dollar amat adipiscing elit"
   >>> b = "qui dolorem ipsum quia dolor sit amet consectetur adipisci velit"
   >>>
   >>> a = [NGrams(s).load(s, 3) for s in a.split()]
   >>> b = [NGrams(s).load(s, 3) for s in b.split()]
   >>>
   >>> a, b, score = aligner.align(a, b, NGrams.similarity, lambda: NGrams("-"))
   >>> print(
   ...     to_table(list(map(str, a)), list(map(str, b)))
   ... )  # doctest: +NORMALIZE_WHITESPACE
   -   Lorem   ipsum -    dollar -   amat -           adipiscing elit
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit


Multiple alignment: We repeatedly align two lists of NGrams against each other.

.. code-block:: python

   >>> from super_collator.aligner import Aligner
   >>> from super_collator.ngrams import NGrams
   >>> from super_collator.super_collator import to_table
   >>>
   >>> def similarity(aa, bb):
   ...     sim = float("-inf")
   ...     for a in aa:
   ...         for b in bb:
   ...             score = NGrams.similarity(a, b)
   ...             if score > sim:
   ...                 sim = score
   ...     return sim
   ...
   >>>
   >>> def merge(aa, bb):
   ...     return [a + b for a, b in zip(aa, bb)]
   ...
   >>>
   >>> aligner = Aligner(-1.0, -0.5, -0.5)
   >>> a = "qui dolorem ipsum quia dolor sit amet consectetur adipisci velit"
   >>> b = "Lorem ipsum adipiscing"
   >>> c = "Lorem dollar amat elit"
   >>>
   >>> a = [[NGrams(s).load(s, 2)] for s in a.split()]
   >>> b = [[NGrams(s).load(s, 2)] for s in b.split()]
   >>> c = [[NGrams(s).load(s, 2)] for s in c.split()]
   >>>
   >>> a, b, score = aligner.align(
   ...     a, b, similarity, lambda: [NGrams("-")], lambda: [NGrams("-")]
   ... )
   >>> ab = merge(a, b)
   >>> ab, c, score = aligner.align(
   ...     ab, c, similarity, lambda: [NGrams("-")] * 2, lambda: [NGrams("-")]
   ... )
   >>> abc = merge(ab, c)
   >>>
   >>> print(
   ...     to_table(*zip(*[[t.user_data for t in nn] for nn in abc]))
   ... )  # doctest: +NORMALIZE_WHITESPACE
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit
   -   Lorem   ipsum -    -      -   -    -           adipiscing -
   -   Lorem   -     -    dollar -   amat -           -          elit


Align two sentences using their part-of-speech tags only:

.. code-block:: python

   >>> from super_collator.aligner import Aligner
   >>> from super_collator.super_collator import to_table
   >>>
   >>> class PosToken:
   ...     def __init__(self, s, pos):
   ...         self.s = s
   ...         self.pos = pos
   ...
   ...     def __str__(self):
   ...         return self.s
   ...
   ...     @staticmethod
   ...     def similarity(a, b):
   ...         return 1.0 if a.pos == b.pos else 0.0
   ...
   >>>
   >>> aligner = Aligner()
   >>> a = "it/PRP was/VBD a/DT dark/JJ and/CC stormy/JJ night/NN"
   >>> b = "it/PRP is/VBZ a/DT fine/JJ day/NN"
   >>>
   >>> a = [PosToken(*s.split("/")) for s in a.split()]
   >>> b = [PosToken(*s.split("/")) for s in b.split()]
   >>>
   >>> c, d, score = aligner.align(a, b, PosToken.similarity, lambda: PosToken("-", ""))
   >>> print(
   ...     to_table(list(map(str, c)), list(map(str, d)))
   ... )  # doctest: +NORMALIZE_WHITESPACE
   it was a dark and stormy night
   it is  a fine -   -      day
