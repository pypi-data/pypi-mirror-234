"""Main module."""

from typing import List, Sequence
from super_collator.aligner import Data


def to_string(seq: Sequence, f=str):
    """Convert a sequence of tokens into a string.

    This function calls f(t) on each token t.
    """
    return " ".join([f(t) for t in seq])


def transpose(*sequences):
    """Transpose a matrix."""
    return list(zip(*sequences))


def to_table(*sequences: Sequence[str]):
    """Convert sequences of aligned strings into an ascii table."""
    strings_columnwise = transpose(*sequences)
    column_widths = [max(map(len, col)) for col in strings_columnwise]

    result = []
    for row in sequences:
        for s, length in zip(row, column_widths):
            result.append(f"{str(s):<{length + 1}}")
        result.append("\n")
    return "".join(result)


def to_table_html(id_: str, *sequences: Sequence[str]):
    """Convert sequences of aligned strings into an HTML table."""

    result = [f"<table class='super-collator super-collator-result' id={id_}>"]

    for row in sequences:
        result.append("<tr>")
        for cell in row:
            result.append(f"<td>{str(cell)}</td>")
        result.append("</tr>\n")
    result.append("</table>\n")
    return "".join(result)


def build_debug_matrix(
    matrix: List[List[Data]],
    ts_a: Sequence[object],
    ts_b: Sequence[object],
) -> str:
    """Build a human-readable debug matrix as ASCII table.

    :param matrix: the full scoring matrix
    :param ts_a: the first input sequence
    :param ts_b: the second input sequence
    :return str: the debug matrix as human readable string
    """

    s = []
    w = Data.str_size() - 2
    w1 = max(len(str(a)) for a in ts_a)

    # header row
    headers = [""] + list(ts_b)
    s.append(" " * w1)
    s.append(" ")
    for header in headers:
        s.append(str.format("| {0:{w}s}", str(header), w=w))
    s.append("\n")

    # data rows
    headers = [""] + list(ts_a)
    for header, m in zip(headers, matrix):
        # header column
        s.append(str.format("{0:>{w}s} ", str(header), w=w1))
        # data columns
        for data in m:
            s.append(str(data))
        s.append("\n")
    s.append("\n")

    return "".join(s)


def build_debug_matrix_html(
    matrix: List[List[Data]],
    ts_a: Sequence[object],
    ts_b: Sequence[object],
    id_: str,
) -> str:
    """Build a human-readable debug matrix as HTML table.

    :param matrix: the full scoring matrix
    :param ts_a: the first input sequence
    :param ts_b: the second input sequence
    :param id_: the HTML id for the table
    :return str: the debug matrix as human readable string
    """

    s = [f"<table class='super-collator super-collator-debug-matrix' id={id_}>"]

    # header row
    headers = [""] + list(ts_b)
    s.append("<tr><th/>")
    for header in headers:
        s.append(f"<th class='top'>{header}</th>")
    s.append("</tr>\n")

    # data rows
    headers = [""] + list(ts_a)
    for header, m in zip(headers, matrix):
        # header column
        s.append(f"<tr><th class='left'>{header}</th>")
        # data columns
        for data in m:
            s.append(data.html())
        s.append("</tr>\n")

    s.append("</table>\n")
    return "".join(s)


def html_style():
    """Output a style element for the debug matrix in HTML."""

    return """
    <style>
    table.super-collator              { border-collapse: collapse }
    table.super-collator th,
    table.super-collator td.outer     { border: 1px solid black }
    table.super-collator td.inner     { width: 50%; padding: 0 0.5ex; text-align: right }
    table.super-collator td.prefilled { background-color: #eee }
    table.super-collator td.bt        { background-color: #fdd }
    table.super-collator td.em        { font-weight: bold }
    table.super-collator th           { padding: 0 0.5ex; text-align: right }
    table.super-collator table        { width: 100% }
    table.super-collator-result td    { border: 1px solid black; padding: 0 1ex }
    </style>
    """
