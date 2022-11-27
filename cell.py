class Cell:
    def __init__(self, row, col, value=None):
        self.row = row
        self.col = col
        self.value = value
        self.possible_values = []
        if value is None:
            self.possible_values = list(range(1, 10))
        self.error = False
        self.zone = -1
        if row <= 2:
            if col <= 2:
                self.zone = 0
            elif col <= 5:
                self.zone = 1
            elif col <= 8:
                self.zone = 2
        elif row <= 5:
            if col <= 2:
                self.zone = 3
            elif col <= 5:
                self.zone = 4
            elif col <= 8:
                self.zone = 5
        elif row <= 8:
            if col <= 2:
                self.zone = 6
            elif col <= 5:
                self.zone = 7
            elif col <= 8:
                self.zone = 8

    def remove_possible_value(self, value: int):
        if self.value is not None:
            return False
        if value not in self.possible_values:
            return False
        if len(self.possible_values) == 1:
            self.set_value(self.possible_values[0])
        elif len(self.possible_values) == 0:
            raise ValueError(f"There is no possible values for row {self.row}, col {self.col}")
        self.possible_values.remove(value)
        return True

    def set_value(self, value: int):
        self.value = value
        self.possible_values = [value]