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
    Callable,
    ClassVar,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Union,
)

import networkx as grph
from logger_36 import LOGGER

from cell_tracking_BC.standard.number import INFINITY_MINUS
from cell_tracking_BC.task.tracking.constant import TRACKING_AFFINITY_LABEL
from cell_tracking_BC.type.compartment.cell import cell_t, state_e
from cell_tracking_BC.type.track.single.structured import (
    PerThreadCells,
    cells_w_optional_time_points_h,
    per_thread_cells_h,
    structured_track_t,
)
from cell_tracking_BC.type.track.single.thread import thread_track_t
from cell_tracking_BC.type.track.single.unstructured import (
    TIME_POINT,
    unstructured_track_t,
)

# TODO: check if grph.descendants and grph.ancestors could be used in place of more complex code here
# TODO: cell iteration methods should have a topologic_mode: bool = False parameter to allow cell-state-independent
#     iterations


# Cannot be a dataclass due to in/out_degree declarations (which are only here to silence unfound attribute warnings)
class forking_track_t(structured_track_t, grph.DiGraph):
    """
    Affinities are stored as edge attributes
    """

    THREAD_LABEL: ClassVar[str] = "thread_label"

    # Mutable tuple[List[cell_t], List[cell_t]] for without and with time points lists
    _splitting_cells_cache: List[
        Optional[List[Union[cell_t, tuple[cell_t, int]]]]
    ] = None

    in_degree: Callable[[cell_t], int]
    out_degree: Callable[[cell_t], int]

    def __init__(
        self,
        track: Union[grph.DiGraph, unstructured_track_t],
        next_thread_label: int,
        **kwargs,
    ) -> None:
        """"""
        grph.DiGraph.__init__(self, incoming_graph_data=track, **kwargs)

        if isinstance(track, unstructured_track_t):
            # /!\ Otherwise, root and leaves (and the remaining attributes of structured_track_t) must be assigned later on.
            # Use case: __NewFromJsonDescription__
            root, root_time_point = track.RootCellWithTimePoint()
            leaves, _ = track.LeafCellsWithTimePoints()
            labels = {
                _lef: _lbl for _lbl, _lef in enumerate(leaves, start=next_thread_label)
            }

            grph.set_node_attributes(self, labels, name=forking_track_t.THREAD_LABEL)

            structured_track_t.__init__(self, root=root, leaves=leaves)
            self.topologic_root_time_point = root_time_point
            # Avoid worrying about dict.values() order in future Python versions by using code below
            self.topologic_labels = tuple(labels[_lef] for _lef in leaves)

    @classmethod
    def NewFromUnstructuredTrack(
        cls, track: unstructured_track_t, next_thread_label: int, /
    ) -> tuple[forking_track_t, int]:
        """"""
        instance = cls(track, next_thread_label)

        return instance, next_thread_label + instance.leaves.__len__()

    def CellTimePoint(self, cell: cell_t) -> int:
        """"""
        return self.nodes[cell][TIME_POINT]

    def SplittingCells(
        self, /, *, with_time_point: bool = False
    ) -> Sequence[Union[cell_t, tuple[cell_t, int]]]:
        """"""
        if with_time_point:
            which = 1
        else:
            which = 0
        if (self._splitting_cells_cache is None) or (
            self._splitting_cells_cache[which] is None
        ):
            if with_time_point:
                output = (
                    _rcd
                    for _rcd in self.nodes.data(TIME_POINT)
                    if self.out_degree(_rcd[0]) > 1
                )
            else:
                output = (_cll for _cll in self.nodes if self.out_degree(_cll) > 1)
            output = tuple(output)

            if self._splitting_cells_cache is None:
                self._splitting_cells_cache = [None, None]
            self._splitting_cells_cache[which] = output
        else:
            output = self._splitting_cells_cache[which]

        return output

    def MarkDividingCells(
        self,
        before_deaths: bool,
        /,
        *,
        division_responses: Dict[int, Optional[Sequence[float]]] = None,
        lower_bound: float = None,
        CombinedResponse: Callable[[Iterable], float] = max,
    ) -> None:
        """
        A division is set if the highest response at a splitting cell among the adjacent threads is above the
        threshold.

        Returns the sequence of fully-pruned threads.
        """
        if self._dividing_marked:
            LOGGER.warning(f"{self}: Dividing cells already marked")
            return

        # TODO: check the interest of the before_deaths parameter, here and where the method is called
        if before_deaths and not self._dead_marked:
            raise RuntimeError(
                'Division marking cannot be done in "before deaths" mode '
                "if dead cells have not been previously marked"
            )

        self._dividing_marked = True

        if (division_responses is None) or (lower_bound is None):
            for cell in self.SplittingCells():
                cell.state = state_e.dividing
            return

        for cell, time_point in self.SplittingCells(with_time_point=True):
            if cell.state in (state_e.dead, state_e.discarded):
                continue

            sibling_labels = self.TrackLabelsContainingCell(cell)
            combined = CombinedResponse(
                division_responses[_lbl][time_point]
                if (division_responses[_lbl] is not None)
                and (division_responses[_lbl][time_point] is not None)
                else INFINITY_MINUS
                for _lbl in sibling_labels
            )
            if combined >= lower_bound:
                cell.state = state_e.dividing
            else:
                successors = self.CellSuccessors(cell)
                areas = tuple(_cll.area for _cll in successors)
                smallest = successors[areas.index(min(areas))]
                main_track = self.TrackLabelsContainingCell(cell)
                subtracks = self.TrackLabelsContainingCell(smallest)
                if subtracks.__len__() == 1:
                    subtracks = subtracks[0]
                LOGGER.info(
                    f"Full pruning of (thread sub-)track(s) {subtracks} "
                    f"(from time point {time_point + 1}) "
                    f"after splitting invalidation of track {sorted(main_track)} "
                    f"at time point {time_point}"
                )
                invalid_leaves = []
                for descendant in self.CellDescendants(smallest):
                    descendant.state = state_e.discarded
                    if descendant in self.leaves:
                        invalid_leaves.append(descendant)
                self.leaves = tuple(set(self.leaves).difference(invalid_leaves))

    @property
    def n_dividing_cells(self) -> int:
        """"""
        if not self._dividing_marked:
            raise RuntimeError("Dividing cells have not been marked yet")

        return sum(1 for _cll in self if _cll.state is state_e.dividing)

    def DividingCells(
        self,
        /,
        *,
        with_time_point: bool = False,
        per_thread: bool = False,
    ) -> Union[cells_w_optional_time_points_h, per_thread_cells_h]:
        """"""
        if not self._dividing_marked:
            raise RuntimeError("Dividing cells have not been marked yet")

        if with_time_point:
            output = (
                _rcd
                for _rcd in self.nodes.data(TIME_POINT)
                if _rcd[0].state is state_e.dividing
            )
        else:
            output = (_cll for _cll in self if _cll.state is state_e.dividing)
        # Note: PerThreadCells does not accept an iterator
        output = tuple(output)

        if per_thread:
            return PerThreadCells(output, with_time_point, self)

        return output

    @property
    def label(self) -> int:
        """"""
        raise RuntimeError("A Forking track has no unique thread label")

    @property
    def labels(self) -> Sequence[int]:
        """"""
        return tuple(self.TrackLabelWithLeaf(_lef) for _lef in self.leaves)

    @property
    def pruned_labels(self) -> Sequence[int]:
        """"""
        return tuple(set(self.topologic_labels).difference(self.labels))

    def TrackLabelsContainingCell(self, cell: cell_t, /) -> Sequence[int]:
        """"""
        if cell.state is state_e.discarded:
            return ()

        descendants = self.CellDescendants(cell)
        leaves = set(self.leaves).intersection(descendants)
        output = tuple(self.TrackLabelWithLeaf(_lef) for _lef in leaves)

        assert output.__len__() > 0

        return output

    def TrackLabelWithLeaf(self, leaf: cell_t, /) -> int:
        """
        TrackLabelWithLeaf: Implicitly, it is ThreadLabelWithLeaf
        Returns label even if cell is not a leaf
        """
        label = self.nodes[leaf].get(forking_track_t.THREAD_LABEL)
        if label is None:
            # The track has been pruned from after this "logical" leaf. All the labels of the descendant, topologic
            # leaves are therefore unused. Their minimum will be picked as the label.
            descendants = grph.descendants(self, leaf)
            topologic_leaves = set(self.topologic_leaves).intersection(descendants)
            label = min(
                self.nodes[_lef][forking_track_t.THREAD_LABEL]
                for _lef in topologic_leaves
            )

        return label

    @property
    def tracking_affinities(self) -> tuple[float, ...]:
        """"""
        return tuple(grph.get_edge_attributes(self, TRACKING_AFFINITY_LABEL).values())

    def CellSuccessors(self, cell: cell_t, /) -> Sequence[cell_t]:
        """"""
        return tuple(
            _ngh for _ngh in self.neighbors(cell) if _ngh.state is not state_e.discarded
        )

    def CellDescendants(
        self,
        cell: cell_t,
        /,
        *,
        including_self: bool = True,
        topologic_mode: bool = False,
    ) -> Optional[Sequence[cell_t]]:
        """"""
        output = grph.descendants(self, cell)

        if topologic_mode:
            output = tuple(output)
        else:
            output = tuple(
                _cll for _cll in output if _cll.state is not state_e.discarded
            )

        if including_self:
            output = (cell,) + output

        return output

    def ConfirmCellLineage(self, youngest: cell_t, oldest: cell_t, /) -> bool:
        """
        Returns True if youngest is oldest even if youngest is not in self
        """
        if youngest is oldest:
            return True

        return oldest in grph.descendants(self, youngest)

    def PathFromTo(self, first: cell_t, last: cell_t, /) -> Sequence[cell_t]:
        """"""
        return grph.shortest_path(self, source=first, target=last)

    @property
    def segments_iterator(self) -> Iterator[tuple[int, cell_t, cell_t, bool]]:
        """"""
        time_points = grph.get_node_attributes(self, TIME_POINT)

        for edge in self.edges:
            if all(_cll.state is not state_e.discarded for _cll in edge):
                time_point = time_points[edge[0]]
                is_last = edge[1] in self.leaves
                yield time_point, *edge, is_last

    def PiecesIterator(
        self, /, *, with_affinities: bool = False, topologic_mode: bool = False
    ) -> Iterator[
        Union[
            tuple[Sequence[cell_t], int, Optional[int]],
            tuple[Sequence[cell_t], int, Optional[int], Sequence[float]],
        ]
    ]:
        """"""
        already = []
        for path, label in self.LabeledThreadIterator(topologic_mode=topologic_mode):
            root, leaf = path[0], path[-1]
            # The root can have an out-degree > 1, or not, and it must be included in milestones. A solution is to
            # exclude it below and add it unconditionally afterwards.
            if topologic_mode:
                forks = [
                    (_idx, _cll)
                    for _idx, _cll in enumerate(path[1:-1], start=1)
                    if self.out_degree(_cll) > 1
                ]
            else:
                forks = [
                    (_idx, _cll)
                    for _idx, _cll in enumerate(path[1:-1], start=1)
                    if self.CellSuccessors(_cll).__len__() > 1
                ]
            milestones = [(0, root), *forks, (path.__len__() - 1, leaf)]

            for m_idx in range(milestones.__len__() - 1):
                (f_idx, first), (s_idx, second) = (
                    milestones[m_idx],
                    milestones[m_idx + 1],
                )
                if (edge := (first, second)) in already:
                    continue

                piece = path[f_idx : (s_idx + 1)]
                time_point = self.CellTimePoint(first)
                if second is leaf:
                    piece_label = label
                else:
                    piece_label = None
                if with_affinities:
                    affinities = tuple(
                        self.edges[_fst, _scd][TRACKING_AFFINITY_LABEL]
                        for _fst, _scd in zip(piece[:-1], piece[1:])
                    )
                    yield piece, time_point, piece_label, affinities
                else:
                    yield piece, time_point, piece_label
                already.append(edge)

    def LabeledThreadIterator(
        self,
        /,
        *,
        topologic_mode: bool = False,
    ) -> Iterator[tuple[Sequence[cell_t], int]]:
        """"""
        if topologic_mode:
            root = self.topologic_root
            leaves = self.topologic_leaves
        else:
            root = self.root
            leaves = self.leaves
        for leaf in leaves:
            yield self.PathFromTo(root, leaf), self.TrackLabelWithLeaf(leaf)

    def AsThreadTrack(self) -> thread_track_t:
        """"""
        output = [self.root]

        tracking_affinities = []
        while True:
            last_cell = output[-1]

            if last_cell in self.leaves:
                neighbors = None
                n_neighbors = 0
            else:
                neighbors = self.CellSuccessors(last_cell)
                n_neighbors = neighbors.__len__()

            if n_neighbors == 0:
                label = self.TrackLabelWithLeaf(last_cell)
                break
            elif n_neighbors == 1:
                next_cell = neighbors[0]
                output.append(next_cell)
                tracking_affinity = self[last_cell][next_cell][TRACKING_AFFINITY_LABEL]
                tracking_affinities.append(tracking_affinity)
            else:
                raise ValueError(
                    f"Attempt to convert the forking track with root {self.root} and "
                    f"{self.leaves.__len__()} leaves into a thread track"
                )

        output = thread_track_t.NewFromOrderedCells(
            output, tracking_affinities, self.root_time_point, label
        )

        return output
