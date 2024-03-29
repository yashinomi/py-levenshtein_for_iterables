# MIT License
#
# Copyright (c) 2021 yashinomi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
    seq1 : Sequence[T]
        Before
    seq2 : Sequence[T]
        After
    insert_cost
    delete_cost
    replace_cost

    Returns
    -------
    alignments : List[Tuple[Optional[T], Optional[T]]]
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
        previous_idx = dp_index_memo[row_idx][col_idx]
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


def align_all(seq1: Sequence[T], seq2: Sequence[T], *,
              insert_cost: int = 1, delete_cost: int = 1, replace_cost: int = 1) \
        -> List[List[Tuple[Optional[T], Optional[T]]]]:
    """
    Align two sequences using Levenshtein distance.
    The two sequences would be aligned using dynamic programming.
    Therefore, it will align in a way that minimizes the Levenshtein Distance from the start.

    Parameters
    ----------
    seq1 : Sequence[T]
        Before
    seq2 : Sequence[T]
        After
    insert_cost
    delete_cost
    replace_cost

    Returns
    -------
    alignments : List[Tuple[Optional[T], Optional[T]]]
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
    # A memo table of the index to trace it back to do DP
    dp_index_memo: List[List[List[Tuple[int, int]]]] = [
        [[] for _1 in range(len_str1 + 1)] for _2 in range(len_str2 + 1)
    ]
    # Do DP
    for col_idx, item1 in enumerate(seq1):
        for row_idx, item2 in enumerate(seq2):
            is_replaced = item1 != item2
            cost_if_inserted: int = dp_table[row_idx][col_idx + 1] + insert_cost
            cost_if_deleted: int = dp_table[row_idx + 1][col_idx] + delete_cost
            cost_if_replaced: int = dp_table[row_idx][col_idx] + replace_cost * int(is_replaced)

            least_possible_cost: int = min(cost_if_inserted, cost_if_deleted, cost_if_replaced)

            if cost_if_inserted == least_possible_cost:
                (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx, col_idx + 1))
            if cost_if_deleted == least_possible_cost:
                (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx + 1, col_idx))
            if cost_if_replaced == least_possible_cost:
                (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx, col_idx))

            dp_table[row_idx + 1][col_idx + 1] = least_possible_cost

    # A memo for tracing back to the root
    alignments_q: deque[Tuple[Optional[T], Optional[T]]] = deque()
    state_stack_for_dfs: List[Tuple[int, int, deque[Tuple[Optional[T], Optional[T]]]]] = []
    # Caching the method
    state_append: Callable[[Tuple[int, int, deque[Tuple[Optional[T], Optional[T]]]]], None] = state_stack_for_dfs.append
    state_append((len_str2, len_str1, alignments_q))

    result: List[List[Tuple[Optional[T], Optional[T]]]] = []

    while state_stack_for_dfs:
        row_idx, col_idx, alignments_q = state_stack_for_dfs.pop()
        if row_idx > 0 and col_idx > 0:
            for previous_idx in dp_index_memo[row_idx][col_idx]:
                alignments_q_next = alignments_q.copy()
                if previous_idx[0] + 1 == row_idx and previous_idx[1] == col_idx:
                    alignments_q_next.appendleft((None, seq2[row_idx - 1]))
                elif previous_idx[0] == row_idx and previous_idx[1] + 1 == col_idx:
                    alignments_q_next.appendleft((seq1[col_idx - 1], None))
                else:
                    alignments_q_next.appendleft((seq1[col_idx - 1], seq2[row_idx - 1]))
                state_stack_for_dfs.append((previous_idx[0], previous_idx[1], alignments_q_next))
        else:
            alignments_list: List[Tuple[Optional[T], Optional[T]]] = list(alignments_q)

            if row_idx > 0:
                alignments_list = [(None, item2) for item2 in seq2[:row_idx]] + alignments_list
            elif col_idx > 0:
                alignments_list = [(item1, None) for item1 in seq1[:col_idx]] + alignments_list

            result.append(alignments_list)

    return result


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


class CustomizedLevenshtein:
    def __init__(self, *,
                 is_equal: Callable[[T, T], bool] = lambda a, b: a == b,
                 insert_cost: Callable[[T], int] = lambda a: 1,
                 delete_cost: Callable[[T], int] = lambda a: 1,
                 replace_cost: Callable[[T, T], int] = lambda a, b: 1
                 ):
        self._is_equal = is_equal
        self._insert_cost = insert_cost
        self._delete_cost = delete_cost
        self._replace_cost = replace_cost

    def align(self, seq1: Sequence[T], seq2: Sequence[T]) -> List[Tuple[Optional[T], Optional[T]]]:
        """
        Align two sequences using Levenshtein distance.
        The two sequences would be aligned using dynamic programming.
        Therefore, it will align in a way that minimizes the Levenshtein Distance from the start.

        Parameters
        ----------
        seq1 : Sequence[T]
            Before
        seq2 : Sequence[T]
            After

        Returns
        -------
        alignments : List[Tuple[Optional[T], Optional[T]]]
            An aligned items that minimizes the Levenshtein distance.
            When there is multiple ways to align, only one candidate is returned.
        """
        # Caching the lengths
        len_str1: int = len(seq1)
        len_str2: int = len(seq2)

        # Caching methods
        delete_cost: Callable[[T], int] = self._delete_cost
        insert_cost: Callable[[T], int] = self._insert_cost
        replace_cost: Callable[[T, T], int] = self._replace_cost
        is_equal: Callable[[T, T], bool] = self._is_equal

        # Initialize table. Only dp_table[0, col_idx] and dp_table[row_idx, 0] matters
        dp_table: List[List[int]] = [
            [
                (col_idx * delete_cost(seq1[col_idx - 1]) if col_idx > 0 else 0)
                + (row_idx * insert_cost(seq2[row_idx - 1] if row_idx > 0 else 0))
                for col_idx in range(len_str1 + 1)
            ]
            for row_idx in range(len_str2 + 1)
        ]

        dp_index_memo: List[List[Tuple[int, int]]] = [
            [(-1, -1) for _1 in range(len_str1 + 1)] for _2 in range(len_str2 + 1)
        ]

        for col_idx, item1 in enumerate(seq1):
            for row_idx, item2 in enumerate(seq2):
                is_replaced = not is_equal(item1, item2)
                cost_if_inserted: int = dp_table[row_idx][col_idx + 1] + insert_cost(item2)
                cost_if_deleted: int = dp_table[row_idx + 1][col_idx] + delete_cost(item1)
                cost_if_replaced: int = dp_table[row_idx][col_idx] + replace_cost(item1, item2) * int(is_replaced)

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
            previous_idx = dp_index_memo[row_idx][col_idx]
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

    def align_all(self, seq1: Sequence[T], seq2: Sequence[T]) -> List[List[Tuple[Optional[T], Optional[T]]]]:
        """
        Align two sequences using Levenshtein distance.
        The two sequences would be aligned using dynamic programming.
        Therefore, it will align in a way that minimizes the Levenshtein Distance from the start.

        Parameters
        ----------
        seq1 : Sequence[T]
            Before
        seq2 : Sequence[T]
            After

        Returns
        -------
        alignments : List[Tuple[Optional[T], Optional[T]]]
            An aligned items that minimizes the Levenshtein distance.
            When there is multiple ways to align, only one candidate is returned.
        """
        # Caching the lengths
        len_str1: int = len(seq1)
        len_str2: int = len(seq2)
        # Caching methods
        delete_cost: Callable[[T], int] = self._delete_cost
        insert_cost: Callable[[T], int] = self._insert_cost
        replace_cost: Callable[[T, T], int] = self._replace_cost
        is_equal: Callable[[T, T], bool] = self._is_equal
        # Initialize table. Only dp_table[0, col_idx] and dp_table[row_idx, 0] matters
        dp_table: List[List[int]] = [
            [
                (col_idx * delete_cost(seq1[col_idx - 1]) if col_idx > 0 else 0)
                + (row_idx * insert_cost(seq2[row_idx - 1] if row_idx > 0 else 0))
                for col_idx in range(len_str1 + 1)
            ]
            for row_idx in range(len_str2 + 1)
        ]
        # A memo table of the index to trace it back to do DP
        dp_index_memo: List[List[List[Tuple[int, int]]]] = [
            [[] for _1 in range(len_str1 + 1)] for _2 in range(len_str2 + 1)
        ]
        # Do DP
        for col_idx, item1 in enumerate(seq1):
            for row_idx, item2 in enumerate(seq2):
                is_replaced = not is_equal(item1, item2)
                cost_if_inserted: int = dp_table[row_idx][col_idx + 1] + insert_cost(item2)
                cost_if_deleted: int = dp_table[row_idx + 1][col_idx] + delete_cost(item1)
                cost_if_replaced: int = dp_table[row_idx][col_idx] + replace_cost(item1, item2) * int(is_replaced)

                least_possible_cost: int = min(cost_if_inserted, cost_if_deleted, cost_if_replaced)

                if cost_if_inserted == least_possible_cost:
                    (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx, col_idx + 1))
                if cost_if_deleted == least_possible_cost:
                    (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx + 1, col_idx))
                if cost_if_replaced == least_possible_cost:
                    (dp_index_memo[row_idx + 1][col_idx + 1]).append((row_idx, col_idx))

                dp_table[row_idx + 1][col_idx + 1] = least_possible_cost

        # A memo for tracing back to the root
        alignments_q: deque[Tuple[Optional[T], Optional[T]]] = deque()
        state_stack_for_dfs: List[Tuple[int, int, deque[Tuple[Optional[T], Optional[T]]]]] = []
        # Caching the method
        state_append: Callable[
            [Tuple[int, int, deque[Tuple[Optional[T], Optional[T]]]]], None] = state_stack_for_dfs.append
        state_append((len_str2, len_str1, alignments_q))

        result: List[List[Tuple[Optional[T], Optional[T]]]] = []

        while state_stack_for_dfs:
            row_idx, col_idx, alignments_q = state_stack_for_dfs.pop()
            if row_idx > 0 and col_idx > 0:
                for previous_idx in dp_index_memo[row_idx][col_idx]:
                    alignments_q_next = alignments_q.copy()
                    if previous_idx[0] + 1 == row_idx and previous_idx[1] == col_idx:
                        alignments_q_next.appendleft((None, seq2[row_idx - 1]))
                    elif previous_idx[0] == row_idx and previous_idx[1] + 1 == col_idx:
                        alignments_q_next.appendleft((seq1[col_idx - 1], None))
                    else:
                        alignments_q_next.appendleft((seq1[col_idx - 1], seq2[row_idx - 1]))
                    state_stack_for_dfs.append((previous_idx[0], previous_idx[1], alignments_q_next))
            else:
                alignments_list: List[Tuple[Optional[T], Optional[T]]] = list(alignments_q)

                if row_idx > 0:
                    alignments_list = [(None, item2) for item2 in seq2[:row_idx]] + alignments_list
                elif col_idx > 0:
                    alignments_list = [(item1, None) for item1 in seq1[:col_idx]] + alignments_list

                result.append(alignments_list)

        return result
