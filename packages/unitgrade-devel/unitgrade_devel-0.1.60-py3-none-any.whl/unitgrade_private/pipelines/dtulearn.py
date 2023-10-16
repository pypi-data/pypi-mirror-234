import pickle
import shutil
import os
import glob
import tempfile
import time
import tabulate
from unitgrade_private.plagiarism.mossit import moss_it, get_id
from unitgrade_private import load_token
from collections import defaultdict
from coursebox.core.info_paths import get_paths
from unitgrade_private.docker_helpers import compile_docker_image, download_docker_images
from unitgrade_private.docker_helpers import docker_run_token_file
from coursebox.core.info import class_information
from coursebox.core.projects import gather_instructor_sheets
import numpy as np
from unitgrade_private.token_loader import unpack_sources_from_token
import subprocess
import fnmatch
from coursebox.core.projects import unpack_zip_file_recursively
from unitgrade_private.token_loader import determine_token_difference, combine_token_results
from unitgrade_private.token_loader import token_gather_hidden


def write_summary_report_xlsx_file(write_html=True, open_browser=True):
    """ This function write a summary of the students' performance in the three reports to a XLSX-sheet. This is pretty defunct. """
    projects = [1, 2, 3, 4]
    code_part_weight = {1: 0.5, 2: 0.4, 3: 0.7, 4: 1}
    report_weights = {1: 1, 2:1, 3:.5, 4:.5}

    paths = get_paths()
    info = class_information()
    gather_instructor_sheets(info)
    # Now sheets are saved to main xlsx-file. This file reflects all handins.
    info = class_information() # Reload information to make sure the report field is set. This gives all available reports.
    tres = {}
    # p = 4
    # handle_project_handins(project_id=p, moss=False, docker_verify=False, verbose=False)

    for p in projects:
        try:
            tres[p] = handle_project_handins(project_id=p, moss=False, docker_verify=False,verbose=False)
        except Exception as e:
            tres[p] = None
    dd = defaultdict(dict)
    for j, (id, v) in enumerate(info['students'].items()):
        def add(name, value):
            if isinstance(value, float):
                value = np.round(value, decimals=3)
            dd[id][name] = value # .append(value)
        add('id', id)
        score = 0 # Compute the total score.

        for p in projects:
            if p not in v['reports'] or v['reports'][p] is None: # This is because report 4 has no handin evaluated by TAs.
                group_id = -1
            else:
                group_id = v['reports'][p]['group_id']
            add(f'{p}: group-id', group_id)
            ta_score = v['reports'][p]['pct'] if group_id > -1 else 0
            # code_score = tres[p][group_id]['student-token-total']  if group_id > -1 and group_id in tres[p] else (0,1)
            if tres[p] is None:
                continue
            if p == 4:
                code_score = tres[p][id]['student-token-total'] if id in tres[p] else (0,1)
            else:
                code_score = tres[p][group_id]['student-token-total'] if group_id > -1 and group_id in tres[p] else (0, 1)
            add(f'{p}: did_handin_code', code_score != (0,1))
            add(f'{p}: did_handin_pdf', group_id != -1)

            code_score = code_score[0] / code_score[1]
            # print("RPadfsf")

            add(f'{p}: ta-score', ta_score)
            add(f'{p}: verified-token-score', tres[p][group_id]['verified-token-total'] if group_id > -1 and group_id in tres[p] else 0)
            add(f'{p}: student-token-score', code_score)
            add(f'{p}: student-token-location', tres[p][group_id]['token_location'] if group_id > -1 else None)

            score += report_weights[p] * (1-code_part_weight[p] ) * ta_score / sum(report_weights.values())
            score += report_weights[p] * ( code_part_weight[p]) * code_score / sum(report_weights.values())
        add(f'TOTAL SCORE', score)

    d2 = {}
    d2['key'] = list(dd[list(dd.keys())[-1]].keys())
    for k, v in dd.items():
        d2[k] = list(v.values())
    print(tabulate.tabulate(d2, headers='keys'))
    try:
        for p in projects:
            print(p, len( [k for k, v in dd.items() if isinstance(v[f'{p}: student-token-score'], tuple)] ))
    except Exception as e:
        pass

    print(tabulate.tabulate(d2, headers='keys', tablefmt='html'))
    fout = paths['semester'] +"/report_summary.html"
    if write_html:
        import pandas as pd
        df = pd.DataFrame.from_dict(d2)
        from pretty_html_table import build_table
        html_table_blue_light = build_table(df, 'blue_light')
        # Save to html file
        with open(fout, 'w') as f:
            f.write(html_table_blue_light)

        df.to_excel(paths['semester'] + "/legacy_evaluations_" + info['semester_id'] + ".xlsx")
        print("Saved output to", fout)
    import webbrowser
    if open_browser:
        webbrowser.open_new_tab(fout)
    import pickle
    with open(paths['semester'] + "/legacy_evaluations_" + info['semester_id'] + ".pkl", 'wb') as f:
        pickle.dump(dd, f)

    return dd


