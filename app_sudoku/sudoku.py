from random import randrange, choice
from copy import copy


class Square3x3:
    """The class creates base square of sudoku with dimension 3x3"""

    def __init__(self):
        self.squares = [self._get_base_square()]

    def __str__(self):
        square_repr = []
        # converts list to string with dividers
        for square in self.squares:
            for row in square:
                rows_repr = "| "
                for col in row:
                    rows_repr += (str(col) + " ")
                square_repr += [rows_repr]

        num_lines = len(self.squares)
        # returns one square if this is Square3x3 class
        if num_lines == 1:
            return "\n".join(square_repr)
        # for inherits classes, if self.squares has more then one square
        hor_divider = "-" * 25
        full_square_repr = [hor_divider]
        for i in range(num_lines):
            num = i + int(i / 3) * 6
            new_line = square_repr[num] + square_repr[num + 3] + square_repr[num + 6] + "|"
            full_square_repr += [new_line]
            if not (i + 1) % 3:
                full_square_repr += [hor_divider]
        return "\n".join(full_square_repr)

    def __repr__(self):
        return self.__str__()

    def _get_base_square(self):
        """
        Create a array 3x3 with base square numbers from 1 to 9.
        Return a list with nested lists.
        """
        numbers = list(range(1, 10))
        mod_numbers = []
        for i in range(9):
            mod_numbers += [numbers.pop(randrange(len(numbers)))]
        base_square = [
            mod_numbers[:3],
            mod_numbers[3:6],
            mod_numbers[6:],
        ]
        return base_square


class Square3x9(Square3x3):
    """The class increase base square 3x3 to 3x9"""

    def __init__(self):
        super().__init__()
        self._get_horizontals_squares()

    def _get_horizontals_squares(self):
        """Append two squares to base"""
        shear_direction = choice(["bottom", "top"])
        for i in range(2):
            shifted_square = self.shift_square(self.squares[-1], shear_direction)
            new_square = self._horizontal_mixing(shifted_square)
            self.squares += [new_square]

    def _horizontal_mixing(self, square):
        """
        Complicates sudoku.
        Returns a square with mixed values in lines
        """
        mod_square = []
        for line in square:
            mod_line = []
            base_line = copy(line)
            for num in line:
                mod_line += [base_line.pop(randrange(len(base_line)))]
            mod_square += [mod_line]
        return mod_square

    def shift_square(self, square, side="bottom"):
        """
        Return vertical shifted list by one position to 'top' or 'bottom'
        """
        mod_square = []
        if side == "bottom":
            mod_square += [square[-1]]
            mod_square += square[:-1]
        else:
            mod_square += square[1:]
            mod_square += [square[0]]
        return mod_square


class Square9x9(Square3x9):

    def __init__(self):
        super().__init__()
        self._get_squares()
        self.full_square = self._connect_cells()

    def _connect_cells(self):
        """Connects all nine lists of self.squares to two-dimensional list"""
        # connects lists of self.squares to three list of columns
        connected_cols = []
        for col_num in range(3):
            cols = self.squares[col_num::3]
            connected_col = []
            for col in cols:
                connected_col += col
            connected_cols += [connected_col]
        # connects rows of connected_cols. And return two-dimensional list.
        connected_rows = []
        for i in range(9):
            row = []
            for col in connected_cols:
                row += col[i]
            connected_rows += [row]
        return connected_rows

    def _get_squares(self):
        """Increases self.squares 3x9 to 9x9"""
        move_directions = self._get_move_directions()
        for i in range(2):
            order = self._get_changed_order()
            for y in range(3):
                square = copy(self.squares[-3])
                square = self._rotate(square)
                square = self.shift_square(square, move_directions[y])
                square = self._rotate(square)
                square = self._change_order_of_rows(square, order)
                self.squares += [square]

    def _get_move_directions(self):
        """Creates a list with shift directions for three columns"""
        choices = ["bottom", "top"]
        return [choice(choices), choice(choices), choice(choices)]

    def _rotate(self, square):
        """Replaces rows and columns"""
        new_square = []
        square_len = len(square)
        for i in range(square_len):
            new_row = []
            for row in square:
                new_row += [row[i]]
            new_square += [new_row]
        return new_square

    def _get_changed_order(self):
        """
        Сomplicates sudoku.
        Returns a list with queue of rows
        """
        base_order = list(range(3))
        new_order = []
        while base_order:
            index = randrange(len(base_order))
            new_order += [base_order.pop(index)]
        return new_order

    def _change_order_of_rows(self, square, order):
        """Changes the order of rows in square"""
        new_square = []
        for num in order:
            new_square += [square[num]]
        return new_square


