from typing import Collection, List, TypeVar

T = TypeVar("T")


def distance(str1: Collection[T], str2: Collection[T], *,
             insert_cost: int = 1, delete_cost: int = 1, replace_cost: int = 1) -> int:
    dp_table: List[List[int]] = [
        [col_idx + row_idx for col_idx in range(len(str1) + 1)] for row_idx in range(len(str2) + 1)
    ]

    for col_idx, item1 in enumerate(str1):
        for row_idx, item2 in enumerate(str2):
            is_replaced = item1 != item2
            dp_table[row_idx + 1][col_idx + 1] = min(
                dp_table[row_idx][col_idx + 1] + insert_cost,
                dp_table[row_idx + 1][col_idx] + delete_cost,
                dp_table[row_idx][col_idx] + replace_cost * int(is_replaced)
            )

    return dp_table[row_idx + 1][col_idx + 1]