def f2date(f):
    date = os.path.basename(f).split("-")[-1].strip()

    import datetime
    # date = " 31 August, 2023 3:44 PM"
    # date = "31 August, 2023"
    # date = "3:44 PM"
    # datetime_obj = datetime.datetime.strptime(date.strip(), "%I:%M %p")
    if ":" in date:
        datetime_obj = datetime.datetime.strptime(date.strip(), "%d %B, %Y  %I:%M %p")
    else:
        datetime_obj = datetime.datetime.strptime(date.strip(), "%d %B, %Y  %I%M %p")
    return datetime_obj


def docker_stagewise_evaluation(base_directory, Dockerfile=None, instructor_grade_script=None,
                                student_handout_folder=None,
                                clear_stage1_plus=False,
                                clear_stage3_plus=False,
                                clear_stage2_plus=False,
                                clear_stage4_plus=False,
                                configuration=None,
                                unmute_docker = True,
                                plagiarism_check=False,
                                accept_problems=True, # No!
                                ):
    """
    This is the main verification scripts. It is the main entry point for project verifications as downloaded from DTU Learn.

    It is given a folder location which represents the staging directory. For instance:

    {year-semester}/project1

    It will then assume that within this project, there is a folder called:

    {year-semester}/project1/stage0_learn

    The content of that folder is zip-files etc. downloaded from DTU Learn.

    Then these will be extracted to:

    {year-semester}/project1/stage1_raw_handins

    These are student-id/project-id coded handins.

    These are then processed into:

    {year-semester}/project1/stage2_single_handins

    These contain either the .token files or the .py files.

    :param learn_zip_file_path:
    :param Dockerfile:
    :param instructor_grade_script:
    :return:
    """
    if configuration is None:
        configuration = {'stage0': {'excluded_files': ['*.pdf', '*_grade.py'], 'allowed_files': []},
                         'stage1': {'excluded_files': ['*.pdf']}}

    stage0_dir = base_directory + "/stage0_downloads"
    stage1_dir = base_directory + "/stage1_extracted" # This contains the extracted handins, i.e. all unique student ids.
    stage2_dir = base_directory + "/stage2_unique_handins"
    stage3_dir = base_directory + "/stage3_staged_for_execution"
    stage4_dir = base_directory + "/stage4_execution_product"

    messages = defaultdict(list)

    def clear_stage_plus(stage):
        for k, v in {1: stage1_dir, 2: stage2_dir, 3: stage3_dir, 4: stage4_dir}.items():
            if k >= stage and os.path.isdir(v):
                    shutil.rmtree(v)

    if clear_stage1_plus: clear_stage_plus(1)
    if clear_stage2_plus: clear_stage_plus(2)
    if clear_stage3_plus: clear_stage_plus(3)
    if clear_stage4_plus: clear_stage_plus(4)

    if not os.path.isdir(stage0_dir):
        os.makedirs(stage0_dir)

    info = class_information()

    def _stage0():

        # stage0_excluded_files = ["*.pdf"]
        stage0_excluded_files = configuration['stage0']['excluded_files']
        found = []

        # ids_and_directories = []

        relevant_directories = {}

        # Set up stage 1:
        for z in glob.glob(f"{stage0_dir}/*.*"):
            if not z.endswith(".zip"):
                raise Exception("The downloaded files must be .zip files from DTU Learn")

            unpack_zip_file_recursively(z[:-4] + ".zip", z[:-4] + "/raw", remove_zipfiles=True)

            for f in glob.glob(z[:-4] + "/raw/*"):
                if os.path.basename(f) == "index.html":
                    continue
                elif os.path.isdir(f):
                    id = fname2id(os.path.basename(f), info)

                    # now get the directory.

                    if id not in relevant_directories:
                        relevant_directories[id] = f
                    else:
                        dold = f2date(relevant_directories[id])
                        dnew = f2date(f)
                        if dnew == dold:
                            pass
                            raise Exception("User has two handins with the same date. Not possible. \n" + f + "\n " + relevant_directories[id])

                        if dnew > dold:
                            relevant_directories[id] = f
                else:
                    assert student_handout_folder is not None
                    raise Exception(
                        "The .zip files can only contain directories with names such as: '67914-43587 - s214598, Andreas Rahbek-Palm - 09 February, 2023 441 PM', got " + student_handout_folder)

            for id, f in relevant_directories.items():
                found.append(id)
                dest = stage1_dir +"/" + id

                if not os.path.isdir(dest):
                    shutil.copytree(f, dest )
                else:
                    # merge the files...
                    for new_file in glob.glob(f +"/**/*", recursive=True):
                        # print(os.path.relpath(new_file, f))
                        shutil.copy(new_file, dest + "/"+os.path.relpath(new_file, f))

                # Now remove blacklisted files to simplify it.
                for g in glob.glob(dest +"/**/*", recursive=True):
                    import fnmatch
                    if g.endswith(".py"):
                        print(g)
                    if os.path.basename(g) in configuration['stage0']['rename']:
                        dst_name = configuration['stage0']['rename'][os.path.basename(g)]
                        dst_name = os.path.dirname(g) + "/" + dst_name
                        if not os.path.isfile(dst_name):
                            shutil.move(g, dst_name)

                    if len([ex for ex in stage0_excluded_files if fnmatch.fnmatch(g, ex)]) > 0:
                        os.remove(g)


    _stage0()

    def _stage1():
        # In this we move on to stage1.
        # In this stage, we move the files over to a staging area. The staging area consist of actual (complete) handins (tokens or .py files).

        found_ids = []
        for fid in glob.glob( stage1_dir +"/*"):

            id = os.path.basename(fid)
            # Perhaps take all files and seperate them into different handins?

            handins = {'token': [],
                       'python': []}

            for f in glob.glob(fid+"/**/*", recursive=True):
                if os.path.isdir(f):
                    pass # Directories we don't care about.
                elif f.endswith(".token"):
                    handins['token'].append(f)
                elif f.endswith(".py"):
                    handins['python'].append(f)
                elif f.endswith("pyc") and "__pycache__" in f:
                    pass # This file was likely generated while mucking about. It has no meaning.
                else:
                    excluded = configuration.get('stage1', {}).get('excluded_files', [])

                    if len( [ex for ex in excluded if fnmatch.fnmatch(f, ex) ] ) > 0:
                        pass
                    else:
                        raise Exception("Handin file found with bad extensions: " + f)

            # Now move to destination directories:
            for handin_type in handins:
                fid_type = f"{stage2_dir}/{id}-{handin_type}"
                if len(handins[handin_type]) == 0 or os.path.isdir(fid_type): # If there are no files associated with this handin type then skip it.
                    # Skip because this has already been made.
                    continue

                for f in handins[handin_type]:
                    s = os.path.relpath(f, fid)
                    # print(s)
                    dst = f"{fid_type}/{s}"
                    if not os.path.isdir(os.path.dirname(dst)):
                        os.makedirs(os.path.dirname(dst))
                    shutil.copy(f, dst)
                    # print(dst)
    _stage1()
    # Now move through the files and extract. I guess we do that by recursively unpacking them?

    def get_grade_script_location(instructor_grade_script):
        with open(instructor_grade_script, 'r') as f:
            gs = f.read().splitlines()[0][1:].strip()
        return os.path.dirname(gs) + "/"+os.path.basename(instructor_grade_script)

    def _stage2(fix_user=True, xvfb=True):
        # configuration
        """ Unpack token or prep python files. """
        for fid in glob.glob(stage2_dir + "/*"):
            # print(fid)
            id, type = os.path.basename(fid).split("-")
            s3dir = f"{stage3_dir}/{os.path.basename(fid)}"
            if os.path.isdir(s3dir):
                continue
            grade_script_relative = get_grade_script_location(instructor_grade_script)
            if type == "token":
                tokens = glob.glob(fid + "/**/*.token", recursive=True)
                assert len(tokens) == 1, f"{id} has too many tokens: The tokens found are {tokens}"
                try:
                    unpack_sources_from_token(tokens[0], s3dir)
                except Exception as e:
                    print("-" * 100)
                    print("Not a valid token file", tokens[0], "investigate and potentially blacklist", id)

                    if id in configuration.get('stage2', {}).get('skip_students', []):
                        pass
                    else:
                        raise e

                # This will copy in resource files etc. that may not be contained in the .token file.
                for g in glob.glob(student_handout_folder + "/**/*.*", recursive=True):
                    rg = os.path.relpath(g, student_handout_folder)
                    if not os.path.isfile(s3dir + "/"+rg) and not rg.endswith(".py"):
                        if not os.path.isdir(os.path.dirname(s3dir + "/"+rg)): os.makedirs(os.path.dirname(s3dir + "/"+rg))
                        if os.path.isfile(g):
                            shutil.copy(g, s3dir + "/"+rg)
                        else:
                            shutil.copytree(g, s3dir + "/" + g)
            else:
                shutil.copytree(student_handout_folder, s3dir)
                for g in glob.glob(fid+"/**/*.*", recursive=True):
                    # Find location in student handout folder.
                    fn = glob.glob(student_handout_folder + "/**/" + os.path.basename(g), recursive=True)
                    if len(fn) == 0:
                        print("I was unable to locate", g)
                        print("Bad?")
                    os.path.relpath(fn[0], student_handout_folder)

                    dst = s3dir + "/"+os.path.dirname(grade_script_relative) + "/"+ os.path.basename(g)
                    dst = s3dir + "/" + os.path.relpath(fn[0], student_handout_folder)

                    if os.path.isfile(dst):
                        shutil.copy(g, dst)
                    else:
                        shutil.move(g, dst)
                        print("> Stage two: Created", dst)

            ### Copy in the instructor grade script. We are now ready for deployment.
            shutil.copy(instructor_grade_script, os.path.dirname(s3dir + "/" + grade_script_relative) + "/" + os.path.basename(instructor_grade_script))

            ## Check files are readable...
        for fid in glob.glob(stage2_dir + "/*"):
            # print(fid)
            id, type = os.path.basename(fid).split("-")
            s3dir = f"{stage3_dir}/{os.path.basename(fid)}"
            # if os.path.isdir(s3dir):
            #     continue
            for f in glob.glob(s3dir +"/**/*.py", recursive=True):
                if os.path.isdir(f):
                    continue
                try:
                    with open(f, 'r') as ff:
                        ff.read()
                except UnicodeDecodeError as e:
                    print("""Student file not readable. add to stage2 kill list as in { configurations['projects']['project1']['stage3']['exclude_if_bad_encoding'] += ['*/~BROMIUM/*.py'] }""", f)
                    for p in configuration['stage2'].get('exclude_if_bad_encoding', []):
                        if fnmatch.fnmatch(f, p):
                            print("Skipping file with shit encoding", f)
                            os.remove(f)
                            break
                    if os.path.isfile(f):
                        raise e





    _stage2()

    def _stage3(Dockerfile, fix_user=True, xvfb=True, unmute=False, verbose=False):
        if Dockerfile is None:
            images = download_docker_images()
            Dockerfile = images['unitgrade-docker']
        tag = compile_docker_image(Dockerfile, verbose=verbose)

        # This should create stage3. The directories that are ready for execution.
        recombined_evaluations = {}
        nn = 0
        # did_nag_about = {}
        conf = configuration.get('stage3', {})

        for fid in glob.glob(stage3_dir + "/*"):
            s4dir = f"{stage4_dir}/{os.path.basename(fid)}"
            grade_script_relative = get_grade_script_location(instructor_grade_script)
            grade_script_destination = os.path.dirname(fid + "/" + grade_script_relative) + "/" + os.path.basename(instructor_grade_script)

            # combine the token and student python versions. Check if we are happy with the current result, i.e., do we get as many points as the student expected or not?
            RERUN_TOKEN = True #Re-evaluate this staged execution and re-create the token.
            if os.path.isdir(s4dir):
                RERUN_TOKEN = False
                # Try to get the old token file
                id, type = os.path.basename(fid).split("-")
                # now combine the student and instructor versions of this file for an evaluations.
                products = glob.glob(f"{stage4_dir}/{id}-*/*.token")
                student_token_file = glob.glob(f"{stage2_dir}/{id}-token/**/*.token", recursive=True)
                assert len(student_token_file) <= 1
                if type == 'token': assert len(student_token_file) == 1

                if len(products) == 2:
                    rc = combine_token_results(load_token(products[0])[0], load_token(products[1])[0])
                    # flag when student has a test item that pass which the token file does not.
                elif len(products) > 2:
                    raise Exception(f"Handins not recognized {products}")
                elif len(products) == 1:
                    rc = load_token(products[0])[0]

                if len(products) == 0: # No .token file has actually been generated. So obviously we have to re-generate it.
                    RERUN_TOKEN = True
                elif len(student_token_file) > 0 and id not in configuration.get('stage2', {}).get('skip_students', []):
                    # We check if the student id is marked as skipped. This is reserved for cases where student uploads a token file, but it is fundamentally broken (as determined by manual inspection).
                    if len(student_token_file) == 0:
                        print(f"Strange error in stage 3: this student did not have a token file {id}")
                    try:
                        stoken, _ = load_token(student_token_file[0])
                    except Exception as e:
                        print(f"did not load token file for student {id}: {student_token_file}")
                        raise e
                    # if os.path.basename(student_token_file[0]).split("_")[0] != os.path.basename(products[0]).split("_")[0]:
                    #     print("bad")
                    # We check if the student ran the actual token file they were supposed to run. If not, it may still have the right sources...
                    if "sources" not in rc:
                        print("no sources")

                    ptoken = load_token(products[0])[0]
                    if ".".join(stoken['sources'][0]['report_module_specification']).lower().replace(" ", "") == ".".join(ptoken['sources'][0]['report_module_specification']).replace("_tests_complete", "").lower(): #
                        s_better_than_i, _ = determine_token_difference(stoken, rc)
                        acceptable_broken = False
                    elif id in configuration.get('stage3', {}).get('accept_incompatible_token_names', []):
                        print("Incompatible token names accepted...")
                        s_better_than_i = []
                        acceptable_broken = True
                    else:
                        print(".".join(stoken['sources'][0]['report_module_specification']).lower())
                        print(".".join(rc['sources'][0]['report_module_specification']).replace("_tests_complete", "").lower())

                        raise Exception("Bad student token. Add id incompatible token names " + str(student_token_file) )
                        pass

                    if len(s_better_than_i) > 0:
                        for q in s_better_than_i:
                            for item in s_better_than_i[q]['items']:
                                messages['stage3'].append(f"{id}> ERROR: Student strictly better than instructor. q{q}. item: {item}")
                                RERUN_TOKEN = True

                    rch = token_gather_hidden(rc)

                    for q in stoken['details']:
                        if acceptable_broken:
                            continue
                        for item in stoken['details'][q]['items']:
                            sitem = stoken['details'][q]['items'][item]
                            iitems = rch['details'][q]['items'][item]
                            if sitem['status'] == 'pass' and not all([i['status'] == 'pass' for i in iitems]) and id not in conf.get('verified_problematic_items', {}).get(item, []):
                                # print('disagreement found.')
                                iitems = rch['details'][q]['items'][item]
                                fails = [i['nice_title'] for i in iitems if i['status'] != 'pass']
                                messages['stage3'].append(f"{id} {nn+1}> Hidden test disagreement. Public ok but hidden got failues in: {fails}, {item}")
                                from unitgrade_private.token_loader import get_coverage_files
                                cfiles = get_coverage_files(student_token_file[0], instructor_grade_script_dir=os.path.dirname(grade_script_destination))

                                # with open(f"{os.path.dirname(grade_script_destination)}/unitgrade_data/{stoken['details'][q]['name']}.pkl", 'rb') as f:
                                #     pk = pickle.load(f)
                                # fls = list( pk[(item, 'coverage')].keys() )[0]
                                fls = cfiles[q][(item, 'coverage')][0]
                                if fid.endswith("token"):
                                    failures = [i for i in iitems if i['status'] != 'pass']
                                    print("*"*100)
                                    print(item)
                                    print(id)
                                    print("-"*20 + "---We got the error " + "-"*20)
                                    print(failures.pop()['stderr'])
                                    print("-"*20 + "Please make sure the following is broken" + "-"*20 )
                                    with open(f"{fid}/{fls}", 'r') as f:
                                        print( f.read() )
                                    print("="*100)

                                RERUN_TOKEN = True
                                nn += 1
            else:
                print("No token rerunning", s4dir)

            if not RERUN_TOKEN:
                # Check if the instructor script is identical to the current one.
                # a '234
                import filecmp

                if not filecmp.cmp(instructor_grade_script, grade_script_destination, shallow=False):
                    print("grade script has been updated subsequently. Rerunning the tests...")
                    messages['stage3'].append(f"Rerunning token bc. of new grade script {grade_script_destination}")
                    RERUN_TOKEN = True
                else:
                    continue

            # Copy the instructor grade script before a run. Although this is also set at the previous stage, it is likely it will be updated
            # during grading to reflect changes to tests, new tests, etc.

            shutil.copy(instructor_grade_script, grade_script_destination)
            for fdel in glob.glob(os.path.dirname(fid + "/" + grade_script_relative) + "/*.token"):
                os.remove(fdel) # Delete existing token file.

            if tag is None:
                dockname = os.path.basename(os.path.dirname(Dockerfile))
            else:
                dockname = tag

            pycom = ".".join(grade_script_relative[:-3].split("/")) + " --noprogress"
            pycom = "python3 -m " + pycom
            if fix_user:
                user_cmd = ' --user "$(id -u):$(id -g)" '
            else:
                user_cmd = ''
            if xvfb:
                user_cmd = " -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix " + user_cmd
            tmp_path = os.path.abspath(fid).replace("\\", "/")
            with_ls = True
            if with_ls:
                pycom = f"""sh -c 'xvfb-run -s "-screen 0 1400x900x24" {pycom}'"""

            dcom = f"docker run {user_cmd} -v {tmp_path}:/home {dockname} {pycom}"
            cdcom = f"cd {os.path.dirname(Dockerfile)}"
            fcom = f"{cdcom}  && {dcom}"
            print("> Running docker command in", fid)
            print(fcom)
            if os.path.basename(fid) == 'Group33-token':
                a = 234
            from unitgrade.utils import Capturing2, Capturing, Logger

            if unmute: # This is a pretty big mess.
                from unitgrade_private.run import run
                out = run(fcom, print_output=True, log_output=False, check=False)
                stdout = out.stderr.getvalue()
                stderr = out.stderr.getvalue()

                if not os.path.isdir(s4dir):
                    os.makedirs(s4dir)
                with open(s4dir + "/output.txt", 'w') as ff:
                    ff.write(stdout)
                if len(stderr.strip()) > 0:
                    with open(s4dir + "/errors.txt", 'w') as ff:
                        ff.write(stderr)
            else:
                out = subprocess.check_output(fcom, shell=True).decode("utf-8")
                if not os.path.isdir(s4dir):
                    os.makedirs(s4dir)
                with open(s4dir + "/output.txt", 'w') as ff:
                    ff.write(out)

            # out.split(">")[-1].strip()
            tokens = glob.glob(os.path.dirname(fid + "/" + grade_script_relative) + "/*.token")
            if not os.path.isdir(s4dir):
                os.makedirs(s4dir)

            for f in glob.glob(s4dir + "/*.token"):
                os.remove(f)
            try:
                shutil.move(tokens[0], s4dir + "/" + os.path.basename(tokens[0]))
            except Exception as e:
                print("-"*50)
                print("Got a problem wit hthis student")
                print("dir", s4dir)
                print("tokens", tokens)
                raise e

    _stage3(Dockerfile, unmute=unmute_docker)

    def _stage_report():
        found_students = defaultdict(dict)
        rs = {}

        for fid in glob.glob(stage1_dir + "/*"):
            id = os.path.basename(fid)
            rs[id] = {'token_downloaded': None, 'token_produced': []}

            for tf in glob.glob(fid +"/**/*.token", recursive=True):
                rs[id]['token_downloaded'] = tf

                if id in configuration.get('stage2', {}).get('skip_students', []):
                    blake_hash = "BAD TOKEN: STUDENT IS MARKED AS SKIPPED."
                else:
                    tdata, _ = load_token(tf)
                    blake_hash = tdata['metadata']['file_reported_hash']

                rs[id]['token_downloaded_hash'] = blake_hash


            for cid in glob.glob(f"{stage4_dir}/{id}-*"):
                type = os.path.basename(cid).split("-")[1]
                tokens = glob.glob(f"{cid}/*.token")
                if len(tokens) > 1:
                    shutil.rmtree(cid)
                    print(tokens)
                    print("Removed output tokens because there were multiple tokens.")
                assert len(tokens) == 1
                found_students[id][type] = tokens[0]
                if id not in rs:
                    rs[id] = {}

                rs[id]['token_produced'].append(tokens[0])

        assert len(found_students) == len(glob.glob(stage1_dir + "/*")) # Ensure all students have been found.
        for id in found_students:
            if 'python' in found_students[id] and 'token' in found_students[id]:
                t_best, p_best = determine_token_difference(load_token(found_students[id]['token'])[0], load_token(found_students[id]['python'])[0])
                if len(p_best) > 0:
                    for q in p_best.values():
                        for item in q['items']:
                            messages['report'].append(f"{id}> Evaluation of student code was better than the token file evaluation. " + str(item) ) # + " student stderr: \n" + str(q['items'][item]['a']['stderr']) + "\n instructor stderr: \n" + str(q['items'][item]['b']['stderr']))

            elif 'token' in found_students[id] and 'python' not in found_students[id]:
                pass
            elif 'token' not in found_students[id] and 'python' in found_students[id]:
                if id not in configuration.get('stage_report', {}).get("python_handin_checked", []):
                    print("="*50)
                    s = f"{id}> only handed in the .py files and not the .token files. " +str(found_students[id]['python'] + " to skip this mesage, alter the stage_report['python_handin_checked'] field. ")
                    messages['report'].append(s)
                    stoken =token_gather_hidden(load_token(found_students[id]['python'])[0])
                    print(s)
                    dd = defaultdict(list)
                    for q in stoken['details']:
                        for item in stoken['details'][q]['items']:
                            # print(item, stoken['details'][q]['items'][item][0]['status'])
                            dd['test'].append(item)
                            dd['status'].append(stoken['details'][q]['items'][item][0]['status'])
                    print(tabulate.tabulate(dd, headers='keys'))



            else:
                raise Exception(id + "> No code handin for this student")
            tkns = [found_students[id][key] for key in ['token','python'] if key in found_students[id]]
            if len(tkns) == 2:
                t = combine_token_results(load_token(tkns[0])[0], load_token(tkns[1])[0])
            else:
                t, _ = load_token(tkns[0])
            rs[id] = {**rs[id], **t}
        return rs

    rs = _stage_report()
    if len(messages) > 0:
        print("=" * 50)
        print("Oy veh, there are messages")
        for stage in messages:
            print("Messages from", stage)
            for s in messages[stage]:
                print(">> ", s)
        print("-" * 50)
        if accept_problems:
            assert False, "No messages allowed!"

    if plagiarism_check and True:
        from unitgrade_private.plagiarism.mossit import moss_it2023
        moss_it2023(submissions_base_dir=stage4_dir, submissions_pattern="*-token", instructor_grade_script=instructor_grade_script)

    if plagiarism_check and False: # This check is based on detector and is deprecated. I don't like detector.
        from coursebox.core.info_paths import get_paths
        paths = get_paths()
        from copydetect import CopyDetector
        detector = CopyDetector(extensions=["py"], display_t=0.7)
        # rs['Group10']['sources'][0]['report_relative_location']
        relatives = []
        for id in rs:
            v = [int(s.split("_")[-3]) for s in rs[id]['token_produced']]
            token = rs[id]['token_produced'][v.index(max(v))]
            tk, _ = load_token(token)
            rl = tk['sources'][0]['report_relative_location']
            bd = f"{stage3_dir}/{os.path.basename(os.path.dirname(token))}/{os.path.dirname(rl)}"
            chk_files = []
            for q in tk['details']:
                # print(q)
                with open(f"{bd}/unitgrade_data/{tk['details'][q]['name']}.pkl", 'rb') as f:
                    pk = pickle.load(f)

                for item in tk['details'][q]['items']:
                    key = (item, 'coverage')
                    if key in pk:
                        for f in pk[key]:
                            relatives.append(f)
                            chk_files.append( f"{stage3_dir}/{os.path.basename(os.path.dirname(token))}/{f}")
            # print(chk_files)
            chk_files = list(set(chk_files))

            for f in chk_files:
                detector.add_file(f)
            # Fuck this shit just add the solutions.
            for f in set(relatives):
                ff = paths['02450private']+"/Exam/exam2023spring/handout/" + f
                detector.add_file(ff, type="boilerplate")

            detector.run()
            detector.generate_html_report()








        # 799171 89568609
        # _stage_plagiarism()

        pass


    return rs

