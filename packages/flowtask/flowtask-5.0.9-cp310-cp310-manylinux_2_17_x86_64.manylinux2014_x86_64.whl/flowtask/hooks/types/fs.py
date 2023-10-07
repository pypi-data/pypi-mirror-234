import time
import os
from collections import defaultdict
from navconfig.logging import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from flowtask.exceptions import ComponentError
from .watch import BaseWatcher, BaseWatchdog


# TODO> PatternMatchingEventHandler

fslog = logging.getLogger('watchdog.observers')
fslog.setLevel(logging.WARNING)


class fsHandler(PatternMatchingEventHandler):

    def __init__(self, parent: BaseWatchdog, patterns=None, *args, **kwargs):
        super().__init__(patterns=patterns, *args, **kwargs)
        self.debounced_events = defaultdict(lambda: 0)
        self.parent = parent
        self.recently_created = set()
        self._logger = logging.getLogger('Watcher.FS')

    def zero_size(self, filepath: str):
        """Check if the file is of zero size."""
        return os.path.getsize(filepath) == 0

    def process(self, event):
        """Process the event if it matches the patterns and isn't a directory."""
        if event.is_directory:
            return None

        # Check if an event for this path has been triggered recently
        last_event_time = self.debounced_events[event.src_path]
        current_time = time.time()
        if current_time - last_event_time < 0.5:  # 0.5 seconds debounce time
            return

        self.debounced_events[event.src_path] = current_time

    def on_created(self, event):
        if event.is_directory:
            return
        if "created" not in self.parent.events:
            return
        if self.zero_size(event.src_path):
            self._logger.warning(
                f"File {event.src_path} has zero size!"
            )
        print(f"Watchdog received created event - {event.src_path} s.")
        self.recently_created.add(event.src_path)  # recently created
        self.process(event)
        # after, running actions:
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path
        }
        self.parent.call_actions(**args)

    def on_modified(self, event):
        if event.is_directory:
            return
        if "modified" not in self.parent.events:
            return
        if event.src_path in self.recently_created:  # Add this block
            self.recently_created.remove(event.src_path)
            return
        if self.zero_size(event.src_path):
            self._logger.warning(
                f"File {event.src_path} has zero size!"
            )
        print(
            f"Watchdog received modified event - {event.src_path} s."
        )
        self.process(event)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path
        }
        self.parent.call_actions(**args)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path
        }
        self.parent.call_actions(**args)

    def on_moved(self, event):
        if event.is_directory:
            return
        if "moved" not in self.parent.events:
            return
        print(f"Watchdog received moved event - {event.src_path} s.")
        self.process(event)

    def on_deleted(self, event):
        if "deleted" not in self.parent.events:
            return
        print(f"Watchdog received deleted event - {event.src_path} s.")
        self.process(event)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path
        }
        self.parent.call_actions(**args)

class fsWatcher(BaseWatcher):
    def __init__(self, pattern, *args, **kwargs):
        super(fsWatcher, self).__init__(*args, **kwargs)
        self.directory = kwargs.pop('directory', None)
        self.filename = kwargs.pop('filename', [])
        self.recursive = kwargs.pop('recursive', True)
        self.observer = Observer()
        self._patterns = pattern

    def run(self):
        event_handler = fsHandler(
            parent=self.parent,
            patterns=self._patterns
        )
        self.observer.schedule(
            event_handler,
            self.directory,
            recursive=self.recursive
        )
        self.observer.start()
        try:
            while True:
                time.sleep(self.timeout)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Watchdog FS Observer was stopped")
            self.observer.join()

    def stop(self):
        try:
            self.observer.stop()
        except Exception:
            pass
        self.observer.join()

class FSWatchdog(BaseWatchdog):
    """FSWatchdog.
        Checking for changes in the filesystem and dispatch events.
    """
    timeout: int = 5
    recursive: bool = True

    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        self.recursive = kwargs.pop('recursive', True)
        self.events = kwargs.pop('on', ["created", "modified", "deleted", "moved"])
        self.filename = kwargs.pop('filename', [])
        if not self.filename:
            self.filename = ["*"]
        else:
            self.filename = [f"*{filename}" for filename in self.filename]
        try:
            self.directory = kwargs['directory']
        except KeyError as exc:
            raise ComponentError(
                "Unable to load Directory on FSWatchdog"
            ) from exc
        return fsWatcher(
            pattern=self.filename,
            directory=self.directory,
            timeout=self.timeout,
            recursive=self.recursive
        )
