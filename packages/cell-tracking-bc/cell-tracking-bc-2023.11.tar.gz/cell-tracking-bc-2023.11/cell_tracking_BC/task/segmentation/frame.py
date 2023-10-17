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

from typing import Dict, Optional, Sequence

import numpy as nmpy
import scipy.ndimage as spim
import scipy.optimize as spop
from logger_36 import LOGGER
from scipy import ndimage as ndimage_t
from scipy.spatial import distance as dstc
from skimage import morphology as mrph
from skimage import segmentation as sgmt

import cell_tracking_BC.task.registration.rigid as rgst
from cell_tracking_BC.catalog.matching.jaccard import PseudoJaccard
from cell_tracking_BC.type.compartment.base import CompartmentReference

array_t = nmpy.ndarray


MAX_N_NUCLEI = 3

_ROUNDED_SQUARE_5 = nmpy.ones((5, 5), dtype=nmpy.bool_)
_ROUNDED_SQUARE_5[0, 0] = False
_ROUNDED_SQUARE_5[0, -1] = False
_ROUNDED_SQUARE_5[-1, 0] = False
_ROUNDED_SQUARE_5[-1, -1] = False


def CorrectBasedOnTemporalCoherence(
    current: array_t,
    previous: array_t,
    /,
    *,
    min_jaccard: float = 0.75,
    max_area_discrepancy: float = 0.25,
    min_cell_area: int = 0,
    time_point: int = None,
) -> tuple[int, array_t]:
    """
    min_jaccard: Actually, Pseudo-Jaccard
    """
    assert nmpy.issubdtype(current.dtype, nmpy.bool_)

    if time_point is None:
        at_time_point = ""
    else:
        at_time_point = f" at time point {time_point}"

    labeled_current, n_cells_current = mrph.label(
        current, return_num=True, connectivity=1
    )
    labeled_previous, n_cells_previous = mrph.label(
        previous, return_num=True, connectivity=1
    )
    jaccards = _PairwiseJaccards(
        n_cells_previous, n_cells_current, labeled_previous, labeled_current
    )
    c_to_p_links = _CurrentToPreviousLinks(jaccards, min_jaccard)

    frontiers = nmpy.zeros_like(current)
    n_corrections = 0
    for label_current in range(1, n_cells_current + 1):
        labels_previous = c_to_p_links.get(label_current - 1)
        if (labels_previous is not None) and (labels_previous.__len__() > 1):
            labels_previous = nmpy.array(labels_previous) + 1
            context = f"between cells {sorted(labels_previous)} and fused cell {label_current}{at_time_point}"

            where_fused = labeled_current == label_current

            splitted = _SplitLabels(
                where_fused,
                labeled_previous,
                labels_previous,
                max_area_discrepancy,
                min_cell_area,
                context,
            )
            if splitted is None:
                continue

            frontier = nmpy.logical_and(where_fused, splitted == 0)
            current[frontier] = False
            frontiers[frontier] = True
            n_corrections += 1

    return n_corrections, frontiers


def _PairwiseJaccards(
    n_cells_previous: int,
    n_cells_current: int,
    labeled_previous: array_t,
    labeled_current: array_t,
    /,
) -> array_t:
    """"""
    labels_previous = nmpy.fromiter(range(1, n_cells_previous + 1), dtype=nmpy.uint64)
    labels_current = nmpy.fromiter(range(1, n_cells_current + 1), dtype=nmpy.uint64)
    # Note the reversed parameter order in PseudoJaccard since a fusion is a division in reversed time
    _PseudoJaccard = lambda lbl_1, lbl_2: PseudoJaccard(
        labeled_current, labeled_previous, lbl_2, lbl_1
    )

    return dstc.cdist(
        labels_previous[:, None], labels_current[:, None], metric=_PseudoJaccard
    )


