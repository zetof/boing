import pygame
from pygame.locals import QUIT
import sys

class Theater:
    """
        Class used to build main window of the application, also called theater
        This theater holds the stage (or eventually  multiple stages) and all possible controls that
        influences stage's behaviour
    """


    def __init__(self, width, height, tempo=120, color=(0, 0, 0)):
        """
        Class constructor
        :param width: width of theater window in pixels
        :param height: height of theater window in pixels
        :param tempo: tempo in beats per second (BPM) - sets interval between two notes, not two ticks
        :param color: background color of theater expressed in a RGB triplet
        """

        # Store class properties
        self._width = width
        self._height = height
        self._color = color
        self._tempo = tempo

        # Store different stages added to this theater
        self._stages = []

        # Start pygame engine and init drawing window
        pygame.init()
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("BOING - Automated music generator")

        # Controls main loop refresh rate and tempo
        self._clock = pygame.time.Clock()
        self._delay = 60000 / tempo
        self._next_tick = 0
        self._current_step = 0;

    def _loop(self):
        # Theater main loop

        # This flag is used to keep main loop running
        while self.running:

            # Typical pygame event, controls end of program when closing window
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # When it is time to perform an action
            if self._tick():

                # Look for all stages and trigger changes
                for stage in self._stages:
                    stage.next_tick()

                # Update window display
                pygame.display.update()

            # Set framerate to 60 FPS
            self._clock.tick(60)

    def _tick(self):
        # Keep an eye on elapsed time and return true if it is time to trigger an action
        # A tick is triggered every time the amount of computed delay has been reached

        # Get current time and compare it to stored next time when a tick will occur
        current_time = pygame.time.get_ticks()
        if self._next_tick <= current_time:
            self._next_tick = current_time + self._delay
            return True
        else:
            return False

    def start_performance(self):
        """
        Used to start a performance - set the running flag to True and start main loop

        """
        self.running = True
        self._loop()

    def stop_performance(self):
        """
        Used to stop a performance - set the running flag to False and the main loop will automatically exit
        """
        self.running = False

    def add_stage(self, stage):
        """
        Add a stage to the theater, where instruments can perform
        :param stage: a Stage object
        """
        stage.set_theater(self._window)
        self._stages.append(stage)
