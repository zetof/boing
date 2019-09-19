from interface.theater import Theater
from interface.stage import Stage
from helpers.instrument import Instrument
from helpers.scale import Scale

THEATER_WIDTH = 400     # Width of main window in pixels
THEATER_HEIGHT = 400    # Height of main window in pixels
STAGE_SIZE = 8          # Number of cells in a border of a square stage
TEMPO = 40              # Tempo in BPM
OSC_URL = '127.0.0.1'   # IP address where to send OSC messages
OSC_PORT = 57120        # Port where to send OSC messages

# Prepare the main window, also called the theater
theater = Theater(THEATER_WIDTH, THEATER_HEIGHT, TEMPO * (STAGE_SIZE - 1))

# Prepare the stage
stage = Stage(2, 2, THEATER_HEIGHT - 4, STAGE_SIZE, OSC_URL, OSC_PORT, seed=3578)

# Build two instruments
xylophone = Instrument('xylophone', 6, 0, 6, motion='RIGHT')
bass = Instrument('bass', 2, 0, 20)

# Prepare two scales
major_penta_x = Scale('MAJOR PENTATONIC',60, STAGE_SIZE)
major_penta_b = Scale('IONIAN',43, STAGE_SIZE)

# Add scales to instruments
xylophone.set_scale(major_penta_x)
bass.set_scale(major_penta_b)

# Add instruments to stage
stage.add_instrument(xylophone)
stage.add_instrument(bass)

# Add stage to theater
theater.add_stage(stage)

# Start playing !!!
theater.start_performance()