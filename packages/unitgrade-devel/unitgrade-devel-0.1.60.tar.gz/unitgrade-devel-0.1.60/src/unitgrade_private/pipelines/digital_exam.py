import os
import shutil
import zipfile
import glob
import sys
import shutil
from collections import defaultdict

def digital_exam2instructors(de_zipfile_in, destination_zipfile):
    def digital_exam_repack(de_zipfile_in, destination_folder):
        pass
    dz = os.path.dirname(destination_zipfile) +"/de_repacked"
    if os.path.isdir(dz):
        shutil.rmtree(dz)

    with zipfile.ZipFile(de_zipfile_in, 'r') as zip_ref:
        zip_ref.extractall(dz)

    sh = defaultdict(list)
    files = glob.glob(dz + "/*_*_*")
    for f in files:
        name = os.path.basename(f)
        n = name.split("_")
        sh[n[0]].append(f)
    assert sum(map(len, sh.values())) == len(files)
    for id in sh:
        dname = f"{dz}/XXXX-YYYY - {id}, NAME - XX January, 2023 931 PM"
        if not os.path.isdir(dname):
            os.makedirs(dname) #f"{dz}/{dname}")
        for f in sh[id]:
            name = os.path.basename(f).split("_")
            assert name[3] in ['Bilag', 'Hovedopgave', 'Forside']
            if name[3] == 'Forside':
                name[4] = 'Forside' + name[4]
            shutil.move(f, f"{dname}/{name[4]}")

    shutil.make_archive(destination_zipfile, 'zip', dz)
    shutil.rmtree(dz)


    # unpacked and ready.
    # This deployed the DE.
    # What to do next?
    # Do a report!




if __name__ == "__main__":
    # de_zipfile_in =

    pass