def docker_verify_projects(learn_zip_file_path, Dockerfile=None, instructor_grade_script=None):
    dzip, tokens = unzip(learn_zip_file_path)
    # paths = get_paths()
    if Dockerfile is None:
        images = download_docker_images()
        # os.path.isfile(images['unitgrade-docker'])
        Dockerfile = images['unitgrade-docker']
    # info = class_information()
    # Dockerfile = paths['02450instructors'] + "/docker/Dockerfile"
    tag = compile_docker_image(Dockerfile)
    print("Docker verify project image tag:", tag)

    if not os.path.isdir(dzip + "/verified_tokens"):
        os.mkdir(dzip + "/verified_tokens")

    res = {}
    # Create a logdir.
    if not os.path.isdir(dzip + "/verified_tokens/logs/"):
        os.mkdir(dzip + "/verified_tokens/logs/")
    if os.path.isdir(dzip + "/verified_tokens/problematic_logs/"):
        shutil.rmtree(dzip + "/verified_tokens/problematic_logs/")
    if not os.path.isdir(dzip + "/verified_tokens/problematic_logs/"):
        os.mkdir(dzip + "/verified_tokens/problematic_logs/")

    def points_from_name(token_name):
        return token_name.split("_")[-3]

    for id in tokens:
        stoken = tokens[id]['token']
        if 'verified_token' in tokens[id]:
            if tokens[id]['verified_token'].split("_")[-3] == tokens[id]['token'].split("_")[-3]:
                print("skipping", id)
                continue
            else:
                print("Token points obtained did not agree, re-running:")
                print("> token   ", tokens[id]['token'])
                print("> verified", tokens[id]['verified_token'])
                for t in glob.glob(os.path.dirname(tokens[id]['verified_token']) + "/*.token"):
                    print(t)
                    os.remove(tokens[id]['verified_token'])

        t0 = time.time()
        # ig = paths['02450students'] + grade_file_paths[project_id] #"/irlc/project0/fruit_project_grade.py"
        instructor_token, out = docker_run_token_file(Dockerfile_location=Dockerfile,
                                                      host_tmp_dir=os.path.dirname(Dockerfile) + "/tmp",
                                                      student_token_file=stoken,
                                                      instructor_grade_script=instructor_grade_script,
                                                      xvfb=True  # Run X11-display (requires that docker is run on Linux).
                                                      )

        if points_from_name(instructor_token) != points_from_name(tokens[id]['token']):
            with open(dzip + "/verified_tokens/problematic_logs/"+id+".txt", 'w') as f:
                f.write(out)

        # Just write the ordinary log file.
        with open(dzip + "/verified_tokens/logs/" + id + ".txt", 'w') as f:
            f.write(out)

        if not os.path.isdir(dzip + "/verified_tokens/" + id):
            os.mkdir(dzip + "/verified_tokens/" + id)

        shutil.copy(instructor_token, dzip + "/verified_tokens/" + id +"/" + os.path.basename(instructor_token))
        print(f"> Verified {stoken} after", time.time()-t0, "instructor token", instructor_token)
        res[id] = {'stoken': stoken, 'time': time.time()-t0, 'instructor_token': instructor_token}

    print("--------docker_verify_projects completed. Summary:------------")
    for id, rs in res.items():
        print(f"> Verified {rs['stoken']} after {rs['time']}, instructor token {rs['instructor_token']}")
    print("---------done--------------")


