import fnmatch
from threading import Lock
import time
import datetime
import os
import logging
import sys
import glob
from flask import Flask, render_template
from flask_socketio import SocketIO
from unitgrade.utils import load_token
from unitgrade.dashboard.app_helpers import get_available_reports, _run_test_cmd
from unitgrade.dashboard.watcher import Watcher
from unitgrade.dashboard.file_change_handler import FileChangeHandler
from unitgrade.utils import DKPupDB
from unitgrade.dashboard.dbwatcher import DBWatcher
from diskcache import Cache
logging.getLogger('werkzeug').setLevel("WARNING")

def mkapp(base_dir="./", use_command_line=True):
    print("BUILDING THE APPLICATION ONCE!")
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
    x = {'watcher': None, 'handler': None, 'db_watcher': None}  # maintain program state across functions.
    app.config["SECRET_KEY"] = "secret!"
    app.config["fd"] = None
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["child_pid"] = None
    socketio = SocketIO(app)
    available_reports = get_available_reports(jobfolder=base_dir)
    current_report = {}
    watched_files_lock = Lock()
    watched_files_dictionary = {}

    def test_handle_function(key, db):
        state = db.get('state')
        wz = db.get('wz_stacktrace') if 'wz_stacktrace' in db.keys() else None
        if wz is not None:
            wz = wz.replace('<div class="traceback">', f'<div class="traceback"><div class="{key}-traceback">')
            wz += "</div>"
        coverage_files_changed = db.get('coverage_files_changed') if 'coverage_files_changed' in db.keys() else None
        if state == "fail":
            pass

        socketio.emit('testupdate', {"id": key, 'state': state, 'stacktrace': wz, 'stdout': db.get('stdout'),
                                     'run_id': db.get('run_id'),
                                     'coverage_files_changed': coverage_files_changed}, namespace="/status")

    def do_something(file_pattern):
        """
        `file` has changed on disk. We need to open it, look at it, and then do stuff based on what is in it.
        Then push all changes to clients.
        """
        with watched_files_lock:
            file = watched_files_dictionary[file_pattern]['file']
            type = watched_files_dictionary[file_pattern]['type']
            lrc = watched_files_dictionary[file_pattern]['last_recorded_change']

        if type == 'question_json': # file.endswith(".json"); these no longer exists so this should never be triggered.
            if file is None:
                return # There is nothing to do, the file does not exist.
        elif type =='coverage':
            if lrc is None: # Program startup. We don't care about this.
                return

            for q in current_report['questions']:
                for i in current_report['questions'][q]['tests']:
                    test_invalidated = False
                    for f in current_report['questions'][q]['tests'][i]['coverage_files']:
                        if fnmatch.fnmatch(file, "**/" + f):
                            # This file has been matched. The question is now invalid.
                            test_invalidated = True
                            break
                    if test_invalidated:
                        dbf = current_report['root_dir'] + "/" + current_report['questions'][q]['tests'][i]['artifact_file']
                        db2 = DKPupDB(dbf)
                        print("A test has been invalidated. Setting coverage files", file, dbf)
                        db2.set('coverage_files_changed', [file])

        elif type =="token":
            if file is not None:
                a, b = load_token(file)
                rs = {}
                for k in a['details']:
                    for ikey in a['details'][k]['items']:
                        rs['-'.join(ikey)] = a['details'][k]['items'][ikey]['status']
                socketio.emit('token_update', {"full_path": file, 'token': os.path.basename(file),
                                               'results': rs, 'state': 'evaluated'}, namespace="/status")
        else:
            raise Exception("Bad type: " + type)

    def select_report_file(json):
        current_report.clear()
        for k, v in available_reports[json].items():
            current_report[k] = v

        def mkempty(pattern, type):
            fls = glob.glob(current_report['root_dir'] + pattern)
            fls.sort(key=os.path.getmtime)
            f = None if len(fls) == 0 else fls[-1] # Bootstrap with the given best matched file.
            return {'type': type, 'last_recorded_change': None, 'last_handled_change': None, 'file': f}

        watched_blocks = []
        with watched_files_lock:
            watched_files_dictionary.clear()
            for q in current_report['questions'].values():
                for i in q['tests'].values():
                    file = "*/"+i['artifact_file']
                    watched_blocks.append(os.path.basename( i['artifact_file'])[:-5])
                    watched_files_dictionary[file] = mkempty(file, 'question_json')  # when the file was last changed and when that change was last handled. Superflous.
                    for c in i['coverage_files']:
                        file = "*/"+c
                        watched_files_dictionary[file] = mkempty(file, "coverage")

            # tdir = "*/"+os.path.dirname(current_report['relative_path_token']) + "/" + os.path.basename(current_report['relative_path'])[:-3] + "*.token"
            tdir = "*/"+current_report['token_stub'] + "*.token"
            watched_files_dictionary[tdir] = mkempty(tdir, 'token')

        for l in ['watcher', 'handler', 'db_watcher']:
            if x[l] is not None: x[l].close()

        x['watcher'] = Watcher(current_report['root_dir'], watched_files_dictionary, watched_files_lock)
        x['watcher'].run()

        x['handler'] = FileChangeHandler(watched_files_dictionary, watched_files_lock, do_something)
        x['handler'].start()

        x['db_watcher'] = DBWatcher(os.path.dirname( current_report['json'] ), watched_blocks, test_handle_function=test_handle_function)
        x['db_watcher'].start()


    if len(available_reports) == 0:
        print("Unitgrade was launched in the directory")
        print(">", base_dir)
        print("But this directory does not contain any reports. Please run unitgrade from a directory which contains report files.")
        sys.exit()

    select_report_file(list(available_reports.keys()).pop())

    @socketio.on("ping", namespace="/status") # Unclear if used.
    def ping():
        json = current_report['json']
        socketio.emit("pong", {'base_json': json})

    @app.route("/info")
    def info_page():
        db = Cache( os.path.dirname( current_report['json'] ) )
        info = {k: db[k] for k in db}
        return render_template("info.html", **current_report, available_reports=available_reports, db=info)

    @app.route("/")
    def index_bare():
        return index(list(available_reports.values()).pop()['menu_name'])

    @app.route("/report/<report>")
    def index(report):
        if report != current_report['menu_name']:
            for k, r in available_reports.items():
                if report == r['menu_name']:
                    select_report_file(k)
            raise Exception("Bad report selected", report)

        rs = current_report
        qenc = rs['questions']
        x = {}
        for k, v in current_report.items():
            x[k] = v
        x['questions'] = {}

        for q in qenc:
            x['questions'][q] = current_report['questions'][q].copy()
            items = {}
            for it_key, it_value in current_report['questions'][q]['tests'].items():
                it_key_js = "-".join(it_key)
                # do a quick formatting of the hints. Split into list by breaking at *.
                hints = it_value['hints']
                hints = [] if hints is None else hints.copy()
                for k in range(len(hints)):
                    ahints = []
                    for h in hints[k][0].split("\n"):
                        if h.strip().startswith("*"):
                            ahints.append('')
                            h = h.strip()[1:]
                        if len(ahints) == 0: # In case we forgot to add a *-mark in front of the hint.
                            ahints.append('')
                        ahints[-1] += "\n" + h
                    hints[k] = (ahints, hints[k][1], hints[k][2])
                # items[it_key_js] =
                items[it_key_js] = {'title': it_value['title'], 'hints': hints, 'runable': it_value['title'] != 'setUpClass', "coverage_files": it_value['coverage_files']}
            x['questions'][q]['tests'] = items # = current_report['questions'][q] # {'title': qenc[q]['title'], 'tests': items}

        run_cmd_grade = '.'.join(x['modules']) + "_grade"
        x['grade_script'] = x['modules'][-1] + "_grade.py"
        x['run_cmd_grade'] = f"python -m {run_cmd_grade}"
        x['available_reports'] = available_reports
        return render_template("index3.html", **x)

    @socketio.on("rerun", namespace="/status")
    def rerun(data):
        t0 = time.time()
        """write to the child pty. The pty sees this as if you are typing in a real
        terminal.
        """
        targs = ".".join( data['test'].split("-") )
        m = '.'.join(current_report['modules'])
        _run_test_cmd(dir=current_report['root_dir'], module_name=m, test_spec=targs, use_command_line=use_command_line)
        for q in current_report['questions']:
            for i in current_report['questions'][q]['tests']:
                if "-".join(i) == data['test']:
                    with watched_files_lock:
                        watched_files_dictionary["*/"+current_report['questions'][q]['tests'][i]['artifact_file']]['last_recorded_change'] = datetime.datetime.now()
        print("rerun tests took", time.time()-t0)


    @socketio.on("rerun_all", namespace="/status")
    def rerun_all(data):
        """write to the child pty. The pty sees this as if you are typing in a real
        terminal.
        """
        m = '.'.join(current_report['modules'])
        _run_test_cmd(dir=current_report['root_dir'], module_name=m, test_spec="", use_command_line=use_command_line)

    @app.route("/crash")
    def navbar():
        assert False

    @app.route('/wz')
    def wz():
        return render_template('wz.html')

    # @socketio.event
    # def connect(sid, environ):
    #     print(environ)
    #     print(sid)

    @socketio.on("reconnected", namespace="/status")
    def client_reconnected(data):
        """write to the child pty. The pty sees this as if you are typing in a real
        terminal.
        """
        print("--------Client has reconnected----------")
        # sid = 45;
        # print(f"{sid=}, {data=}")
        with watched_files_lock:
            for k in watched_files_dictionary:
                if watched_files_dictionary[k]['type'] in ['token', 'question_json']:
                    watched_files_dictionary[k]['last_handled_change'] = None
                elif watched_files_dictionary[k]['type'] == 'coverage':
                    pass
                else:
                    raise Exception()
        x['client_id'] = data['id']
        x['db_watcher'].mark_all_as_fresh()

    closeables = [x['watcher'], x['handler'], x['db_watcher']]
    return app, socketio, closeables

def main():
    # from cs108 import deploy
    # from cs108.report_devel import mk_bad
    # deploy.main(with_coverage=True) # Deploy for debug.
    # mk_bad()
    # bdir = os.path.dirname(deploy.__file__)
    bdir = "/home/tuhe/Documents/02002students_complete/cp/project5"


    args_port = 5000
    args_host = "127.0.0.1"

    app, socketio, closeables = mkapp(base_dir=bdir)
    debug = False
    logging.info(f"serving on http://{args_host}:{args_port}")
    os.environ["WERKZEUG_DEBUG_PIN"] = "off"
    socketio.run(app, debug=debug, port=args_port, host=args_host, allow_unsafe_werkzeug=True)
    for c in closeables:
        c.close()
    sys.exit()

if __name__ == "__main__":
    main() # 386