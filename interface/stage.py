import pygame
from random import seed as set_seed
from .osc_client import Osc_client

class Stage:
    """
    Class used to build a stage, a place where instruments can perform
    A stage to
    """

    def __init__(self, x, y, width, size,
                 osc_url, osc_port,
                 seed=None,
                 border_color=(255, 255, 255), background_color=(0, 0, 0), padding=10):
        """
        Class constructor
        :param x: x position in pixels of the upper left corner on theater window
        :param y: y position in pixels of the upper left corner on theater window
        :param width: width in pixels of stage
        :param size: size in cells of stage
        :param osc_url: URL used to reach OSC listener
        :param osc_port: port used to reach OSC listener
        :param seed: a number used to seed random values - may be used to repeat same sequence over and over
        :param border_color: border color of stage as a RGB triplet
        :param background_color: background color of stage as a RGB triplet
        :param padding: padding in pixels between cells
        """
        
        # Store class properties
        self._x = x
        self._y = y
        self._width = width
        self._size = size
        self._osc_url = osc_url
        self._osc_port = osc_port
        self._seed = seed
        self._border_color = border_color
        self._background_color = background_color
        self._padding = padding

        # Store different instruments added to this stage
        self._instruments = []

        # Compute cell width in pixels (we don't round to avoid calculation errors - is done further
        self._cell_width = width / size - padding / 2

        # Initiate OSC client
        self._osc_client = Osc_client()

        # Initialize random seed for eventual reproducibility
        set_seed(seed)

    def _draw_cell(self, col, line, color):
        # Draw a cell at a given column and line in specified color

        # Compute x and y pixel position based on line and column attributes and draw cell in specified color
        x = self._x + self._padding / 2 + int(line * (self._cell_width + self._padding / 2))
        y = self._y + self._padding / 2 + int(col * (self._cell_width + self._padding / 2))

        # Display cell
        pygame.draw.rect(self.window, color, (x, y, self._cell_width - self._padding / 2, self._cell_width - self._padding / 2))

    def _draw_all(self):
        # Draw whole stage

        # Clear stage in background color and draw border
        pygame.draw.rect(self.window, self._background_color, (self._x, self._y, self._width, self._width))
        pygame.draw.lines(self.window, self._border_color, True, ((self._x, self._y), (self._width, self._y), (self._width, self._y + self._width), (self._x, self._y + self._width)))

        # Loop through all instruments and draw their cells
        for instrument in self._instruments:
            for cell in instrument.get_cells():
                self._draw_cell(cell.get_line(), cell.get_col(), instrument.get_color(cell.get_flash(), cell.get_collide()))

    def _play(self):
        # Prepare OSC messages to be sent to remote synthesiser

        # Loop through all instrumentss
        for instrument in self._instruments:

            # Get scale associated to instrument
            scale = instrument.get_scale()

            # Prepare OSC URL to route to the right synthesiser
            osc_url = instrument.get_name()

            # Prepare an array of notes to be played for this instrument
            # An instrument is only playing when one of its moving cell has reached a border (is so called flashing)
            # Note played is picked from defined scale at position line + column
            osc_notes = []
            for cell in instrument.get_cells():
                if cell.get_flash():
                    osc_notes.append(scale.get_note(cell.get_line() + cell.get_col()))

            # If there are notes to play, send a message to OSC listener
            if osc_notes:
                self._osc_client.send(osc_url, osc_notes)

    def set_theater(self, window):
        """
        Used to associate pygame window object to this instrument for drawing features
        :param window: pygame window holder
        """
        self.window = window

    def add_instrument(self, instrument):
        """
        Add an instrument to stage
        :param instrumet: an Instrument object
        """
        instrument.set_size(self._size)
        self._instruments.append(instrument)

    def next_tick(self):
        """
        Method to be fired when a tick occurs oat theater level
        """
        # Loop through all populations
        for population in self._instruments:
            population.next_tick()

        # Draw whole stage
        self._draw_all()

        # Play notes from cells that have reached an edge
        self._play()