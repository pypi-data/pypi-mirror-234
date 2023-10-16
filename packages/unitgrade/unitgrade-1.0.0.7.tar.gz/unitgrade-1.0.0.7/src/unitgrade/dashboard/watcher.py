from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import datetime
import fnmatch

class Watcher:
    def __init__(self, base_directory, watched_files_dictionary, watched_files_lock):
        self.base_directory = base_directory
        self.watched_files_dictionary = watched_files_dictionary
        self.watched_files_lock = watched_files_lock
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.watched_files_dictionary, self.watched_files_lock)
        # print("self.base_directory", self.base_directory)
        self.observer.schedule(event_handler, self.base_directory, recursive=True)
        self.observer.start()

    def close(self):
        self.observer.stop()
        self.observer.join()
        print("Closed file change watcher.")

    def __del__(self):
        self.close()


class Handler(FileSystemEventHandler):
    def __init__(self, watched_files_dictionary, watched_files_lock):
        self.watched_files_dictionary = watched_files_dictionary
        self.watched_files_lock = watched_files_lock
        super().__init__()

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created' or event.event_type == 'modified':
            with self.watched_files_lock:
                fnd_ = None
                for k in self.watched_files_dictionary:
                    if fnmatch.fnmatch(event.src_path, k):
                        fnd_ = k
                        break
                if fnd_ is not None:
                    # print("Watcher, recording change to", fnd_)
                    if event.src_path.endswith("json"):
                        from pupdb.core import PupDB
                        db = PupDB(event.src_path)
                        # if db.get("state") == "fail":
                        #     print("File watcher state:", db.get("state"), "in", event.src_path)

                    self.watched_files_dictionary[fnd_]['last_recorded_change'] = datetime.datetime.now()
                    self.watched_files_dictionary[fnd_]['file'] = event.src_path
