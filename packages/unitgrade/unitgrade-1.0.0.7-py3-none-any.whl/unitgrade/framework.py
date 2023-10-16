from threading import Thread
import importnb
import numpy as np
import sys
import pickle
import os
import inspect
import colorama
import unittest
import time
import textwrap
import urllib.parse
import requests
import ast
import numpy
from unittest.case import TestCase
from unitgrade.runners import UTextResult
from unitgrade.utils import gprint, Capturing2, Capturing
from unitgrade.artifacts import StdCapturing
from unitgrade.utils import DKPupDB


colorama.init(autoreset=True)  # auto resets your settings after every output
numpy.seterr(all='raise')

def setup_dir_by_class(C, base_dir):
    name = C.__class__.__name__
    return base_dir, name

_DASHBOARD_COMPLETED_MESSAGE = "Dashboard> Evaluation completed."

# Consolidate this code.
class classmethod_dashboard(classmethod):
    def __init__(self, f):
        def dashboard_wrap(cls: UTestCase):
            if not cls._generate_artifacts:
                f(cls)
                return
            db = DKPupDB(cls._artifact_file_for_setUpClass())
            r = np.random.randint(1000 * 1000)
            db.set('run_id', r)
            db.set('coverage_files_changed', None)

            state_ = 'fail'
            try:
                _stdout = sys.stdout
                _stderr = sys.stderr
                std_capture = StdCapturing(stdout=sys.stdout, stderr=sys.stderr, db=db, mute=False)

                # Run this unittest and record all of the output.
                # This is probably where we should hijack the stdout output and save it -- after all, this is where the test is actually run.
                # sys.stdout = stdout_capture
                sys.stderr = std_capture.dummy_stderr
                sys.stdout = std_capture.dummy_stdout
                db.set("state", "running")
                f(cls)
                state_ = 'pass'
            except Exception as e:
                from werkzeug.debug.tbtools import DebugTraceback, _process_traceback
                state_ = 'fail'
                db.set('state', state_)
                exi = e
                dbt = DebugTraceback(exi)
                sys.stderr.write(dbt.render_traceback_text())
                html = dbt.render_traceback_html(include_title="hello world")
                db.set('wz_stacktrace', html)
                raise e
            finally:
                db.set('state', state_)
                std_capture.dummy_stdout.write_mute(_DASHBOARD_COMPLETED_MESSAGE)
                sys.stdout = _stdout
                sys.stderr = _stderr
                std_capture.close()

        super().__init__(dashboard_wrap)

