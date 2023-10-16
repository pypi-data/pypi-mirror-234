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
from enum import Enum as enum_t
from typing import ClassVar, Dict, Sequence, Union

import numpy as nmpy
import skimage.morphology as mrph

from cell_tracking_BC.type.compartment.base import compartment_id_t, compartment_t
from cell_tracking_BC.type.compartment.cytoplasm import cytoplasm_t
from cell_tracking_BC.type.compartment.nucleus import nucleus_t

array_t = nmpy.ndarray


class state_e(enum_t):
    unknown = None
    discarded = -1
    living = 1
    dividing = 2
    dead = 0

    def IsActive(self, /, *, strict_mode: bool = False) -> bool:
        """"""
        if strict_mode:
            return self not in (state_e.dead, state_e.discarded, state_e.unknown)

        return self not in (state_e.dead, state_e.discarded)

    def IsAlive(self, /, *, strict_mode: bool = False) -> bool:
        """"""
        if strict_mode:
            return self in (state_e.living, state_e.dividing)

        return self in (state_e.living, state_e.dividing, state_e.unknown)


@dtcl.dataclass(repr=False, eq=False)
class cell_t(compartment_t):
    NEXT_AVAILABLE_LABEL: ClassVar[int] = 1

    label: int = None
    state: state_e = state_e.unknown
    cytoplasm: cytoplasm_t = None
    nuclei: tuple[nucleus_t, ...] = None
    # And inherited from compartment_t (among others): features

    def __post_init__(self) -> None:
        """"""
        self.__class__.NEXT_AVAILABLE_LABEL += 1

    @classmethod
    def NewFromMap(cls, _: array_t, /, *, is_plain: bool = True) -> compartment_t:
        """"""
        raise RuntimeError(
            f"{cell_t.NewFromMap.__name__}: Not meant to be called from class {cell_t.__name__}; "
            f"Use {cell_t.NewFromMaps.__name__} instead"
        )

    @classmethod
    def NewFromMaps(
        cls,
        /,
        *,
        cell_map: array_t = None,
        nucleus_map: array_t = None,
    ) -> cell_t:
        """
        cell_map: Defined optional for convenience (calling with kwargs), but never None in fact
        Valid options: see CellAndCytoplasmMapsFromCombinations
        """
        cell = compartment_t.NewFromMap(cell_map)
        if nucleus_map is None:
            cytoplasm = None
            nuclei = None
        else:
            cytoplasm = cytoplasm_t.NewFromMap(
                nmpy.logical_xor(cell_map, nucleus_map), is_plain=False
            )
            labeled_nuclei, n_nuclei = mrph.label(
                nucleus_map, return_num=True, connectivity=1
            )
            nuclei = tuple(
                nucleus_t.NewFromMap(labeled_nuclei == _lbl)
                for _lbl in range(1, n_nuclei + 1)
            )

        instance = cls(
            label=cls.NEXT_AVAILABLE_LABEL,
            cytoplasm=cytoplasm,
            nuclei=nuclei,
            centroid=cell.centroid,
            bb_slices=cell.bb_slices,
            touches_border=cell.touches_border,
            map_stream=cell.map_stream,
            area=cell.area,
        )

        return instance

    @property
    def compartments(
        self,
    ) -> Dict[
        Union[compartment_id_t, str], Union[compartment_t, Sequence[compartment_t]]
    ]:
        """"""
        if self.cytoplasm is None:
            return {compartment_id_t.CELL: self}

        return {
            compartment_id_t.CELL: self,
            compartment_id_t.CYTOPLASM: self.cytoplasm,
            compartment_id_t.NUCLEUS: self.nuclei,
        }

    def Map(
        self,
        shape: Sequence[int],
        /,
        *,
        as_boolean: bool = False,
        with_labels: bool = False,
        margin: float = None,
    ) -> array_t:
        """
        with_labels: cytoplasm will be marked with label 1, nuclei with subsequent labels
        /!\ If with_labels, no margin should be requested. Indeed, what should be done with the nucleus map then?
        Apply the same margin or not? Or the method should take an additional margin parameter for the nucleus.
        """
        output = super().Map(shape, as_boolean=as_boolean, margin=margin)

        if with_labels:
            if as_boolean:
                raise ValueError('"with_labels" and "as_boolean" cannot be both True')

            if self.nuclei is not None:
                for n_idx, nucleus in enumerate(self.nuclei, start=2):
                    map_ = nucleus.Map(shape, as_boolean=True)
                    output[map_] = n_idx

        return output

    def NucleiMap(
        self,
        shape: Sequence[int],
        /,
        *,
        as_boolean: bool = False,
        margin: float = None,
    ) -> array_t:
        """"""
        output, one = compartment_t.EmptyMap(shape, as_boolean=as_boolean)

        for nucleus in self.nuclei:
            output[nucleus.Map(shape, as_boolean=True, margin=margin)] = one

        return output

    def __hash__(self) -> int:
        """
        Note that (from Python documentation:
            if it defines __eq__() but not __hash__(), its instances will not be usable as items in hashable collections
        """
        return hash((self.label, tuple(self.centroid), self.map_stream))

    def __str__(self) -> str:
        """"""
        if self.nuclei is None:
            n_nuclei = 0
        else:
            n_nuclei = self.nuclei.__len__()

        return super().__str__() + f"    Label: {self.label}\n    Nuclei: {n_nuclei}\n"
