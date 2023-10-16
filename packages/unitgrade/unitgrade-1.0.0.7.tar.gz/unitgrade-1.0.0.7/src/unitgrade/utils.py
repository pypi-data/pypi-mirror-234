import re
import sys
import threading
import time
import lzma
import hashlib
import pickle
import base64
import os
from collections import namedtuple
from io import StringIO
import numpy as np
import tqdm
from colorama import Fore
from functools import _make_key
from diskcache import Cache

_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])

def gprint(s):
    print(f"{Fore.LIGHTGREEN_EX}{s}")

myround = lambda x: np.round(x)  # required for obfuscation.
msum = lambda x: sum(x)
mfloor = lambda x: np.floor(x)

"""
Clean up the various output-related helper classes.
"""
class Logger(object):
    def __init__(self, buffer, write_to_stdout=True):
        # assert False
        self.terminal = sys.stdout
        self.write_to_stdout = write_to_stdout
        self.log = buffer

    def write(self, message):
        if self.write_to_stdout:
            self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        pass


class Capturing(list):
    def __init__(self, *args, stdout=None, unmute=False, **kwargs):
        self._stdout = stdout
        self.unmute = unmute
        super().__init__(*args, **kwargs)

    def __enter__(self, capture_errors=True):  # don't put arguments here.
        self._stdout = sys.stdout if self._stdout == None else self._stdout
        self._stringio = StringIO()
        self._stringio_err = StringIO()

        if self.unmute:
            sys.stdout = Logger(self._stringio)
        else:
            sys.stdout = self._stringio

        if capture_errors:
            self._sterr = sys.stderr
            # sys.sterr = StringIO()  # memory hole it
            sys.sterr = self._stringio_err

        self.capture_errors = capture_errors
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout
        if self.capture_errors:
            sys.sterr = self._sterr
            self.errors = self._stringio_err.getvalue()

class Capturing2(Capturing):
    def __exit__(self, *args):
        lines = self._stringio.getvalue().splitlines()
        txt = "\n".join(lines)
        numbers = extract_numbers(rm_progress_bar(txt))
        self.extend(lines)
        del self._stringio  # free up some memory
        sys.stdout = self._stdout
        if self.capture_errors:
            sys.sterr = self._sterr

        self.output = txt
        self.numbers = numbers


def rm_progress_bar(txt):
    # More robust version. Apparently length of bar can depend on various factors, so check for order of symbols.
    nlines = []
    for l in txt.splitlines():
        pct = l.find("%")
        ql = False
        if pct > 0:
            i = l.find("|", pct + 1)
            if i > 0 and l.find("|", i + 1) > 0:
                ql = True
        if not ql:
            nlines.append(l)
    return "\n".join(nlines)


class ActiveProgress():
    def __init__(self, t, start=True, title="my progress bar", show_progress_bar=True, file=None, mute_stdout=False):
        if file == None:
            file = sys.stdout
        self.file = file
        self.mute_stdout = mute_stdout
        self._running = False
        self.title = title
        self.dt = 0.025
        self.n = max(1, int(np.round(t / self.dt)))
        self.show_progress_bar = show_progress_bar
        self.pbar = None

        if start:
            self.start()

    def start(self):
        if self.mute_stdout:
            import io
            # from unitgrade.utils import Logger
            self._stdout = sys.stdout
            sys.stdout = Logger(io.StringIO(), write_to_stdout=False)

        self._running = True
        if self.show_progress_bar:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        self.time_started = time.time()

    def terminate(self):
        if not self._running:
            # print("Stopping a progress bar which is not running (class unitgrade.utils.ActiveProgress")
            pass
            # raise Exception("Stopping a stopped progress bar. ")
        self._running = False
        if self.show_progress_bar:
            self.thread.join()
        if self.pbar is not None:
            self.pbar.update(1)
            self.pbar.close()
            self.pbar = None

        self.file.flush()

        if self.mute_stdout:
            import io
            sys.stdout = self._stdout

        return time.time() - self.time_started

    def run(self):
        self.pbar = tqdm.tqdm(total=self.n, file=self.file, position=0, leave=False, desc=self.title, ncols=100,
                              bar_format='{l_bar}{bar}| [{elapsed}<{remaining}]')
        t_ = time.time()
        for _ in range(self.n - 1):  # Don't terminate completely; leave bar at 99% done until terminate.
            if not self._running:
                self.pbar.close()
                self.pbar = None
                break
            tc = time.time()
            tic = max(0, self.dt - (tc - t_))
            if tic > 0:
                time.sleep(tic)
            t_ = time.time()
            self.pbar.update(1)


