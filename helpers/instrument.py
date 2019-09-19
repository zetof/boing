from random import randrange
from .cell import Cell
from .scale import Scale

class Instrument:
    """
    Class used to define an instrument
    An instrument needs to be put on stage to be able to play
    """

    def __init__(self,  name, max_cells, first_birth, birth_rate, motion='UP', color=None):
        """
        Class constructor
        :param name: name of instrument - this name is used to send OSC messages and acts as a selector for synthesiser
        :param max_cells: maximum number of active cells that may be alive together
        :param first_birth: number of beats before apparition of first cell
        :param birth_rate: number of beats between each new birth of a new cell
        :param motion: how cells move - DOWN, LEFT, UP or RIGHT
        :param color: cell's color as a RGB triplet
        """

        # Saves class properties
        self._name = name
        self._max_cells = max_cells
        self._birth_rate = birth_rate
        self._motion = motion

        # Saves cell's color or pick a random one if none has been given
        if color == None:
            self._color = (randrange(30, 225), randrange(30, 225), randrange(30, 225))
        else:
            self._color = color

        # A population contains a list of living cells
        self._cells = []

        # Initialize population cursor
        # This cursor has to be reached to trigger a new cell birth
        self._cursor = first_birth

    def _move_cursor(self):
        # Decrement cursor and check if it comes to zero
        # In this case, a new cell has to raise and timer is reset for next cell birth

        self._cursor -= 1
        if self._cursor <= 0:
            self._cursor = self._birth_rate
            self._add_cell()

    def _move_cells(self):
        # Move all cells making up the instrument

        for cell in self._cells:
            cell.move(self._size)

    def _check_collisions(self):
        # Check if some cells collide in cell's collection

        # We go through entire collection, one by one
        start = 0
        for cell_1 in self._cells:

            # And we check from current position against remaining cells in collection
            start += 1
            for cell_2 in self._cells[start:]:

                # If two cells collide, we notify it
                if cell_1.get_collision() == cell_2.get_collision():
                    cell_1.collide()
                    cell_2.collide()

    def _remove_oldest_cell(self):
        # Remove oldest cells as number of cells may not be greater than maximum authorized cells

        self._cells = self._cells[1:]

    def _add_cell(self):
        # Add a new cell to cell's collection
        # A cell may not appear on a spot already occupied by another cell
        # If adding a cell to collection makes it bigger than maximum authorized size, remove oldest cell from collection

        new_cell_ok = False
        while not new_cell_ok:
            line = randrange(0, self._size - 1)
            col = randrange(0, self._size - 1)
            if not self._cells:
                new_cell_ok = True
            else:
                for cell in self._cells:
                    if line == cell.get_line() and col == cell.get_col():
                        new_cell_ok = False
                        break
                    else:
                        new_cell_ok = True
            if new_cell_ok:
                self._cells.append(Cell(line, col, self._motion))
        if len(self._cells) > self._max_cells:
            self._remove_oldest_cell()

    def get_name(self):
        """
        Get instrument's name
        :return: instrument's name
        """

        return self._name

    def get_color(self, flash, collide):
        """
        Get instrument's color
        :param flash: flag that tells if a cell has hit a border during this tick
        :param collide: flag that tells if cell is colliding another
        :return: cell's color, white if flashing, red if colliding, instrument's natural color otherwise
        """

        if flash:
            return (255, 255, 255)
        elif collide:
            return (255, 0, 0)
        else:
            return self._color

    def set_color(self, color):
        """
        Set instrument's color
        :param color: instrument's color as a RGB triplet
        """

        self._color = color

    def add_cell(self, cell):
        """
        Add a cell to instrument
        :param cell: a Cell object
        """

        self._cells.append(cell)

    def get_cells(self):
        """
        Add a cell to instrument
        :param cell: a Cell object
        """

        return self._cells

    def get_scale(self):
        """
        Get instrument's defined range from chosen scale
        If no scale has been defined for this instrument, compute a default one based on MAJOR scale
        :return: instrument's range
        """
        try:
            return self._scale
        except AttributeError:
            print('No scale has been defined for this population. Set it to default one')
            self._scale = Scale(size=self._size)
            return self._scale

    def set_scale(self, scale):
        """
        Set a new scale
        :param scale: a Scale object
        """

        self._scale = scale

    def set_size(self, size):
        """
        Set size in cells of instrument
        :param size: size in cells
        """

        self._size = size

        # cursor and birth rate have to be multiplie by size in cell to reflect real boundaries
        self._cursor *= (size - 1)
        self._birth_rate *= (size - 1)

    def next_tick(self):
        """
        Used to perform all actions during a tick relative to instrument
        """
        self._move_cells()
        self._move_cursor()
        self._check_collisions()