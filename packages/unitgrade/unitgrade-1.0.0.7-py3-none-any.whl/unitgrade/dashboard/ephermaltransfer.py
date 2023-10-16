import threading
from threading import Thread
import datetime
import time
from datetime import timedelta
import os




class AbstractDBWatcher(Thread):
    def __init__(self, unitgrade_data_dir):
        super().__init__()
        self.stoprequest = threading.Event()
        # self.unitgrade_data = unitgrade_data_dir
        # self.watched_blocks_list = watched_blocks_list
        from diskcache import Cache
        self.db = Cache(unitgrade_data_dir)
        # self.test_handle_function = test_handle_function
        SLEEP_INTERVAL = 5

    # def mark_all_as_fresh(self):
    #     for k in self.watched_blocks_list:
    #         self.db[k + "-updated"] = True

    def watch_function(self):

        pass

    def run(self):
        # print("A DB WATCHER INSTANCE HAS BEEN STARTED!")
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.is_set():
            ct = datetime.datetime.now()
            self.watch_function()
            # d = None
            # k = "undef"
            # for k in self.watched_blocks_list:
            #     ukey = k + "-updated"
            #     with self.db.transact():
            #         if ukey in self.db and self.db[ukey] and k in self.db:
            #             d = self.db[k] # Dict of all values.
            #             self.db[ukey] = False
            #             break
            time.sleep(max(0.2, (datetime.datetime.now()-ct).seconds ) )
            # if d is not None:
            #     self.test_handle_function(k, d)

    def join(self, timeout=None):
        self.stoprequest.set()
        super().join(timeout)

    def close(self):
        self.join()
        # print("Stopped DB watcher.")


class EphermalDBWatcher(AbstractDBWatcher):
    def watch_function(self):
        # self.db.get(tag="ephermal")
        for k in self.db:
            # get all keys in cache.

            val, tag = self.db.get(k, tag=True)
            print(k, val, tag)

        pass


if __name__ == '__main__':
    import os
    f = os.path.dirname(__file__)
    print(f)
    f = os.path.normpath(f +"/../../../../unitgrade_private/devel/example_devel/instructor/cs108/unitgrade_data")
    os.path.isdir(f)

    edbw = EphermalDBWatcher(unitgrade_data_dir=f)
    edbw.start()


    import wandb
    import numpy as np
    print("Random id", wandb.util.generate_id())
    wandb.init(project="unitgrade_report1", id="my_random_job", resume="allow")
    wandb.log({'stuff': 'good', 'x': np.random.rand()})
    z = 234
    pass
