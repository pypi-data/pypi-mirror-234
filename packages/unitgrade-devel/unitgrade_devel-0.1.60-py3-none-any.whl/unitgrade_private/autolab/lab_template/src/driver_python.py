import os
import glob
import shutil
import sys
import subprocess
from unitgrade_private.autolab.autolab import format_autolab_json
from unitgrade_private.docker_helpers import student_token_file_runner
from unitgrade_private import load_token
import time
import unitgrade_private

verbose = False
tag = "[driver_python.py]"

if not verbose:
    print("="*10)
    print(tag, "Starting unitgrade evaluation...")
import unitgrade
print(tag, "Unitgrade version", unitgrade.version.__version__)
print(tag, "Unitgrade-devel version", unitgrade_private.version.__version__)


sys.stderr = sys.stdout
wdir = os.getcwd()

def pfiles():
    print("> Files in dir:")
    for f in glob.glob(wdir + "/*"):
        print(f)
    print("---")

handin_filename = "{{handin_filename}}"
student_token_file = '{{handin_filename if student_should_upload_token else student_token_src_filename}}'
instructor_grade_script = '{{instructor_grade_file}}'
grade_file_relative_destination = "{{grade_file_relative_destination}}"
host_tmp_dir = wdir + "/tmp"
homework_file = "{{homework_file}}"
# homework_file = "{{homework_file}}"
student_should_upload_token = {{student_should_upload_token}} # Add these from template.

if not verbose:
    pfiles()
    print(f"{host_tmp_dir=}")
    print(f"{student_token_file=}")
    print(f"{instructor_grade_script=}")

print("Current directory", os.getcwd())
print("student_token_file", student_token_file)
for f in glob.glob(os.getcwd() + "/*"):
    print(f)
try:
    # This is how we get the student file structure.
    command, host_tmp_dir, token = student_token_file_runner(host_tmp_dir, student_token_file, instructor_grade_script,
                                                             grade_file_relative_destination)
    # run the stuff.
    if not student_should_upload_token:
        """ Add the student homework to the right location. """
        print("Moving uploaded file from", os.path.basename(handin_filename), "to", handin_filename)
        # print("file exists?", os.path.isfile(os.path.basename(handin_filename)))
        shutil.move(os.path.basename(handin_filename), host_tmp_dir + "/" + handin_filename)

    command = f"cd tmp && {command} --noprogress --autolab"
    def rcom(cm):
        rs = subprocess.run(cm, capture_output=True, text=True, shell=True)
        print(rs.stdout)
        if len(rs.stderr) > 0:
            print(tag, "There were errors in executing the file:")
            print(rs.stderr)

    start = time.time()
    rcom(command)
    ls = glob.glob(token)
    f = ls[0]
    results, _ = load_token(ls[0])

except Exception as e:
    if not student_should_upload_token:
        print(tag, "A major error occured while starting unitgrade.")
        print(tag, "This can mean the grader itself is badly configured, or (more likely) that you submitted a completely wrong file.")
        print(tag, "The following is the content of the file you uploaded; is it what you expect?")
        with open(host_tmp_dir + "/" + handin_filename, 'r') as f:
            print( f.read() )
        print(" ")
        print(tag, "If you cannot resolve the problem, please contact the teacher and include details such as this log, as well as the file you submitted.")

    raise e

if verbose:
    print(tag, f"{token=}")
    print(tag, results['total'])

format_autolab_json(results)