def _CurrentToPreviousLinks(
    pairwise_jaccards: array_t, min_jaccard: float, /
) -> Dict[int, Sequence[int]]:
    """"""
    output = {}

    while True:
        row_idc, col_idc = spop.linear_sum_assignment(1.0 - pairwise_jaccards)
        valid_idc = pairwise_jaccards[row_idc, col_idc] > min_jaccard
        if not nmpy.any(valid_idc):
            break

        valid_row_idc = row_idc[valid_idc]
        for col_idx, row_idx in zip(col_idc[valid_idc], valid_row_idc):
            if col_idx in output:
                output[col_idx].append(row_idx)
            else:
                output[col_idx] = [row_idx]

        pairwise_jaccards[valid_row_idc, :] = 0.0

    return output


def _SplitLabels(
    where_fused: array_t,
    labeled_previous: array_t,
    labels_previous: array_t,
    max_area_discrepancy: float,
    min_cell_area: int,
    context: str,
    /,
) -> Optional[array_t]:
    """"""
    output = nmpy.zeros_like(labeled_previous)
    for l_idx, label_previous in enumerate(labels_previous, start=1):
        output[labeled_previous == label_previous] = l_idx

    fused_area = nmpy.count_nonzero(where_fused)
    split_area = nmpy.count_nonzero(output)
    discrepancy = abs(split_area - fused_area) / fused_area
    if discrepancy > max_area_discrepancy:
        LOGGER.warning(
            f"Segmentation correction discarded due to high t-total-area/(t+1)-fused-area discrepancy "
            f"{context}: "
            f"Actual={discrepancy}; Expected<={max_area_discrepancy}."
        )
        return None

    (fused_local, split_local), corners = rgst.InCommonNonZeroRectangles(
        where_fused, output, for_rotation=True
    )

    angle = rgst.RotationInBinary(fused_local, split_local > 0)
    rotated = rgst.RotatedLabeled(split_local, angle)

    split_local = _DilatedWithLabelPreservation(rotated, fused_local, min_cell_area)
    if split_local is None:
        LOGGER.warning(
            f"Segmentation correction discarded due to invalid split regions "
            f"{context}"
        )
        return None

    corner = corners[0]
    rows_gbl, cols_gbl = nmpy.meshgrid(
        range(corner[0], corner[0] + split_local.shape[0]),
        range(corner[1], corner[1] + split_local.shape[1]),
        indexing="ij",
    )
    rows_lcl, cols_lcl = nmpy.indices(split_local.shape)
    valid = nmpy.logical_and(
        nmpy.logical_and(rows_gbl >= 0, cols_gbl >= 0),
        nmpy.logical_and(rows_gbl < output.shape[0], cols_gbl < output.shape[1]),
    )
    output.fill(0)
    output[rows_gbl[valid], cols_gbl[valid]] = split_local[
        rows_lcl[valid], cols_lcl[valid]
    ]

    return output


def _DilatedWithLabelPreservation(
    labeled: array_t, roi: array_t, min_cell_area: int, /
) -> Optional[array_t]:
    """"""
    output = nmpy.ones_like(labeled)

    n_labels = nmpy.amax(labeled).item()
    non_roi = nmpy.logical_not(roi)

    distance_map = spim.distance_transform_edt(labeled != 1)
    for label in range(2, n_labels + 1):
        current_map = spim.distance_transform_edt(labeled != label)
        closer_b_map = current_map < distance_map
        output[closer_b_map] = label
        distance_map[closer_b_map] = current_map[closer_b_map]

    while True:
        intermediate = nmpy.zeros_like(output)
        for label in range(1, n_labels + 1):
            where_label = output == label
            if not nmpy.any(where_label):
                return None
            # TODO: check how erosion behaves on image borders
            eroded = mrph.binary_erosion(where_label)
            intermediate[eroded] = label
        nmpy.copyto(output, intermediate)
        output[non_roi] = 0

        labeled_output, n_output_labels = mrph.label(
            output > 0, return_num=True, connectivity=1
        )
        areas = tuple(
            nmpy.count_nonzero(labeled_output == _lbl)
            for _lbl in range(1, n_output_labels + 1)
        )
        for label, area in enumerate(areas, start=1):
            if area < min_cell_area:
                output[labeled_output == label] = 0
                n_output_labels -= 1
        if n_output_labels == n_labels:
            break

    return output


