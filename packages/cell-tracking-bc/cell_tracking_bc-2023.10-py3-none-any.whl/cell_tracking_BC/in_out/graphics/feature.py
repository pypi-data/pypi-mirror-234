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

import numbers as nmbr
from typing import Optional

from cell_tracking_BC.in_out.graphics.dbe.matplotlib.context import DRAWING_CONTEXT
from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t
from cell_tracking_BC.in_out.graphics.type.context import context_t
from cell_tracking_BC.in_out.graphics.type.figure import figure_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t


def ShowCellFeatureEvolution(
    tracks: tracks_t,
    feature: str,
    /,
    *,
    figure_name: str = "cell-feature-evolution",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
    dbe: context_t = DRAWING_CONTEXT,
) -> Optional[figure_t]:
    """"""
    output = None

    figure, axes = dbe.figure_2d_t.NewFigureAndAxes(title=feature)
    axes: axes_2d_t

    max_track_duration = 0
    for track in tracks:
        root_time_point = track.topologic_root_time_point
        for path, label in track.LabeledThreadIterator(topologic_mode=True):
            leaf_time_point = track.CellTimePoint(path[-1])
            evolution = tuple(_cll.features[feature] for _cll in path)
            if not isinstance(evolution[0], nmbr.Number):
                break

            axes.PlotLines(
                range(root_time_point, leaf_time_point + 1),
                evolution,
                label=label,
            )

            duration = leaf_time_point - root_time_point
            if duration > max_track_duration:
                max_track_duration = duration

    # evolutions = sequence.CellFeature(feature)
    # for label, (track, evolution) in evolutions.items():
    #     axes.PlotLines(
    #         range(track.root_time_point, track.leaf_time_point + 1),
    #         evolution,
    #         label=label,
    #     )
    #
    #     if track.length > max_track_duration:
    #         max_track_duration = track.length

    axes.SetTimeAxisProperties(max_track_duration)
    axes.PlotLegend()

    # figure.Archive(name=figure_name, archiver=archiver)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output