class Report:
    title = "report title"
    abbreviate_questions = False # Should the test items start with 'Question ...' or just be q1).
    version = None # A version number of the report (1.0). Used to compare version numbers with online resources.
    url = None  # Remote location of this problem.
    remote_url = None  # Remote url of documentation. This will be used to gather results.

    questions = []
    pack_imports = []
    individual_imports = []

    _remote_check_cooldown_seconds = 60*60*2  # Seconds between remote check of report.
    nL = 120  # Maximum line width
    _config = None  # Private variable. Used when collecting results from student computers. Should only be read/written by teacher and never used for regular evaluation.
    _setup_mode = False # True if test is being run in setup-mode, i.e. will not fail because of bad configurations, etc.

    @classmethod
    def reset(cls):
        for (q, _) in cls.questions:
            if hasattr(q, 'reset'):
                q.reset()

    @classmethod
    def mfile(clc):
        return inspect.getfile(clc)

    def _file(self):
        return inspect.getfile(type(self))

    def _artifact_file(self):
        """ File for the artifacts DB (thread safe). This file is optional. Note that it is a pupdb database file.
        Note the file is shared between all sub-questions.
        TODO: Describe what is actually in this file.
        """
        return os.path.join(os.path.dirname(self._file()), "unitgrade_data/main_config_"+ os.path.basename(self._file()[:-3]) + ".artifacts.pkl")

    def _manifest_file(self):
        """
        The manifest is the file we append all artifact hashes to so we can check results at some later time.
        file is plaintext, and can be deleted.
        """
        # print("_file", self._file())
        return os.path.join(os.path.dirname(self._file()), "unitgrade_data/token_" + os.path.basename(self._file()[:-3]) + ".manifest")

    def _is_run_in_grade_mode(self):
        """ True if this report is being run as part of a grade run. """
        return self._file().endswith("_grade.py") # Not sure I love this convention.

    def _import_base_relative(self):
        if hasattr(self.pack_imports[0], '__path__'):
            root_dir = self.pack_imports[0].__path__[0]
        else:
            root_dir = self.pack_imports[0].__file__

        root_dir = os.path.dirname(root_dir)
        relative_path = os.path.relpath(self._file(), root_dir)
        modules = os.path.normpath(relative_path[:-3]).split(os.sep)
        relative_path = relative_path.replace("\\", "/")
        if relative_path.startswith(".."):
            error = """
    --------------------------------------------------------------------------------------            
    Oh no, you got an installation problem!
    
    You have accidentally downloaded (and installed) the course software in two locations on your computer.
    The first place is: 
    
    > %s
    
    And the second place is the location that contains this file, namely:
    
    > %s 
    
    I can't be certain which of these two contains your actual homework, so therefore I have to give you an error :-(. 
    
    But it is easy to fix! Determine which of the two folders contain your homework and simply delete the other one. That
    should take care of the problem!
    (The terminal in VS Code will tell you the location on your computer you have open right now -- most likely, that is the 
    location of the right 02002student folder!).
    
    In the future, try to avoid downloading and installing the course software many times -- most issues 
    can be solved in a much simpler way.
    
    If this problem persists, please contact us on piazza, discord, or directly on tuhe@dtu.dk (or come by my office, building 321, room 127).
    Include a copy of this error and a screenshot of VS Code.
            """%(root_dir, self._file())
            print(error)
            sys.exit(1)
            raise Exception(error)

        return root_dir, relative_path, modules

    def __init__(self, strict=False, payload=None):
        working_directory = os.path.abspath(os.path.dirname(self._file()))
        self.wdir, self.name = setup_dir_by_class(self, working_directory)
        # self.computed_answers_file = os.path.join(self.wdir, self.name + "_resources_do_not_hand_in.dat")
        for (q, _) in self.questions:
            q.nL = self.nL  # Set maximum line length.

        if payload is not None:
            self.set_payload(payload, strict=strict)

    def main(self, verbosity=1):
        # Run all tests using standard unittest (nothing fancy).
        loader = unittest.TestLoader()
        for q, _ in self.questions:
            start = time.time()  #
            suite = loader.loadTestsFromTestCase(q)
            unittest.TextTestRunner(verbosity=verbosity).run(suite)
            total = time.time() - start
            q.time = total

    def _setup_answers(self, with_coverage=False, verbose=True):
        if with_coverage:
            for q, _ in self.questions:
                q._with_coverage = True
                q._report = self
        for q, _ in self.questions:
            q._setup_answers_mode = True
            # q._generate_artifacts = False # Disable artifact generation when the report is being set up.

        # Ensure that the lock file exists.
        if self.url is not None:
            if not os.path.dirname(self._get_remote_lock_file()):
                os.makedirs(os.path.dirname(self._get_remote_lock_file()))
            if not os.path.isdir(d_ := os.path.dirname(self._get_remote_lock_file())):
                os.makedirs(d_)
            with open(self._get_remote_lock_file(), 'w') as f:
                f.write("If this file is present, we will not synchronize this directory with a remote (using report.url).\nThis is a very good idea during development, but the lock-file should be disabled (in gitignore) for the students.")

        from unitgrade import evaluate_report_student
        evaluate_report_student(self, unmute=verbose, noprogress=not verbose, generate_artifacts=False) # Disable artifact generation.
        # self.main()  # Run all tests in class just to get that out of the way...
        report_cache = {}
        for q, _ in self.questions:
            # print(self.questions)
            if hasattr(q, '_save_cache'):
                q()._save_cache()
                # print("q is", q())
                report_cache[q.__qualname__] = q._cache2
            else:
                report_cache[q.__qualname__] = {'no cache see _setup_answers in framework.py': True}
        if with_coverage:
            for q, _ in self.questions:
                q._with_coverage = False

            # report_cache is saved on a per-question basis.
        # it could also contain additional information such as runtime metadata etc. This may not be appropriate to store with the invidivual questions(?).
        # In this case, the function should be re-defined.
        return report_cache

    def set_payload(self, payloads, strict=False):
        for q, _ in self.questions:
            q._cache = payloads[q.__qualname__]
        self._config = payloads['config']

    def _get_remote_lock_file(self):
        return os.path.join(os.path.dirname( self._artifact_file() ), "dont_check_remote.lock")

    def _check_remote_versions(self):
        if self.url is None: # No url, no problem.
            return

        if os.path.isfile(self._get_remote_lock_file() ):
            print("Since the file", self._get_remote_lock_file(), "was present I will not compare the files on this computer with git")
            print("i.e., I am assuming this is being run on the teachers computer. Remember to put the file in .gitignore for the students!")
            return

        if self._file().endswith("_complete.py"):
            print("Unitgrade> You are trying to check the remote version of a *_tests_complete.py-file, and you will potentially overwrite part of this file.")
            print("Unitgrade> Please add a unitgrade_data/note_remote_check.lock - file to this directory (and put it in the .gitignore) to avoid data loss.")
            print(self._file())
            raise Exception("Unitgrade> You are trying to check the remote version of a *_tests_complete.py-file, and you will potentially overwrite part of this file.")

        # print("CHECKING THE REMOTE VERSION. ")
        print("Unitgrade> Checking the remote version...")
        url = self.url
        if not url.endswith("/"):
            url += "/"

        db = DKPupDB("check_on_remote")

        if 'last_check_time' in db:
            # with open(snapshot_file, 'r') as f:
            t = db['last_check_time']
            if (time.time() - t) < self._remote_check_cooldown_seconds:
                return
            db['last_check_time'] = time.time()


        if self.url.startswith("https://gitlab"):
            # Try to turn url into a 'raw' format.
            # "https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/examples/autolab_example_py_upload/instructor/cs102_autolab/report2_test.py?inline=false"
            # url = self.url
            url = url.replace("-/tree", "-/raw")
            url = url.replace("-/blob", "-/raw")
            # print(url)
            # "https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/tree/master/examples/autolab_example_py_upload/instructor/cs102_autolab"
            # "https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/examples/autolab_example_py_upload/instructor/report2_test.py?inline=false"
            # "https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/examples/autolab_example_py_upload/instructor/cs102_autolab/report2_test.py?inline=false"
            raw_url = urllib.parse.urljoin(url, os.path.basename(self._file()) + "?inline=false")
            # raw_url = url
            # print("Is this file run in local mode?", self._is_run_in_grade_mode())
            if self._is_run_in_grade_mode():
                remote_source = requests.get(raw_url).text
                with open(self._file(), 'r') as f:
                    local_source = f.read()
                if local_source != remote_source:
                    print("\nThe local version of this report is not identical to the remote version which can be found at")
                    print(self.url)
                    print("The most likely reason for this is that the remote version was updated by the teacher due to an issue.")
                    print("You can find the most recent code here:")
                    print(self.url)
                    raise Exception(f"Version of grade script does not match the remote version. Please update your grade script.")
            else:
                text = requests.get(raw_url).text
                node = ast.parse(text)
                classes = [n for n in node.body if isinstance(n, ast.ClassDef) if n.name == self.__class__.__name__][0]
                version_remote = None
                for b in classes.body:
                    # print(b.)
                    if b.targets[0].id == "version":
                        version_remote = b.value.value
                        break

                if version_remote is not None and version_remote != self.version:
                    print("\nThe version of this report", self.version, "does not match the version of the report on git:", version_remote)
                    print("The most likely reason for this is that the remote version was updated by the teacher due to some issue.")
                    print("What I am going to do is to download the correct version from git so you are up to date. ")

                    print("You should check if there was an announcement and update the test to the most recent version. This can be done by downloading the files in")
                    print(self.url)
                    print("and putting them in the corresponding folder on your computer.")
                    with open(self._file(), "w") as f:
                        f.write(text)

                    raise Exception(f"Version of test on remote is {version_remote}, which is different than this version of the test {self.version}. I have manually updated your tests.")

                for (q, _) in self.questions:
                    if issubclass(q, UTestCase):
                        qq = q(skip_remote_check=True)
                        cfile = q._cache_file()
                        if not os.path.isdir(d_ := os.path.dirname(cfile)):
                            os.makedirs(d_)  # The unitgrade_data directory does not exist so we create it.

                        relpath = os.path.relpath(cfile, os.path.dirname(self._file()))
                        relpath = relpath.replace("\\", "/")
                        raw_url = urllib.parse.urljoin(url, relpath + "?inline=false")

                        if os.path.isfile(cfile):
                            with open(cfile, 'rb') as f:
                                b1 = f.read()
                        else:
                            b1 = bytes() # No pkl file exists. We set it to the empty string.

                        b2 = requests.get(raw_url).content
                        if b1 != b2:
                            print("\nQuestion ", qq.title, "relies on the data file", cfile)
                            print("However, it appears that this file is missing or in a different version than the most recent found here:")
                            print(self.url)
                            print("The most likely reason for this is that the remote version was updated by the teacher.")
                            print("I will now try to download the file automatically, WCGW?")
                            with open(cfile, 'wb') as f:
                                f.write(b2)
                            print("Local data file updated successfully.")
                            # print("You should check if there was an announcement and update the test to the most recent version; most likely")
                            # print("This can be done by simply running the command")
                            # print("> git pull")
                            # print("to avoid running bad tests against good code, the program will now stop. Please update and good luck!")
                            # raise Exception("The data file for the question", qq.title, "did not match remote source found on git. The test will therefore automatically fail. Please update your test/data files.")

                # t = time.time()
                if os.path.isdir(os.path.dirname(self._file()) + "/unitgrade_data"):
                    db['last_check_time'] = time.time()

                    # with open(snapshot_file, 'w') as f:
                    #     f.write(f"{t}")

