from pythonosc import udp_client

class Osc_client():
    """
    Class used to creat an OSC client to send message to an external synthesiser listening to OSC messages
    """

    def __init__(self, host='127.0.0.1', port=57120):
        """
        Class constructor
        :param host: URL used to reach OSC listener
        :param port: port used to reach OSC listener
        """

        # Initiate OSC client
        self._osc_client = udp_client.SimpleUDPClient(host, port)

    def send(self, url, notes):
        """
        Send an OSC message to a synthesiser listening to OSC messages
        :param url: used to trigger right instrument on synthesiser - most of the time this is instrument's name
        :param notes: an array containing notes to play in midi note format
        """
        if url != '':
            self._osc_client.send_message('/' + url, notes)