class SudokuPlaySquare:

    def set_level(self, level: "easy, medium, hard"):
        """
        Set level of sudoku.
        Levels: easy, medium, hard.
        """
        base_play_square = self._create_play_square(level)
        return base_play_square

    def _create_play_square(self, level: "easy, medium, hard"):
        """Creates play square"""
        base_play_square = self._generate_play_square(level)
        play_square = self._roll_square(base_play_square)
        return play_square

    def _roll_square(self, play_square):
        """
        Converts one-dimensions lists to two-dimensions lists 3x3
        and connect them
        """
        rolled_play_square = []
        for i in range(3):
            square_3x9 = play_square[:3]
            play_square = play_square[3:]
            for t in range(3):
                new_line = []
                for y in range(3):
                    new_line += square_3x9[y][:3]
                    square_3x9[y] = square_3x9[y][3:]
                rolled_play_square += [new_line]
        return rolled_play_square

    def _generate_play_square(self, level: "easy, medium, hard"):
        """Returns a list with a play square for all squares 3x3"""
        nums = self._generate_num_of_digits(level)
        square = self._generate_zero_square()
        num_line = 0
        for num in nums:
            line = list(range(9))
            for i in range(num):
                pop_ind = randrange(len(line))
                non_zero_ind = line.pop(pop_ind)
                square[num_line][non_zero_ind] = 1
            num_line += 1

        return square

    def _generate_num_of_digits(self, level: "easy, medium, hard"):
        """Generates a list with numbers of digits in each sudoku' square 3x3"""
        levels = {
            "easy": [4, 4, 4, 4, 5, 5, 5, 6, 6],
            "medium": [2, 2, 3, 3, 3, 4, 4, 4, 5],
            "hard": [2, 2, 2, 2, 3, 3, 3, 4, 4],
        }
        base_nums = levels[level]
        num_of_digits = []
        for i in range(9):
            r_num = randrange(len(base_nums))
            num_of_digits += [base_nums.pop(r_num)]
        return num_of_digits

    def _generate_zero_square(self):
        """Returns a two-dimensional list 9x9 with zero values"""
        zero_square = []
        for i in range(9):
            zero_line = []
            for y in range(9):
                zero_line += [0]
            zero_square += [zero_line]
        return zero_square


class Sudoku(Square9x9, SudokuPlaySquare):

    def __init__(self, level="easy"):
        super().__init__()
        self.level = level
        self.play_square = self.set_level(level)

    def __repr__(self):
        sudoku_repr = []
        # makes a list with joined rows by string with divide sign "|"
        for row in self.play_square:
            row_repr = "| "
            count = 0
            for i in row:
                count += 1
                row_repr += str(i)
                if count == 3:
                    row_repr += " | "
                    count = 0
                else:
                    row_repr += " "
            sudoku_repr += [row_repr]
        # adds horizontal divide rows in list
        hor_line = "-" * 25
        hor_line_nums = [0, 4, 8, 12]
        for line_num in hor_line_nums:
            sudoku_repr.insert(line_num, hor_line)
        # joins all list' elements in one string
        # and replaces "0" to " "
        str_repr = "\n".join(sudoku_repr)
        str_repr = str_repr.replace("0", " ")
        return str_repr

    def __str__(self):
        return self.__repr__()

    def set_level(self, level):
        self.level = level
        base_play_square = super().set_level(level)
        play_square = []
        for i in range(9):
            play_line = []
            for y in range(9):
                play_line += [self.full_square[i][y] * base_play_square[i][y]]
            play_square += [play_line]
        return play_square
