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

class LPD8:
    """
    Class used to interract with MIDI devices
    """

    # Define MIDI message types coming from LPD8
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
            print('LPD8 input device connected...')
        except midi.MidiException:
            self._lpd8_in = None
            print('LPD8 input device not found...')

    def _get_msg_type(self, raw_msg_type):
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
        elif msg_type >= self._CTRL and msg_type <= self._CTRL + 3:
            pygame_event = event.Event(LPD8_Events.LPD8_CTRL, {'pgm': self._program,
                                                               'bank': self._bank,
                                                               'ctrl': msg_action,
                                                               'value': msg_value})
            event.post(pygame_event)

    def get_messages(self):
        """
        Reads MIDI messages from LPD8 if any
        :return:
        """

        # Only perform reading if LPD8 is connected
        if not self._lpd8_in == None:

            # Check there are awaiting messages
            if self._lpd8_in.poll():

                # Read awaiting messages
                midi_events = self._lpd8_in.read(self._buffer_size)

                # Only take last message as reading of a pad should only generate one message within game loop
                # When reading a control knob, we are only interested by last final value if we turn the knob
                # fast in one or another direction
                midi_event = midi_events.pop()

                # Transform this MIDI event into a pygame event for treatment in main loop
                self._treat_midi_event(midi_event)

    def close(self):

        # Only perform closing if LPD8 is connected
        if not self._lpd8_in == None:
            self._lpd8_in.close()
