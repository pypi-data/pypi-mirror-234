#!/usr/bin/env python3
import sys
import subprocess
import unittest
import os
import glob
import pickle
from pathlib import Path

def get_available_reports(jobfolder):
    bdir = os.path.abspath(jobfolder)
    available_reports = {}
    if os.path.isdir(bdir):
        fls = glob.glob(bdir + "/**/main_config_*.artifacts.pkl", recursive=True)
    elif os.path.isfile(bdir):
        fls = glob.glob(os.path.dirname(bdir) + "/**/main_config_*.artifacts.pkl", recursive=True)
    else:
        raise Exception("No report files found in the given directory. Start the dashboard in a folder which contains a report test file.")

    for f in fls:
        with open(f, 'rb') as file:
            db = pickle.load(file)

        # db = PupDB(f)

        report_py = db['relative_path']
        lpath_full = Path(os.path.normpath(os.path.dirname(f) + f"/../{os.path.basename(report_py)}"))
        # rpath =
        base = lpath_full.parts[:-len(Path(report_py).parts)]

        # rs['local_base_dir_for_test_module'] = str(Path(*base))
        # print("root_dir", base)
        # print(f"{lpath_full=}")
        root_dir = str(Path(*base))
        # print(f"{root_dir=}")
        # print(f"{base=}")
        # print(f"{report_py=}")

        # lpath_full = Path(os.path.normpath(os.path.dirname(dbjson) + "/../" + os.path.basename(dbjson)[12:].split(".")[0] + ".py"))
        # rpath = Path(rs['relative_path'])
        # base = lpath_full.parts[:-len(rpath.parts)]

        # rs['local_base_dir_for_test_module'] = str(Path(*base))
        # rs['test_module'] =


        token = report_py[:-3] + "_grade.py"
        available_reports[f] = {'json': f,
                                'questions': db['questions'],
                                'token_stub': db['token_stub'],
                                'modules': db['modules'],
                                'relative_path': report_py,
                                'root_dir': root_dir,
                                'title': db.get('title', 'untitled report'),
                                'relative_path_token': None if not os.path.isfile(root_dir + "/" + token) else token,
                                'menu_name': os.path.basename(report_py),
                                'rest_module': ".".join(db['modules'])
                                }
    return available_reports

def _run_test_cmd(dir, module_name, test_spec="", use_command_line=False):
    """
    Example: run_test_cmd('/home/tuhe/../base', 'cs108.my_test_file', test_spect='Numpy.test_something')
    """
    if use_command_line:
        try:
            cmd = f"python -m unittest {module_name}{'.'+test_spec if test_spec is not None and len(test_spec)> 0 else ''}"
            out = subprocess.run(cmd, cwd=dir, shell=True,  check=True, capture_output=True, text=True)
            print("running command", cmd, "output\n", out)
        except Exception as e:
            print(e)
    else:
        # If you use this, you have to do reliable refresh of the library to re-import files. Not sure that is easy or not.
        dir = os.path.normpath(dir)
        if dir not in sys.path:
            sys.path.append(dir)
        test = unittest.main(module=module_name, exit=False, argv=['', test_spec])
