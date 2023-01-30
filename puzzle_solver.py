# Joel van der Boom 209668862 intro to cs ex8
from typing import List, Set, Tuple, Optional
import copy


def count_horizontal(horizon_list: List[int], index: int, side: str, max: bool) -> int:
    """counts how much 'seen' values are in the horizon of a index"""
    if max:
        changed_value = -1
    else:
        changed_value = len(horizon_list) + 999
    if side == "LEFT":
        count = 0
        for i in reversed(horizon_list[:index]):
            if i == 1 or i == changed_value:
                count += 1
            else:
                break
        return count
    if side == "RIGHT":
        count = 0
        for i in horizon_list[index:]:
            if i == 1 or i == changed_value:
                count += 1
            else:
                break
        return count
    return 0


def column_to_row(game_list: List[List[int]], index: int) -> List[int]:
    """change column to row to use count horizontal func"""
    new_list = []
    for i in range(len(game_list)):
        new_list.append(game_list[i][index])
    return new_list


def max_seen_cells(picture: List[List[int]], row: int, col: int) -> int:
    """count the max seen cells can be"""
    if picture[row][col] == 0:
        return 0
    horizontal = 0
    vertical = 0
    horizontal += count_horizontal(picture[row], col, 'RIGHT', True)
    horizontal += count_horizontal(picture[row], col, 'LEFT', True)
    vertical_list = column_to_row(picture, col)
    vertical += count_horizontal(vertical_list, row, 'RIGHT', True)
    vertical += count_horizontal(vertical_list, row, 'LEFT', True)
    if horizontal != 0 or vertical != 0:
        return horizontal + vertical - 1
    return horizontal + vertical


def min_seen_cells(picture: List[List[int]], row: int, col: int) -> int:
    """counts the min of seen cells can be"""
    if (picture[row][col] == -1 or picture[row][col] == 0):
        return 0
    horizontal = 0
    vertical = 0
    horizontal += count_horizontal(picture[row], col, 'RIGHT', False)
    horizontal += count_horizontal(picture[row], col, 'LEFT', False)
    vertical_list = column_to_row(picture, col)
    vertical += count_horizontal(vertical_list, row, 'RIGHT', False)
    vertical += count_horizontal(vertical_list, row, 'LEFT', False)
    if horizontal != 0 or vertical != 0:
        return horizontal + vertical - 1
    return horizontal + vertical


def check_constraints(picture: List[List[int]], constraints_set: Set[Tuple[int, int, int]]) -> int:
    """checks if the constraints set is legel or it is exactly good or it is ilegel """
    ret_0 = False
    ret_1 = True
    for i, item in enumerate(constraints_set):
        min_val = min_seen_cells(picture, item[0], item[1])
        max_val = max_seen_cells(picture, item[0], item[1])
        if (min_val != item[2] or max_val != item[2]):
            ret_1 = False  # if the seen value can be only one value return true
        if item[2] < min_val or item[2] > max_val:
            ret_0 = True  # if the value is ok
    if ret_1:
        return 1
    elif ret_0:
        return 0
    else:
        return 2


def solve_puzzle(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> Optional[List[List[int]]]:
    """solve puzzle"""
    picture1 = [[-1 for i in range(m)] for j in range(n)]
    solve = solve_puzzle_helper(constraints_set, picture1, 0, 0)

    return solve


def solve_puzzle_helper(constraints_set: Set[Tuple[int, int, int]], picture: List[List[int]], n: int, m: int) -> \
        Optional[List[List[int]]]:
    """solve puzzle helper- returs the correct solution"""
    picture_copy = copy.deepcopy(picture)

    if n > len(picture) - 1:
        n = 0
        m += 1
        if m > len(picture[0]) - 1:
            return None
    picture_copy[n][m] = 0
    if check_constraints(picture_copy, constraints_set) == 1:
        return picture_copy
    if check_constraints(picture_copy, constraints_set) == 0:
        picture_copy[n][m] = 1
    if check_constraints(picture_copy, constraints_set) == 1:
        return picture_copy
    if check_constraints(picture_copy, constraints_set) == 0:
        return None

    if check_constraints(picture_copy, constraints_set) == 2:
        picture_copy[n][m] = 0
        solve1 = solve_puzzle_helper(constraints_set, picture_copy, n + 1, m)
        if solve1 is not None:
            return solve1
        picture_copy[n][m] = 1
        solve2 = solve_puzzle_helper(constraints_set, picture_copy, n + 1, m)
        return solve2
    return None


def how_many_solutions(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> int:
    """counts the number of legal solutions of constraints set"""
    picture1 = [[-1 for i in range(m)] for j in range(n)]
    x = count_solution(copy.deepcopy(constraints_set), picture1, 0, 0)
    return x


def count_solution(constraints_set: Set[Tuple[int, int, int]], picture: List[List[int]], n: int, m: int) -> int:
    """counts the number of legal solutions of constraints set"""

    picture_copy = copy.deepcopy(picture)
    if n > len(picture) - 1:
        n = 0
        m += 1
        if m > len(picture[0]) - 1:
            if check_constraints(picture_copy, constraints_set) == 1:
                return 1
            else:
                return 0
            if check_constraints(picture_copy, constraints_set) == 0:
                return 0
    picture_copy[n][m] = 0
    x = count_solution(constraints_set, picture_copy, n + 1, m)
    picture_copy[n][m] = 1
    y = count_solution(constraints_set, picture_copy, n + 1, m)
    if x is None and y is None:
        return 0
    return x + y


def generate_puzzle(picture: List[List[int]]) -> Set[Tuple[int, int, int]]:
    """gets all the solutions and returns the min  one"""
    all_values = set()

    for index_r, row in enumerate(picture):
        for index_c, col in enumerate(row):
            all_values.add((index_r, index_c, max_seen_cells(picture, index_r, index_c)))

            if how_many_solutions(all_values, len(picture), len(picture[0])) == 1:
                return _generate_helper(all_values, picture)
    return all_values


def _generate_helper(all_values: Set[Tuple[int, int, int]], picture: List[List[int]]) -> Set[Tuple[int, int, int]]:
    """gets the min solution"""
    lst_of_min = []
    lst = list(copy.deepcopy(all_values))
    for i in range(len(all_values)):
        new_all_values = copy.deepcopy(all_values)
        new_all_values.remove(lst[i])
        lst_of_min.append(new_all_values)

    for j in lst_of_min:
        if check_good(j, len(picture), len(picture[0])):
            save_j = j
            return _generate_helper(copy.deepcopy(save_j), picture)
    return all_values


def check_good(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> bool:
    if how_many_solutions(constraints_set, n, m) == 1:
        return True
    return False
