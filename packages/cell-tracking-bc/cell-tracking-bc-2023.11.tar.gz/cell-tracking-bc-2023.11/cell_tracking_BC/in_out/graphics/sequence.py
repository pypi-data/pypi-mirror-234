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

import cell_tracking_BC.in_out.graphics.generic.d_2 as gnr2
import cell_tracking_BC.in_out.graphics.generic.d_3 as gnr3
import cell_tracking_BC.in_out.graphics.generic.d_any as gnrc
from cell_tracking_BC.in_out.graphics.dbe.matplotlib.context import DRAWING_CONTEXT
from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t, axes_3d_t
from cell_tracking_BC.in_out.graphics.type.context import context_t
from cell_tracking_BC.in_out.graphics.type.figure import figure_t
from cell_tracking_BC.in_out.graphics.type.s_viewer_2d import s_viewer_2d_t
from cell_tracking_BC.type.acquisition.sequence import sequence_t
from cell_tracking_BC.type.analysis import analysis_t

array_t = nmpy.ndarray


def ShowSequenceStatistics(
    sequence: sequence_t,
    /,
    *,
    channel: Union[str, Sequence[str]] = None,
    figure_name: str = "Sequence Statistics",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    if channel is None:
        channels = sequence.base_channels
    elif isinstance(channel, str):
        channels = (channel,)
    else:
        channels = channel

    statistics = ("amin", "amax", "mean", "median")
    ComputedStatistics = tuple(getattr(nmpy, _stt) for _stt in statistics)
    records = {_stt: {_chl: [] for _chl in channels} for _stt in statistics}
    for frames in sequence.FramesIterator(channels=channels):
        for channel, frame in zip(channels, frames):
            for name, Computed in zip(statistics, ComputedStatistics):
                records[name][channel].append(Computed(frame))
    for name, records_per_channel in records.items():
        for channel, evolution in records_per_channel.items():
            min_value = nmpy.amin(evolution)
            normalization = nmpy.amax(evolution) - min_value
            if normalization == 0:
                normalization = 1.0
            records[name][channel] = (
                (evolution - min_value) / normalization,
                min_value,
                normalization,
            )

    figure, all_axes = dbe.figure_2d_t.NewFigureAndAxes(
        n_rows=statistics.__len__(), title=figure_name
    )
    all_axes: Sequence[axes_2d_t]

    for s_idx, (name, records_per_channel) in enumerate(records.items()):
        for channel, (
            evolution,
            min_value,
            normalization,
        ) in records_per_channel.items():
            all_axes[s_idx].PlotLines(
                range(evolution.__len__()),
                evolution,
                label=f"({channel} - {min_value:.2f}) / {normalization:.2g}",
            )

    for name, axes in zip(records.keys(), all_axes):
        axes.SetTimeAxisProperties(sequence.length - 1)
        axes.PlotLegend()
        axes.SetTitle(name)

    # figure.Archive(name=figure_name, archiver=archiver)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def ShowSequence(
    analysis: Union[Sequence[array_t], analysis_t],
    /,
    *,
    channel: str = None,
    with_segmentation: bool = True,
    with_cell_labels: bool = True,
    with_track_labels: bool = True,
    mode: str = "2d+t",
    keep_every: int = 2,
    n_levels: int = 100,
    iso_value: float = None,
    with_ticks: bool = True,
    with_colorbar: bool = True,
    figure_name: str = "sequence",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[Union[figure_t, s_viewer_2d_t]]:
    """
    mode: "2d+t", "mille-feuille", "tunnels"
    """
    output = None

    if mode == "2d+t":
        viewer = dbe.s_viewer_2d_t.NewForChannels(
            analysis,
            dbe,
            channel=channel,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            with_track_labels=with_track_labels,
            with_ticks=with_ticks,
            with_colorbar=with_colorbar,
        )
        viewer.SetConversionToAnnotatedVolume(gnr2.AsAnnotatedVolume)
        viewer.figure.Archive(name=figure_name)
        if prepare_only:
            output = viewer
        else:
            viewer.figure.Show(
                interactively=interactively, in_main_thread=in_main_thread
            )
    elif mode in ("mille-feuille", "tunnels"):
        if isinstance(analysis, analysis_t):
            if channel is None:
                channel = analysis.sequence.plot_channel
            frames = analysis.sequence[channel]
        else:
            frames = analysis

        figure, axes = dbe.figure_3d_t.NewFigureAndAxes()
        axes: axes_3d_t
        if mode == "mille-feuille":
            cell_contours = gnrc.CellContours(analysis, with_segmentation)
            tracks = gnrc.CellTracks(analysis, with_track_labels)
            gnr3.ShowFramesAsMilleFeuille(
                frames,
                cell_contours,
                with_cell_labels,
                tuple(analysis.segmentations.cells_iterator),
                tracks,
                axes,
                dbe.CellAnnotationStyle,
                keep_every=keep_every,
                n_levels=n_levels,
            )
        else:
            if iso_value is None:
                iso_value = nmpy.percentile(frames[0], 75).item()
            gnr3.ShowFramesAsTunnels(
                frames, axes, keep_every=keep_every, iso_value=iso_value
            )

        figure.Archive(name=figure_name)
        if prepare_only:
            output = figure
        else:
            figure.Show(interactively=interactively, in_main_thread=in_main_thread)
    else:
        raise ValueError(
            f'{mode}: Invalid mode. Expected="2d+t", "mille-feuille", "tunnels".'
        )

    return output