def token2rs(token):
    r = {'questions': {}}
    for k in token['details']:
        name = token['details'][k]['name']
        r['questions'][name] = {'items': {}}
        for key, item in token['details'][k]['items'].items():
            assert key[0] == name
            r['questions'][name]['items'][key[1]] = item['status']
    return r

def project_print_results(learn_zip_file,verbose=True):
    dzip, tokens = unzip(learn_zip_file)
    dd = defaultdict(list)
    dd['question'] = []
    rs = {}

    for i, id in enumerate(tokens):
        # if os.path.isfile(tokens[id]['token']):
        r = {}
        stoken, _ = load_token(tokens[id]['token'])
        if 'verified_token' in tokens[id]:
            vtoken, _ = load_token(tokens[id]['verified_token'])
        else:
            vtoken = None

        r['stoken'] = token2rs(stoken)
        r['vtoken'] = token2rs(vtoken) if vtoken is not None else {}


        if vtoken is not None:
            for j, k in enumerate(vtoken['details']):
                vob = vtoken['details'][k]['obtained'] if vtoken is not None else -1
                sob = stoken['details'][k]['obtained'] if stoken is not None else -1

                if vob != sob:
                    print(vob, sob)
                    print(k)
                    name = stoken['details'][k]['name']
                    print(name)


                    d = defaultdict(list)
                    for kk, val in vtoken['details'][k]['items'].items():
                        d['verified'].append(kk)
                        d['verified-result'].append(val['status'])
                        d['student-result'].append(stoken['details'][k]['items'][kk]['status'])

                    print(tabulate.tabulate(d, headers='keys'))
                    if name != 'Kiosk3':
                        print(id, "A score could not be verified in the test", name)
                    print("Bad")
                if i == 0:
                    dd['question'].append(stoken['details'][k]['name'])

                dd[id].append(sob) # We go by the students score. This is in case of rounding issues etc.

        dd[id].append(vtoken['total'] if vtoken is not None else -1)
        r['verified-token-total'] = vtoken['total'] if vtoken is not None else -1
        r['student-token-total'] = stoken['total'] if stoken is not None else -1
        r['token_location'] = tokens[id]['token']
        r['id'] = id
        if id.startswith("Group"):
            id = int(id[5:])
        else:
            id = id.lower()
            if len(id) != 7 or id[0] != 's':
                print("Very bad id", id)
                # raise Exception()
        rs[id] = r

    dd['question'].append('Total')
    if verbose:
        print(tabulate.tabulate(dd, headers='keys'))
    # Now sanitize the result. Replace internal learn-ids with 6-digit ids.
    # info = class_information()

    # Turn all of this into a big xlsx file.
    make_xlsx_file(rs)
    return rs


