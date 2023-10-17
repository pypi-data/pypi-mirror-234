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
from operator import itemgetter as ItemAt
from typing import Any, Callable, Dict, Iterable, Iterator, Optional, Sequence, Union

import networkx as grph
import numpy as nmpy
from logger_36 import LOGGER

from cell_tracking_BC.standard.issue import ISSUE_SEPARATOR
from cell_tracking_BC.standard.number import INFINITY_MINUS, MAX_INT
from cell_tracking_BC.standard.uid import Identity
from cell_tracking_BC.type.compartment.cell import cell_t, state_e

feature_filtering_h = Callable[..., Optional[Sequence[Any]]]
# int: thread label
per_thread_feature_h = Dict[int, Optional[Sequence[Any]]]
cells_wo_time_points = Sequence[cell_t]
cells_w_time_points_h = Sequence[tuple[cell_t, int]]
cells_w_optional_time_points_h = Union[cells_wo_time_points, cells_w_time_points_h]
per_thread_cells_h = Dict[int, cells_w_optional_time_points_h]
per_thread_cell_h = Dict[int, Optional[Union[cell_t, tuple[cell_t, int]]]]


# TODO: check if grph.descendants and grph.ancestors could be used in place of more complex code here
# TODO: cell iteration methods should have a topologic_mode: bool = False parameter to allow cell-state-independent
#     iterations


