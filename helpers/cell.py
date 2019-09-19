class Cell:
    """
    Class that implement a cell behaviour
    Cells are used in instruments to generate notes based on a sort of cellular automate kind of algorithm
    """

    def __init__(self, line, col, motion):
        """
        Class constructor
        :param line: line where to place new cell
        :param col: column where to place new cell
        :param motion: direction where cell is going to - DOWN, LEFT, UP or RIGHT
        """

        # Saves class properties
        self._line = line
        self._col = col

        # Compute mtion according to motion label
        # L-
        if motion == 'UP':
            self._line_inc = -1
            self._col_inc = 0
        elif motion == 'DOWN':
            self._line_inc = 1
            self._col_inc = 0
        elif motion == 'LEFT':
            self._line_inc = 0
            self._col_inc = -1
        elif motion == 'RIGHT':
            self._line_inc = 0
            self._col_inc = 1
        else:
            self._line_inc = 0
            self._col_inc = 0

        # Tells when cell has to flash when hitting walls or collide
        self._flash = False

        # Used to find and display collisions
        self._collision = 100 * line + col
        self._collide = False

    def get_line(self):
        """
        Get cell's current line number
        :return: line number
        """

        return self._line

    def get_col(self):
        """
        Get cell's current column number
        :return: column number
        """

        return self._col

    def get_flash(self):
        """
        Get cell's flashing state (is it hitting an instrument's border)
        :return: flashing state
        """

        return self._flash

    def get_collision(self):
        """
        Get cell's collision number
        This number is set when moving cell and is addition of hundred times line number and column number
        It gives a unique cell number for each line / column coordinate
        :return: collision number
        """

        return self._collision

    def get_collide(self):
        """
        Get cell's collide state (is it hitting another cell)
        :return: collide state
        """

        return self._collide

    def move(self, size):
        """
        Move cell according to its position, increments, instrument's boundaries and cell's current state
        :param size: instrument's size
        """

        # Compute new line ond column position
        self._line += self._line_inc
        self._col += self._col_inc

        # This was needed for new cells that appear on the border of a pad and go to that direction
        if self._line < 0:
            self._line = 0
        elif self._line == size:
            self._line = size - 1
        elif self._col < 0:
            self._col = 0
        elif self._col == size:
            self._col = size - 1

        # Compute collision number
        self._collision = 100 * self._line + self._col

        # Check if we have reached a low or high border
        if self._line_inc != 0:
            if self._line == 0 or self._line == size - 1:
                self._line_inc = -self._line_inc
                self._flash = True
            else:
                self._flash = False

        # Check if we have reached a left or right border
        elif self._col_inc != 0:
            if self._col == 0 or self._col == size - 1:
                self._col_inc = - self._col_inc
                self._flash = True
            else:
                self._flash = False

        # Reset the collision flag as it has already be treated in previous cursor position
        self._collide = False

    def collide(self):
        """
        Perform cell collision direction and state changes
        """

        # Only perform collide action if this cell has not already been tagged as collided and if it is not flashing
        # Flashing state check has been added because of wrong behaviour at boundaries, especially in corners
        if not self._collide and not self._flash:

            # Change direction
            if self._line_inc != 0:
                self._col_inc = self._line_inc
                self._line_inc = 0;
            else:
                self._line_inc = self._col_inc
                self._col_inc = 0

            # Set thr collision flag for display
            self._collide = True