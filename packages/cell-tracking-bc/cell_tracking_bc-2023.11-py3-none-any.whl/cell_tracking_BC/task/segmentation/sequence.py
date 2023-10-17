# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import List, Optional, Sequence

import numpy as nmpy
import scipy.ndimage as ndimage_t

import cell_tracking_BC.in_out.text.progress as prgs
from cell_tracking_BC.task.segmentation.frame import (
    AllCompartmentsFromSome as AllFrameCompartmentsFromSome,
)
from cell_tracking_BC.task.segmentation.frame import (
    CorrectBasedOnTemporalCoherence as CorrectFrameBasedOnTemporalCoherence,
)

array_t = nmpy.ndarray


def FillTemporalGaps(frames: Sequence[array_t], extent: Optional[int], /) -> None:
    """"""
    if (extent is None) or (extent <= 0):
        return

    volume = nmpy.dstack(frames)
    line = nmpy.ones((1, 1, extent + 1), dtype=nmpy.bool_)
    # TODO: choose between skimage.morphology and ndimage_t versions (same remark everywhere morph. math. is used)
    ndimage_t.binary_closing(volume, structure=line, origin=(0, 0, 0), output=volume)

    # Exclude first and last frames to avoid border effects
    for f_idx in range(1, frames.__len__() - 1):
        frames[f_idx][...] = volume[..., f_idx]


def CorrectBasedOnTemporalCoherence(
    frames: Sequence[array_t],
    /,
    *,
    min_jaccard: float = 0.75,
    max_area_discrepancy: float = 0.25,
    min_cell_area: int = 0,
) -> Sequence[array_t]:
    """
    Actually, Pseudo-Jaccard
    """
    assert nmpy.issubdtype(frames[0].dtype, nmpy.bool_)

    output = frames.__len__() * [nmpy.zeros_like(frames[0])]

    base_description = "Segmentation Correction(s) "
    n_corrections = 0
    with prgs.ProgressDesign() as progress:
        progress_context = prgs.progress_context_t(
            progress,
            frames.__len__() - 1,
            first=1,
            description=base_description + "0",
        )
        for f_idx in progress_context.elements:
            n_new_corrections, output[f_idx] = CorrectFrameBasedOnTemporalCoherence(
                frames[f_idx],
                frames[f_idx - 1],
                min_jaccard=min_jaccard,
                max_area_discrepancy=max_area_discrepancy,
                min_cell_area=min_cell_area,
                time_point=f_idx,
            )
            n_corrections += n_new_corrections
            progress_context.UpdateDescription(base_description + str(n_corrections))

    return output


def AllCompartmentsFromSome(
    *,
    cells_maps: Sequence[array_t] = None,
    cytoplasms_maps: Sequence[array_t] = None,
    nuclei_maps: Sequence[array_t] = None,
) -> tuple[List[array_t], List[array_t], List[array_t]]:
    """
    Valid options: see AllFrameCompartmentsFromSome
    """
    output_cells = []
    output_cytoplasms = []
    output_nuclei = []

    lengths = tuple(
        0 if _mps is None else _mps.__len__()
        for _mps in (cells_maps, cytoplasms_maps, nuclei_maps)
    )
    if ((max_length := max(lengths)) == 0) or (
        min(_lgt for _lgt in lengths if _lgt > 0) != max_length
    ):
        raise ValueError(
            f"{lengths}: Compartments maps with different lengths, or all empty"
        )
    length = lengths[0]

    if cells_maps is None:
        cells_maps = length * [None]
    if cytoplasms_maps is None:
        cytoplasms_maps = length * [None]
    if nuclei_maps is None:
        nuclei_maps = length * [None]
    for cells_map, cytoplasms_map, nuclei_map in zip(
        cells_maps, cytoplasms_maps, nuclei_maps
    ):
        compartments = AllFrameCompartmentsFromSome(
            cells_map=cells_map,
            cytoplasms_map=cytoplasms_map,
            nuclei_map=nuclei_map,
        )
        output_cells.append(compartments[0])
        output_cytoplasms.append(compartments[1])
        output_nuclei.append(compartments[2])

    return output_cells, output_cytoplasms, output_nuclei