def AllCompartmentsFromSome(
    *,
    cells_map: array_t = None,
    cytoplasms_map: array_t = None,
    nuclei_map: array_t = None,
) -> tuple[array_t, array_t, array_t]:
    """
    Maps need not be booleans since they are converted.

    Valid options:
        - cell               => nucleus = cell reference pixel, cytoplasm = cell - nucleus
        - cell, cytoplasm    => nucleus = cell - cytoplasm
        - cell, nucleus      => cytoplasm = cell - nucleus
        - cytoplasm          => cell = filled cytoplasm, nucleus = cell - cytoplasm
        - cytoplasm, nucleus => cell = filled cytoplasm
    """
    if (cells_map is None) and (cytoplasms_map is None):
        raise ValueError("Cytoplasms and cells maps both None")
    if not ((cells_map is None) or (cytoplasms_map is None) or (nuclei_map is None)):
        raise ValueError("Nuclei, cytoplasms and cells maps all not None")

    if cells_map is not None:
        cells_map = cells_map > 0
        _CorrectCellsMap(cells_map)
        _CheckCellsMap(cells_map)
    if cytoplasms_map is not None:
        cytoplasms_map = cytoplasms_map > 0
        _CorrectCytoplasmsMap(cytoplasms_map)
        _CheckCytoplasmsMap(cytoplasms_map)
    if nuclei_map is not None:
        nuclei_map = nuclei_map > 0
        _CorrectNucleiMap(nuclei_map)
        _CheckNucleiMap(nuclei_map)

    if cells_map is None:  # Then cytoplasms_map is not None
        if (nuclei_map is not None) and nmpy.any(cytoplasms_map[nuclei_map]):
            raise ValueError("Cytoplasms and nuclei maps intersect")

        cells_map = _CellsMapFromCytoplasms(cytoplasms_map)

        if nuclei_map is None:
            nuclei_map = _InnerCompartmentsMapFromCellsAndOtherInners(
                cells_map, cytoplasms_map
            )
        else:
            eroded_cells_map = _SafelyErodedCellsMap(cells_map)
            if not nmpy.all(eroded_cells_map[nuclei_map]):
                LOGGER.warning(
                    "Nuclei not restricted to cells, or tangent: Correcting nuclei and cytoplasms maps"
                )
                _FitNucleiInErodedCells(eroded_cells_map, nuclei_map)
                cytoplasms_map = _InnerCompartmentsMapFromCellsAndOtherInners(
                    cells_map, nuclei_map
                )
            else:
                union = nmpy.logical_or(cytoplasms_map, nuclei_map)
                if not nmpy.array_equal(cells_map, union):
                    raise ValueError(
                        "Cytoplasms inner borders do not coincide with nuclei"
                    )

            _CorrectNumberOfNucleiPerCell(cells_map, cytoplasms_map, nuclei_map)
    elif cytoplasms_map is None:  # ...and cells_map is not None
        if nuclei_map is None:
            LOGGER.warning("Synthetic cytoplasms and nuclei maps")
            nuclei_map = _NucleiMapFromCells(cells_map)
            cytoplasms_map = _InnerCompartmentsMapFromCellsAndOtherInners(
                cells_map, nuclei_map
            )
        else:  # cells_map is not None, cytoplasms_map is None, and nuclei_map is not None
            # /!\ Almost code duplication
            eroded_cells_map = _SafelyErodedCellsMap(cells_map)
            if not nmpy.all(eroded_cells_map[nuclei_map]):
                LOGGER.warning(
                    "Nuclei not restricted to cells, or tangent: Correcting nuclei map"
                )
                _FitNucleiInErodedCells(eroded_cells_map, nuclei_map)

            cytoplasms_map = _InnerCompartmentsMapFromCellsAndOtherInners(
                cells_map, nuclei_map
            )

            _CorrectNumberOfNucleiPerCell(cells_map, cytoplasms_map, nuclei_map)
    else:  # cells_map is not None and cytoplasms_map is not None (hence, nuclei_map is None)
        _CheckNumberOfCytoplasmsPerCell(cells_map, cytoplasms_map)

        from_cytoplasm = _CellsMapFromCytoplasms(cytoplasms_map)
        if not nmpy.array_equal(from_cytoplasm, cells_map):
            raise ValueError("Cytoplasms outer borders do not coincide with cells")

        nuclei_map = _InnerCompartmentsMapFromCellsAndOtherInners(
            cells_map, cytoplasms_map
        )

    return cells_map, cytoplasms_map, nuclei_map


