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


if __name__ == '__main__':
    unittest.main()
