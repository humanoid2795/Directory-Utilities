import os
from fnmatch import fnmatch
from heapq import heappush, heappushpop
from local_data import ConfigFile, ExtensionFile


BLOCK_SIZE = 1024


class LargestFile:

    '''
    LargestFile handles returning n largest files by size with their sizes in
    Mega Bytes
    '''

    def __init__(self, total_files=10):
        self.total_files = total_files
        self.largest_files = []

    def add(self, file_path, file_size):
        if len(self.largest_files) < self.total_files:
            heappush(self.largest_files, (file_size, file_path))
        else:
            heappushpop(self.largest_files, (file_size, file_path))

    def get_files(self, directory_path, exclude_patterns):
        directory_files = os.listdir(directory_path)
        for file_name in directory_files:
            for exclude_pattern in exclude_patterns:
                if fnmatch(file_name, exclude_pattern):
                    directory_files.remove(file_name)
                    break
        return directory_files

    def _run(self, directory_path):
        directory_files = self.get_files(
            directory_path,
            ConfigFile().get('ExcludePattern')
        )

        for file_name in directory_files:
            file_path = os.path.join(directory_path, file_name)
            print file_path
            try:
                if os.path.isfile(file_path):
                    self.add(file_path, os.path.getsize(file_path))
                else:
                    self._run(file_path)
            except:
                '''
                Read permission not available, the current file/folder will not
                be included in results.
                '''
                pass

    def start(self):
        root = ConfigFile().get('Root')
        self._run(root)
        return self.largest_files


class ClutterRemover:

    '''
    ClutterRemover handles sorting of cluttered directory.
    The directory from which clutter has to be removed is specified in the
    config file under 'SourcePath' and the directory in which the files have
    to be arranged is specified in the config file under 'DestinationPath'.
    '''
    def move(self, source_path, destination_path):
        with open(source_path, 'rb') as source:
            with open(destination_path, 'wb') as destination:
                while True:
                    data = source.read(BLOCK_SIZE)
                    if not data:
                        break
                    destination.write(data)
        os.remove(source_path)

    def get_files(self, directory_path, exclude_patterns):
        directory_files = os.listdir(directory_path)
        for file_name in directory_files:
            for exclude_pattern in exclude_patterns:
                if fnmatch(file_name, exclude_pattern):
                    directory_files.remove(file_name)
                    break
        return directory_files

    def _run(self, source_path, destination_path):
        extension_data = ExtensionFile().get()
        directory_files = []
        directory_files = self.get_files(
            source_path,
            ConfigFile().get('ExcludePattern'),
        )
        for file_name in directory_files:
            file_extension = os.path.splitext(file_name)[1]
            for extension_key, extension_value in extension_data.items():
                if file_extension in extension_value:
                    destination_directory = os.path.join(
                        destination_path,
                        extension_key,
                    )
                    if not os.path.isdir(destination_directory):
                        os.mkdir(destination_directory)
                    self.move(
                        os.path.join(source_path, file_name),
                        os.path.join(destination_directory, file_name),
                    )
                    break

    def start(self):
        config_file = ConfigFile()
        source_path = config_file.get('SourcePath')
        destination_path = config_file.get('DestinationPath')
        self._run(source_path, destination_path)
