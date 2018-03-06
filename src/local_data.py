import json
import os
import sys

from sets import Set
from directory_organizer_exceptions import PlatformError, ConfigError, \
    ExtensionError

CONFIG_FILE = 'config'
EXTENSION_FILE = 'extension'


class LocalData(object):
    '''
    The LocalData class handles the data that is stored locally on the users
    device based on the platform being used.
    '''

    def __init__(self):
        self.local_data = None
        if sys.platform.startswith('linux'):
            self.local_data = os.path.join(
                os.environ['HOME'],
                '.DirectoryUtility',
            )
        elif sys.platform.startswith('win'):
            self.local_data = os.path.join(
                os.environ['LocalAppData'],
                'DirectoryUtility',
            )
        else:
            # Additional platforms can be supported as per the need.
            raise PlatformError

        if not os.path.isdir(self.local_data):
            os.mkdir(self.local_data)

    def _load_data(self, local_file_path):
        local_data = {}
        with open(local_file_path, 'r') as local_file:
            local_data = json.load(local_file)
        return local_data

    def _dump_data(self, local_file_path, local_data):
        with open(local_file_path, 'w') as local_file:
            json.dump(local_data, local_file, sort_keys=True, indent=4)

    def get(self, data_key, data_value):
        raise NotImplementedError

    def set(self, data_key, data_value):
        raise NotImplementedError


class ConfigFile(LocalData):
    '''
    The ConfigFile class handles the config file data which has been
    stored locally on the users device.
    '''

    def __init__(self):
        super(ConfigFile, self).__init__()
        config_file_path = os.path.join(self.local_data, CONFIG_FILE)
        if not os.path.isfile(config_file_path):
            '''
            'Largest File'
            Scan for finding the largest n files will start from the root
            directory.
            Root: Users personal files[default], excluding system files.

            'Removing Clutter'
            SourcePath: Desktop directory[default]
            DestinationPath: Documents directory[default]
            '''
            source = None
            destination = None
            root = None
            if sys.platform.startswith('linux'):
                source = os.path.join(os.environ['HOME'], 'Desktop')
                destination = os.path.join(os.environ['HOME'], 'Documents')
                root = os.environ['HOME']
            elif sys.platform.startswith('win'):
                source = os.path.join(os.environ['HOMEPATH'], 'Desktop')
                destination = os.path.join(os.environ['HOMEPATH'], 'Documents')
                root = os.environ['HOMEPATH']
            else:
                # Additional platforms can be supported as per the need.
                raise exceptions.PlatformError('Platform not supported')

            # Initialzation of config file.
            config_data = {}
            config_data['Root'] = root
            config_data['SourcePath'] = source
            config_data['DestinationPath'] = destination
            config_data['ExcludePattern'] = ['.*', '*.o']
            self._dump_data(config_data)

    def _load_data(self):
        config_file_path = os.path.join(self.local_data, CONFIG_FILE)
        config_data = {}
        try:
            config_data = super(ConfigFile, self)._load_data(config_file_path)
        except IOError:
            raise ConfigError('Config File does not exist')
        return config_data

    def _dump_data(self, config_data):
        config_file_path = os.path.join(self.local_data, CONFIG_FILE)
        super(ConfigFile, self)._dump_data(config_file_path, config_data)

    def get(self, config_key):
        config_data = {}
        config_data = self._load_data()
        return config_data.get(config_key, None)

    def set(self, config_key, config_value):
        config_data = {}
        config_data = self._load_data()
        config_data[config_key] = config_value
        self._dump_data(config_data)


class ExtensionFile(LocalData):
    '''
    The ExtensionFile class handles the directory names along with the list
    of extensions that classify a file to be of a particular directory.
    '''

    def __init__(self):
        super(ExtensionFile, self).__init__()
        extension_file_path = os.path.join(self.local_data, EXTENSION_FILE)
        if not os.path.isfile(extension_file_path):
            extension_data = {}
            # Default directory and extensions
            extension_data['MP3'] = ['.mp3']
            extension_data['DOC'] = ['.doc', '.docx']
            extension_data['PDF'] = ['.pdf']
            self._dump_data(extension_data)

    def _load_data(self):
        extension_file_path = os.path.join(self.local_data, EXTENSION_FILE)
        extension_data = {}
        try:

            extension_data = \
                super(ExtensionFile, self)._load_data(extension_file_path)
        except IOError:
            raise ExtensionError('Extension file does not exist')
        for extension_key, extension_value in extension_data.items():
            extension_data[extension_key] = Set(extension_value)
        return extension_data

    def _dump_data(self, extension_data):
        extension_file_path = os.path.join(self.local_data, EXTENSION_FILE)
        for extension_key, extension_value in extension_data.items():
            extension_data[extension_key] = list(extension_value)
        super(ExtensionFile, self)._dump_data(
            extension_file_path,
            extension_data,
        )

    def add(self, extension_key, extension_value):
        extension_data = {}
        extension_data = self._load_data()
        extension_data[extension_key] = Set(extension_value)
        self._dump_data(extension_data)

    def update(self, extension_key, extension_value):
        extension_data = {}
        extension_data = self._load_data()
        try:
            extension_data[extension_key].update(Set(extension_value))
        except KeyError:
            raise ExtensionError('Invalid extension key')
        self._dump_data(extension_data)

    def delete(self, extension_key):
        extension_data = {}
        extension_data = self._load_data()
        try:
            del extension_data[extension_key]
        except KeyError:
            raise ExtensionError('Invalid extension key')
        self._dump_data(extension_data)

    def get(self):
        extension_data = {}
        extension_data = self._load_data()
        return extension_data