def _CorrectCellsMap(map_: array_t, /) -> None:
    """"""
    mrph.remove_small_holes(map_, area_threshold=1000, out=map_)
    _RemoveTinyCompartments(map_, map_, "cells")


def _CorrectCytoplasmsMap(map_: array_t, /) -> None:
    """"""
    filled = _CellsMapFromCytoplasms(map_)
    _RemoveTinyCompartments(map_, filled, "cytoplasms")


def _CorrectNucleiMap(map_: array_t, /) -> None:
    """"""
    mrph.remove_small_holes(map_, area_threshold=1000, out=map_)


def _RemoveTinyCompartments(
    to_be_corrected: array_t, to_be_labeled: array_t, plural_name: str, /
) -> None:
    """"""
    l_map, n_compartments = ndimage_t.label(to_be_labeled)  # connectivity=1
    modified = False
    for label in range(1, n_compartments + 1):
        current = l_map == label
        distance_map = ndimage_t.distance_transform_edt(current)
        if nmpy.amax(distance_map) < 2.0:
            to_be_corrected[current] = False
            modified = True

    if modified:
        LOGGER.warning(f"Tiny {plural_name} were removed")


def _CellsMapFromCytoplasms(map_: array_t, /) -> array_t:
    """"""
    return ndimage_t.binary_fill_holes(map_)


def _NucleiMapFromCells(map_: array_t, /) -> array_t:
    """"""
    output = nmpy.zeros_like(map_)

    cells_l_map, n_cells = ndimage_t.label(map_)  # connectivity=1
    for label in range(1, n_cells + 1):
        output[tuple(CompartmentReference(cells_l_map == label))] = True

    return output


def _InnerCompartmentsMapFromCellsAndOtherInners(
    cells_map: array_t, inners_map: array_t, /
) -> array_t:
    """"""
    output = cells_map.copy()
    output[inners_map] = False

    return output


def _FitNucleiInErodedCells(eroded_cells_map: array_t, nuclei_map: array_t, /) -> None:
    """"""
    nuclei_map[nmpy.logical_not(eroded_cells_map)] = False

    cells_l_map, n_cells = ndimage_t.label(eroded_cells_map)  # connectivity=1
    for label in range(1, n_cells + 1):
        cell_l_map = cells_l_map == label
        if not nmpy.any(nuclei_map[cell_l_map]):
            nuclei_map[tuple(CompartmentReference(cell_l_map))] = True


def _CorrectNumberOfNucleiPerCell(
    cells_map: array_t, cytoplasms_map: array_t, nuclei_map: array_t, /
) -> None:
    """"""
    cells_l_map, n_cells = ndimage_t.label(cells_map)  # connectivity=1
    nuclei_l_map, _ = ndimage_t.label(nuclei_map)  # connectivity=1

    for label in range(1, n_cells + 1):
        cell_l_map = cells_l_map == label
        nuclei_inside_cell = nuclei_l_map[cell_l_map]
        nuclei_labels = nmpy.unique(nuclei_inside_cell)
        # Do not use nuclei_labels[1:] since nuclei_labels[0] is not necessarily zero
        nuclei_labels = nuclei_labels[nuclei_labels > 0]
        n_nuclei = nuclei_labels.size
        if n_nuclei == 0:
            LOGGER.warning(
                f"{n_nuclei}: Invalid number of nuclei in cytoplasm. Expected=1 or 2. "
                f"Correcting nuclei and cytoplasms maps"
            )
            reference = tuple(CompartmentReference(cell_l_map))
            nuclei_map[reference] = True
            cytoplasms_map[reference] = False
        elif n_nuclei > MAX_N_NUCLEI:
            LOGGER.warning(
                f"{n_nuclei}: Invalid number of nuclei in cytoplasm. Expected>=1, <={MAX_N_NUCLEI}. "
                f"Correcting nuclei and cytoplasms maps"
            )
            nuclei_labels = sorted(
                nuclei_labels,
                key=lambda _lbl: nmpy.count_nonzero(nuclei_inside_cell == _lbl),
                reverse=True,
            )
            for too_small in nuclei_labels[MAX_N_NUCLEI:]:
                extra_nucleus = nuclei_l_map == too_small
                nuclei_map[extra_nucleus] = False
                cytoplasms_map[extra_nucleus] = True


