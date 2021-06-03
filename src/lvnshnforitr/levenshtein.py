from collections import deque
from typing import Callable, Collection, List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


def align(seq1: Sequence[T], seq2: Sequence[T], *,
          insert_cost: int = 1, delete_cost: int = 1, replace_cost: int = 1) \
        -> List[Tuple[Optional[T], Optional[T]]]:
    """
    Align two sequences using Levenshtein distance.
    The two sequences would be aligned using dynamic programming.
    Therefore, it will align in a way that minimizes the Levenshtein Distance from the start.

    Parameters
    ----------
    seq1
    seq2
    insert_cost
    delete_cost
    replace_cost

    Returns
    -------
    alignments : List[Tuple[T, T]]
        An aligned items that minimizes the Levenshtein distance.
        When there is multiple ways to align, only one candidate is returned.
    """
    # Caching the lengths
    len_str1: int = len(seq1)
    len_str2: int = len(seq2)
    # Initialize table. Only dp_table[0, col_idx] and dp_table[row_idx, 0] matters
    dp_table: List[List[int]] = [
        [col_idx * delete_cost + row_idx * insert_cost for col_idx in range(len_str1 + 1)] for row_idx in
        range(len_str2 + 1)
    ]

    dp_index_memo: List[List[Tuple[int, int]]] = [
        [(-1, -1) for _1 in range(len_str1 + 1)] for _2 in range(len_str2 + 1)
    ]

    for col_idx, item1 in enumerate(seq1):
        for row_idx, item2 in enumerate(seq2):
            is_replaced = item1 != item2
            cost_if_inserted: int = dp_table[row_idx][col_idx + 1] + insert_cost
            cost_if_deleted: int = dp_table[row_idx + 1][col_idx] + delete_cost
            cost_if_replaced: int = dp_table[row_idx][col_idx] + replace_cost * int(is_replaced)

            if cost_if_inserted <= cost_if_deleted and cost_if_inserted <= cost_if_replaced:
                dp_table[row_idx + 1][col_idx + 1] = cost_if_inserted
                dp_index_memo[row_idx + 1][col_idx + 1] = (row_idx, col_idx + 1)
            elif cost_if_deleted <= cost_if_inserted and cost_if_deleted <= cost_if_replaced:
                dp_table[row_idx + 1][col_idx + 1] = cost_if_deleted
                dp_index_memo[row_idx + 1][col_idx + 1] = (row_idx + 1, col_idx)
            elif cost_if_replaced <= cost_if_inserted and cost_if_replaced <= cost_if_deleted:
                dp_table[row_idx + 1][col_idx + 1] = cost_if_replaced
                dp_index_memo[row_idx + 1][col_idx + 1] = (row_idx, col_idx)

    alignments_q: deque[Tuple[Optional[T], Optional[T]]] = deque()
    # Caching the method
    align_l_append: Callable[[Tuple[Optional[T], Optional[T]]], None] = alignments_q.appendleft

    col_idx = len_str1
    row_idx = len_str2
    while row_idx > 0 and col_idx > 0:
        print(f"{row_idx}, {col_idx}")
        previous_idx = dp_index_memo[row_idx][col_idx]
        print(previous_idx)
        if previous_idx[0] + 1 == row_idx and previous_idx[1] == col_idx:
            align_l_append((None, seq2[row_idx - 1]))
        elif previous_idx[0] == row_idx and previous_idx[1] + 1 == col_idx:
            align_l_append((seq1[col_idx - 1], None))
        else:
            align_l_append((seq1[col_idx - 1], seq2[row_idx - 1]))
        row_idx, col_idx = previous_idx

    alignments_list: List[Tuple[Optional[T], Optional[T]]] = list(alignments_q)

    if row_idx > 0:
        alignments_list = [(None, item2) for item2 in seq2[:row_idx]] + alignments_list
    elif col_idx > 0:
        alignments_list = [(item1, None) for item1 in seq1[:col_idx]] + alignments_list

    return alignments_list


def distance(str1: Collection[T], str2: Collection[T], *,
             insert_cost: int = 1, delete_cost: int = 1, replace_cost: int = 1) -> int:
    """
    Calculates the Levenshtein distance between Collection objects T using dynamic programming.

    Parameters
    ----------
    str1 : Collection[T]
        Before
    str2 : Collection[T]
        After
    insert_cost
    delete_cost
    replace_cost

    Returns
    -------
    levenshtein_distance : int
        Levenshtein distance between the Collections
    """
    # Caching the lengths
    len_str1: int = len(str1)
    len_str2: int = len(str2)
    # Initialize table. Only dp_table[0, col_idx] and dp_table[row_idx, 0] matters
    dp_table: List[List[int]] = [
        [col_idx * delete_cost + row_idx * insert_cost for col_idx in range(len_str1 + 1)]
        for row_idx in range(len_str2 + 1)
    ]

    for col_idx, item1 in enumerate(str1):
        for row_idx, item2 in enumerate(str2):
            is_replaced = item1 != item2
            dp_table[row_idx + 1][col_idx + 1] = min(
                dp_table[row_idx][col_idx + 1] + insert_cost,
                dp_table[row_idx + 1][col_idx] + delete_cost,
                dp_table[row_idx][col_idx] + replace_cost * int(is_replaced)
            )

    return dp_table[len_str2][len_str1]