def make_xlsx_file(rs):
    Q = {}
    for id, v in rs.items():
        for token in ['stoken', 'vtoken']:
            for q in v[token]['questions']:
                if q not in Q:
                    Q[q] = {}
                for i in v[token]['questions'][q]['items']:
                    Q[q][i] = True

    # Now we got all of the questions.
    # Dictionary to write to xlsx file.
    d = {}
    for id in rs:
        d['Question'] = []
        d[id] = []
        for q in Q:
            d['Question'].append(q)
            d[id].append(" ")

            for i in Q[q]:
                d['Question'].append(i)

                def gbk(token, q, i):
                    return rs[id][token]['questions'][q]['items'][i] if token in rs[id] and q in rs[id][token]['questions'] and i in rs[id][token]['questions'][q]['items'] else ' - '

                d[id].append(f"{gbk('stoken', q, i)}/{gbk('vtoken', q, i)}" )
            d['Question'].append(" ")
            d[id].append(" ")

        d['Question'].append("Student total (obtained/possible)")
        d[id].append(f"{rs[id]['student-token-total']}")

        d['Question'].append("Verified total (obtained/possible)")
        d[id].append(f"{rs[id]['verified-token-total']}")

    import pandas as pd
    df = pd.DataFrame.from_dict(d)
    df.to_excel("token_evaluations.xlsx")
    print(tabulate.tabulate(d, headers='keys'))
    import pickle
    with open("token_evaluations.pkl", 'wb') as f:
        pickle.dump(rs, f)


