"""Provide development tools for monitoring."""

from watchdog.events import FileSystemEventHandler

from regscale.utils.files import print_file_contents


class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.file_path:
            print(f"{self.file_path} modified!")
            print_file_contents(self.file_path)
