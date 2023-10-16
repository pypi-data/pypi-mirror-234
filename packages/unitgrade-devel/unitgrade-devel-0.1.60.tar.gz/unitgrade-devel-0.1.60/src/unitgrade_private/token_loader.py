import os
import zipfile
import io
import numpy as np
import pickle

def unpack_sources_from_token(token_file, destination=None):
    from unitgrade_private import load_token

    rs, _ = load_token(token_file)
    if destination is None:
        destination = os.path.dirname(token_file)
    destination = os.path.normpath(destination)

    for k, data in rs['sources'].items():
        out = destination + "/" + os.path.basename(token_file)[:-6] + f"_{k}/"
        out = destination
        # if not os.path.exists(out):
        zf = zipfile.ZipFile(io.BytesIO(data['zipfile']))
        zf.extractall(out)

# Another token-blocking function


def get_coverage_files(token_file, instructor_grade_script_dir):
    """
    Get the files in the token which are part of the coverage analysis. This is useful for determining which files should be
    e.g. plagiarism checked.

    :param token_file:
    :param instructor_grade_script_dir:
    :return:
    """
    stoken, _ = load_token(token_file)
    cov_files = {}

    for q in stoken['details']:
        cov_files[q] = {}

        with open(f"{instructor_grade_script_dir}/unitgrade_data/{stoken['details'][q]['name']}.pkl", 'rb') as f:
            pk = pickle.load(f)
        for item in stoken['details'][q]['items']:
            key = (item, 'coverage')
            if key in pk:
                cov_files[q][key] = list( pk[(item, 'coverage')].keys() )
    return cov_files



def token_gather_hidden(token_rs, public_test_items_weight=1.):
    """
    Token-rs is a loaded token load_token(...)
    Return a version of the rs structure with the tokens blocked together.

    :param token_rs:
    :return:
    """

    r = token_rs
    rb = {'details': {}}
    ntot = 0
    for q in r['details']:
        rb['details'][q] = r['details'][q].copy()
        rb['details'][q]['items'] = {}
        for item in r['details'][q]['items']:
            if "hide" not in item[1] and 'hidden' not in item[1]:
                rb['details'][q]['items'][item] = [r['details'][q]['items'][item]]
                for i in r['details'][q]['items']:
                    if ("hide" in i[1] or 'hidden' in i[1]) and item[0] == i[0] and i[1].startswith(item[1]):
                        rb['details'][q]['items'][item].append(r['details'][q]['items'][i])
        # Now fix the score.
        item_scores = 0


        for item in rb['details'][q]['items']:
            # w0 = 1 if len(rb['details'][q]['items'][item]) == 1 else public_test_items_weight

            passed =  [i['status'] == 'pass' for i in rb['details'][q]['items'][item]  ]
            if len(passed) == 1:
                dt = np.mean(passed)
            else:
                dt = sum([(public_test_items_weight if k == 0 else 1) * e for k, e in enumerate(passed) ]) / (len(passed)-1+public_test_items_weight if len(passed) > 0 else 1)
            item_scores += dt

            if public_test_items_weight == 1:
                assert dt == np.mean( passed )

            # item_scores +=
        item_scores = item_scores / len(rb['details'][q]['items'])

        # This much score we got from the items.
        # print(q, ntot, item_scores)
        rb['details'][q]['obtained'] = item_scores * rb['details'][q]['possible']
        ntot += rb['details'][q]['obtained']
    rb['total'] = (ntot, r['total'][1])
    return rb

from unitgrade.utils import load_token

def determine_token_difference(student_token_rs, instructor_token_rs):
    # rsa, _ = load_token(student_token)
    # rsb, _ = load_token(instructor_token)
    rsa = student_token_rs
    rsb = instructor_token_rs
    # Must have same keys.
    assert rsa.keys() == rsb.keys()

    def where_a_better_b(a,b):
        a_better_than_b = {}
        kk = list(a.keys())
        kk +=  [k for k in b.keys() if b not in kk]
        for q in kk:
            for item in a[q]['items']:
                # print(q)
                if a[q]['items'][item]['status'] == 'pass' and (item not in b[q]['items'] or b[q]['items'][item]['status'] != 'pass'):
                    if q not in a_better_than_b:
                        a_better_than_b[q] = {'items': {}}
                    a_better_than_b[q]['items'][item] = {'a': a[q]['items'][item], 'b': b[q]['items'].get(item,None)}
        return a_better_than_b
    try:
        a_better_than_b = where_a_better_b(rsa['details'], rsb['details'])
        b_better_than_a = where_a_better_b(rsb['details'], rsa['details'])
    except Exception as e:
        print("Oh no", student_token_rs, instructor_token_rs)
        raise e
    return a_better_than_b, b_better_than_a


def combine_token_results(token_a_rs, token_b_rs):
    """
    token_a_rs = load_token(...)
    token_b_rs = load_token(...)

    Combine by or'in the inputs. It will also recompute the token scores.


    :param token_a_rs:
    :param token_b_rs:
    :return:
    """
    rsd = {}
    n_tot = 0
    n_obt = 0

    for q in set(token_a_rs['details'].keys()) | set(token_b_rs['details'].keys()):
        itemsa = list(token_a_rs['details'][q]['items'])
        itemsb = list(token_b_rs['details'][q]['items'])
        items = itemsa + [i for i in itemsb if i not in itemsa]
        rsd[q] = {'items': {}}
        eql = True
        for i in items:
            ia = token_a_rs['details'][q]['items'].get(i, None) #[i]
            ib = token_b_rs['details'][q]['items'].get(i, None) #[i]
            if ia is None and ib is not None:
                item = ib
                eql = False
            elif ia is not None and ib is None:
                item = ia
                eql = False
            else:
                item = ia if ia['status'] == 'pass' else ib
                if ia['status'] != ib['status']:
                    eql = False
            rsd[q]['items'][i] = item


        for k in token_a_rs['details'][q].keys():
            if k not in ['obtained', 'items']:
                rsd[q][k] = token_a_rs['details'][q][k]
                assert token_a_rs['details'][q][k]  == token_b_rs['details'][q][k], k
            # rsd[q] = k

        w = token_a_rs['details'][q]['w']
        nc = int( np.floor( np.mean( [i['status'] == 'pass' for i in token_a_rs['details'][q]['items'].values()] ) * w ) )
        if eql:
            abt = token_a_rs['details'][q]['obtained']
            assert nc == token_a_rs['details'][q]['obtained'] and nc == token_b_rs['details'][q]['obtained'], f"points differ. {nc} != {abt}"
        rsd[q]['obtained'] = nc
        n_tot += w
        n_obt += nc


    rs = dict(total=(n_obt, n_tot), details=rsd, sources=None, metadata=None)
    return rs