def _CheckCellsMap(map_: array_t, /) -> None:
    """"""
    _CheckCompartmentsHoles(map_, "cell", False, 0, 0)


def _CheckCytoplasmsMap(map_: array_t, /) -> None:
    """"""
    _CheckCompartmentsHoles(map_, "cytoplasm", True, 1, MAX_N_NUCLEI)
    # cleared = sgmt.clear_border(cytoplasm)
    # labeled_components, n_components = mrph.label(
    #     cleared, return_num=True, connectivity=1
    # )
    # for label in range(1, n_components + 1):
    #     # Actually, n_holes = n_true_holes + background
    #     _, n_holes = mrph.label(
    #         labeled_components != label, return_num=True, connectivity=2
    #     )
    #     if n_holes < 2:
    #         # print(label)
    #         # import matplotlib.pyplot as p
    #         # p.matshow(a)
    #         # p.matshow(labeled_components)
    #         # p.matshow(b)
    #         # p.show()
    #         raise ValueError("Cytoplasm w/o holes")


def _CheckNumberOfCytoplasmsPerCell(
    cells_map: array_t, cytoplasms_map: array_t, /
) -> None:
    """"""
    cells_l_map, n_cells = ndimage_t.label(cells_map)  # connectivity=1
    cytoplasms_l_map, _ = ndimage_t.label(cytoplasms_map)  # connectivity=1

    for label in range(1, n_cells + 1):
        cell_l_map = cells_l_map == label
        cytoplasms_labels = nmpy.unique(cytoplasms_l_map[cell_l_map])
        # Do not use cytoplasms_labels[1:] since cytoplasms_labels[0] is not necessarily zero
        cytoplasms_labels = cytoplasms_labels[cytoplasms_labels > 0]
        n_cytoplasms = cytoplasms_labels.size
        if n_cytoplasms != 1:
            raise ValueError(
                f"{n_cytoplasms}: Invalid number of cytoplasms in cell. Expected=1."
            )


def _CheckNucleiMap(map_: array_t, /) -> None:
    """"""
    _CheckCompartmentsHoles(map_, "nucleus", False, 0, 0)


def _CheckCompartmentsHoles(
    compartments_map: array_t,
    name: str,
    expect_on_border: bool,
    min_n_holes: int,
    max_n_holes: int,
    /,
) -> None:
    """"""
    if expect_on_border:
        cleared = sgmt.clear_border(compartments_map)
    else:
        cleared = compartments_map

    # +1 for background
    min_n_holes += 1
    max_n_holes += 1

    compartments_l_map, n_compartments = mrph.label(
        cleared, return_num=True, connectivity=1
    )
    for label in range(1, n_compartments + 1):
        # Actually, n_holes = n_true_holes + 1 for background
        _, n_holes = mrph.label(
            compartments_l_map != label, return_num=True, connectivity=2
        )
        if (n_holes < min_n_holes) or (n_holes > max_n_holes):
            # print(label)
            # import matplotlib.pyplot as p
            # p.matshow(a)
            # p.matshow(labeled_components)
            # p.matshow(b)
            # p.show()
            raise ValueError(
                f"{n_holes}: Invalid number of holes in {name}. Expected>={min_n_holes-1}, <={max_n_holes-1}"
            )


def _SafelyErodedCellsMap(map_: array_t, /) -> array_t:
    """"""
    output = ndimage_t.binary_erosion(map_, structure=_ROUNDED_SQUARE_5)
    if nmpy.any(output):
        return output

    raise ValueError("Cell too small to contain nuclei")
