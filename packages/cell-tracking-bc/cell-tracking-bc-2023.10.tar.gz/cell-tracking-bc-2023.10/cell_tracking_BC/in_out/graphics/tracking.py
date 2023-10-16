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

from typing import Optional, Sequence, Union

import numpy as nmpy

import cell_tracking_BC.in_out.graphics.generic.d_3 as thrd
from cell_tracking_BC.in_out.graphics.dbe.matplotlib.context import DRAWING_CONTEXT
from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t, axes_3d_t
from cell_tracking_BC.in_out.graphics.type.context import context_t
from cell_tracking_BC.in_out.graphics.type.figure import figure_t
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.cell import cell_t
from cell_tracking_BC.type.track.single.unstructured import unstructured_track_t

_LOW_AFFINITY = 0.75
_MATPLOTLIB_COLORS = ("b", "g", "r", "c", "m", "y", "k")


def ShowTracking2D(
    analysis: analysis_t,
    /,
    *,
    with_segmentation: bool = True,
    with_cell_labels: bool = True,
    with_track_labels: bool = True,
    with_ticks: bool = True,
    with_colorbar: bool = True,
    mode: str = "forking",
    figure_name: str = "tracking-2D",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    explorer = dbe.t_explorer_2d_t.NewForSequence(
        analysis,
        dbe,
        with_segmentation=with_segmentation,
        with_cell_labels=with_cell_labels,
        with_track_labels=with_track_labels,
        with_ticks=with_ticks,
        with_colorbar=with_colorbar,
        mode=mode,
    )

    explorer.figure.Archive(name=figure_name)
    if prepare_only:
        output = explorer
    else:
        explorer.figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def ShowTracking3D(
    analysis: analysis_t,
    /,
    *,
    with_track_labels: bool = True,
    with_cell_labels: bool = True,
    figure_name: str = "tracking-3D",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    figure, axes = dbe.figure_3d_t.NewFigureAndAxes(title=figure_name)
    axes: axes_3d_t
    colormap = axes.AddColormapFromMilestones(
        "Tracking Affinity", ((0.0, "black"), (0.75, "red"), (1.0, "blue"))
    )

    thrd.PlotFirstFrameAsFloor(
        analysis.sequence[analysis.sequence.plot_channel][0], axes
    )

    time_scaling = axes.__class__.TimeScaling(
        analysis.sequence.shape, analysis.sequence.length
    )
    for t_idx, track in enumerate(analysis.tracks):
        low_affinities = tuple(
            _ffn < _LOW_AFFINITY for _ffn in track.tracking_affinities
        )
        low_fraction = nmpy.count_nonzero(low_affinities) / (
            0.3 * low_affinities.__len__()
        )
        color = colormap(1.0 - min(1.0, low_fraction))

        for cells, start_time_point, label in track.PiecesIterator():
            n_cells = cells.__len__()
            # Use *cell_labels instead of cell_labels in case with_cell_labels is False, which then makes the labels
            # accessible through cell_labels[0].
            rows, cols, times, *cell_labels = _AsRowsColsTimes(
                cells, start_time_point, with_labels=with_cell_labels
            )
            times = tuple(time_scaling * _tme for _tme in times)

            axes.PlotLines(rows, cols, times, color=color)

            if with_cell_labels:
                after_last_idx = n_cells - 1 if label is None else n_cells
                for c_idx in range(after_last_idx):
                    axes.PlotText(
                        rows[c_idx],
                        cols[c_idx],
                        times[c_idx],
                        str(cell_labels[0][c_idx]),
                        fontsize="x-small",
                        color=color,
                    )
            if with_track_labels and (label is not None):
                axes.PlotText(
                    rows[-1],
                    cols[-1],
                    times[-1] + 0.25,
                    str(label),
                    fontsize="x-small",
                    color=color,
                )

    axes.SetTimeAxisProperties(analysis.sequence.length - 1)

    figure.Archive(name=figure_name)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def ShowInvalidTracking2D(
    analysis: analysis_t,
    /,
    *,
    with_cell_labels: bool = True,
    figure_name: str = "invalid-tracking-2D",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    invalids = [_rcd[0] for _rcd in analysis.tracks.invalids]
    if invalids.__len__() == 0:
        return

    figure, axes = dbe.figure_2d_t.NewFigureAndAxes(title=figure_name)
    axes: axes_2d_t

    height = analysis.sequence.shape[0]
    current_base_pos = 0.0
    colors = _MATPLOTLIB_COLORS
    for t_idx, track in enumerate(invalids):
        color_idx = t_idx % colors.__len__()

        rows, cols = zip(*(_cll.centroid.tolist() for _cll in track))
        positions = tuple(_row + _col * height for _row, _col in zip(rows, cols))
        min_pos = min(positions)
        max_pos = max(positions)
        if max_pos == min_pos:
            pos_scaling = 1.0
        else:
            pos_scaling = 1.0 / (max_pos - min_pos)

        if isinstance(track, unstructured_track_t):
            for time_point, cells, has_leaf in track.multi_segments_iterator:
                n_cells = cells.__len__()
                rows, cols = zip(*(_cll.centroid.tolist() for _cll in cells))
                positions = nmpy.fromiter(
                    (_row + _col * height for _row, _col in zip(rows, cols)),
                    nmpy.float64,
                )
                positions = pos_scaling * (positions - min_pos) + current_base_pos
                times = tuple(time_point + _idx for _idx in range(n_cells))

                axes.PlotLines(times, positions, colors[color_idx])

                if with_cell_labels:
                    after_last_idx = n_cells if has_leaf else n_cells - 1
                    labels = tuple(_cll.label for _cll in cells)
                    for c_idx in range(after_last_idx):
                        axes.PlotText(
                            times[c_idx],
                            positions[c_idx],
                            str(labels[c_idx]),
                            fontsize="x-small",
                            color=colors[color_idx],
                        )
        else:
            for cells, start_time_point, label in track.PiecesIterator():
                n_cells = cells.__len__()
                # Use *cell_labels instead of cell_labels in case with_cell_labels is False, which then makes the labels
                # accessible through cell_labels[0].
                rows, cols, times, *cell_labels = _AsRowsColsTimes(
                    cells, start_time_point, with_labels=with_cell_labels
                )
                positions = nmpy.fromiter(
                    (_row + _col * height for _row, _col in zip(rows, cols)),
                    nmpy.float64,
                )
                positions = pos_scaling * (positions - min_pos) + current_base_pos

                axes.PlotLines(times, positions, colors[color_idx])

                if with_cell_labels:
                    after_last_idx = n_cells - 1 if label is None else n_cells
                    for c_idx in range(after_last_idx):
                        axes.PlotText(
                            times[c_idx],
                            positions[c_idx],
                            str(cell_labels[0][c_idx]),
                            fontsize="x-small",
                            color=colors[color_idx],
                        )
                if label is not None:
                    axes.PlotText(
                        times[-1] + 0.25,
                        positions[-1],
                        str(label),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )
        current_base_pos += 1.25

    axes.SetTimeAxisProperties(analysis.sequence.length - 1)

    figure.Archive(name=figure_name)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def ShowInvalidTracking3D(
    analysis: analysis_t,
    /,
    *,
    with_cell_labels: bool = True,
    figure_name: str = "invalid-tracking-3D",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    invalids = [_rcd[0] for _rcd in analysis.tracks.invalids]
    if invalids.__len__() == 0:
        return

    figure, axes = dbe.figure_3d_t.NewFigureAndAxes(title=figure_name)
    axes: axes_3d_t

    thrd.PlotFirstFrameAsFloor(
        analysis.sequence[analysis.sequence.plot_channel][0], axes
    )

    colors = _MATPLOTLIB_COLORS
    for t_idx, track in enumerate(invalids):
        color_idx = t_idx % colors.__len__()

        if isinstance(track, unstructured_track_t):
            for time_point, cells, has_leaf in track.multi_segments_iterator:
                n_cells = cells.__len__()
                rows, cols = tuple(zip(*(_cll.centroid.tolist() for _cll in cells)))
                times = tuple(time_point + _idx for _idx in range(n_cells))

                axes.PlotLines(rows, cols, times, colors[color_idx])

                if with_cell_labels:
                    after_last_idx = n_cells if has_leaf else n_cells - 1
                    labels = tuple(_cll.label for _cll in cells)
                    for c_idx in range(after_last_idx):
                        axes.PlotText(
                            rows[c_idx],
                            cols[c_idx],
                            times[c_idx],
                            str(labels[c_idx]),
                            fontsize="x-small",
                            color=colors[color_idx],
                        )
        else:
            for cells, start_time_point, label in track.PiecesIterator():
                n_cells = cells.__len__()
                # Use *cell_labels instead of cell_labels in case with_cell_labels is False, which then makes the labels
                # accessible through cell_labels[0].
                rows, cols, times, *cell_labels = _AsRowsColsTimes(
                    cells, start_time_point, with_labels=with_cell_labels
                )

                axes.PlotLines(rows, cols, times, colors[color_idx])

                if with_cell_labels:
                    after_last_idx = n_cells - 1 if label is None else n_cells
                    for c_idx in range(after_last_idx):
                        axes.PlotText(
                            rows[c_idx],
                            cols[c_idx],
                            times[c_idx],
                            str(cell_labels[0][c_idx]),
                            fontsize="x-small",
                            color=colors[color_idx],
                        )
                if label is not None:
                    axes.PlotText(
                        rows[-1],
                        cols[-1],
                        times[-1] + 0.25,
                        str(label),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )

    axes.SetTimeAxisProperties(analysis.sequence.length - 1)

    figure.Archive(name=figure_name)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def _AsRowsColsTimes(
    cells: Sequence[cell_t], start_time_point: int, /, *, with_labels: bool = False
) -> Union[
    tuple[tuple[float, ...], tuple[float, ...], tuple[int, ...]],
    tuple[tuple[float, ...], tuple[float, ...], tuple[int, ...], tuple[int, ...]],
]:
    """"""
    n_cells = cells.__len__()

    rows, cols = tuple(zip(*(_cll.centroid.tolist() for _cll in cells)))
    times = tuple(range(start_time_point, start_time_point + n_cells))

    if with_labels:
        labels = tuple(_cll.label for _cll in cells)
        return rows, cols, times, labels

    return rows, cols, times
