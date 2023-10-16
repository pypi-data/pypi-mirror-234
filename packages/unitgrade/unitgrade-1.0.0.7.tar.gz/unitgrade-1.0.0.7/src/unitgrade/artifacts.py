import threading
from colorama import Fore



class WorkerThread(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, dir_q, db=None):
        super(WorkerThread, self).__init__()
        self.dir_q = dir_q
        # self.result_q = result_q
        self.db = db
        self.stoprequest = threading.Event()

    def empty_queue(self):
        ss = ""
        try:
            while True:
                std_type, m = self.dir_q.get(True, 0.05)
                ss += f"{Fore.RED}{m}{Fore.WHITE}" if std_type == 'stderr' else m
        except Exception as e:
            pass
            # continue
        finally:
            if len(ss) > 0:
                # print(ss)
                cq = self.db.get('stdout')
                self.db.set('stdout', cq + [[len(cq), ss]])

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        import time
        while not self.stoprequest.is_set():
            self.empty_queue()
            time.sleep(0.1)

    def join(self, timeout=None):
        self.stoprequest.set()
        super().join(timeout)
        self.empty_queue()

class DummyPipe:
    def __init__(self, type, std_out_or_err, queue, mute=False):
        self.type = type
        self.std_ = std_out_or_err
        self.queue = queue
        self.mute = mute

    def write(self, message):
        if not self.mute:
            self.std_.write(message)
        self.queue.put((self.type, message))

    def write_mute(self, message):
        self.queue.put((self.type, message))

    def flush(self):
        self.std_.flush()


class StdCapturing():
    def __init__(self, stdout, stderr, db=None, mute=False):
        # self.stdout = stdout
        db.set('stdout', [])
        import queue
        self.queu = queue.Queue()

        self.dummy_stdout = DummyPipe('stdout', stdout, self.queu, mute=mute)
        self.dummy_stderr = DummyPipe('stderr', stderr, self.queu, mute=mute)

        # capture either stdout or stderr.
        # self.mute = mute
        self.recordings = []
        self.recording = False
        import threading
        self.thread = WorkerThread(self.queu, db=db) # threading.Thread(target=self.consume_queue, args=self.lifo)
        self.thread.start()

    def close(self):
        try:
            self.thread.join()
        except Exception as e:
            print(e)
        pass


# class ArtifactMapper:
#     def  __init__(self):
#         self.artifact_output_json = ''
#         from threading import Lock
#         self.lock = Lock()
#         import pupdb
#         self.db = pupdb.Pupdb(self.artifact_output_json)
#         run = self.db.get("run_number", 0)
#
#     def add_stack_trace(self, e):
#         # Add an error.
#         pass
#
#     def print_stdout(self, msg, timestamp):
#         pass
#
#     def print_stderr(self, msg, timestamp):
#         pass
#
#     def restart_test(self):
#         pass
#
#     def register_outcome(self, did_fail=False, did_pass=False, did_error=False):
#         pass
