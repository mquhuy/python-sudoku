from cell import Cell
from division import Division
from copy import deepcopy

class Board:
    def __init__(self, board):
        self._length = 9
        self.cells = []
        self._solved_cells = 0
        self._n_cells = self._length * self._length
        self._rows = [Division() for _ in range(self._length)]
        self._cols = [Division() for _ in range(self._length)]
        self._zones = [Division() for _ in range(self._length)]
        for row in range(self._length):
            for col in range(self._length):
                number = None
                try:
                    number = int(board[row][col])
                except IndexError:
                    print(row, col)
                except ValueError:
                    pass
                c = Cell(row, col, number)
                self.cells.append(c)
                self._rows[row].add_cell(cell=c)
                self._cols[col].add_cell(cell=c)
                self._zones[c.zone].add_cell(cell=c)
                if number is not None:
                    self._solved_cells += 1
        self._round_difference = True
        self.solutions = []

    def round_solve(self):
        make_difference = False
        for idx in range(self._n_cells):
            c = self.cells[idx]
            # print("New Cell")
            # print(f"Row: {c.row}, Col: {c.col}, Val: {c.value}, Possible values: {c.possible_values}")
            if c.value is not None:
                continue
            for c_other in self.cells:
                if c_other == c:
                    continue
                if c_other.value is None:
                    continue
                if c_other.col == c.col or c_other.row == c.row or c_other.zone == c.zone:
                    if self.cells[idx].remove_possible_value(c_other.value):
                        # print(f"Row: {c_other.row}, Col: {c_other.col}, Val: {c_other.value}")
                        make_difference = True
                        # print(f"Row: {c.row}, Col: {c.col}, Val: {c.value}, Possible values: {c.possible_values}")
                    if self.cells[idx].value is not None:
                        self._solved_cells += 1
        for row in self._rows:
            if row.find_cells_for_values():
                make_difference = True
        for col in self._cols:
            if col.find_cells_for_values():
                make_difference = True
        for zone in self._zones:
            if zone.find_cells_for_values():
                make_difference = True
        return make_difference

    def board_output(self):
        output = []
        idx = 0
        for row in range(self._length):
            line = "|"
            for col in range(self._length):
                if self.cells[idx].value is None:
                    line += " _"
                else:
                    line += f" {self.cells[idx].value}"
                idx += 1
                if col in [2, 5, 8]:
                    line += " |"
            output.append(line)
            if row in [2, 5, 8]:
                output.append("-" * 30)
        return "\n".join(output)

    def has_been_solved(self):
        was_solved = True
        is_solvable = True
        for cell in self.cells:
            if cell.value is None:
                if len(cell.possible_values) == 0:
                    return False, False
                was_solved = False
        return was_solved, True

    def solve(self):
        make_difference = True
        while True:
            make_difference = self.round_solve()
            was_solved, is_solvable = self.has_been_solved()
            if was_solved:
                self.solutions.append(self.board_output())
                return True
            if not is_solvable:
                return False
            if not make_difference:
                break
        possible_values_map = {idx: len(self.cells[idx].possible_values) for idx in range(self._n_cells) if self.cells[idx].value is None}
        sorted_map = sorted(possible_values_map.items(), key=lambda kv:(kv[1], kv[0]))
        idx, _ = sorted_map[0]
        for pos in self.cells[idx].possible_values:
            trial = deepcopy(self)
            trial.cells[idx].set_value(pos)
            if trial.solve():
                self.solutions += trial.solutions
                self.cells = trial.cells
                return True

def parse_board(input):
    lines = input.split("\n")
    lines = [line for line in lines if len(line) == 9]
    return lines


if __name__ == "__main__":
    input = """_7__95___
___8__5_3
__8___9_1
_8___7__9
_1__5__27
4__1___6_
8_1___7__
9_3__6__4
___91__5_"""
    input2 = """
___51____
__1___96_
__4__3__1
___7____2
_7__5__4_
8____6___
5__2__8__
_49___1__
____61___"""
    input3 = """
14-7--5--
7----3---
----2---9
3----4-1-
--4---8--
-8-6----3
5---1----
---5----7
--2--7-56
"""
    input4 = """
1----46--
---3-----
-6------8
----1-9-4
--2---5--
3-7-2----
5------9-
-----5---
--82----7
"""
    board = parse_board(input4)
    b = Board(board)
    b.solve()
    print("Solved: ")
    for solution in b.solutions:
        print(solution)