def dprint(first, last, nL, extra = "", file=None, dotsym='.', color='white'):
    if file == None:
        file = sys.stdout
    dot_parts = (dotsym * max(0, nL - len(last) - len(first)))
    print(first + dot_parts, end="", file=file)
    last += extra
    print(last, file=file)


def hide(func):
    return func


def makeRegisteringDecorator(foreignDecorator):
    """
        Returns a copy of foreignDecorator, which is identical in every
        way(*), except also appends a .decorator property to the callable it
        spits out.
    """

    def newDecorator(func):
        # Call to newDecorator(method)
        # Exactly like old decorator, but output keeps track of what decorated it
        R = foreignDecorator(func)  # apply foreignDecorator, like call to foreignDecorator(method) would have done
        R.decorator = newDecorator  # keep track of decorator
        # R.original = func         # might as well keep track of everything!
        return R

    newDecorator.__name__ = foreignDecorator.__name__
    newDecorator.__doc__ = foreignDecorator.__doc__
    return newDecorator


hide = makeRegisteringDecorator(hide)


def extract_numbers(txt):
    numeric_const_pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    all = rx.findall(txt)
    all = [float(a) if ('.' in a or "e" in a) else int(a) for a in all]
    if len(all) > 500:
        print(txt)
        raise Exception("unitgrade_v1.unitgrade_v1.py: Warning, too many numbers!", len(all))
    return all


def cache(foo, typed=False):
    """ Magic cache wrapper
    https://github.com/python/cpython/blob/main/Lib/functools.py
    """
    maxsize = None
    def wrapper(self, *args, **kwargs):
        key = (self.cache_id(), ("@cache", foo.__name__, _make_key(args, kwargs, typed)))
        # print(self._cache.keys())
        # for k in self._cache:
        #     print(k)
        if not self._cache_contains(key):
            value = foo(self, *args, **kwargs)
            self._cache_put(key, value)
        else:
            value = self._cache_get(key)
            # This appears to be required since there are two caches. Otherwise, when deploy method is run twice,
            # the cache will not be set correctly.
            self._cache_put(key, value)
        return value

    return wrapper


def methodsWithDecorator(cls, decorator):
    """
        Returns all methods in CLS with DECORATOR as the
        outermost decorator.

        DECORATOR must be a "registering decorator"; one
        can make any decorator "registering" via the
        makeRegisteringDecorator function.

        import inspect
        ls = list(methodsWithDecorator(GeneratorQuestion, deco))
        for f in ls:
            print(inspect.getsourcelines(f) ) # How to get all hidden questions.
    """
    for maybeDecorated in cls.__dict__.values():
        if hasattr(maybeDecorated, 'decorator'):
            if maybeDecorated.decorator == decorator:
                print(maybeDecorated)
                yield maybeDecorated


""" Methods responsible for turning a dictionary into a string that can be pickled or put into a json file. """
def dict2picklestring(dd):
    """
    Turns a dictionary into a string with some compression.

    :param dd:
    :return:
    """
    b = lzma.compress(pickle.dumps(dd))
    b_hash = hashlib.blake2b(b).hexdigest()
    return base64.b64encode(b).decode("utf-8"), b_hash


def hash_string(s):
    """This is a helper function used to double-hash a something (i.e., hash of a hash).
    Right now it is used in the function in 02002 when a creating the index of student-downloadable evaluations."""
    # gfg = hashlib.blake2b()
    return hashlib.blake2b(s.encode("utf-8")).hexdigest()

def hash2url(hash):
    return hash[:16]

def picklestring2dict(picklestr):
    """ Reverse of the above method: Turns the string back into a dictionary. """
    b = base64.b64decode(picklestr)
    hash = hashlib.blake2b(b).hexdigest()
    dictionary = pickle.loads(lzma.decompress(b))
    return dictionary, hash

token_sep = "-"*70 + " ..ooO0Ooo.. " + "-"*70
def load_token(file_in):
    """ We put this one here to allow loading of token files for the dashboard. """
    with open(file_in, 'r') as f:
        s = f.read()
    splt = s.split(token_sep)
    data = splt[-1]
    info = splt[-2]
    head = token_sep.join(splt[:-2])
    plain_text=head.strip()
    hash, l1 = info.split(" ")
    hash = hash.strip()
    data = "".join( data.strip()[1:-1].splitlines() )
    l1 = int(l1)
    dictionary, b_hash = picklestring2dict(data)
    dictionary['metadata'] = {'file_reported_hash':b_hash, 'actual_hash': hash}  # This contains information about the hashes right now.
    assert len(data) == l1
    assert b_hash == hash.strip()
    return dictionary, plain_text


