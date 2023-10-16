# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import logging

# +
from typing import Iterable

from nilearn.datasets import utils
from nilearn import plotting

import numpy as np

import pandas as pd

# -

import nibabel as nib

from neurolang import frontend as fe

# # Prepare NeuroSynth

# +
d_neurosynth = utils._get_dataset_dir("neurosynth", data_dir="neurolang_data")

f_neurosynth = utils._fetch_files(
    d_neurosynth,
    [
        (
            f,
            "https://github.com/neurosynth/neurosynth-data/raw/master/current_data.tar.gz",
            {"uncompress": True},
        )
        for f in ("database.txt", "features.txt")
    ],
    verbose=True,
)

database = pd.read_csv(f_neurosynth[0], sep="\t")
features = pd.read_csv(f_neurosynth[1], sep="\t")

features_normalised = features.melt(
    id_vars=features.columns[0],
    var_name="term",
    value_vars=features.columns[1:],
    value_name="tfidf",
).query("tfidf > 0")


# -

nsh = fe.neurosynth_utils.NeuroSynthHandler()
ns_ds = nsh.ns_load_dataset()
it = ns_ds.image_table
vox_ids, study_ids_ix = it.data.nonzero()
study_ids = ns_ds.image_table.ids[study_ids_ix]
study_id_vox_id = np.transpose([study_ids, vox_ids])
masked_ = it.masker.unmask(np.arange(it.data.shape[0]))
nnz = masked_.nonzero()
vox_id_MNI = np.c_[
    masked_[nnz].astype(int),
    nib.affines.apply_affine(it.masker.volume.affine, np.transpose(nnz)),
]

# # Initialise Probabilistic frontend

# %load_ext snakeviz

from importlib import reload

from neurolang.frontend.probabilistic_frontend import NeurolangPDL
from neurolang.probabilistic import weighted_model_counting
reload(weighted_model_counting)

