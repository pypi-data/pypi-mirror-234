from unitgrade import evaluate
import jinja2
import pickle
import inspect
import time
import os
from unitgrade_private import hidden_gather_upload
from unitgrade_private.deployment import remove_hidden_methods
import os
import glob

data = """
{{head}}

report1_source = {{source}}
report1_payload = '{{payload}}'
name="{{Report1}}"

report = source_instantiate(name, report1_source, report1_payload)
output_dir = os.path.dirname(__file__)
gather_upload_to_campusnet(report, output_dir)
"""


def strip_main(report1_source):
    dx = report1_source.find("__main__")
    report1_source = report1_source[:dx]
    report1_source = report1_source[:report1_source.rfind("\n")]
    return report1_source


def rmimports(s, excl):
    s = "\n".join([l for l in s.splitlines() if not any([l.strip().startswith(e) for e in excl])])
    return s

def lload(flist, excl):
    s = ""
    for fname in flist:
        with open(fname, 'r', encoding="utf-8") as f:
            s += f.read() + "\n" + "\n"
    s = rmimports(s, excl)  # remove import statements from helper class.
    return s

def setup_grade_file_report(ReportClass, execute=False, obfuscate=False, minify=False, bzip=True, nonlatin=False, source_process_fun=None, with_coverage=True, verbose=True,
                            remove_hidden=False, name_without_hidden=None):
    if remove_hidden:
        name = os.path.basename(ReportClass.mfile())
        if name_without_hidden is None:
            if name.endswith("_complete.py"):
                name_without_hidden = name[:-12] + ".py"
            else:
                raise Exception("Must spacify name to give new report file")

        fout, Report = remove_hidden_methods(ReportClass, outfile=name_without_hidden)  # Create report3.py without @hide-methods
        return setup_grade_file_report(Report, remove_hidden=False, bzip=bzip) # Create report3_grade.py for the students

    print("Setting up answers...")
    url = ReportClass.url
    ReportClass.url = None
    report = ReportClass()
    # report.url = None # We set the URL to none to skip the consistency checks with the remote source.
    payload = report._setup_answers(with_coverage=with_coverage, verbose=verbose)
    payload['config'] = {}

    # Save metadata about the test for use with the dashboard (and nothing else). Do not use this data for any part of the evaluation, etc. -- only the dashboard!
    # Don't save using diskcache, as we want to easily be able to remove the diskcache files without any issues.
    # db = {}
    # db = PupDB(report._artifact_file())
    from unitgrade_private.hidden_gather_upload import dict2picklestring, picklestring2dict
    artifacts = {}
    artifacts['questions'] = {}
    root_dir, relative_path, modules = report._import_base_relative()
    db = {'encoding_scheme': "from unitgrade_private.hidden_gather_upload import dict2picklestring, picklestring2dict;",
          'root_dir': root_dir,
          'relative_path': relative_path,
         'modules': modules,
         'token_stub': os.path.dirname(relative_path) + "/" + ReportClass.__name__ + "_handin",
          }
    # db.set('encoding_scheme',
    #        "from unitgrade_private.hidden_gather_upload import dict2picklestring, picklestring2dict;")
    # db.set('root_dir', root_dir)
    # db.set('relative_path', relative_path)
    # db.set('modules', modules)
    # db.set('token_stub', os.path.dirname(relative_path) +"/" + ReportClass.__name__ + "_handin")

    # Set up the artifact file. Do this by looping over all tests in the report. Assumes that all are of the form UTestCase.
    from unitgrade.evaluate import SequentialTestLoader
    loader = SequentialTestLoader()
    for q, points in report.questions:

        artifacts['questions'][q.__qualname__] = {'title': q.question_title() if hasattr(q, 'question_title') else         q.__qualname__, 'tests': {} }
        suite = loader.loadTestsFromTestCase(q)
        from unitgrade.framework import classmethod_dashboard

        if 'setUpClass' in q.__dict__ and isinstance(q.__dict__['setUpClass'], classmethod_dashboard):
            ikey = tuple( os.path.basename( q._artifact_file_for_setUpClass() )[:-5].split("-") )


            artifacts['questions'][q.__qualname__]['tests'][ikey] = {'title': 'setUpClass',
                                                                   'artifact_file': os.path.relpath(q._artifact_file_for_setUpClass(),
                                                                                                    root_dir),
                                                                   # t._artifact_file(),
                                                                   'hints': None,
                                                                   'coverage_files': q()._get_coverage_files(),
                                                                   }
        for t in suite._tests:
            try:
                id = t.cache_id()
                cf = t._get_coverage_files()
                cf = [] if cf is None else cf
                artifacts['questions'][q.__qualname__]['tests'][id] = {'title': t.title,
                                                                       'artifact_file': os.path.relpath(t._artifact_file(), root_dir), # t._artifact_file(),
                                                                       'hints': t._get_hints(),
                                                                       'coverage_files': cf
                                                                       }
            except Exception as e:
                pass
            a = 34
    # s, _ = dict2picklestring(artifacts['questions'])
    db['questions'] = artifacts['questions'] # ('questions', s)
    if not os.path.isdir(os.path.dirname(report._artifact_file())):
        os.makedirs(os.path.dirname(report._artifact_file()))
    with open(report._artifact_file(), 'wb') as f:
        pickle.dump(db, f)

    for f in glob.glob(os.path.dirname(report._artifact_file()) + "/*.json") + glob.glob(os.path.dirname(report._artifact_file()) + "/cache.db*"): # blow old artifact files. should probably also blow the test cache.
        os.remove(f)

    from unitgrade_private.hidden_gather_upload import gather_report_source_include
    sources = gather_report_source_include(report)
    known_hashes = [v for s in sources.values() for v in s['blake2b_file_hashes'].values() ]
    # assert len(known_hashes) == len(set(known_hashes)) # Check for collisions.
    payload['config']['blake2b_file_hashes'] = known_hashes
    time.sleep(0.1)
    print("Packing student files...")

    fn = inspect.getfile(ReportClass)
    with open(fn, 'r') as f:
        report1_source = f.read()
    report1_source = strip_main(report1_source)

    # Do fixing of source. Do it dirty/fragile:
    if source_process_fun == None:
        source_process_fun = lambda s: s

    report1_source = source_process_fun(report1_source)
    picklestring = pickle.dumps(payload)

    import unitgrade
    excl = ["unitgrade.unitgrade_helpers",
            "from . import",
            "from unitgrade.",
            "from unitgrade ",
            "import unitgrade"]

    report1_source = rmimports(report1_source, excl)

    pyhead = lload([evaluate.__file__, hidden_gather_upload.__file__], excl)
    from unitgrade import version
    from unitgrade import utils
    from unitgrade import runners
    # print(unitgrade.__file__)
    report1_source = lload([unitgrade.__file__, utils.__file__, runners.__file__, unitgrade.framework.__file__,
                            unitgrade.evaluate.__file__, hidden_gather_upload.__file__,
                            version.__file__], excl) + "\n" + report1_source

    s = jinja2.Environment().from_string(data).render({'Report1': ReportClass.__name__,
                                                       'source': repr(report1_source),
                                                       'payload': picklestring.hex(), #repr(picklestring),
                                                       'token_out': repr(fn[:-3] + "_handin"),
                                                       'head': pyhead})
    # if fn[:-3].endswith("_test.py"):
    #     output = fn[:-8] + "_grade.py"
    # elif fn.endswith("_tests.py"):
    #     output = fn[:-9] + "_grade.py"
    # else:
    #     output = fn[:-3] + "_grade.py"

    output = test2grade(fn)

    print("> Writing student script to", output, "(this script may be shared)")
    # Add the relative location string:

    # Add relative location to first line of file. Important for evaluation/sanity-checking.
    report_relative_dir = report._import_base_relative()[1]
    s = "# " + report_relative_dir + "\n" + s

    with open(output, 'w', encoding="utf-8") as f:
        f.write(s)

    if minify or bzip:  # obfuscate:
        obs = '-O ' if obfuscate else ""
        # output_obfuscated = output[:-3]+"_obfuscated.py"
        extra = [  # "--nonlatin",
            # '--bzip2',
        ]
        if bzip: extra.append("--bzip2")
        if minify:
            obs += " --replacement-length=20"
        from pyminifier_bundled.__main__ import runpym

        cmd = f'pyminifier {obs} {" ".join(extra)} -o "{output}" "{output}"' # TH 2023 Juli: Backslashes for windows + spaces.
        import shlex
        # shlex.split(cmd)
        sysargs = shlex.split(cmd) # cmd.split(" ")
        runpym(sysargs[1:])
        # print(cmd)
        # os.system(cmd)
        time.sleep(0.2)
        with open(output, 'r') as f:
            sauce = f.read().splitlines()
        wa = """ WARNING: Modifying, decompiling or otherwise tampering with this script, it's data or the resulting .token file will be investigated as a cheating attempt. """
        sauce = ["'''" + wa + "'''"] + sauce[:-1]
        sauce = "\n".join(sauce)
        sauce = "# " + report_relative_dir + "\n" + sauce
        with open(output, 'w') as f:
            f.write(sauce)

    if execute:
        time.sleep(0.1)
        print("Testing packed files...")
        fn = inspect.getfile(ReportClass)
        print(fn)
        s = os.path.basename(output)[:-3]
        # s = os.path.basename(fn)[:-3] + "_grade"
        print(s)
        exec("import " + s)

    print("====== EXECUTION AND PACKING OF REPORT IS COMPLETE ======")
    ReportClass.url = url
    return output

def test2grade(file_with_test):
    if file_with_test.endswith("_test.py"):
        grade = file_with_test[:-8] + "_grade.py"
    elif file_with_test.endswith("_tests.py"):
        grade = file_with_test[:-9] + "_grade.py"
    else:
        grade = file_with_test[:-3] + "_grade.py"
    return grade