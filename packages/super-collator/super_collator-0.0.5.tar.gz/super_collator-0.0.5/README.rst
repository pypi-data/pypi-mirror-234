==============
Super Collator
==============

.. |py39| image:: docs/_images/badge-py39.svg

.. |py310| image:: docs/_images/badge-py310.svg

.. |py311| image:: docs/_images/badge-py311.svg

.. |py312| image:: docs/_images/badge-py312.svg

.. |pypy39| image:: docs/_images/badge-pypy39.svg

.. |coverage| image:: docs/_images/badge-coverage.svg

|py39| |py310| |py311| |py312| |pypy39| |coverage|

Collates textual sources with relaxed spelling.  Uses Gotoh's variant of the
Needleman-Wunsch sequence alignment algorithm.

.. code-block:: shell

   $ pip install super-collator

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
   >>> print(to_table(list(map(str, a)), list(map(str, b))))  # doctest: +NORMALIZE_WHITESPACE
   -   Lorem   ipsum -    dollar -   amat -           adipiscing elit
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit

Documentation: https://cceh.github.io/super-collator/

PyPi: https://pypi.org/project/super-collator/
