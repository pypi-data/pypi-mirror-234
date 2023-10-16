import threading
from threading import Thread
import datetime
import time
from datetime import timedelta
import os

class DBWatcher(Thread):
    def __init__(self, unitgrade_data_dir, watched_blocks_list, test_handle_function):
        super().__init__()
        self.stoprequest = threading.Event()
        # self.unitgrade_data = unitgrade_data_dir
        self.watched_blocks_list = watched_blocks_list
        from diskcache import Cache
        self.db = Cache(unitgrade_data_dir)
        self.test_handle_function = test_handle_function

    def mark_all_as_fresh(self):
        for k in self.watched_blocks_list:
            self.db[k + "-updated"] = True


    def run(self):
        # print("A DB WATCHER INSTANCE HAS BEEN STARTED!")
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.is_set():
            ct = datetime.datetime.now()
            d = None
            k = "undef"
            for k in self.watched_blocks_list:
                ukey = k + "-updated"
                with self.db.transact():
                    if ukey in self.db and self.db[ukey] and k in self.db:
                        d = self.db[k] # Dict of all values.
                        self.db[ukey] = False
                        break
            time.sleep(max(0.2, (datetime.datetime.now()-ct).seconds ) )
            if d is not None:
                self.test_handle_function(k, d)

    def join(self, timeout=None):
        self.stoprequest.set()
        super().join(timeout)

    def close(self):
        self.join()
        print("Stopped DB watcher.")