def moss_check(dzip, out, moss_id=None):
    # Moss stuff.
    # paths = get_paths()
    # dzip, out = unzip(0)
    if not os.path.isdir(dzip + "/submissions"):
        os.mkdir(dzip + "/submissions")
    if not os.path.isdir(dzip + "/whitelist"):
        os.mkdir(dzip + "/whitelist")

    for student_id in out:
        token = out[student_id]['token']
        if not os.path.isdir(dzip + "/submissions/" + student_id):
            os.mkdir(dzip + "/submissions/" + student_id)

        shutil.copy(token, dzip + "/submissions/" + student_id+"/"+os.path.basename(token))

    # if not os.path.isdir(dzip  + "/whitelist/irlc"):
    #     shutil.copytree(paths['02450students'] + "/irlc", dzip  + "/whitelist/irlc")
    if moss_id is None:
        # id = get_id()
        from pathlib import Path
        id = get_id( str(Path.home())+"/moss.pl")
    print("Calling moss using moss-id", id)
    blacklist = ['*_grade.py', '*project1.py', '*kiosk.py', '*pacman_demo.py', '*pacman.py']
    moss_it(whitelist_dir=dzip + "/whitelist", submissions_dir=dzip +"/submissions", moss_id=id, blacklist=blacklist)



def fname2id(fname, info=None):
    # fname = os.path.basename(f)
    id_cand = fname.split("-")[2].strip().split(",")[0]
    # print(id_cand, token)
    if id_cand.startswith("Group"):
        id = id_cand.replace(" ", "")
    else:
        id = id_cand
        if info is not None:
            if not id[1:].isdigit():
                possible = [sid for sid in info['students'] if info['students'][sid]['initials']  == id]
                if len(possible) == 0:
                    raise Exception(f"Tried to find student id {id} but was not found. You need to download the CSV file from inside and put it in the main config excel sheet.")
                real_id = possible.pop()
                if real_id != id:
                    print("Changing id from", id, "to", real_id)
                    id = real_id



    return id

