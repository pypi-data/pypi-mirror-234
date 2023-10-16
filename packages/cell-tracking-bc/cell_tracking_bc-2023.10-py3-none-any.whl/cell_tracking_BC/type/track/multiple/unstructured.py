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

from typing import Iterator

import networkx as grph

from cell_tracking_BC.task.tracking.constant import TRACKING_AFFINITY_LABEL
from cell_tracking_BC.type.compartment.cell import cell_t
from cell_tracking_BC.type.track.single.unstructured import (
    TIME_POINT,
    unstructured_track_t,
)


class unstructured_tracks_t(grph.DiGraph):
    def AddTrackSegment(
        self,
        src_cell: cell_t,
        tgt_cell: cell_t,
        src_time_point: int,
        tracking_affinity: float,
        /,
    ) -> None:
        """"""
        time_point = {TIME_POINT: src_time_point}
        time_point_p_1 = {TIME_POINT: src_time_point + 1}
        affinity = {TRACKING_AFFINITY_LABEL: tracking_affinity}
        self.add_node(src_cell, **time_point)
        self.add_node(tgt_cell, **time_point_p_1)
        self.add_edge(src_cell, tgt_cell, **affinity)

    @property
    def track_iterator(self) -> Iterator[unstructured_track_t]:
        """"""
        for cells in grph.weakly_connected_components(self):
            track_view = self.subgraph(cells)
            # Copy or re-instantiation is necessary since the subgraph is a view
            yield unstructured_track_t(track_view)