def checkout_remote_results(remote_url, manifest):
    """

    :param remote_url:
    :param manifest:
    :return:
    """
    import urllib
    # urllib.
    import urllib.request
    if remote_url.endswith("/"):
        remote_url = remote_url[:-1]

    with urllib.request.urlopen(remote_url +"/index.html") as response:
        html = response.read().decode()

    SEP = "-----------"
    remote = {ll[0]: ll[1] for ll in [l.strip().split(" ") for l in html.split(SEP)[1].strip().splitlines()] }
    # lines =
    # print(remote_url)
    # print(remote)

    mf = [m.strip().split(" ")[-1] for m in manifest.strip().splitlines()]
    a = 23
    html = None
    url = None
    for hash in reversed(mf):
        if hash_string(hash) in remote:
            url = f"{remote_url}/{os.path.dirname( remote[hash_string(hash)] )}/{hash2url(hash)}/index.html"
            with urllib.request.urlopen(url) as response:
                html = response.read().decode()
                # print( html )
            break
    # if debug:
    # url = f"https://cp.pages.compute.dtu.dk/02002public/_static/evaluation/project_evaluations_2023fall/project0/student_html/5a2db54fcce2f3ee/index.html"
    # with urllib.request.urlopen(url) as response:
    #     html = response.read().decode()

    if html is not None:
        try:
            from xml.etree import ElementTree as ET
            s = html[html.find("<table"):html.find("</table>")+len("</table>")]
            table = ET.XML(s)
            head = list(iter(table))[0]
            body = list(iter(table))[1]
            from collections import defaultdict
            dd = defaultdict(list)
            keys = []
            for tr in head:
                for td in tr:
                    keys.append(td.text)

            for tr in body:
                for k, td in enumerate(tr):
                    dd[keys[k]].append(td.text)
        except Exception as e:
            print("Sorry results not parsed. Perhaps bad file upload?")
            keys = ["Key", "Values"]
            dd = {keys[0]: ['Results were not parsed', 'Score'], keys[1]: ['Results were not readable. Contact a TA', 0]}

        # rows = iter(table)
        # for r in list(iter(table)):
        #     print(r)
        # import tabulate
        # print( tabulate.tabulate(dd, headers="keys") )
        # headers = [col.text for col in next(rows)]
        # for row in rows:
        #     values = [col.text for col in row]
        # print(dict(zip(headers, values)))
        # dd[keys[1]][-1]
        # dfs = pd.read_html(html)
        # df = dfs[0]
        # df.__format__()
        # tabular
        # print( df.to_string(index=False) )
        # df.as
        result = dict(html=html, dict=dd, score=float( dd[keys[1]][-1] ), url=url)
    else:
        result=dict(html=html)

    return result



## Key/value store related.
class DKPupDB:
    DISABLE_DB = False
    """ This key/value store store artifacts (associated with a specific question) in a dictionary. """
    def __init__(self, artifact_file, use_pupdb=False, register_ephemeral=False):
        # Make a double-headed disk cache thingy.
        try:
            self.dk = Cache(os.path.dirname(artifact_file)) # Start in this directory.
            self.name_ = os.path.basename(artifact_file[:-5])
            if self.name_ not in self.dk:
                self.dk[self.name_] = dict()
            self.use_pupdb = use_pupdb
            self.register_ephemeral = register_ephemeral
            if self.use_pupdb:
                from pupdb.core import PupDB
                self.db_ = PupDB(artifact_file)
        except Exception as e:
            # print("Artifact file not readable. Possibly ")
            self.DISABLE_DB = True
            pass

    def __setitem__(self, key, value):
        if self.DISABLE_DB:
            return
        if self.use_pupdb:
            self.db_.set(key, value)
        with self.dk.transact():
            d = self.dk[self.name_]
            d[key] = value
            self.dk[self.name_] = d
            self.dk.set(key=np.random.randint(0, high=1e8), value=(key,value), tag="ephemeral")
            self.dk[self.name_ + "-updated"] = True

    def __getitem__(self, item):
        if self.DISABLE_DB:
            return "db disabled due to bad artifact file."
        v = self.dk[self.name_][item]
        if self.use_pupdb:
            v2 = self.db_.get(item)
            if v != v2:
                print("Mismatch v1, v2 for ", item)
        return v

    def keys(self): # This one is also deprecated.
        return tuple(self.dk[self.name_].keys()) #.iterkeys())
        # return self.db_.keys()

    def set(self, item, value): # This one is deprecated.
        if self.DISABLE_DB:
            return
        self[item] = value

    def get(self, item, default=None):
        if self.DISABLE_DB:
            return "artifact file not loaded."
        return self[item] if item in self else default

    def __contains__(self, item):
        if self.DISABLE_DB:
            return False
        return item in self.dk[self.name_] #keys()
        # return item in self.dk

