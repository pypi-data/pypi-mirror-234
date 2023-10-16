#!/usr/bin/python3
"""CLI script"""

import argparse
import logging
import sys

import super_collator.aligner
from super_collator.aligner import Aligner
from super_collator.ngrams import NGrams
from super_collator.super_collator import (
    to_table,
    to_table_html,
    build_debug_matrix,
    build_debug_matrix_html,
    html_style,
)


def build_parser(description: str) -> argparse.ArgumentParser:
    """Build the commandline parser."""
    parser = argparse.ArgumentParser(
        description=description,
        # don't wrap my description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        help="increase output verbosity",
        default=0,
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="debug mode",
        default=False,
    )
    parser.add_argument(
        "--html",
        action="store",
        metavar="ID",
        help="output a HTML table with this id",
        default=None,
    )
    parser.add_argument(
        "--style",
        action="store_true",
        help="output the HTML CSS stylesheet",
        default=False,
    )
    parser.add_argument(
        "--start",
        type=float,
        action="store",
        metavar="N",
        help="starting gap penalty",
        default=0.5,
    )
    parser.add_argument(
        "--open",
        type=float,
        action="store",
        metavar="N",
        help="gap opening penalty",
        default=0.5,
    )
    parser.add_argument(
        "--extend",
        type=float,
        action="store",
        metavar="N",
        help="gap extension penalty",
        default=0.2,
    )
    parser.add_argument(
        "inputs",
        metavar="TOKENS",
        type=str,
        nargs="+",
        help="the input strings to process",
    )

    return parser


def preprocess(seq):
    return [[NGrams(t).load(t, 3)] for t in seq]


def similarity(aa, bb):
    sim = float("-inf")
    for a in aa:
        for b in bb:
            score = NGrams.similarity(a, b)
            if score > sim:
                sim = score
    return sim


def merge(aa, bb):
    return [a + b for a, b in zip(aa, bb)]


def merge_strings(aa):
    return [" ".join([b.user_data for b in a]) for a in aa]


def gap(n: int = 1):
    return [NGrams("-")] * n


def extract(aligned, n):
    """Extract the nth sequence."""
    return [t[n].user_data for t in aligned]


def to_string(aligned, n):
    return " ".join(t[n].user_data for t in aligned)


def main():
    parser = build_parser(__doc__)
    args = parser.parse_args()
    if args.style:
        print(html_style())

    aligner = Aligner(-args.start, -args.open, -args.extend)

    a = args.inputs[0].split()
    aa = preprocess(a)
    for inp in args.inputs[1:]:
        b = inp.split()
        bb = preprocess(b)
        aa, bb, _, matrix = aligner.align_debug(
            aa, bb, similarity, lambda: gap(1), lambda: gap(1), args.debug
        )
        if __debug__ and args.debug:
            if args.html:
                print(build_debug_matrix_html(matrix, a, b, args.html))
            else:
                print(build_debug_matrix(matrix, a, b))
            a = merge_strings(aa)
        aa = merge(aa, bb)

    results = []
    for n, inp in enumerate(args.inputs):
        results.append(extract(aa, n))

    if not args.debug:
        if args.html:
            print(to_table_html(args.html, *results))
        else:
            print(to_table(*results))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
