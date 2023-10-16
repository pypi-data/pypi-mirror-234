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

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Union,
)

from logger_36 import LOGGER

from cell_tracking_BC.type.compartment.cell import cell_t, state_e
from cell_tracking_BC.type.track.single.structured import (
    cells_w_optional_time_points_h,
    per_thread_cells_h,
    structured_track_t,
)

# TODO: check if grph.descendants and grph.ancestors could be used in place of more complex code here
# TODO: cell iteration methods should have a topologic_mode: bool = False parameter to allow cell-state-independent
#     iterations


class thread_track_t(structured_track_t, List[cell_t]):
    label: int = None
    tracking_affinities: tuple[float, ...] = None

    def __init__(
        self,
        cells: Sequence[cell_t],
        tracking_affinities: Sequence[float],
        root_time_point: int,
        label: Optional[int],
        /,
    ) -> None:
        """"""
        list.__init__(self, cells)

        # Place after list init to get access to self[...]
        structured_track_t.__init__(
            self,
            root=self[0],
            leaves=(self[-1],),
        )
        self.topologic_root_time_point = root_time_point
        self.topologic_labels = (label,)
        self._dividing_marked = True

        self.label = label
        self.tracking_affinities = tuple(tracking_affinities)

    @classmethod
    def NewFromOrderedCells(
        cls,
        cells: Sequence[cell_t],
        tracking_affinities: Sequence[float],
        root_time_point: int,
        label: Optional[int],
        /,
    ) -> thread_track_t:
        """
        This must be the only place where direct instantiation is allowed. Anywhere else, instantiation must be
        performed with this class method.

        label: Can be None only to accommodate the creation of branches as threads
        """
        n_cells = cells.__len__()
        if (n_affinities := tracking_affinities.__len__()) != (
            n_expected := n_cells - 1
        ):
            raise ValueError(
                f"{n_affinities}: Invalid number of tracking_affinities. Expected={n_expected}"
            )

        return cls(cells, tracking_affinities, root_time_point, label)

    @property
    def unpruned_cells(self) -> Sequence[cell_t]:
        """"""
        return self[self.index(self.root) : (self.index(self.leaves[0]) + 1)]

    def CellTimePoint(self, cell: cell_t, /) -> int:
        """"""
        return self.topologic_root_time_point + self.index(cell)

    def SplittingCells(
        self, /, *, with_time_point: bool = False
    ) -> Sequence[Union[cell_t, tuple[cell_t, int]]]:
        """"""
        return ()

    def MarkDividingCells(
        self,
        before_deaths: bool,
        /,
        *,
        division_responses: Dict[int, Optional[Sequence[float]]] = None,
        lower_bound: float = None,
        CombinedResponse: Callable[[Iterable], float] = max,
    ) -> None:
        """"""
        LOGGER.warning(f"{self}: Dividing cells already marked")

    @property
    def n_dividing_cells(self) -> int:
        """"""
        return 0

    def DividingCells(
        self,
        /,
        *,
        with_time_point: bool = False,
        per_thread: bool = False,
    ) -> Union[cells_w_optional_time_points_h, per_thread_cells_h]:
        """"""
        if per_thread:
            return {}
        return ()

    @property
    def labels(self) -> Sequence[int]:
        """
        This method is supposed to be called from not fully-pruned multiple.
        """
        return (self.label,)  # Note: this is a tuple

    @property
    def pruned_labels(self) -> Sequence[int]:
        """
        This method is supposed to be called from not fully-pruned multiple.
        """
        return ()

    def TrackLabelsContainingCell(self, cell: cell_t, /) -> Sequence[int]:
        """
        Returns valid sequence even if cell is not in self
        """
        if cell.state is state_e.discarded:
            return ()

        return self.labels

    def TrackLabelWithLeaf(self, _: cell_t, /) -> int:
        """
        Returns label even if cell is not in self or is not a leaf
        """
        return self.label

    def TrackingAffinitiesBetween(
        self, first: cell_t, second: cell_t, /
    ) -> Sequence[float]:
        """"""
        return self.tracking_affinities[self.index(first) : self.index(second)]

    def CellSuccessors(self, cell: cell_t, /) -> Sequence[cell_t]:
        """"""
        where = self.index(cell)
        if where < self.__len__() - 1:
            successor = self[where + 1]
            if successor.state is state_e.discarded:
                output = ()
            else:
                output = (successor,)
        else:
            output = ()

        return output

    def CellDescendants(
        self,
        cell: cell_t,
        /,
        *,
        including_self: bool = True,
        topologic_mode: bool = False,
    ) -> Sequence[cell_t]:
        """"""
        where = self.index(cell)
        if not including_self:
            where += 1

        if where > self.__len__() - 1:
            output = ()
        else:
            output = tuple(self[where:])
            if not topologic_mode:
                pruned = tuple(_cll.state is state_e.discarded for _cll in output)
                if any(pruned):
                    first_pruned = pruned.index(True)
                    output = output[:first_pruned]

        return output

    def ConfirmCellLineage(self, youngest: cell_t, oldest: cell_t, /) -> bool:
        """"""
        return self.index(youngest) <= self.index(oldest)

    def PathFromTo(self, first: cell_t, last: cell_t, /) -> Sequence[cell_t]:
        """"""
        return self[self.index(first) : (self.index(last) + 1)]

    @property
    def segments_iterator(self) -> Iterator[tuple[int, cell_t, cell_t, bool]]:
        """"""
        root_idx = self.index(self.root)
        leaf_idx = self.index(self.leaves[0])
        for c_idx in range(root_idx, leaf_idx):
            time_point = self.topologic_root_time_point + c_idx
            is_last = c_idx == leaf_idx - 1
            yield time_point, *self[c_idx : (c_idx + 2)], is_last

    def PiecesIterator(
        self, /, *, with_affinities: bool = False, topologic_mode: bool = False
    ) -> Iterator[
        Union[
            tuple[Sequence[cell_t], int, Optional[int]],
            tuple[Sequence[cell_t], int, Optional[int], Sequence[float]],
        ]
    ]:
        """
        int: time point of first cell
        Optional[int]: thread label if last cell is (topologic) leaf
        """
        if topologic_mode:
            if with_affinities:
                return iter(
                    (
                        (
                            self,
                            self.topologic_root_time_point,
                            self.label,
                            self.tracking_affinities,
                        ),
                    )
                )
            else:
                return iter(((self, self.topologic_root_time_point, self.label),))
        else:
            if with_affinities:
                return iter(
                    (
                        (
                            self.PathFromTo(self.root, self.leaves[0]),
                            self.root_time_point,
                            self.label,
                            self.TrackingAffinitiesBetween(self.root, self.leaves[0]),
                        ),
                    )
                )
            else:
                return iter(
                    (
                        (
                            self.PathFromTo(self.root, self.leaves[0]),
                            self.root_time_point,
                            self.label,
                        ),
                    )
                )

    def LabeledThreadIterator(
        self,
        /,
        *,
        topologic_mode: bool = False,
    ) -> Iterator[tuple[Sequence[cell_t], int]]:
        """"""
        if topologic_mode:
            output = (self, self.label)
        else:
            output = (self.unpruned_cells, self.label)

        return iter((output,))

    def CellFeature(
        self, feature: str, /, *, topologic_mode: bool = False
    ) -> Sequence[Any]:
        """
        Contrary to structured_track_t.features which are rooted at time point zero using Nones if needed, here the
        feature is returned for the unpruned part only.
        """
        if topologic_mode:
            return tuple(_cll.features[feature] for _cll in self)

        return tuple(_cll.features[feature] for _cll in self.unpruned_cells)