import logging
logger = logging.getLogger(weighted_model_counting.__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

study_ids = np.unique(study_ids)

study_ids_ = study_ids[:10, None]

sv = pd.DataFrame(study_id_vox_id, columns=['study', 'vox'])
sv = sv[sv.study.isin(study_ids_)]

# +
nl = NeurolangPDL()

study = nl.add_uniform_probabilistic_choice_over_set(study_ids_, name='study')
study_voxel = nl.add_tuple_set(sv.values, name='study_voxel')
# -

with nl.scope as e:
    e.vox[e.x] = study_voxel[e.s, e.x] & study[e.s]
    res = nl.solve_query(e.vox[e.x])


import sys
sys.exit(0)
from pysdd import sdd as SDD

import numpy as np

sdd = SDD.SddManager()



v1 = sdd.add_var_after_last()
v2 = sdd.add_var_after_last()
sdd.add_var_after_last()

weights = np.r_[1, 1, .2, .4, .6, .8, 0, 0]
weights

v1, v2, v3, v4 = sdd.vars

v1.manager.literal(1)

v12 = (v1 & v2)
v1n2 = (v1 & ~v2)



q = (v3 & (v1)) | (v4 & (v1 | v2))
wmc = q.wmc(log_mode=False)
wmc.set_literal_weights_from_array(weights)
wmc.propagate()
wmc.literal_derivative(v3), wmc.literal_derivative(v4)



wmc = (v1 | v2).wmc(log_mode=False)
wmc.set_literal_weights_from_array(weights)
wmc.propagate()

wmc = v12.wmc(log_mode=False)
wmc.set_literal_weights_from_array(weights)
wmc.propagate()

sdd.var

# # Initialise and load the front-end

# +
nl = fe.NeurolangDL()


@nl.add_symbol
def agg_count(x: Iterable) -> int:
    return len(x)


@nl.add_symbol
def agg_sum(x: Iterable) -> float:
    return x.sum()


@nl.add_symbol
def agg_mean(x: Iterable) -> float:
    return x.mean()


@nl.add_symbol
def agg_create_region(x: Iterable, y: Iterable, z: Iterable) -> fe.ExplicitVBR:
    mni_t1 = it.masker.volume
    voxels = nib.affines.apply_affine(np.linalg.inv(mni_t1.affine), np.c_[x, y, z])
    return fe.ExplicitVBR(voxels, mni_t1.affine, image_dim=mni_t1.shape)


@nl.add_symbol
def agg_create_region_overlay(
    x: Iterable, y: Iterable, z: Iterable, v: Iterable
) -> fe.ExplicitVBR:
    mni_t1 = it.masker.volume
    voxels = nib.affines.apply_affine(np.linalg.inv(mni_t1.affine), np.c_[x, y, z])
    return fe.ExplicitVBROverlay(voxels, mni_t1.affine, v, image_dim=mni_t1.shape)


ns_pmid_term_tfidf = nl.add_tuple_set(
    features_normalised.values, name="ns_pmid_term_tfidf"
)
ns_activations = nl.add_tuple_set(
    database[["id", "x", "y", "z", "space"]].values, name="ns_activations"
)
ns_activations_by_id = nl.add_tuple_set(study_id_vox_id, name="ns_activations_by_id")
ns_vox_id_MNI = nl.add_tuple_set(vox_id_MNI, name="ns_vox_id_MNI")
# -

# ## Forward inference on term "Auditory"

datalog_script = """
term_docs(term, pmid) :- ns_pmid_term_tfidf(pmid, term, tfidf),\
    term == 'auditory', tfidf > .003

act_term_counts(term, voxid, agg_count(pmid)) :- \
    ns_activations_by_id(pmid, voxid) &\
    term_docs(term, pmid)\

term_counts(term, agg_count(pmid)) :-  \
    ns_pmid_term_tfidf(pmid, term, tfidf) & \
    term_docs(term, pmid)

p_act_given_term(voxid, x, y, z, term, prob) :- \
    act_term_counts(term, voxid, act_term_count) & \
    term_counts(term, term_count) & \
    ns_vox_id_MNI(voxid, x, y, z) & \
    prob == (act_term_count / term_count)

auditory_voxels(voxid) :- p_act_given_term(voxid, x, y, z, term, prob) & prob > .1

region_prob(agg_create_region_overlay(x, y, z, prob)) :- \
    p_act_given_term(voxid, x, y, z, term, prob)

thr_prob(agg_create_region(x, y, z)) :- \
    p_act_given_term(voxid, x, y, z, term, prob) & \
    prob > 0.1
"""

with nl.scope as e:
    nl.execute_datalog_program(datalog_script)
    res = nl.solve_all()

for k, v in res.items():
    nl.add_tuple_set(v.unwrap(), name=k)

r = next(iter(res["thr_prob"].unwrap()))[0]
plotting.plot_roi(r.spatial_image())

r = next(iter(res["region_prob"].unwrap()))[0]
plotting.plot_stat_map(r.spatial_image())



datalog_reverse_inference = '''
term_docs_all(term, pmid) :- ns_pmid_term_tfidf(pmid, term, tfidf), tfidf > .003

auditory_activations(pmid, voxid) :- \
    ns_activations_by_id(pmid, voxid) & \
    p_act_given_term(voxid, x, y, z, term, prob) & \
    prob > 0.1

num_docs(agg_count(pmid)) :- ns_activations_by_id(pmid, voxid)

act_counts_aud(voxid, agg_count(pmid)) :- auditory_activations(pmid, voxid)

act_term_counts_all(term, voxid, agg_count(pmid)) :- \
    term_docs_all(term, pmid) & \
    auditory_activations(pmid, voxid)
    
p_term_given_act(term, voxid, prob) :- \
    act_counts_aud(voxid, act_count) & \
    act_term_counts_all(term, voxid, act_term_count) & \
    prob == act_term_count / act_count
    
p_act_aud(voxid, prob) :- \
    act_counts_aud(voxid, count) & \
    num_docs(doc_count) & \
    prob == count / doc_count
    
p_term_g_aud_voxels(term, agg_sum(prob)) :- \
    p_term_given_act(term, voxid, prob_t_g_a) & \
    p_act(voxid, prob_act) & \
    prob == prob_t_g_a * prob_act 

'''
with nl.scope as e:
    nl.execute_datalog_program(datalog_reverse_inference)
    res = nl.solve_all()

import pandas as pd

pd.DataFrame(res['p_term'].unwrap()).sort_values(1, ascending=False)

res['p_term'].unwrap()

res['act_counts'].row_type

# +

with nl.scope as e:
    #e.term_docs[e.term, e.pmid] :- e.ns_pmid_term_tfidf(e.pmid, e.term, e.tfidf),\
    #term == 'auditory', tfidf > .003    
    e.auditory_activations[e.pmid, e.voxid] = (
        ns_activations_by_id(e.pmid, e.voxid) &
        e.p_act_given_term(e.voxid, e.x, e.y, e.z, e.term, e.prob) &
        (e.prob > 0.1)
    )
    
    e.act_term_counts_all[e.term, e.voxid, agg_count(e.pmid)] = (
        e.term_docs[e.term, e.pmid] &
        e.auditory_activations[e.pmid, e.voxid]
    )
    e.act_counts[e.voxid, agg_count(e.pmid)] = e.auditory_activations(e.pmid, e.voxid)

    e.p_term_given_act[e.term, e.voxid, e.prob] = (
        e.act_term_counts_all[e.term, e.voxid, e.act_term_count] &
        e.act_counts[e.voxid, e.act_count] &
        (e.prob == e.act_term_count / e.act_count)
    )
    
    #e.e_term_given_aud_act[e.term, agg_sum(e.p)] = (
    #    e.p_term_given_act[e.term, e.voxid, e.prob] & 
    #    e.act_prob[e.voxid, e.act_prob_] &
    #    (e.p == e.prob * e.act_prob_)    
    #)
    res = nl.solve_all()
# -


