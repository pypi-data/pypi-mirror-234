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
from sys import maxsize as MAX_INTEGER
from typing import Any, List, Sequence

import networkx as grph
import numpy as nmpy
from logger_36 import LOGGER

from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t as axes_t
from cell_tracking_BC.in_out.graphics.type.color import colormap_h, rgba_color_h
from cell_tracking_BC.in_out.graphics.type.context import context_t, path_collection_h
from cell_tracking_BC.in_out.graphics.type.figure import figure_t
from cell_tracking_BC.in_out.graphics.type.track import VersionOfForkingForLayout
from cell_tracking_BC.type.compartment.cell import cell_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t
from cell_tracking_BC.type.track.single.forking import forking_track_t
from cell_tracking_BC.type.track.single.structured import structured_track_t
from cell_tracking_BC.type.track.single.thread import thread_track_t

_EDGE_COLORS = {True: "gray", False: "red"}
_TICK_COLORS = {True: "black", False: "red"}


# TODO: factorization and simplification needed


@dtcl.dataclass(repr=False, eq=False)
class t_viewer_2d_t:
    figure: figure_t
    axes: axes_t
    colormap: colormap_h

    scatter: path_collection_h = dtcl.field(init=False, default=None)

    # Cell details
    labels: List[int] = dtcl.field(init=False, default_factory=list)
    time_points: List[int] = dtcl.field(init=False, default_factory=list)
    tracking_affinities: List[float] = dtcl.field(init=False, default_factory=list)
    colors: List[rgba_color_h] = dtcl.field(init=False, default_factory=list)

    dbe: context_t = None

    @classmethod
    def NewForTracks(
        cls,
        tracks: tracks_t,
        dbe: context_t,
        /,
        *,
        mode: str = "forking",
        in_axes: axes_t = None,
    ) -> t_viewer_2d_t:
        """
        mode: thread or forking
        """
        if mode not in ("thread", "forking"):
            raise ValueError(
                f'{mode}: Invalid plotting mode. Expected="thread" or "forking".'
            )

        if in_axes is None:
            figure, axes = dbe.figure_2d_t.NewFigureAndAxes()
        else:
            figure = in_axes.Figure()
            axes = in_axes
        n_leaves = sum(_tck.leaves.__len__() for _tck in tracks)
        n_leaves += sum(_tck.leaves.__len__() for _tck in tracks.fully_pruned)
        n_leaves += sum(
            _rcd[0].leaves.__len__()
            for _rcd in tracks.invalids
            if isinstance(_rcd[0], structured_track_t)
        )
        axes.SetTrackingAxesProperties(range(1, n_leaves + 1))
        colormap = axes.AddStandardColormap(
            "Tracking Affinity", "plasma", position="left"
        )

        instance = cls(
            figure=figure,
            axes=axes,
            colormap=colormap,
            dbe=dbe,
        )

        all_cell_heights = []
        all_tracks = list(tracks)
        limit_valid = all_tracks.__len__()
        all_tracks.extend(
            _rcd[0]
            for _rcd in tracks.invalids
            if isinstance(_rcd[0], structured_track_t)
        )
        limit_invalid = all_tracks.__len__()
        all_tracks.extend(tracks.fully_pruned)
        tick_details = []
        for t_idx, track in enumerate(all_tracks):
            is_valid = t_idx < limit_valid
            is_fully_pruned = t_idx >= limit_invalid
            if is_fully_pruned:
                min_label = min(track.pruned_labels)
                n_topologic_leaves = track.topologic_leaves.__len__()
                heights = tuple(range(min_label, min_label + n_topologic_leaves))
                tick_details.extend((_hgt, "fp", "magenta") for _hgt in heights)
                continue

            if isinstance(track, thread_track_t):
                PlotTrackEdges = instance._PlotThreadEdges
            elif mode == "thread":
                raise NotImplementedError
                # PlotTrackEdges = instance._PlotForkingTrackEdgesAsThread
            else:
                PlotTrackEdges = instance._PlotForkingTrackEdges
            new_labels = PlotTrackEdges(track, all_cell_heights, is_valid)
            tick_details.extend(new_labels)

        instance.scatter = axes.PlotPoints(
            instance.time_points,
            all_cell_heights,
            marker="o",
            c=instance.colors,
            zorder=2,
        )
        positions, labels, colors = zip(*tick_details)
        axes.SetAxisTicks("yaxis", positions, labels, colors=colors)

        return instance

    def _PlotThreadEdges(
        self,
        track: thread_track_t,
        all_cell_heights: List[int],
        is_valid: bool,
        /,
    ) -> Sequence[tuple[float, int, Any]]:
        """"""
        durations, time_points, where = self._ElementsForTrackPiece(
            track.unpruned_cells,
            track.root_time_point,
            track.TrackingAffinitiesBetween(track.root, track.leaves[0]),
        )
        label = track.label

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.tracking_affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        heights = (durations + 1) * (label,)
        all_cell_heights.extend(heights)

        self.axes.PlotLines(
            time_points, heights, color=_EDGE_COLORS[is_valid], zorder=1
        )

        return ((label, label, _TICK_COLORS[is_valid]),)  # Note: this is a tuple

    # def _PlotForkingTrackEdgesAsThread(
    #     self,
    #     track: forking_track_t,
    #     all_cell_heights: List[int],
    #     is_valid: bool,
    #     /,
    # ) -> Sequence[tuple[float, int, Any]]:
    #     """"""
    #     output = []
    #
    #     for thread in track.ThreadIterator():  # ThreadIterator does not exist; Just to indicate what is needed
    #         height_label = self._PlotThreadEdges(
    #             thread, all_cell_heights, is_valid
    #         )
    #         output.extend(height_label)
    #
    #     return output

    def _PlotForkingTrackEdges(
        self,
        track: forking_track_t,
        all_cell_heights: List[int],
        is_valid: bool,
        /,
    ) -> Sequence[tuple[float, int, Any]]:
        """"""
        with_int_labels, integer_to_cell = VersionOfForkingForLayout(track)
        try:
            int_layout = grph.nx_agraph.pygraphviz_layout(with_int_labels, prog="dot")
        except Exception as exc:
            LOGGER.warning(
                f"Track layout failed for track {track.labels} with error:\n{exc}"
            )
            return ()
        positions = {
            integer_to_cell[_idx]: _pst
            for _idx, _pst in int_layout.items()
            if isinstance(_idx, int)
        }

        output = []

        all_time_points, all_heights = [], []
        min_height = max_height = positions[track.root][0]
        min_label = MAX_INTEGER
        root_height = None
        where = None
        for cells, start_time_point, label, tracking_affinities in track.PiecesIterator(
            with_affinities=True
        ):
            _, time_points, new_where = self._ElementsForTrackPiece(
                cells, start_time_point, tracking_affinities
            )
            heights = nmpy.fromiter(
                (positions[_cll][0] for _cll in cells), dtype=nmpy.float64
            )
            if cells[0] is track.root:
                root_height = heights[0]
            if where is None:
                where = new_where

            all_time_points.append(time_points)
            all_heights.append(heights)
            min_height = min(min_height, min(heights))
            max_height = max(max_height, max(heights))
            if label is not None:
                if label < min_label:
                    min_label = label
                output.append((heights[-1], label, _TICK_COLORS[is_valid]))

        # max(max_height - min_height, 1): Because max_height - min_height can be zero if the track has been pruned so
        # that it now has the structure of a thread.
        height_scaling = (track.leaves.__len__() - 1) / max(max_height - min_height, 1)
        AdjustedHeight = lambda _hgt: height_scaling * (_hgt - min_height) + min_label

        output = tuple(
            (AdjustedHeight(_elm[0]), _elm[1], _TICK_COLORS[is_valid])
            for _elm in sorted(output)
        )

        output += tuple((_hgt, "p", "magenta") for _hgt in track.pruned_labels)

        for time_points, heights in zip(all_time_points, all_heights):
            heights = AdjustedHeight(heights)
            self.axes.PlotLines(
                time_points, heights, color=_EDGE_COLORS[is_valid], zorder=1
            )
            all_cell_heights.extend(heights[1:])
        root_height = AdjustedHeight(root_height)

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.tracking_affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        all_cell_heights.insert(where, root_height)

        return output

    def _ElementsForTrackPiece(
        self,
        cells: Sequence[cell_t],
        start_time_point: int,
        tracking_affinities: Sequence[float],
        /,
    ) -> tuple[int, Sequence[int], int]:
        """"""
        where = self.labels.__len__()

        duration = cells.__len__() - 1
        time_points = tuple(range(start_time_point, start_time_point + duration + 1))

        self.labels.extend(_cll.label for _cll in cells[1:])
        self.time_points.extend(time_points[1:])
        self.tracking_affinities.extend(tracking_affinities)
        self.colors.extend(self.colormap(tracking_affinities))

        return duration, time_points, where
