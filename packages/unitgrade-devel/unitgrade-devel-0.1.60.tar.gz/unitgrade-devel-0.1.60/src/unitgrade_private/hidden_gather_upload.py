import sys
from unitgrade.evaluate import evaluate_report, _print_header, python_code_binary_id
import textwrap
import bz2
import pickle
import os
import zipfile
import io
from unitgrade.utils import picklestring2dict, dict2picklestring, load_token, token_sep
from unitgrade import Report

def bzwrite(json_str, token): # to get around obfuscation issues
    with getattr(bz2, 'open')(token, "wt") as f:
        f.write(json_str)

def gather_imports(imp):
    resources = {}
    m = imp
    f = m.__file__
    if hasattr(m, '__file__') and not hasattr(m, '__path__'):
        top_package = os.path.dirname(m.__file__)
        module_import = True
    else:
        im = __import__(m.__name__.split('.')[0])
        if isinstance(im, list):
            print("im is a list")
            print(im)
        top_package = __import__(m.__name__.split('.')[0]).__path__[0]
        module_import = False

    found_hashes = {}
    # pycode = {}
    resources['pycode'] = {}
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip:
        for root, dirs, files in os.walk(top_package):
            for file in files:
                if file.endswith(".py"):
                    # print("file is", file)
                    fpath = os.path.join(root, file)
                    v = os.path.relpath(fpath, os.path.dirname(top_package) if not module_import else top_package)
                    zip.write(fpath, v)
                    if not fpath.endswith("_grade.py"): # Exclude grade files.

                        # print("I am reading the file", fpath)
                        try:
                            with open(fpath, 'rb') as f:
                                s = f.read()
                        except UnicodeDecodeError as e:
                            print("Unitgrade> Oh no, I tried to read the file", f)
                            print("But I got an error since the file contains unusual content (non-unicode characters). Please go over the file and check that it looks okay. Things that can cause this problem are unusual characters (Japanese, Arabic, etc.) or Emojis.")
                            print("This problem sometimes also occurs when virus scanners or viruses write unusual files on your computer. In that case, try to disable or remove the program.")
                            raise e
                        # print("Read")
                        found_hashes[v] = python_code_binary_id(s)
                        resources['pycode'][v] = s

    resources['zipfile'] = zip_buffer.getvalue()
    resources['top_package'] = top_package
    resources['module_import'] = module_import
    resources['blake2b_file_hashes'] = found_hashes
    return resources, top_package