@dtcl.dataclass(repr=False, eq=False)
class structured_track_t:
    """
    Adding Iterable to the class inheritance silences warnings at "cell in self". Unfortunately, forking multiple become
    un-instantiable for they "lack" an __iter__ method.

    root, leaves: "logical" versions, i.e. accounting for pruning. Geometric versions are topologic_root and
    topologic_leaves.
    """

    root: cell_t = None
    leaves: Sequence[cell_t] = None
    # TODO: take advantage of these new topologic attr
    topologic_root: cell_t = dtcl.field(init=False, default=None)
    topologic_leaves: tuple[cell_t] = dtcl.field(init=False, default=None)
    topologic_root_time_point: int = dtcl.field(init=False, default=None)
    topologic_labels: tuple[int, ...] = dtcl.field(init=False, default=None)
    features: Dict[str, per_thread_feature_h] = dtcl.field(
        init=False, default_factory=dict
    )
    _dividing_marked: bool = dtcl.field(init=False, default=False)
    _dead_marked: bool = dtcl.field(init=False, default=False)

    def __post_init__(self) -> None:
        """"""
        self.topologic_root = self.root
        self.topologic_leaves = tuple(self.leaves)

    @property
    def root_time_point(self) -> int:
        """"""
        return self.CellTimePoint(self.root)

    @property
    def leaves_time_points(self) -> Sequence[int]:
        """"""
        return tuple(self.CellTimePoint(_lef) for _lef in self.leaves)

    def CellTimePoint(self, cell: cell_t, /) -> int:
        """"""
        raise NotImplementedError

    @property
    def durations(self) -> Sequence[int]:
        """
        Segment-wise, not node-wise
        """
        return tuple(_ltp - self.root_time_point for _ltp in self.leaves_time_points)

    def SplittingCells(
        self, /, *, with_time_point: bool = False
    ) -> Sequence[Union[cell_t, tuple[cell_t, int]]]:
        """"""
        raise NotImplementedError

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
        raise NotImplementedError

    @property
    def n_dividing_cells(self) -> int:
        """"""
        raise NotImplementedError

    def DividingCells(
        self,
        /,
        *,
        with_time_point: bool = False,
        per_thread: bool = False,
    ) -> Union[cells_w_optional_time_points_h, per_thread_cells_h]:
        """"""
        raise NotImplementedError

    def DivisionTimePoints(self) -> Dict[int, Optional[Sequence[int]]]:
        """
        Note: There is no sense in returning not-per-thread time points
        """
        if not self._dividing_marked:
            raise RuntimeError("Dividing cells have not been marked yet")

        dividing = self.DividingCells(with_time_point=True, per_thread=True)
        if dividing.__len__() > 0:
            return {
                _key: tuple(map(ItemAt(1), _val)) for _key, _val in dividing.items()
            }

        return {}  # Used to be (-1,), then None

    def MarkDeadCells(
        self,
        death_responses: Dict[int, Optional[Sequence[float]]],
        lower_bound: float,
        after_divisions: bool,
        method: str,
        /,
        *,
        CombinedResponse: Callable[[Iterable], float] = max,
        called_from_educated_code: bool = False,
    ) -> bool:
        """
        A death is set if the highest response at a cell among the adjacent threads is above the threshold.

        Note that dead cells make part of the track, the subsequent ones having the "discarded" state. So they are also
        leaves. Therefore, there are living and dead leaves.

        called_from_educated_code: A track might be entirely pruned out here. Since it cannot remove itself from its
        referring objects, this method must be called from a piece of code that can do it if needed. This parameter is
        meant to prevent an "accidental" call from some "uneducated" piece of code.

        Returns the fully-pruned status.
        """
        if self._dead_marked:
            LOGGER.warning(f"{self}: Dead cells already marked")
            return False

        if after_divisions and not self._dividing_marked:
            raise RuntimeError(
                'Death marking cannot be done in "after divisions" mode '
                "if dividing cells have not been previously marked"
            )
        if not called_from_educated_code:
            raise ValueError(
                f"{self.MarkDeadCells.__name__}: Must be called from a piece of code handling full pruning"
            )

        self._dead_marked = True

        if (death_responses is None) or (lower_bound is None):
            return False

        if after_divisions:
            dividing_cells = self.DividingCells()
        else:
            dividing_cells = ()

        sibling_labels = self.TrackLabelsContainingCell(self.root)
        sibling_responses = {}
        for label in sibling_labels:
            if death_responses[label] is None:
                sibling_responses[label] = nmpy.array(
                    [lower_bound - 1.0], dtype=nmpy.float64
                )
            else:
                sibling_responses[label] = nmpy.array(
                    death_responses[label], dtype=nmpy.float64
                )
        # TODO: Use the above variable of "first above" also.
        # TODO: Note that global max and first max ignore the CombinedResponse option.
        if method == "global max":
            where_maxes = {}
            for label, sibling_response in sibling_responses.items():
                where_max = nmpy.nonzero(
                    sibling_response == nmpy.amax(sibling_response)
                )[0][0]
                if sibling_response[where_max] >= lower_bound:
                    where_maxes[label] = where_max
        elif method == "first max":
            where_maxes = {}
            for label, sibling_response in sibling_responses.items():
                where_above = nmpy.nonzero(sibling_response >= lower_bound)[0]
                if where_above.size == 0:
                    continue
                where_above = where_above[0]
                while (where_above + 1 < sibling_response.size) and (
                    sibling_response[where_above + 1] >= sibling_response[where_above]
                ):
                    where_above += 1
                where_maxes[label] = where_above
        else:
            where_maxes = None
        if method in ("global max", "first max"):
            dead_cells = []
            # Threads must be iterated over in topologic mode since death responses cover the whole cell range.
            for thread, label in self.LabeledThreadIterator(topologic_mode=True):
                if label in where_maxes:
                    cell = thread[where_maxes[label]]
                    if after_divisions and any(
                        self.ConfirmCellLineage(cell, _dvd) for _dvd in dividing_cells
                    ):
                        continue
                    dead_cells.append(cell)
        elif method == "first above":
            # This loop must not prune cells or modify leaves since it could change the sibling labels to labels of leaves
            # that have been pruned in a prior step (e.g. when validating divisions). For example, behind a cell are 2
            # leaves with labels 1 and 2. Suppose that the leaf with label 1 has been pruned in a prior step. So the cell
            # has 2 as its sibling labels. So has the cell before it. If the cell is marked dead, and the leaf with label 2
            # is pruned, the previous cell will now receive the label min(1,2), which is different from what it had.
            dead_cells = []
            if isinstance(self, list):
                cells = self
            else:
                cells = grph.dfs_preorder_nodes(self, source=self.topologic_root)
            for cell in cells:
                if cell.state in (state_e.dividing, state_e.discarded):
                    continue
                if after_divisions and any(
                    self.ConfirmCellLineage(cell, _dvd) for _dvd in dividing_cells
                ):
                    continue

                time_point = self.CellTimePoint(cell)
                sibling_labels = self.TrackLabelsContainingCell(cell)
                combined = CombinedResponse(
                    death_responses[_lbl][time_point]
                    if (death_responses[_lbl] is not None)
                    and (death_responses[_lbl][time_point] is not None)
                    else INFINITY_MINUS
                    for _lbl in sibling_labels
                )
                if combined >= lower_bound:
                    # Note: The cell can be a leaf (see new_leaves below)
                    dead_cells.append(cell)
        else:
            raise ValueError(f"{method}: Invalid method for marking dead cells.")

        # Do not log inside the loop on dead_cells since it does not update leaves (update is done after the loop),
        # leaving the track in a transient state not suitable for TrackLabelsContainingCell.
        summary = {}
        max_duration = max(self.durations)
        for cell in dead_cells:
            labels = self.TrackLabelsContainingCell(cell)
            if labels.__len__() == 1:
                labels = labels[0]
            time_point = self.CellTimePoint(cell)
            summary[labels] = min(summary.get(labels, max_duration), time_point)
        for labels, time_point in summary.items():
            LOGGER.info(
                f"Partial or full pruning of track {labels} after dead cell at time point {time_point}"
            )

        invalid_leaves = []
        for cell in dead_cells:
            if cell.state is state_e.discarded:
                # It has been pruned below as a descendant
                continue

            cell.state = state_e.dead

            for descendant in self.CellDescendants(cell, including_self=False):
                descendant.state = state_e.discarded
                if descendant in self.leaves:
                    invalid_leaves.append(descendant)

        # 1. Do not use dead_cells here since it may contain dead cells after other dead cells
        # 2. Cells marked dead can already be leaves; They must not be included in new_leaves then (see documentation
        #    about dead cells and leaves).
        new_leaves = tuple(
            _cll
            for _cll in self
            if (_cll.state is state_e.dead) and (_cll not in self.leaves)
        )
        self.leaves = tuple(set(self.leaves).difference(invalid_leaves)) + new_leaves

        output = self.root.state in (state_e.dead, state_e.discarded)
        if output:
            LOGGER.info(f"{self.topologic_labels}: Fully pruned track (all threads)")

        return output

    def DeadCells(
        self,
        sequence_length: int,
        /,
        *,
        with_time_point: bool = False,
        with_living_leaves: bool = False,
        per_thread: bool = False,
    ) -> Union[cells_w_optional_time_points_h, per_thread_cell_h]:
        """"""
        if not self._dead_marked:
            raise RuntimeError("Dead cells have not been marked yet")

        output = []

        for leaf in self.leaves:
            time_point = self.CellTimePoint(leaf)
            if (is_dead := leaf.state is state_e.dead) or (
                with_living_leaves and (time_point < sequence_length - 1)
            ):
                if with_time_point:
                    if is_dead:
                        output.append((leaf, time_point))
                    else:
                        output.append((leaf, -time_point))
                else:
                    output.append(leaf)

        if per_thread:
            return PerThreadCells(
                output, with_time_point, self, expect_unique_cell=True
            )

        return output

    def DeathTimePoints(
        self,
        sequence_length: int,
        /,
        *,
        with_living_leaves: bool = False,
    ) -> Optional[Dict[int, Optional[int]]]:
        """
        Note: There is no sense in returning not-per-thread time points
        """
        if not self._dead_marked:
            raise RuntimeError("Dead cells have not been marked yet")

        dead = self.DeadCells(
            sequence_length,
            with_time_point=True,
            with_living_leaves=with_living_leaves,
            per_thread=True,
        )

        if dead.__len__() > 0:
            output = {
                _key: None if _val is None else _val[1] for _key, _val in dead.items()
            }

            return output

        return {}  # Used to be (-1,), then None

    @property
    def labels(self) -> Sequence[int]:
        """
        Thread labels
        """
        raise NotImplementedError

    @property
    def pruned_labels(self) -> Sequence[int]:
        """"""
        raise NotImplementedError

    def TrackLabelsContainingCell(self, cell: cell_t, /) -> Sequence[int]:
        """
        Returns empty tuple if cell has been pruned
        """
        raise NotImplementedError

    def TrackLabelWithLeaf(self, leaf: cell_t, /) -> int:
        """"""
        raise NotImplementedError

    def CellSuccessors(self, cell: cell_t, /) -> Sequence[cell_t]:
        """
        Accounts for pruning
        """
        raise NotImplementedError

    def CellDescendants(
        self,
        cell: cell_t,
        /,
        *,
        including_self: bool = True,
        topologic_mode: bool = False,
    ) -> Sequence[cell_t]:
        """"""
        raise NotImplementedError

    def ConfirmCellLineage(self, youngest: cell_t, oldest: cell_t, /) -> bool:
        """
        Including youngest is oldest
        """
        raise NotImplementedError

    def PathFromTo(self, first: cell_t, last: cell_t, /) -> Sequence[cell_t]:
        """"""
        raise NotImplementedError

    @property
    def segments_iterator(self) -> Iterator[tuple[int, cell_t, cell_t, bool]]:
        """"""
        raise NotImplementedError

    def PiecesIterator(
        self, /, *, with_affinities: bool = False, topologic_mode: bool = False
    ) -> Iterator[
        Union[
            tuple[Sequence[cell_t], int, Optional[int]],
            tuple[Sequence[cell_t], int, Optional[int], Sequence[float]],
        ]
    ]:
        """"""
        raise NotImplementedError

    def LabeledThreadIterator(
        self,
        /,
        *,
        topologic_mode: bool = False,
    ) -> Iterator[tuple[Sequence[cell_t], int]]:
        """"""
        raise NotImplementedError

    def AddFeature(
        self,
        name: str,
        cell_feature_names: Sequence[str],
        FeatureComputation: feature_filtering_h,
        /,
        *args,
        **kwargs,
    ) -> None:
        """
        Topologic mode is enforced. Otherwise, there is no way to extend the feature list to the corresponding
        topologic leaf since there can be several.
        """
        if name in self.features:
            raise ValueError(f"{name}: Already existing feature for track {self}.")

        self.features[name] = {}

        per_thread = self.features[name]
        for path, label in self.LabeledThreadIterator(topologic_mode=True):
            all_series = [
                tuple(_cll.features[_ftr] for _cll in path)
                for _ftr in cell_feature_names
            ]
            feature = FeatureComputation(
                *all_series, *args, track_label=label, **kwargs
            )
            per_thread[label] = feature

    def __hash__(self) -> int:
        """
        Note that (from Python documentation:
            if it defines __eq__() but not __hash__(), its instances will not be usable as items in hashable collections
        """
        return hash((self.root, *self.leaves))

    __repr__ = Identity

    def __str__(self) -> str:
        """"""
        if hasattr(self, "nodes"):
            cells = self.nodes
        else:
            cells = self
        cell_labels = tuple(_cll.label for _cll in cells)

        return (
            f"{repr(self)}\n"
            f"    Labels: {self.labels}\n"
            f"    Root time point: {self.root_time_point}\n"
            f"    Leaves time points: {self.leaves_time_points}\n"
            f"    Duration: {self.durations}\n"
            f"    Cell labels: {cell_labels}\n"
        )


