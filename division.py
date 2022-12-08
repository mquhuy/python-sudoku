class Division:
    def __init__(self):
        self._cells = []

    def add_cell(self, cell):
        self._cells.append(cell)

    def find_cells_for_values(self):
        make_difference = False
        for value in range(1, 10):
            found = False
            value_cells = []
            for cell in self._cells:
                if found:
                    break
                if cell.value == value:
                    found = True
                if cell.value is not None:
                    continue
                if value in cell.possible_values:
                    value_cells.append(cell)
            if found:
                continue
            if len(value_cells) == 0:
                raise ValueError(f"Cannot find cell for value {value}")
            if len(value_cells) == 1:
                value_cells[0].set_value(value)
                make_difference = True
        return make_difference