import argparse
parser = argparse.ArgumentParser(description='Evaluate your report.', epilog="""Use this script to get the score of your report. Example:

> python report1_grade.py

Depending on the course configuration, you get the online evaluation/verification results using the `--evaluation`-flag. Example:

> python report1_grade.py --evaluation 

The evaluation is of course only available after the teacher has made it available.

Note that if your report is part of a module (package), and the report script requires part of that package, the -m option for python may be useful.
For instance, if the report file is in Documents/course_package/report3_complete.py, and `course_package` is a python package, then change directory to 'Documents/` and run:

> python -m course_package.report1

see https://docs.python.org/3.9/using/cmdline.html
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--evaluation',  action="store_true",  help='Get the remote evaluation of this report')
parser.add_argument('--noprogress',  action="store_true",  help='Disable progress bars')
parser.add_argument('--autolab',  action="store_true",  help='Show Autolab results')
parser.add_argument('--force_kill',  action="store_true",  help='Forcefully quit on exit.')

def gather_report_source_include(report):
    sources = {}
    # print("")
    # if not args.autolab:
    if len(report.individual_imports) > 0:
        print("By uploading the .token file, you verify the files:")
        for m in report.individual_imports:
            print(">", m.__file__)
        print("Are created/modified individually by you in agreement with DTUs exam rules")
        report.pack_imports += report.individual_imports

    if len(report.pack_imports) > 0:
        print("Including files in upload...")
        for k, m in enumerate(report.pack_imports):
            nimp, top_package = gather_imports(m)
            _, report_relative_location, module_import = report._import_base_relative()

            nimp['report_relative_location'] = report_relative_location
            nimp['report_module_specification'] = module_import
            nimp['name'] = m.__name__
            sources[k] = nimp
            print(f" * {str(m.__name__)}")
    return sources

def gather_upload_to_campusnet(report, output_dir=None, token_include_plaintext_source=False):
    # n = report.nL
    args = parser.parse_args()

    if report.remote_url is not None and args.evaluation:
        import datetime
        # print("Performing a remote evaluation...")
        _print_header(now=datetime.datetime.now(), big_header=True)

        # get the remote evaluation.
        # os.path.dirname(report._artifact_file())
        mf = report._manifest_file()
        # print("looking for manifest file", mf)
        if os.path.isfile(mf):
            with open(mf, 'r') as f:
                s = f.read()
            from unitgrade.utils import checkout_remote_results

            results = checkout_remote_results(report.remote_url, s.strip())
            if results['html'] is None:
                print("""Oy! I failed to download the verified results. 
There are four likely reasons why this this command failed:
                
    * You have not yet uploaded a .token file (i.e., you have not yet handed in)
    * You did not upload a .token file, but rather a file in some other format. 
    * You have reset/deleted files from the unitgrade_data directory. In this case I don't know what file to look for remotely.
    * The .token files associated with this project have not yet been processed by the course responsible.
    
Assuming you have handed in, and it has been announced the results should be available online, you should contact a TA 
for more information about what happened to your evaluation. Please don't contact the teachers directly. 
""")
                sys.exit()
            print("Your verified results are:")
            import tabulate
            print( tabulate.tabulate(results['dict'], headers="keys" ) )
            print("These scores are based on our internal tests.")
            print("To see all your results, visit:")
            print(">", results['url'])
            print("Your total score was", results['score'])
            sys.exit()
            # import tabulate
            # print( tabulate.tabulate(df, showindex=False) )


        else:



            print(f"""
The --evaluation flag is used to download and display the (teacher) verification of your result from: 
> %s
That means you should only use this command after you have uploaded your .token file. 
            
Error: I could not find information about previously generated tokens. The likely causes are: 

    * You have not generated a token and uploaded a .token-file yet
    * You have uploaded a .token file, but it has not yet been evaluated. 
"""%(report.remote_url,))
        sys.exit()

    results, table_data = evaluate_report(report, show_help_flag=False, show_expected=False, show_computed=False, silent=True,
                                          show_progress_bar=not args.noprogress,
                                          big_header=not args.autolab,
                                          generate_artifacts=False,
                                          )
    print("")
    sources = {}
    if not args.autolab:
        results['sources'] = sources = gather_report_source_include(report)

    token_plain = """
# This file contains your results. Do not edit its content. Simply upload it as it is. """

    s_include = [token_plain]
    known_hashes = []
    cov_files = []
    use_coverage = True
    if report._config is not None:
        known_hashes = report._config['blake2b_file_hashes']
        for Q, _ in report.questions:
            from unitgrade import UTestCase
            use_coverage = use_coverage and isinstance(Q, UTestCase)
            for key in Q._cache:
                if len(key) >= 2 and key[1] == "coverage":
                    for f in Q._cache[key]:
                        cov_files.append(f)

    for s in sources.values():
        for f_rel, hash in s['blake2b_file_hashes'].items():
            if hash in known_hashes and f_rel not in cov_files and use_coverage:
                print("Skipping", f_rel)
            else:
                if token_include_plaintext_source:
                    s_include.append("#"*3 +" Content of " + f_rel +" " + "#"*3)
                    s_include.append("")
                    s_include.append(s['pycode'][f_rel])
                    s_include.append("")

    if output_dir is None:
        output_dir = os.getcwd()

    payload_out_base = report.__class__.__name__ + "_handin"

    obtain, possible = results['total']
    vstring = f"_v{report.version}" if report.version is not None else ""
    token = "%s_%i_of_%i%s.token"%(payload_out_base, obtain, possible, vstring)
    token = os.path.normpath(os.path.join(output_dir, token))

    b_hash = save_token(results, "\n".join(s_include), token)
    try:
        with open(report._manifest_file(), 'a') as _file:
            _file.write("\n"+token + " " + b_hash)
    except Exception as e:
        print(e)

    # ug_dir = os.path.dirname(report._artifact_file())
    # ug_name = os.path.basename(report._artifact_file())
    # MANIFEST = ug_dir + "/manifest."




    if not args.autolab:
        print("> Testing token file integrity...", sep="")
        load_token(token)
        print("Done!")
        print(" ")
        print("To get credit for your results, please upload the single unmodified file: ")
        print(">", token)

    if args.force_kill:
        print("Running sys.exit...")
        import threading
        # import sys
        # import os
        print("These are all the threads:")
        for thread in threading.enumerate():
            print(thread.name)
            if thread.name != "MainThread":
                thread.join(timeout=0.5)
            print("timed out thread...")
        print("Sys.exiting...")
        # sys.exit()

        print("Killing my own pid. ")
        pid = os.getpid()
        # os.kill(pid)
        import signal

        print("Threads that survive")

        for thread in threading.enumerate():
            print(thread.name)
            # if thread.name != "MainThread":
            #     thread.join(timeout=0.5)
            # print("timed out thread...")
        print("My pid", pid)
        os.kill(pid, 9)
        print("Raising exception instead...")
        # raise Exception("Quitting this shit.")
        os._exit(0)
        sys.exit()
        print("Sys.exit ran.")


def save_token(dictionary, plain_text, file_out):
    if plain_text is None:
        plain_text = ""
    if len(plain_text) == 0:
        plain_text = "Start token file"
    plain_text = plain_text.strip()
    b, b_hash = dict2picklestring(dictionary)
    b_l1 = len(b)
    b = "."+b+"."
    b = "\n".join( textwrap.wrap(b, 180))

    out = [plain_text, token_sep, f"{b_hash} {b_l1}", token_sep, b]
    with open(file_out, 'w') as f:
        f.write("\n".join(out))
    return b_hash



def source_instantiate(name, report1_source, payload):
    # print("Executing sources", report1_source)
    eval("exec")(report1_source, globals())
    # print("Loaind gpayload..")
    pl = pickle.loads(bytes.fromhex(payload))
    report = eval(name)(payload=pl, strict=True)
    return report
