# -*- coding: utf-8 -*-
# %%
r'''
NeuroLang Datalog Example based on the Destrieux Atlas and Neurosynth
=====================================================================


Uploading the Destrieux left sulci into NeuroLang and
executing some simple queries.
'''
import nibabel as nib
from nilearn import datasets
from nilearn import plotting
import numpy as np

# %%
from neurolang import frontend as fe

# %% [markdown]
# ##############################################################################
# Load the Destrieux example from nilearn
# ---------------------------------------

# %%
destrieux_dataset = datasets.fetch_atlas_destrieux_2009()
destrieux_map = nib.load(destrieux_dataset['maps'])


# %% [markdown]
# ##############################################################################
# Initialize the NeuroLang instance and load Destrieux's cortical parcellation
# -----------------------------------------------------------------------------


# %%
nl = fe.NeurolangDL()
destrieux = nl.new_symbol(name='destrieux')
d = []
for label_number, name in destrieux_dataset['labels']:
    if label_number == 0:
        continue
    name = name.decode()
    region = nl.create_region(destrieux_map, label=label_number)
    if region is None:
        continue
    name = name.replace('-', '_').replace(' ', '_')
    d.append((name.lower(), region))

# %%
destrieux = nl.add_tuple_set(d, name='destrieux')

# %% [markdown]
# ##############################################################################
# Add a function to measure a region's volume
# -----------------------------------------------------------------------------

# %%
from typing import AbstractSet, Tuple
from neurolang.type_system import Unknown


# %%
class FrozenArray(np.ndarray):
    def __array_finalize__(self, obj):
        print(self, obj)
    def __hash__(self):
        return hash(vv.tobytes())


# %%
a = np.array([0, 1])
a.setflags(write=False)
a.flags


# %%
class FrozenArray(np.ndarray):

    def __new__(cls, input_array, info=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls).setflags(write=False)
        # add the new attribute to the created instance
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        pass
    
    def __hash__(self):
        return hash(self.tobytes())


# %%
b = a.view(FrozenArray)
hash(b)

# %%
hash(a.view(FrozenArray))


# %%
@nl.add_symbol
def region_volume(region: fe.ExplicitVBR) -> float:
    volume = (
        len(region.voxels) *
        float(np.product(np.abs(np.linalg.eigvals(region.affine[:-1, :-1]))))
    )
    return volume

@nl.add_symbol
def region_affine(region: fe.ExplicitVBR) -> FrozenArray:
    return region.affine.view(FrozenArray)

@nl.add_symbol
def region_voxels(region: fe.ExplicitVBR) -> FrozenArray:
    v = region.voxels.copy()
    v.setflags(write=False)
    return v

@nl.add_symbol
def length(x: AbstractSet) -> int:
    return int(len(x))


# %% [markdown]
# ##############################################################################
# Load all contiguous regions from Neurosynth that fit the term "supramarginal"
# -----------------------------------------------------------------------------


# %%
with nl.environment as e:
    res = nl.query(e.q(length(e.y)), e.destrieux(e.x, e.y))
print(res)

# %%
from operator import contains

# %%
with nl.environment as e:
    e.q[e.z] = e.destrieux(e.x, e.y) & (e.z == region_affine(e.y))
    e.qq[e.w] = (contains(e.w, e.z) & e.q(e.z))
v = res.value
v

# %%
neurosynth_supramarginal = nl.load_neurosynth_term_regions(
    'supramarginal',
    name='neurosynth_supramarginal'
)


# %% [markdown]
# #######################################################################
# Query all Destrieux regions that overlap with NeuroSynth supramarginal
# region having volume larger than 2500mm3 with the environment
# ----------------------------------------------------------------------


# %%
with nl.environment as e:
    res = nl.query(
            e.query(e.name, e.region_1),
            e.destrieux(e.name, e.region_1) &
            neurosynth_supramarginal(e.region_2) &
            (region_volume(e.region_2) > 2500) &
            nl.symbols.overlapping(e.region_1, e.region_2)
    )


# %%
for name, region in res.value:
    plotting.plot_roi(region.spatial_image(), title=name)


# %% [markdown]
# #######################################################################
# Query all Destrieux regions that overlap with NeuroSynth supramarginal
# region having volume larger than 2500mm3
# ----------------------------------------------------------------------


# %%
region_1 = nl.new_symbol(name='region_1')
region_2 = nl.new_symbol(name='region_2')
query = nl.new_symbol(name='query')
name = nl.new_symbol(name='name')

# %%
res = nl.query(
        query(name, region_1),
        destrieux(name, region_1) & neurosynth_supramarginal(region_2) &
        (region_volume(region_2) > 2500) &
        nl.symbols.overlapping(region_1, region_2)
)


# %%
for name, region in res.value:
    plotting.plot_roi(region.spatial_image(), title=name)
