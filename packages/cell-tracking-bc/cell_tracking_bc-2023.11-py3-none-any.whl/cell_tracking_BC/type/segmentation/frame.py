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

from __future__ import annotations

import dataclasses as dtcl
from typing import Callable, Dict, List, Optional, Sequence, Union

import numpy as nmpy
import skimage.morphology as mrph
from scipy.sparse import csr_array as s_array_t

from cell_tracking_BC.type.compartment.base import compartment_id_t
from cell_tracking_BC.type.compartment.cell import cell_t

array_t = nmpy.ndarray
frame_h = s_array_t
inner_outer_associations_h = Dict[int, Union[int, tuple[int, int]]]
CellIssues_h = Callable[[int, array_t, dict], Optional[Union[str, Sequence[str]]]]


_AsArray = s_array_t.toarray


@dtcl.dataclass(repr=False, eq=False)
class segmentation_t:
    shape: tuple[int, int] = None
    _cells_map: frame_h = None  # dtype=bool; Never None after instantiation
    _nuclei_map: frame_h = None  # dtype=bool
    cells: List[cell_t] = dtcl.field(init=False, default_factory=list)
    invalid_cells: List[tuple[int, Union[str, Sequence[str]]]] = dtcl.field(
        init=False, default_factory=list
    )

    @classmethod
    def NewFromCellsMap(
        cls,
        cells_map: array_t,
        /,
        *,
        nuclei_map: array_t = None,
    ) -> segmentation_t:
        """"""
        shape = cells_map.shape
        cells_map = s_array_t(cells_map)
        if nuclei_map is not None:
            nuclei_map = s_array_t(nuclei_map)

        return cls(shape=shape, _cells_map=cells_map, _nuclei_map=nuclei_map)

    @property
    def has_nuclei(self) -> bool:
        """"""
        return self._nuclei_map is not None

    @property
    def cells_map(self) -> array_t:
        """"""
        return _AsArray(self._cells_map)

    @property
    def cytoplasms_map(self) -> array_t:
        """"""
        output = (
            self.cells_map.copy()
        )  # Copy: only in case "cells_map" becomes an array one day
        output[self.nuclei_map] = False

        return output

    @property
    def nuclei_map(self) -> array_t:
        """"""
        return _AsArray(self._nuclei_map)

    # TODO: regularly check if this method (and its segmentations_t equivalent) is still needed
    def Compartment(self, compartment: compartment_id_t, /) -> array_t:
        """"""
        if compartment is compartment_id_t.CELL:
            return self.cells_map

        if compartment is compartment_id_t.CYTOPLASM:
            return self.cytoplasms_map

        if compartment is compartment_id_t.NUCLEUS:
            return self.nuclei_map

        raise ValueError(f"{compartment}: Invalid compartment, or compartment is None")

    def BuildCellsFromMaps(self) -> None:
        """
        Segmentation are supposed to be binary (as opposed to already labeled)
        """
        labeled_cells, n_cells = mrph.label(
            self.cells_map, return_num=True, connectivity=1
        )

        if self.has_nuclei:
            labeled_nuclei = mrph.label(self.nuclei_map, connectivity=1)
            # TODO: code duplication with task>segmentation>_CorrectNumberOfNucleiPerCell
            for label in range(1, n_cells + 1):
                current_cell = labeled_cells == label
                inside_cell = labeled_nuclei[current_cell]
                labels_inside = nmpy.unique(inside_cell)
                assert labels_inside[0] == 0
                assert labels_inside.size > 1
                current_nuclei = labeled_nuclei == labels_inside[1]
                if labels_inside.size > 2:
                    for nucleus_lbl in labels_inside[2:]:
                        current_nuclei = nmpy.logical_or(
                            current_nuclei, labeled_nuclei == nucleus_lbl
                        )
                cell = cell_t.NewFromMaps(
                    cell_map=current_cell, nucleus_map=current_nuclei
                )
                self.cells.append(cell)
        else:
            for label in range(1, n_cells + 1):
                cell = cell_t.NewFromMaps(cell_map=labeled_cells == label)
                self.cells.append(cell)

    @property
    def has_cells(self) -> bool:
        """"""
        return (self.cells is not None) and (self.cells.__len__() > 0)

    # @property
    # def available_cell_features(self) -> Sequence[str]:
    #     """"""
    #     return self.cells[0].available_features
    #
    # @property
    # def available_cytoplasm_features(self) -> Sequence[str]:
    #     """"""
    #     if self.has_nuclei:
    #         return self.cells[0].cytoplasm.available_features
    #
    #     return ()
    #
    # @property
    # def available_nucleus_features(self) -> Sequence[str]:
    #     """"""
    #     if self.has_nuclei:
    #         return self.cells[0].nuclei[0].available_features
    #
    #     return ()

    @property
    def cell_areas(self) -> Sequence[int]:
        """"""
        labeled, n_cells = mrph.label(self.cells_map, return_num=True, connectivity=1)
        output = tuple(
            nmpy.count_nonzero(labeled == _lbl) for _lbl in range(1, n_cells + 1)
        )

        return output

    def CellAreaHistogram(
        self,
        /,
        *,
        n_bins: int = None,
        should_return_centers: bool = False,
        should_round_centers: bool = True,
    ) -> tuple[array_t, array_t]:
        """"""
        areas = self.cell_areas

        if n_bins is None:
            n_bins = int(round(nmpy.sqrt(areas.__len__())))
        counts, edges = nmpy.histogram(areas, bins=n_bins)
        if should_return_centers:
            centers = 0.5 * (edges[:-1] + edges[1:])
            if should_round_centers:
                centers = nmpy.around(centers).astype(nmpy.uint64)
            edges = centers

        return counts, edges
