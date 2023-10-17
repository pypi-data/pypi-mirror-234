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

import functools as fctl
from itertools import starmap, zip_longest
from multiprocessing import Pool as pool_t
from typing import Any, Iterator, List, Sequence, Union

import numpy as nmpy
import skimage.morphology as mrph

import cell_tracking_BC.in_out.text.progress as prgs
from cell_tracking_BC.task.feature.base import feature_computation_h
from cell_tracking_BC.type.compartment.base import compartment_id_t
from cell_tracking_BC.type.compartment.cell import cell_t
from cell_tracking_BC.type.compartment.cytoplasm import cytoplasm_t
from cell_tracking_BC.type.compartment.nucleus import nucleus_t
from cell_tracking_BC.type.segmentation.frame import segmentation_t

array_t = nmpy.ndarray


class segmentations_t(List[segmentation_t]):
    @classmethod
    def NewFromCellsMaps(
        cls,
        cells_maps: Sequence[array_t],
        /,
        *,
        nuclei_maps: Sequence[array_t] = None,
    ) -> segmentations_t:
        """"""
        instance = cls()

        if nuclei_maps is None:
            nuclei_maps = cells_maps.__len__() * [None]

        for cells_map, nuclei_map in zip(cells_maps, nuclei_maps):
            segmentation = segmentation_t.NewFromCellsMap(
                cells_map, nuclei_map=nuclei_map
            )
            instance.append(segmentation)

        return instance

    @property
    def length(self) -> int:
        """"""
        return self.__len__()

    def Compartments(self, compartment: compartment_id_t, /) -> Sequence[array_t]:
        """"""
        return tuple(_sgm.Compartment(compartment) for _sgm in self)

    def BuildCellsFromMaps(self) -> None:
        """
        Segmentation are supposed to be binary (as opposed to already labeled)
        """
        for segmentation in self:
            segmentation.BuildCellsFromMaps()

    def NCells(
        self, /, *, in_frame: Union[int, Sequence[int]] = None
    ) -> Union[int, Sequence[int]]:
        """
        in_frame: None=>total over the sequence
        """
        if in_frame is None:
            return sum(_cll.__len__() for _cll in self.cells_iterator)

        just_one = isinstance(in_frame, int)
        if self.has_cells:
            if just_one:
                in_frame = (in_frame,)

            output = in_frame.__len__() * [0]

            for f_idx, cells in enumerate(self.cells_iterator):
                if f_idx in in_frame:
                    output[in_frame.index(f_idx)] = cells.__len__()

            if just_one:
                output = output[0]
        elif just_one:
            output = 0
        else:
            output = in_frame.__len__() * (0,)

        return output

    @property
    def cells_iterator(self) -> Iterator[Sequence[cell_t]]:
        """"""
        for segmentation in self:
            yield segmentation.cells

    @property
    def cytoplasms_iterator(self) -> Iterator[Sequence[cytoplasm_t]]:
        """"""
        for segmentation in self:
            yield tuple(_cll.cytoplasm for _cll in segmentation.cells)

    @property
    def nuclei_iterator(self) -> Iterator[Sequence[tuple[nucleus_t, ...]]]:
        """"""
        for segmentation in self:
            nuclei = []
            for cell in segmentation.cells:
                nuclei.extend(cell.nuclei)
            yield tuple(nuclei)

    def AddCompartmentFeature(
        self,
        compartment: compartment_id_t,
        name: Union[str, Sequence[str]],
        Feature: feature_computation_h,
        /,
        frames: Union[Sequence[array_t], Sequence[Sequence[array_t]]] = None,
        should_run_in_parallel: bool = True,
        should_run_silently: bool = False,
        **kwargs,
    ) -> None:
        """
        name: If an str, then the value returned by Feature will be considered as a whole, whether it is actually a
        single value or a value container. If a sequence of str's, then the object returned by Feature will be iterated
        over, each element being matched with the corresponding name in "name".
        frames: if None, then geometrical feature, else radiometric feature.

        /!\ There is no already-existing check
        """
        if isinstance(name, str):
            description = f'Feature "{name}"'
        elif name.__len__() > 2:
            description = f'Feature "{name[0]}, ..., {name[-1]}"'
        else:
            description = f'Feature "{name[0]}, {name[1]}"'
        PreConfiguredFeatureFct = fctl.partial(Feature, **kwargs)

        with prgs.ProgressDesign(should_be_silent=should_run_silently) as progress:
            if compartment is compartment_id_t.CELL:
                compartment_iterator = self.cells_iterator
            elif compartment is compartment_id_t.CYTOPLASM:
                compartment_iterator = self.cytoplasms_iterator
            else:
                compartment_iterator = self.nuclei_iterator
            if frames is None:
                iterator = compartment_iterator
            else:
                iterator = zip(compartment_iterator, frames)
            progress_context = prgs.progress_context_t(
                progress,
                iterator,
                total=self.__len__(),
                description=description,
            )

            if should_run_in_parallel:
                pool = pool_t()
                MapFunctionOnList = pool.map
                StarMapFunctionOnList = pool.starmap
            else:
                pool = None
                MapFunctionOnList = map
                StarMapFunctionOnList = starmap

            if frames is None:
                if isinstance(name, str):
                    for compartments in progress_context.elements:
                        features = MapFunctionOnList(
                            PreConfiguredFeatureFct, compartments
                        )
                        for compartment, feature in zip(compartments, features):
                            compartment.AddFeature(name, feature)
                else:
                    names = name
                    for compartments in progress_context.elements:
                        multi_features = MapFunctionOnList(
                            PreConfiguredFeatureFct, compartments
                        )
                        for compartment, features in zip(compartments, multi_features):
                            for name, feature in zip(names, features):
                                compartment.AddFeature(name, feature)
            else:
                if isinstance(name, str):
                    for compartments, frame in progress_context.elements:
                        features = StarMapFunctionOnList(
                            PreConfiguredFeatureFct,
                            zip_longest(compartments, (frame,), fillvalue=frame),
                        )
                        for compartment, feature in zip(compartments, features):
                            compartment.AddFeature(name, feature)
                else:
                    names = name
                    for compartments, frame in progress_context.elements:
                        multi_features = StarMapFunctionOnList(
                            PreConfiguredFeatureFct,
                            zip_longest(compartments, (frame,), fillvalue=frame),
                        )
                        for compartment, features in zip(compartments, multi_features):
                            for name, feature in zip(names, features):
                                compartment.AddFeature(name, feature)

            if should_run_in_parallel:
                pool.close()
                pool.terminate()

    @property
    def cell_areas(self) -> Sequence[int]:
        """"""
        output = []

        for segmentation in self:
            labeled, n_cells = mrph.label(
                segmentation.cells_map, return_num=True, connectivity=1
            )
            areas = (
                nmpy.count_nonzero(labeled == _lbl) for _lbl in range(1, n_cells + 1)
            )
            output.extend(areas)

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

    def AsArray(
        self,
        /,
        *,
        compartment: Union[compartment_id_t, Sequence[compartment_id_t]] = None,
    ) -> array_t:
        """"""
        if compartment is None:
            if self.has_nuclei:
                compartment = (
                    compartment_id_t.CELL,
                    compartment_id_t.CYTOPLASM,
                    compartment_id_t.NUCLEUS,
                )
            else:
                compartment = compartment_id_t.CELL

        if isinstance(compartment, compartment_id_t):
            return nmpy.dstack(self.Compartments(compartment))

        compartments = tuple(self.Compartments(_cpt) for _cpt in compartment)
        frames = (nmpy.dstack(_cpt) for _cpt in zip(*compartments))

        return nmpy.stack(tuple(frames), axis=3)

    def __getattribute__(self, name) -> Any:
        """"""
        try:
            output = object.__getattribute__(self, name)
        except AttributeError:
            if self.length > 0:
                output = object.__getattribute__(self[0], name)
            else:
                raise AttributeError(
                    f"{name}: Invalid attribute or attribute access on empty segmentations"
                )

        return output


segmentations_h = Union[Sequence[array_t], Sequence[segmentation_t], segmentations_t]


# def AllSegmentations(
#     segmentations: Union[Sequence[array_t], segmentations_t], /
# ) -> tuple[all_versions_h, str]:
#     """"""
#     if isinstance(segmentations, segmentations_t):
#         compartments = segmentations[0].available_compartments
#         for compartment in compartments:
#                 output = segmentations.Compartments(
#                     compartment
#                 )
#     else:
#         output = segmentations
#
#     return output
