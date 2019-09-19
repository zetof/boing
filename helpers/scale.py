class Scale:
    """
    Class that holds scale's definitions
    A scale is associated to an instrument to make it play with a particular mood
    """

    # Dictionary defining a bunch of well known scales - Stolen from SuperCollider with following script:
    # (
    # s = Scale.names;
    # s.do({arg item;
    # [Scale.all[item].name, Scale.all[item].degrees].postln;
    # });
    # )
    _scales = {
        'AEOLIAN': (0, 2, 3, 5, 7, 8, 10),
        'AHIRBHAIRAV': (0, 1, 4, 5, 7, 9, 10),
        'AJAM': (0, 4, 8, 10, 14, 18, 22),
        'ATHAR KURD': (0, 2, 6, 12, 14, 16, 22),
        'AUGMENTED': (0, 3, 4, 7, 8, 11),
        'AUGMENTED 2': (0, 1, 4, 5, 8, 9),
        'BARTOK': (0, 2, 4, 5, 7, 8, 10),
        'BASTANIKAR': (0, 3, 7, 10, 13, 15, 21),
        'BAYATI': (0, 3, 6, 10, 14, 16, 20),
        'BHAIRAV': (0, 1, 4, 5, 7, 8, 11),
        'CHINESE': (0, 4, 6, 7, 11),
        'CHROMATIC': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        'DIMINISHED': (0, 1, 3, 4, 6, 7, 9, 10),
        'DIMINISHED 2': (0, 2, 3, 5, 6, 8, 9, 11),
        'DORIAN': (0, 2, 3, 5, 7, 9, 10),
        'EGYPTIAN': (0, 2, 5, 7, 10),
        'ENIGMATIC': (0, 1, 4, 6, 8, 10, 11),
        'FARAHFAZA': (0, 4, 6, 10, 14, 16, 20),
        'GONG': (0, 2, 4, 7, 9),
        'HARMONIC MAJOR': (0, 2, 4, 5, 7, 8, 11),
        'HARMONIC MINOR': (0, 2, 3, 5, 7, 8, 11),
        'HEX AEOLIAN': (0, 3, 5, 7, 8, 10),
        'HEX DORIAN': (0, 2, 3, 5, 7, 10),
        'HEX MAJOR 6': (0, 2, 4, 5, 7, 9),
        'HEX MAJOR 7': (0, 2, 4, 7, 9, 11),
        'HEX PHRYGIAN': (0, 1, 3, 5, 8, 10),
        'HEX SUS': (0, 2, 5, 7, 9, 10),
        'HIJAZ': (0, 2, 8, 10, 14, 17, 20),
        'HIJAZ DESCENDING': (0, 2, 8, 10, 14, 16, 20),
        'HIJAZKAR': (0, 2, 8, 10, 14, 16, 22),
        'HINDU': (0, 2, 4, 5, 7, 8, 10),
        'HIRAJOSHI': (0, 2, 3, 7, 8),
        'HUNGARIAN MINOR': (0, 2, 3, 6, 7, 8, 11),
        'HUSSEINI': (0, 3, 6, 10, 14, 17, 21),
        'HUZAM': (0, 3, 7, 9, 15, 17, 21),
        'INDIAN': (0, 4, 5, 7, 10),
        'IONIAN': (0, 2, 4, 5, 7, 9, 11),
        'IRAQ': (0, 3, 7, 10, 13, 17, 21),
        'IWATO': (0, 1, 5, 6, 10),
        'JIAO': (0, 3, 5, 8, 10),
        'JIHARKAH': (0, 4, 8, 10, 14, 18, 21),
        'KARJIGHAR': (0, 3, 6, 10, 12, 18, 20),
        'KIJAZ KAR KURD': (0, 2, 8, 10, 14, 16, 22),
        'KUMAI': (0, 2, 3, 7, 9),
        'Kurd': (0, 2, 6, 10, 14, 16, 20),
        'LEADING WHOLE TONE': (0, 2, 4, 6, 8, 10, 11),
        'LOCRIAN': (0, 1, 3, 5, 6, 8, 10),
        'LOCRIAN MAJOR': (0, 2, 4, 5, 6, 8, 10),
        'LYDIAN': (0, 2, 4, 6, 7, 9, 11),
        'LYDIAN MINOR': (0, 2, 4, 6, 7, 8, 10),
        'MAHUR': (0, 4, 7, 10, 14, 18, 22),
        'MAJOR': (0, 2, 4, 5, 7, 9, 11),
        'MAJOR PENTATONIC': (0, 2, 4, 7, 9),
        'MARVA': (0, 1, 4, 6, 7, 9, 11),
        'MELODIC MAJOR': (0, 2, 4, 5, 7, 8, 10),
        'MELODIC MINOR': (0, 2, 3, 5, 7, 9, 11),
        'MELODIC MINOR DESCENDING': (0, 2, 3, 5, 7, 8, 10),
        'NATURAL MINOR': (0, 2, 3, 5, 7, 8, 10),
        'MINOR PENTATONIC': (0, 3, 5, 7, 10),
        'MIXOLYDIAN': (0, 2, 4, 5, 7, 9, 10),
        'MURASSAH': (0, 4, 6, 10, 12, 18, 20),
        'MUSTAR': (0, 5, 7, 11, 13, 17, 21),
        'NAHAWAND': (0, 4, 6, 10, 14, 16, 22),
        'NAHAWAND DESCENDING': (0, 4, 6, 10, 14, 16, 20),
        'NAIRUZ': (0, 4, 7, 10, 14, 17, 20),
        'NAWA ATHAR': (0, 4, 6, 12, 14, 16, 22),
        'NEAPOLITAN MAJOR': (0, 1, 3, 5, 7, 9, 11),
        'NEAPOLITAN MINOR': (0, 1, 3, 5, 7, 8, 11),
        'NIKRIZ': (0, 4, 6, 12, 14, 18, 20),
        'PARTCH OTONALITY 1': (0, 8, 14, 20, 25, 34),
        'PARTCH OTONALITY 2': (0, 7, 13, 18, 27, 35),
        'PARTCH OTONALITY 3': (0, 6, 12, 21, 29, 36),
        'PARTCH OTONALITY 4': (0, 5, 15, 23, 30, 37),
        'PARTCH OTONALITY 5': (0, 10, 18, 25, 31, 38),
        'PARTCH OTONALITY 6': (0, 9, 16, 22, 28, 33),
        'PARTCH UTONALITY 1': (0, 9, 18, 23, 29, 35),
        'PARTCH UTONALITY 2': (0, 8, 16, 25, 30, 36),
        'PARTCH UTONALITY 3': (0, 7, 14, 22, 31, 37),
        'PARTCH UTONALITY 4': (0, 6, 13, 20, 28, 38),
        'PARTCH UTONALITY 5': (0, 5, 12, 18, 25, 33),
        'PARTCH UTONALITY 6': (0, 10, 15, 21, 27, 34),
        'PELOG': (0, 1, 3, 7, 8),
        'PHRYGIAN': (0, 1, 3, 5, 7, 8, 10),
        'PROMETHEUs': (0, 2, 4, 6, 11),
        'PURVI': (0, 1, 4, 6, 7, 8, 11),
        'RAST': (0, 4, 7, 10, 14, 18, 21),
        'RAST DESCENDING': (0, 4, 7, 10, 14, 18, 20),
        'RITUSEN': (0, 2, 5, 7, 9),
        'ROMANIAN MINOR': (0, 2, 3, 6, 7, 9, 10),
        'SABA': (0, 3, 6, 8, 12, 16, 20),
        'SCRIABIN': (0, 1, 4, 7, 9),
        'SHANG': (0, 2, 5, 7, 10),
        'Shawq afza': (0, 4, 8, 10, 14, 16, 22),
        'SIKAH': (0, 3, 7, 11, 14, 17, 21),
        'SIKAH DESCENDING': (0, 3, 7, 11, 13, 17, 21),
        'SPANISH': (0, 1, 4, 5, 7, 8, 10),
        'SUPER LOCRIAN': (0, 1, 3, 4, 6, 8, 10),
        'SUZNAK': (0, 4, 7, 10, 14, 16, 22),
        'TODI': (0, 1, 3, 6, 7, 8, 11),
        'USHAQ MASHRI': (0, 4, 6, 10, 14, 17, 21),
        'WHOLE TONE': (0, 2, 4, 6, 8, 10),
        'YAKAH': (0, 4, 7, 10, 14, 18, 21),
        'YAKAH DESCENDING': (0, 4, 7, 10, 14, 18, 20),
        'YU': (0, 3, 5, 7, 10),
        'ZAMZAM': (0, 2, 6, 8, 14, 16, 20),
        'ZANJARAN': (0, 2, 8, 10, 14, 18, 20),
        'ZHI': (0, 2, 5, 7, 9),
    }

    def __init__(self, name='MAJOR', base=60, size=9):
        """
        Class constructor
        :param name:
        :param base:
        :param size:
        """

        # Store class properties
        self._name = name
        self._base = base

        # Passed size is equal to stage's size (number of lines or columns)
        # Used size is different. As line's and column's indices are from zero to size - 1
        # A played not is computed as line's position + column's position so derived size is adapted to this
        self._size = 2 * (size - 1)

        # Get instrument's range from base scale and instrument's size
        self._scale = self.set_scale(name, base, self._size)

    def get_scale(self):
        """
        Get instrument's range
        :return: instrument's range
        """
        return self._scale

    def set_scale(self, name, base, size):
        """
        Setes instrument's range
        :param name: name of base scale used to define range
        :param base: starting note of range as a midi note number
        :param size: instrument's size
        :return: instrument's range
        """

        # Initialize instrument's range
        scale = []

        # Try to get base scale degrees
        # If we cannot find base scale, use default MAJOR one
        if name in self._scales:
            base_scale = self._scales[name]
        else:
            base_scale = self._scales['MAJOR']

        # Compute and return instrument's range
        shift = 0
        while len(scale) < size:
            scale.extend(map(lambda note: base + note + shift, base_scale))
            shift += 12
        scale = scale[:size]
        return scale

    def get_note(self, index):
        """
        Get note to be played by giving its index in instrument's range
        :param index: index of degree in instrument's range
        :return: note from instrument's range
        """
        return self._scale[index]
