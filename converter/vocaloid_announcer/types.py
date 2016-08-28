import logging

LOG = logging.getLogger(__name__)


class Target(object):
    """
    Stores data and sounds for a single target configuration.
    """

    _metadata = None
    _sounds = []

    def __init__(self, json_data):
        for sound in json_data['sounds']:
            try:
                self._sounds.append(TargetSound(sound))
            except RuntimeError as e:
                LOG.error(e)

        self._metadata = json_data
        self._metadata.pop('sounds')

    def process(self):
        LOG.info('Processing target %s', self._metadata['profile'])

        # Create output directory
        out_directory = os.path.abspath(self._metadata['directory'])
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        LOG.info('Output directory: %s', out_directory)

        # Create sounds
        for s in self._sounds:
            try:
                s.process()
            except RuntimeError as e:
                LOG.error(e)


class TargetSound(object):
    """
    Stores sound components for a given target sound.
    """

    _filename = ''
    _components = []

    def __init__(self, json_data):
        self._filename = json_data[0]

        import vocaloid_announcer.parser as parser
        self._components = parser.parse_target_sound_str(json_data[1])

    def process(self):
        # TODO
        raise NotImplementedError('TODO')


class SoundComponent(object):
    """
    Base class for components of a target sound.
    """

    def audio(self):
        """
        Generates an audio segment for the component.
        @return Audio segment
        """
        raise NotImplementedError('No audio conversion was implemented')


class VSQRegion(SoundComponent):
    """
    Class representing a sound component extracted from a region of a VSQ file.
    """

    _region_name = ''

    def __init__(self, name):
        super(SoundComponent, self).__init__()
        self._region_name = name

    def audio(self):
        # TODO
        raise NotImplementedError('TODO')


class Pause(SoundComponent):
    """
    Class representing a pause of a given number of measures.
    """

    _measures = 0

    def __init__(self, measures):
        super(SoundComponent, self).__init__()
        if type(measures) is str:
            measures = len(measures)
        self._measures = measures

    def audio(self):
        # TODO
        raise NotImplementedError('TODO')
