from pygame import midi
from pygame import event
from pygame import USEREVENT

class LPD8_Events:
    """
    Class that defines pygame custom events for LPD8
    """
    LPD8_PGM_CHG = USEREVENT + 0
    LPD8_NOTE_ON = USEREVENT + 1
    LPD8_NOTE_OFF = USEREVENT + 2
    LPD8_CTRL = USEREVENT + 3

class LPD8_Ctrl_Knob:

    _MIDI_STEPS = 127
    _MIDI_START = 63
    _TOLERANCE = 3

    def __init__(self, min_value=0, max_value=_MIDI_STEPS, midi_value=_MIDI_START):
        self._min_value = min_value
        self._max_value = max_value
        self.set_value(midi_value, False)

    def set_min_value(self, value):
        self._min_value = value

    def set_max_value(self, value):
        self._max_value = value

    def get_midi_value(self):
        return self._midi_value

    def get_real_value(self):
        return self._real_value

    def set_value(self, midi_value, sticky=True):
        real_value = self._min_value + int((self._max_value - self._min_value) * midi_value / self._MIDI_STEPS)
        if sticky and abs(midi_value - self._midi_value) > self._TOLERANCE:
            real_value = -1
        else:
            self._midi_value = midi_value
            self._real_value = self._min_value + int((self._max_value - self._min_value) * midi_value / self._MIDI_STEPS)
        return real_value


class LPD8_Ctrl_Knob_Array:

    _CTRL_KNOBS = 8

    def __init__(self):

        # Initialize control array
        self._ctrl_knob_array = []
        for pgm in range(4):
            self._ctrl_knob_array.append([])
            for bank in range(8):
                self._ctrl_knob_array[pgm].append([])
                for ctrl in range(self._CTRL_KNOBS):
                    self._ctrl_knob_array[pgm][bank].append(LPD8_Ctrl_Knob())

    def set_value(self, program, bank, knob, midi_value, sticky=True):
        if knob <= self._CTRL_KNOBS:
            return self._ctrl_knob_array[program][bank][knob - 1].set_value(midi_value, sticky)


class LPD8:
    """
    Class used to interract with MIDI devices
    """

    # Define MIDI message types coming from LPD8 (base number in,dependant from chosen program number)
    _PGM_CHG = 192
    _NOTE_ON = 144
    _NOTE_OFF = 128
    _CTRL = 176

    def __init__(self, program=3, bank=0, buffer_size=50):
        """
        Class constructor
        Note that buffer_siez has been set to 50 and is a recommended value for LPD8
        It allows turning control knobs full speed without choking the reader
        :param program: numeric value from 0 to 3 corresponding to choice triggered by PROGRAM key on LPD8
        :param bank: numeric value from 0 to 7  corresponding to choice triggered by PROG/CHNG key on LPD8
        :param buffer_size: MIDI buffer size for read operations
        """

        # Store class properties
        self._program = program
        self._bank = bank
        self._buffer_size = buffer_size

        # Searching for LPD8 in available MIDI devices
        print('starting midi...')
        midi.init()
        nb_of_devices = midi.get_count()
        id = 0
        while id < nb_of_devices:
            infos = midi.get_device_info(id)
            if(infos[1] == b'LPD8' and infos[2] == 1):
                break;
            id += 1
        try:
            self._lpd8_in = midi.Input(id, buffer_size)
            self._ctrl_knob_array = LPD8_Ctrl_Knob_Array()
            print('LPD8 input device connected...')
        except midi.MidiException:
            self._lpd8_in = None
            print('LPD8 input device not found...')

    def _get_msg_type(self, raw_msg_type):
        # Identify message type from MIDI message number
        # MIDI number is always starting from a base number defining message type
        # They come in as message type  base number plus a number ranging from 0 to 3 according to the chosen program
        # This method returns real message type defined in class
        # It also sets program number as no event is triggered on LPD8 when changing this using selector PROGRAM

        msg_type = None
        if raw_msg_type - self._PGM_CHG >= 0:
            self._program = raw_msg_type - self._PGM_CHG
            msg_type = self._PGM_CHG
        elif raw_msg_type - self._CTRL >= 0:
            self._program = raw_msg_type - self._CTRL
            msg_type = self._CTRL
        elif raw_msg_type - self._NOTE_ON >= 0:
            self._program = raw_msg_type - self._NOTE_ON
            msg_type = self._NOTE_ON
        elif raw_msg_type - self._NOTE_OFF >= 0:
            self._program = raw_msg_type - self._NOTE_OFF
            msg_type = self._NOTE_OFF
        return msg_type

    def _treat_midi_event(self, midi_event):
        # Treatment of MIDI message based on message type and associated values
        # Most of the time, it ends up firing a pygame event that will be treated in application main loop

        msg_type = self._get_msg_type(midi_event[0][0])
        msg_action = midi_event[0][1]
        msg_value = midi_event[0][2]
        if msg_type == self._PGM_CHG:
            self._bank = msg_action
            pygame_event = event.Event(LPD8_Events.LPD8_PGM_CHG, {'pgm': self._program,
                                                                 'bank': msg_action})
            event.post(pygame_event)
        elif msg_type == self._NOTE_ON:
            pygame_event = event.Event(LPD8_Events.LPD8_NOTE_ON, {'pgm': self._program,
                                                                 'bank': self._bank,
                                                                 'note': msg_action,
                                                                 'velocity': msg_value})
            event.post(pygame_event)
        elif msg_type == self._NOTE_OFF:
            pygame_event = event.Event(LPD8_Events.LPD8_NOTE_OFF, {'pgm': self._program,
                                                                 'bank': self._bank,
                                                                 'note': msg_action})
            event.post(pygame_event)
        elif msg_type >= self._CTRL:
            msg_value = self._ctrl_knob_array.set_value(self._program, self._bank, msg_action, msg_value)
            if msg_value == -1:
                pass
            else:
                pygame_event = event.Event(LPD8_Events.LPD8_CTRL, {'pgm': self._program,
                                                                   'bank': self._bank,
                                                                   'ctrl': msg_action,
                                                                   'value': msg_value})
                event.post(pygame_event)

    def get_messages(self):
        """
        Read MIDI messages from LPD8 if any and trigger a corresponding pygame event
        """

        # Only perform reading if LPD8 is connected
        if not self._lpd8_in == None:

            # Check there are awaiting messages
            if self._lpd8_in.poll():

                # Read awaiting messages
                midi_events = self._lpd8_in.read(self._buffer_size)

                # Treat message queue
                for midi_event in midi_events:

                    # Transform this MIDI event into a pygame event for treatment in main loop
                    self._treat_midi_event(midi_event)

    def close(self):
        """
        Close MIDI input stream
        """

        # Only perform closing if LPD8 is connected
        if not self._lpd8_in == None:
            self._lpd8_in.close()