def PerThreadCells(
    linear: cells_w_optional_time_points_h,
    has_time_point: bool,
    track: structured_track_t,
    /,
    *,
    expect_unique_cell: bool = False,
) -> Union[per_thread_cell_h, per_thread_cells_h]:
    """"""
    output = {}

    for path, label in track.LabeledThreadIterator():
        if has_time_point:
            per_thread = filter(lambda _rcd: _rcd[0] in path, linear)
            per_thread = sorted(per_thread, key=ItemAt(1))
        else:
            per_thread = tuple(filter(lambda _cll: _cll in path, linear))

        if (n_cells := per_thread.__len__()) > 0:
            if expect_unique_cell:
                if n_cells > 1:
                    raise RuntimeError(
                        f"{n_cells}/{per_thread}: Invalid number of cells in unique-cell mode "
                        f"for thread (sub)track {label}"
                    )

                output[label] = per_thread[0]
            else:
                output[label] = per_thread
        elif expect_unique_cell:
            output[label] = None
        else:
            output[label] = ()

    return output


def BasicTrackIssues(
    track: structured_track_t,  # Actually, either a single or forking track (which are iterable)
    /,
    *,
    root_time_point_interval: Optional[Sequence[Optional[int]]] = None,
    leaves_time_point_interval: Optional[Sequence[Optional[int]]] = None,
    min_duration: int = 0,
    max_n_children: int = 2,
    can_touch_border: bool = False,
) -> Optional[Sequence[str]]:
    """
    All parameters: any limit can be ignored by setting it to None
    All intervals are inclusive.
    leaf_time_point_intervals and min_lengths: first element is for the shortest branch, the second is for the longest.
        For threads, both are the same.
    min_duration: min edge-wise length, inclusive, of shortest thread
    max_n_children: inclusive
    """
    output = []

    if track.root.state is state_e.dead:
        output.append('Root cell has a "dead" state')

    mini, maxi = _IntervalWithDefaults(root_time_point_interval, 0, MAX_INT)
    if not (mini <= track.root_time_point <= maxi):
        output.append(
            f"{track.root_time_point}{ISSUE_SEPARATOR}Invalid root time point. Expected={mini}..{maxi}."
        )

    min_ltp = min(track.leaves_time_points)
    max_ltp = max(track.leaves_time_points)
    mini, maxi = _IntervalWithDefaults(leaves_time_point_interval, 0, MAX_INT)
    for time_point, which in zip((min_ltp, max_ltp), ("shortest", "longest")):
        if not (mini <= time_point <= maxi):
            output.append(
                f"{time_point}{ISSUE_SEPARATOR}Invalid leaf time point of {which} branch. Expected={mini}..{maxi}."
            )

    if min(track.durations) < min_duration:
        output.append(
            f"{min(track.durations)}{ISSUE_SEPARATOR}Invalid duration (edge-wise length) of shortest branch. Expected>={min_duration}."
        )

    for cell in track:  # See comment on track type
        if (n_children := track.CellSuccessors(cell).__len__()) > max_n_children:
            output.append(
                f"C{cell.label}T{track.CellTimePoint(cell)}{ISSUE_SEPARATOR}"
                f"{n_children} successors. Expected=0..{max_n_children}."
            )

    if not can_touch_border:
        for cell in track:  # See comment on track type
            if cell.touches_border:
                output.append(
                    f"C{cell.label}T{track.CellTimePoint(cell)}{ISSUE_SEPARATOR}Touches frame border"
                )

    if output.__len__() == 0:
        output = None

    return output


def _IntervalWithDefaults(
    interval: Optional[Sequence[Optional[int]]], default_min: int, default_max: int, /
) -> Sequence[int]:
    """"""
    if interval is None:
        return default_min, default_max

    tvl_min, tvl_max = interval
    if tvl_min is None:
        tvl_min = default_min
    if tvl_max is None:
        tvl_max = default_max

    return tvl_min, tvl_max
