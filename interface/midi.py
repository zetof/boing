from pygame import midi

class Midi:
    """
    Class used to interract with MIDI devices
    """

    def __init__(self, buffer_size=10):
        """
        Class constructor
        :param buffer_size: MIDI buffer size fior read operations
        """

        # Store class properties
        self._buffer_size = buffer_size

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

    def get_messages(self):
        if not self._lpd8_in == None:
            if self._lpd8_in.poll():
                midi_events = self._lpd8_in.read(self._buffer_size)
                print(midi_events)

    def close(self):
        if not self._lpd8_in == None:
            self._lpd8_in.close()
