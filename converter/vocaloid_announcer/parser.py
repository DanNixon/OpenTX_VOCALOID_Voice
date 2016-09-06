import re
import os
import logging
import json
from six.moves import range

LOG = logging.getLogger(__name__)

TARGET_SOUND_STR_VALIDATION_REGEX = r'\w+(?:\.+\w+)*$'
SOUND_MATCH_REGEX = r'(\w+)'
PAUSE_MATCH_REGEX = r'(\.+)'


def read_json_file(in_file):
    """
    Reads a JSON input/output configuration file.
    @param in_file File to read
    @return Tuple (file base name, data)
    """

    data = json.load(in_file)
    name = os.path.splitext(os.path.basename(in_file.name))[0]
    return (name, data)


def make_json_paths_absolute(data, json_file):
    """
    Converts the paths in a source sound config file to absolute paths.
    @param data JSON data
    @param json_file Path to JSON file
    """

    json_directory = os.path.abspath(os.path.dirname(json_file))
    data['vsq_file'] = os.path.join(json_directory, data['vsq_file'])
    data['audio_file'] = os.path.join(json_directory, data['audio_file'])


def validate_target_sound_str(sound_str):
    """
    Validates the format of a target sound string.
    @param sound_str Sound string to validate
    @return True if the string is valid

    Valdation is done by matching the entire string to the regular expression
    TARGET_SOUND_STR_VALIDATION_REGEX.
    """

    return re.match(TARGET_SOUND_STR_VALIDATION_REGEX, sound_str) is not None


def parse_target_sound_str(sound_str):
    """
    Parses a target sound string and splits it into components.
    @param sound_str Sound string to parse
    @return A list of components that make up this sound in chronological order
    """

    if not validate_target_sound_str(sound_str):
        raise RuntimeError(
            'Target sound string "{}" is not valid'.format(sound_str))

    sound_name_matches = re.findall(SOUND_MATCH_REGEX, sound_str)
    pause_matches = re.findall(PAUSE_MATCH_REGEX, sound_str)

    if len(sound_name_matches) != len(pause_matches) + 1:
        raise RuntimeError('Matched the incorrect number of sound names and pauses ({}, {})'.format(
            len(sound_name_matches), len(pause_matches)))

    from vocaloid_announcer.types import MissingVSQRegion, Pause
    sound_parts = [MissingVSQRegion(s) for s in sound_name_matches]
    pause_parts = [Pause(s) for s in pause_matches]

    sound_components = []

    for i in range(len(sound_parts)):
        sound_components.append(sound_parts[i])
        if i < len(pause_parts):
            sound_components.append(pause_parts[i])

    return sound_components
