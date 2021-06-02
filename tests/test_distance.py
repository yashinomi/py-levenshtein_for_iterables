import unittest
from typing import List, Tuple

from src.lvnshnforitr import levenshtein


class TestDistance(unittest.TestCase):
    def test_str_distance(self):
        test_cases: List[Tuple[str, str, int]] = [
            ('Levenshtein', 'Lenvinsten', 4),
            ('Levenshtein', 'Levensthein', 2),
            ('Levenshtein', 'Levenshten', 1),
            ('Levenshtein', 'Levenshtein', 0)
        ]

        for cor_str, wrg_str, dist in test_cases:
            self.assertEqual(
                levenshtein.distance(cor_str, wrg_str), dist,
                f"Error in case of {cor_str=}, {wrg_str=}, {dist=}"
            )


if __name__ == '__main__':
    unittest.main()
