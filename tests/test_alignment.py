import unittest
from typing import List, Optional, Tuple

from src.lvnshnforitr import levenshtein


class TestAlignment(unittest.TestCase):
    def test_str_alignment(self):
        test_cases: List[Tuple[str, str, List[Tuple[Optional[str], Optional[str]]]]] = [
            ("abc", "adc", [("a", "a"), ("b", "d"), ("c", "c")]),
            ("abcjk", "adck", [("a", "a"), ("b", "d"), ("c", "c"), ("j", None), ("k", "k")]),
            ("abakdj", "abaaakdj", [
                ("a", "a"), ("b", "b"), ("a", "a"), (None, "a"), (None, "a"), ("k", "k"), ("d", "d"), ("j", "j")
            ]),
            ("abaaakdj", "abakdj", [
                ("a", "a"), ("b", "b"), ("a", "a"), ("a", None), ("a", None), ("k", "k"), ("d", "d"), ("j", "j")
            ]),
        ]

        for cor_str, wrg_str, alignment in test_cases:
            self.assertEqual(
                alignment,
                levenshtein.align(cor_str, wrg_str),
                f"Error in case of {cor_str=}, {wrg_str=}, {alignment=}"
            )

    def test_str_all_alignments(self):
        test_cases: List[Tuple[str, str, List[List[Tuple[Optional[str], Optional[str]]]]]] = [
            ("abaaxd", "bax",[
                [("a", None), ("b", "b"), ("a", "a"), ("a", None), ("x", "x"), ("d", None)],
                [("a", None), ("b", "b"), ("a", None), ("a", "a"), ("x", "x"), ("d", None)],
            ])
        ]

        for cor_str, wrg_str, alignment in test_cases:
            self.assertEqual(
                alignment,
                levenshtein.align(cor_str, wrg_str),
                f"Error in case of {cor_str=}, {wrg_str=}, {alignment=}"
            )

    def test_sequence_alignment(self):
        test_cases: List[Tuple[List[int], List[int], List[Tuple[Optional[int], Optional[int]]]]] = [
            ([0, 1, 2], [0, 2], [(0, 0), (1, None), (2, 2)])
        ]

        for cor_item, wrg_item, alignment in test_cases:
            self.assertEqual(
                alignment,
                levenshtein.align(cor_item, wrg_item),
                f"Error in case of {cor_item=}, {wrg_item=}, {alignment=}"
            )


if __name__ == '__main__':
    unittest.main()