def unzip(zipfile):
    dzip = zipfile[:-4]
    from coursebox.core.projects import unpack_zip_file_recursively
    unpack_zip_file_recursively(dzip + ".zip", dzip+"/raw" )

    # Now copy to a more sensible format
    out = {}
    if not os.path.isdir(dzip + "/tokens"):
        os.mkdir(dzip + "/tokens")
    for f in glob.glob(dzip +"/raw/*-*"):
        token = glob.glob(f +"/*.token")
        if len(token) != 1:
            print("Problems ")
        assert len(token) == 1
        token = token[0]
        fname = os.path.basename(f)
        id_cand = fname.split("-")[2].strip()
        # print(id_cand, token)
        if id_cand.startswith("Group"):
            id = id_cand.replace(" ", "")
        else:
            id = id_cand

        if not os.path.isdir(dzip +"/tokens/"+id):
            os.mkdir(dzip +"/tokens/"+id)

        dtoken = dzip +"/tokens/"+id +"/" + os.path.basename(token)
        shutil.copy(token, dtoken)
        out[id] = {'token': dtoken}

        if os.path.isdir(dzip + "/verified_tokens/"+id):
            vtokens = glob.glob(dzip + "/verified_tokens/"+id +"/*.token")
            assert len(vtokens) <= 1
            if len(vtokens) == 1:
                out[id]['verified_token'] = vtokens[0]
    return dzip, out




def process_by_zip_file(learn_zip_file_path, output_xlsx=True, moss=True, docker_verify=True, instructor_grade_script=None):
    # Automatic evaluation of tests.
    # Moss
    # Write to excel file
    # Write to pkl file.
    # hidden tests.
    dzip, out = unzip(learn_zip_file_path)

    if moss:
        moss_check(dzip, out)

    if docker_verify:
        docker_verify_projects(learn_zip_file_path, instructor_grade_script=instructor_grade_script)
    verbose = True
    res = project_print_results(learn_zip_file_path,verbose=verbose)



    a = 24
    pass

if __name__ == "__main__":
    # Process a learn .zip file.



    pass