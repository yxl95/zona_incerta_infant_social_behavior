
# -*- coding: utf-8 -*-
"""
Cell coordinates registration, using the ClearMap2.1 Framework
=======
See the :ref:`TubeMap tutorial </TubeMap.ipynb>` for a tutorial and usage.

References
----------
.. [Kirst2020] `Mapping the Fine-Scale Organization and Plasticity of the Brain Vasculature. Kirst, C., Skriabine, S., Vieites-Prado, A., Topilko, T., Bertin, P., Gerschenfeld, G., Verny, F., Topilko, P., Michalski, N., Tessier-Lavigne, M. and Renier, N., Cell, 180(4):780-795 <https://doi.org/10.1016/j.cell.2020.01.028>`_
"""

if __name__ == '__main__':

    # %%############################################################################
    # Initialization
    ###############################################################################

    # %% Initialize workspace

    from ClearMap.Environment import *  # analysis:ignore

    # directories and files
    directory = '/data/buffer/anamarta.capaz/452'
    resources_directory = settings.resources_path
    ws = wsp.Workspace('TubeMap', directory=directory)
    ws.update(raw=expression_raw, autofluorescence=expression_auto)
    ws.info()
    

    # init atlas and reference files
    annotation_file, reference_file, distance_file = ano.prepare_annotation_files(
        slicing=(slice(None), slice(None), slice(None)), orientation=(-3, 2, 1),
        overwrite=False, verbose=True)

    # alignment parameter files
    align_channels_affine_file = io.join(
        resources_directory, 'Alignment/align_affine.txt')
    align_reference_affine_file = io.join(
        resources_directory, 'Alignment/align_affine.txt')
    align_reference_bspline_file = io.join(
        resources_directory, 'Alignment/align_bspline.txt')
    

###############################################################################
# %% Alignment - resampled to autofluorescence: assumes the existence of a resampled.tif and resampled_autofluorescence.tif files, which are the downsampled versions of the original mosaics at 25µm isotropic
###############################################################################

    # align the two channels
    align_channels_parameter = {
        # moving and reference images
        "moving_image": ws.filename('resampled', postfix='autofluorescence'),
        "fixed_image": ws.filename('resampled'),

        # elastix parameter files for alignment
        "affine_parameter_file": align_channels_affine_file,
        "bspline_parameter_file": None,

        # directory of the alig'/home/nicolas.renier/Documents/ClearMap_Ressources/Par0000affine.txt',nment result
        "result_directory":  ws.filename('resampled_to_auto')
    }

    elx.align(**align_channels_parameter)

    # %% Alignment - autoflourescence to reference

    # align autofluorescence to reference
    align_reference_parameter = {
        # moving and reference images
        "moving_image": reference_file,
        "fixed_image": ws.filename('resampled', postfix='autofluorescence'),

        # elastix parameter files for alignment
        "affine_parameter_file":  align_reference_affine_file,
        "bspline_parameter_file":  align_reference_bspline_file,
        # directory of the alignment result
        "result_directory":  ws.filename('auto_to_reference')
    }

    elx.align(**align_reference_parameter)

    # %% Cell coordinates transform:

    import pandas as pd

    path = "/data/buffer/anamarta.capaz/452/coords_452.csv" #This is the table of cell coordinates in the original image
    rabies = pd.read_csv(path)[["x", "y", "z"]].values

    # %%

    def transformation(coordinates):
        coordinates = res.resample_points(
            coordinates, sink=None, orientation=None,
            source_shape=(6055, 7642, 1948), #This is the size of the original image
            sink_shape=io.shape(ws.filename('resampled')))

        coordinates = elx.transform_points(
            coordinates, sink=None,
            transform_directory=ws.filename('resampled_to_auto'),
            binary=True, indices=False)

        coordinates = elx.transform_points(
            coordinates, sink=None,
            transform_directory=ws.filename('auto_to_reference'),
            binary=True, indices=False)

        return coordinates

    coordinates_transformed = transformation(rabies)



# %%############################################################################
# Voxelize Cell density (for representation)
###############################################################################

    voxelize_cells_parameter = {
        "method": 'sphere',
        "radius": (10, 10, 10),
        "weights": None,
        "shape": io.shape(reference_file),
        "verbose": True
    }

    branch_density = vox.voxelize(coordinates_transformed, sink=ws.filename(
        'density', postfix='cells'), dtype='float32', **voxelize_cells_parameter)

###############################################################################
   # %% Cells regional annotation
###############################################################################

ano.set_annotation_file(annotation_file)
label = ano.label_points(coordinates_transformed, key='id')
names = ano.convert_label(label, key='id', value='name')


coordinates_transformed.dtype = [(t, float) for t in ('xt', 'yt', 'zt')]
label = np.array(label, dtype=[('order', int)])
names = np.array(names, dtype=[('name', 'U256')])
import numpy.lib.recfunctions as rfn
cells_data = rfn.merge_arrays([coordinates_transformed, label, names], flatten=True, usemask=False)

io.write('/data/buffer/anamarta.capaz/452/452.npy', cells_data) #writes an array with the cell annotations and transformed atlas coordinates