def get_hints(ss):
    """ Extract all blocks of the forms:

    Hints:
    bla-bla.

    and returns the content unaltered.
    """
    if ss == None:
        return None
    try:
        ss = textwrap.dedent(ss)
        ss = ss.replace('''"""''', "").strip()
        hints = ["hints:", "hint:"]
        indexes = [ss.lower().find(h) for h in hints]
        j = np.argmax(indexes)
        if indexes[j] == -1:
            return None
        h = hints[j]
        ss = ss[ss.lower().find(h) + len(h) + 1:]
        ss = "\n".join([l for l in ss.split("\n") if not l.strip().startswith(":")])
        ss = textwrap.dedent(ss).strip()
        # if ss.startswith('*'):
        #     ss = ss[1:].strip()
        return ss
    except Exception as e:
        print("bad hints", ss, e)



class UTestCase(unittest.TestCase):
    # a = 234

    api = "053eccb9234af62a683b5733d8c00138ed601a43"  # secret key
    # How should it work?
    # Sync errors online.


    _outcome = None  # A dictionary which stores the user-computed outcomes of all the tests. This differs from the cache.
    _cache = None  # Read-only cache. Ensures method always produce same result.
    _cache2 = None  # User-written cache.
    _with_coverage = False
    _covcache = None # Coverage cache. Written to if _with_coverage is true.
    _report = None  # The report used. This is very, very hacky and should always be None. Don't rely on it!
    _run_in_report_mode = True

    _generate_artifacts = True # Whether the file will generate the artifact .json files. This is used in the _grade-script mode.
    # If true, the tests will not fail when cache is used. This is necesary since otherwise the cache will not be updated
    # during setup, and the deploy script must be run many times.
    _setup_answers_mode = False

    def capture(self):
        if hasattr(self, '_stdout') and self._stdout is not None:
            file = self._stdout
        else:
            file = sys.stdout
        return Capturing2(stdout=file)

    @classmethod
    def question_title(cls):
        """ Return the question title """
        if cls.__doc__ is not None:
            title = cls.__doc__.strip().splitlines()[0].strip()
            if not (title.startswith("Hints:") or title.startswith("Hint:") ):
                return title
        return cls.__qualname__

    def run(self, result):
        # print("Run called in test framework...", self._generate_artifacts)
        if not self._generate_artifacts:
            return super().run(result)

        # print(result)
        mute = False
        if isinstance(result, UTextResult):
            # print(result.show_errors_in_grade_mode)
            mute = not result.show_errors_in_grade_mode
        else:
            pass
            # print("this' not a text result.")
        # print(result.show_errors_in_grade_mode)
        from unitgrade.artifacts import StdCapturing
        from unitgrade.utils import DKPupDB
        self._error_fed_during_run = [] # Initialize this to be empty.

        db = DKPupDB(self._testcase_artifact_file(), register_ephemeral=True)
        db.set("state", "running")
        db.set('run_id', np.random.randint(1000*1000))
        db.set('coverage_files_changed', None)

        _stdout = sys.stdout
        _stderr = sys.stderr
        # mute = True
        std_capture = StdCapturing(stdout=sys.stdout, stderr=sys.stderr, db=db, mute=mute)

        state_ = None
        try:
            # Run this unittest and record all of the output.
            # This is probably where we should hijack the stdout output and save it -- after all, this is where the test is actually run.
            sys.stderr = std_capture.dummy_stderr
            sys.stdout = std_capture.dummy_stdout

            result_ = TestCase.run(self, result)
            from werkzeug.debug.tbtools import DebugTraceback, _process_traceback

            # What could be nice to upload?
            # When the files are edited?
            # When tests are run?
            # how to register it? (report, question, user...)
            # print(result_._excinfo[0])
            actual_errors = []
            for test, err in self._error_fed_during_run:
                if err is None:
                    continue
                else:
                    import traceback
                    actual_errors.append(err)

            if len(actual_errors) > 0:
                ex, exi, tb = actual_errors[0]
                exi.__traceback__ = tb
                dbt = DebugTraceback(exi)

                sys.stderr.write(dbt.render_traceback_text())
                html = dbt.render_traceback_html(include_title="hello world")
                db.set('wz_stacktrace', html)
                state_ = "fail"
            else:
                state_ = "pass"
        except Exception as e:
            state_ = "fail"
            import traceback
            traceback.print_exc()
            raise e
        finally:
            db.set('state', state_)
            std_capture.dummy_stdout.write_mute(_DASHBOARD_COMPLETED_MESSAGE)
            sys.stdout = _stdout
            sys.stderr = _stderr
            std_capture.close()
        return result_

    def _callSetUp(self):
        if self._with_coverage:
            if self._covcache is None:
                self._covcache = {}
            import coverage
            self.cov = coverage.Coverage(data_file=None)
            self.cov.start()
        self.setUp()


    def _callTearDown(self):
        self.tearDown()
        # print("TEaring down.")
        if self._with_coverage:
            # print("TEaring down with coverage")
            from pathlib import Path
            from snipper import snipper_main
            try:
                self.cov.stop()
            except Exception as e:
                print("Something went wrong while tearing down coverage test")
                print(e)
            data = self.cov.get_data()
            base, _, _ = self._report._import_base_relative()
            for file in data.measured_files():
                # print(file)
                file = os.path.normpath(file)
                root = Path(base)
                child = Path(file)
                if root in child.parents:
                    with open(child, 'r') as f:
                        s = f.read()
                    lines = s.splitlines()
                    garb = 'GARBAGE'
                    lines2 = snipper_main.censor_code(lines, keep=True)
                    if len(lines) != len(lines2):
                        for k in range(len(lines)):
                            print(k, ">", lines[k], "::::::::", lines2[k])
                        print("Snipper failure; line lenghts do not agree. Exiting..")
                        print(child, "len(lines) == len(lines2)", len(lines), len(lines2))
                        import sys
                        sys.exit()

                    assert len(lines) == len(lines2)
                    for ll in data.contexts_by_lineno(file):

                        l = ll-1
                        # print(l, lines2[l])
                        if l < len(lines2) and lines2[l].strip() == garb:
                            # print("Got one.")
                            rel = os.path.relpath(child, root)
                            cc = self._covcache
                            j = 0
                            for j in range(l, -1, -1):
                                if "def" in lines2[j] or "class" in lines2[j]:
                                    break
                            from snipper.legacy import gcoms

                            fun = lines2[j]
                            comments, _ = gcoms("\n".join(lines2[j:l]))
                            if rel not in cc:
                                cc[rel] = {}
                            cc[rel][fun] = (l, "\n".join(comments))
                            # print("found", rel, fun)
                            # print(file, ll)
                            self._cache_put((self.cache_id(), 'coverage'), self._covcache)

    def shortDescriptionStandard(self):
        sd = super().shortDescription()
        if sd is None or sd.strip().startswith("Hints:") or sd.strip().startswith("Hint:"):
            sd = self._testMethodName
        return sd

    def shortDescription(self):
        sd = self.shortDescriptionStandard()
        title = self._cache_get((self.cache_id(), 'title'), sd)
        return title if title is not None else sd

    @property
    def title(self):
        return self.shortDescription()

    @title.setter
    def title(self, value):
        self._cache_put((self.cache_id(), 'title'), value)

    def _get_outcome(self):
        if not hasattr(self.__class__, '_outcome') or self.__class__._outcome is None:
            self.__class__._outcome = {}
        return self.__class__._outcome

    def _callTestMethod(self, testMethod):
        t = time.time()
        self._ensure_cache_exists()  # Make sure cache is there.
        if self._testMethodDoc is not None:
            self._cache_put((self.cache_id(), 'title'), self.shortDescriptionStandard())

        self._cache2[(self.cache_id(), 'assert')] = {}
        res = testMethod()
        elapsed = time.time() - t
        self._get_outcome()[ (self.cache_id(), "return") ] = res
        self._cache_put((self.cache_id(), "time"), elapsed)


    def cache_id(self):
        c = self.__class__.__qualname__
        m = self._testMethodName
        return c, m

    def __init__(self, *args, skip_remote_check=False, **kwargs):
        super().__init__(*args, **kwargs)
        # print(f"INIT CALED IN {self}")

        self._load_cache()
        self._assert_cache_index = 0
        if skip_remote_check:
            return
        import importlib, inspect
        found_reports = []
        good_module_name = self.__module__
        try:
            importlib.import_module(good_module_name)
        except Exception as e:
            good_module_name = os.path.basename(good_module_name)[:-3]

        # This will delegate you to the wrong main clsas when running in grade mode.
        #  for name, cls in inspect.getmembers(importlib.import_module(self.__module__), inspect.isclass):
        for name, cls in inspect.getmembers(importlib.import_module(good_module_name), inspect.isclass):
            if issubclass(cls, Report):
                for q,_ in cls.questions:
                    if self.__class__.__name__ == q.__name__:
                        found_reports.append(cls)
        if len(found_reports) == 0:
            pass # This case occurs when the report _grade script is being run.
            # raise Exception("This question is not a member of a report. Very, very odd.")
        if len(found_reports) > 1:
            raise Exception("This question is a member of multiple reports. That should not be the case -- don't get too creative.")
        if len(found_reports) > 0:
            report = found_reports[0]
            try:
                r_ = report()
                if not r_._is_run_in_grade_mode(): # Disable url request handling during evaluation.
                    r_._check_remote_versions()
            except Exception as e:
                print("Unitgrade> Warning, I tried to compare with the remote source for this report but was unable to do so.")
                print(e)
                print("Unitgrade> The exception was", e)

    def _ensure_cache_exists(self):
        if not hasattr(self.__class__, '_cache') or self.__class__._cache == None:
            self.__class__._cache = dict()
        if not hasattr(self.__class__, '_cache2') or self.__class__._cache2 == None:
            self.__class__._cache2 = dict()

    def _cache_get(self, key, default=None):
        self._ensure_cache_exists()
        return self.__class__._cache.get(key, default)

    def _cache_put(self, key, value):
        self._ensure_cache_exists()
        self.__class__._cache2[key] = value

    def _cache_contains(self, key):
        self._ensure_cache_exists()
        return key in self.__class__._cache

    def get_expected_test_value(self):
        key = (self.cache_id(), 'assert')
        id = self._assert_cache_index
        cache = self._cache_get(key)
        _expected = cache.get(id, f"Key {id} not found in cache; framework files missing. Please run deploy()")
        return _expected

    def wrap_assert(self, assert_fun, first, *args, **kwargs):
        key = (self.cache_id(), 'assert')
        if not self._cache_contains(key):
            print("Warning, framework missing", key)
            self.__class__._cache[key] = {}  # A new dict. We manually insert it because we have to use that the dict is mutable.
        cache = self._cache_get(key)
        id = self._assert_cache_index
        _expected = cache.get(id, f"Key {id} not found in cache; framework files missing. Please run deploy()")
        if not id in cache:
            print("Warning, framework missing cache index", key, "id =", id, " - The test will be skipped for now.")
            if self._setup_answers_mode:
                _expected = first # Bypass by setting equal to first. This is in case multiple self.assertEqualC's are run in a row and have to be set.

        # The order of these calls is important. If the method assert fails, we should still store the correct result in cache.
        cache[id] = first
        self._cache_put(key, cache)
        self._assert_cache_index += 1
        if not self._setup_answers_mode:
            assert_fun(first, _expected, *args, **kwargs)
        else:
            try:
                assert_fun(first, _expected, *args, **kwargs)
            except Exception as e:
                print("Mumble grumble. Cache function failed during class setup. Most likely due to old cache. Re-run deploy to check it pass.", id)
                print("> first", first)
                print("> expected", _expected)
                print(e)


    def assertEqualC(self, first, msg=None):
        self.wrap_assert(self.assertEqual, first, msg)

    def _shape_equal(self, first, second):
        a1 = np.asarray(first).squeeze()
        a2 = np.asarray(second).squeeze()
        msg = None
        msg = "" if msg is None else msg
        if len(msg) > 0:
            msg += "\n"
        self.assertEqual(a1.shape, a2.shape, msg=msg + "Dimensions of input data does not agree.")
        assert(np.all(np.isinf(a1) == np.isinf(a2)))  # Check infinite part.
        a1[np.isinf(a1)] = 0
        a2[np.isinf(a2)] = 0
        diff = np.abs(a1 - a2)
        return diff

    def assertLinf(self, first, second=None, tol=1e-5, msg=None):
        """ Test in the L_infinity norm.
        :param first:
        :param second:
        :param tol:
        :param msg:
        :return:
        """
        if second is None:
            return self.wrap_assert(self.assertLinf, first, tol=tol, msg=msg)
        else:
            diff = self._shape_equal(first, second)
            np.testing.assert_allclose(first, second, atol=tol)
            
            max_diff = max(diff.flat)
            if max_diff >= tol:
                from unittest.util import safe_repr
                # msg = f'{safe_repr(first)} != {safe_repr(second)} : Not equal within tolerance {tol}'
                # print(msg)
                # np.testing.assert_almost_equal
                # import numpy as np
                print(f"|first - second|_max = {max_diff} > {tol} ")
                np.testing.assert_almost_equal(first, second)
                # If the above fail, make sure to throw an error:
                self.assertFalse(max_diff >= tol, msg=f'Input arrays are not equal within tolerance {tol}')
                # self.assertEqual(first, second, msg=f'Not equal within tolerance {tol}')

    def assertL2(self, first, second=None, tol=1e-5, msg=None, relative=False):
        if second is None:
            return self.wrap_assert(self.assertL2, first, tol=tol, msg=msg, relative=relative)
        else:
            # We first test using numpys build-in testing method to see if one coordinate deviates a great deal.
            # This gives us better output, and we know that the coordinate wise difference is lower than the norm difference.
            if not relative:
                np.testing.assert_allclose(first, second, atol=tol)
            diff = self._shape_equal(first, second)
            diff = ( ( np.asarray( diff.flatten() )**2).sum() )**.5

            scale = (2/(np.linalg.norm(np.asarray(first).flat) + np.linalg.norm(np.asarray(second).flat)) ) if relative else 1
            max_diff = diff*scale
            if max_diff >= tol:
                msg = "" if msg is None else msg
                print(f"|first - second|_2 = {max_diff} > {tol} ")
                # Deletage to numpy. Let numpy make nicer messages.
                np.testing.assert_almost_equal(first, second) # This function does not take a msg parameter.
                # Make sure to throw an error no matter what.
                self.assertFalse(max_diff >= tol, msg=f'Input arrays are not equal within tolerance {tol}')
                # self.assertEqual(first, second, msg=msg + f"Not equal within tolerance {tol}")

    @classmethod
    def _cache_file(cls):
        # This seems required because python can throw an exception that cls is a 'built-in'(??) when it
        # isn't. I don't know what causes it, but it may be the test system.
        try:
            module_name = inspect.getabsfile(cls)
        except Exception as e:
            module_name = cls.__module__
        return os.path.dirname(module_name) + "/unitgrade_data/" + cls.__name__ + ".pkl"
        # return os.path.dirname(inspect.getabsfile(cls)) + "/unitgrade_data/" + cls.__name__ + ".pkl"

    @classmethod
    def _artifact_file_for_setUpClass(cls):
        file = os.path.join(os.path.dirname(cls._cache_file()), ""+cls.__name__+"-setUpClass.json")
        print("_artifact_file_for_setUpClass(cls): will return", file, "__class__", cls)
        # cf = os.path.dirname(inspect.getabsfile(cls)) + "/unitgrade_data/" + cls.__name__
        return file

    def _testcase_artifact_file(self):
        """ As best as I can tell, this file is only used as an index (key) in the db. For historical reasons it is formatted as a .json
        but the file will not actually be written to. """
        return os.path.join(os.path.dirname(self.__class__._cache_file()), '-'.join(self.cache_id()) + ".json")

    def _save_cache(self):
        # get the class name (i.e. what to save to).
        cfile = self.__class__._cache_file()
        if not os.path.isdir(os.path.dirname(cfile)):
            os.makedirs(os.path.dirname(cfile))

        if hasattr(self.__class__, '_cache2'):
            with open(cfile, 'wb') as f:
                pickle.dump(self.__class__._cache2, f)

    # But you can also set cache explicitly.
    def _load_cache(self):
        if self._cache is not None:  # Cache already loaded. We will not load it twice.
            return
            # raise Exception("Loaded cache which was already set. What is going on?!")
        # str(self.__class__)

        cfile = self.__class__._cache_file()
        if os.path.exists(cfile):
            try:
                with open(cfile, 'rb') as f:
                    data = pickle.load(f)
                self.__class__._cache = data
            except Exception as e:
                print("Cache file did not exist:", cfile)
                print(e)
        else:
            print("Warning! data file not found", cfile)

    def _get_coverage_files(self):
        key = (self.cache_id(), 'coverage')
        # CC = None
        # if self._cache_contains(key):
        return self._cache_get(key, []) # Anything wrong with the empty list?
        # return CC

    def _get_hints(self):
        """
            This code is run when the test is set up to generate the hints and store them in an artifact file. It may be beneficial to simple compute them beforehand
            and store them in the local unitgrade pickle file. This code is therefore expected to superceede the alterative code later.
        """
        hints = []
        # print("Getting hint")
        key = (self.cache_id(), 'coverage')
        if self._cache_contains(key):
            CC = self._cache_get(key)
            # cl, m = self.cache_id()
            # print("Getting hint using", CC)
            # Insert newline to get better formatting.
            # gprint(
            #     f"\n> An error occured during the test: {cl}.{m}. The following files/methods has code in them you are supposed to edit and may therefore be the cause of the problem:")
            for file in CC:
                rec = CC[file]
                # gprint(f">   * {file}")
                for l in rec:
                    _, comments = CC[file][l]
                    hint = get_hints(comments)

                    if hint != None:
                        hints.append((hint, file, l))

        doc = self._testMethodDoc
        # print("doc", doc)
        if doc is not None:
            hint = get_hints(self._testMethodDoc)
            if hint is not None:
                hints = [(hint, None, self.cache_id()[1])] + hints

        return hints

    def _feedErrorsToResult(self, result, errors):
        """ Use this to show hints on test failure.
        It feeds error to the result -- so if there are errors, they will crop up here
        """
        self._error_fed_during_run = errors.copy() # import to copy the error list.

        # result._test._error_fed_during_run = errors.copy()

        if not isinstance(result, UTextResult):
            er = [e for e, v in errors if v != None]
            # print("Errors are", errors)
            if len(er) > 0:
                hints = []
                key = (self.cache_id(), 'coverage')
                if self._cache_contains(key):
                    CC = self._cache_get(key)
                    cl, m = self.cache_id()
                    # Insert newline to get better formatting.
                    gprint(f"\n> An error occured during the test: {cl}.{m}. The following files/methods has code in them you are supposed to edit and may therefore be the cause of the problem:")
                    for file in CC:
                        rec = CC[file]
                        gprint(f">   * {file}")
                        for l in rec:
                            _, comments = CC[file][l]
                            hint = get_hints(comments)

                            if hint != None:
                                hints.append((hint, file, l) )
                            gprint(f">      - {l}")

                er = er[0]

                doc = er._testMethodDoc
                # print("doc", doc)
                if doc is not None:
                    hint = get_hints(er._testMethodDoc)
                    if hint is not None:
                        hints = [(hint, None, self.cache_id()[1] )] + hints
                if len(hints) > 0:
                    # print(hints)
                    for hint, file, method in hints:
                        s = (f"'{method.strip()}'" if method is not None else "")
                        if method is not None and file is not None:
                            s += " in "
                        try:
                            s += (file.strip() if file is not None else "")
                            gprint(">")
                            gprint("> Hints (from " + s + ")")
                            gprint(textwrap.indent(hint, ">   "))
                        except Exception as e:
                            print("Bad stuff in hints. ")
                            print(hints)
        # result._last_errors = errors
        super()._feedErrorsToResult(result, errors)
        b = 234

    def startTestRun(self):
        super().startTestRun()

class Required:
    pass

class ParticipationTest(UTestCase,Required):
    max_group_size = None
    students_in_group = None
    workload_assignment = {'Question 1': [1, 0, 0]}

    def test_students(self):
        pass

    def test_workload(self):
        pass

# 817, 705
class NotebookTestCase(UTestCase):
    notebook = None
    _nb = None
    @classmethod
    def setUpClass(cls) -> None:
        f = cls._cache_file()
        # print(f)
        file = os.path.dirname(os.path.dirname(f)) + "/" + cls.notebook
        # print(f"{f=}, {file=}, {cls.notebook=}")
        # print(__file__)
        print(os.path.curdir)
        # print("cwd", os.getcwd())
        with Capturing():
            # print(__file__)
            f = cls._cache_file()
            # print(f)
            file = os.path.dirname(os.path.dirname(f)) + "/" + cls.notebook
            cls._nb = importnb.Notebook.load_argv(file + " -nograde")

    @property
    def nb(self):
        return self.__class__._nb
 # 870.