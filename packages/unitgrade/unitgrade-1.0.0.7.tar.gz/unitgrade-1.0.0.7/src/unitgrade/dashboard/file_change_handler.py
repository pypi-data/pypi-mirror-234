from threading import Thread
import threading
import datetime
from datetime import timedelta
import time


class FileChangeHandler(Thread):
    def __init__(self, watched_files_dictionary, watched_files_lock, do_something):
        super().__init__()
        self.watched_files_dictionary = watched_files_dictionary
        self.watched_files_lock = watched_files_lock
        self.do_something = do_something
        self.stoprequest = threading.Event()


    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.is_set():
            ct = datetime.datetime.now()
            file_to_handle = None
            with self.watched_files_lock:
                for k, v in self.watched_files_dictionary.items():
                    if v['last_handled_change'] is None:
                        file_to_handle = k
                        break
                    else:
                        # This file has been handled recently. Check last change to the file.
                        if v['last_recorded_change'] is not None:

                            if (v['last_recorded_change'] - v['last_handled_change'] ) > timedelta(seconds=0):
                                file_to_handle = k
                                break

            if file_to_handle is not None:
                # Handle the changes made to this exact file.
                self.do_something(file_to_handle)

                with self.watched_files_lock:
                    self.watched_files_dictionary[file_to_handle]['last_handled_change'] = datetime.datetime.now()

            time.sleep(max(0.1, 0.1 - (datetime.datetime.now()-ct).seconds ) )


    def join(self, timeout=None):
        self.stoprequest.set()
        super().join(timeout)

    def close(self):
        self.join()
        print("Stopped file change handler.")
