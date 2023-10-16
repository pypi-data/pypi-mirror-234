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
from typing import cast

from cell_tracking_BC.in_out.graphics.type.annotation import annotation_h
from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t as axes_t
from cell_tracking_BC.in_out.graphics.type.context import context_t
from cell_tracking_BC.in_out.graphics.type.event import event_h
from cell_tracking_BC.in_out.graphics.type.figure import figure_t

# from cell_tracking_BC.in_out.graphics.type.s_viewer_2d import s_viewer_2d_t
from cell_tracking_BC.in_out.graphics.type.t_viewer_2d import t_viewer_2d_t
from cell_tracking_BC.type.analysis import analysis_t


@dtcl.dataclass(repr=False, eq=False)
class t_explorer_2d_t:
    figure: figure_t
    t_viewer: t_viewer_2d_t
    # s_viewer: s_viewer_2d_t

    annotation: annotation_h = dtcl.field(init=False, default=None)

    dbe: context_t = None

    @classmethod
    def NewForSequence(
        cls,
        analysis: analysis_t,
        dbe: context_t,
        /,
        *,
        with_segmentation: bool = True,
        with_cell_labels: bool = True,
        with_track_labels: bool = True,
        with_ticks: bool = True,
        with_colorbar: bool = True,
        mode: str = "forking",
    ) -> t_explorer_2d_t:
        """
        mode: see t_viewer_2d_t.NewForTracks
        Annotation-on-hover code adapted from:
        https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib
        Answered by ImportanceOfBeingErnest on Nov 7 '17 at 20:23
        Edited by waterproof on Aug 12 '19 at 20:08
        """
        figure, axes_track = dbe.figure_2d_t.NewFigureAndAxes()
        axes_track = cast(axes_t, axes_track)
        # axes_viewer = cast(axes_t, two_axes[1])

        t_viewer = t_viewer_2d_t.NewForTracks(
            analysis.tracks, dbe, mode=mode, in_axes=axes_track
        )
        # s_viewer = dbe.s_viewer_2d_t(*dbe.figure_2d_t.NewFigureAndAxes())
        # s_viewer = dbe.s_viewer_2d_t.NewForAllStreams(
        #     analysis,
        #     dbe,
        #     with_segmentation=with_segmentation,
        #     with_cell_labels=with_cell_labels,
        #     with_track_labels=with_track_labels,
        #     in_axes=axes_viewer,
        #     with_ticks=with_ticks,
        #     with_colorbar=with_colorbar,
        # )
        # Cannot set conversion function here since it creates an import cycle
        # s_viewer.SetConversionToAnnotatedVolume(AsAnnotatedVolume)

        instance = cls(
            figure=figure,
            t_viewer=t_viewer,
            # s_viewer=s_viewer,
            dbe=dbe,
        )

        annotation = t_viewer.axes.PlotAnnotation(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox={"boxstyle": "round", "fc": "c"},
            arrowprops={"arrowstyle": "-"},
        )
        dbe.SetVisibility(annotation, False)

        instance.annotation = annotation

        # figure.ActivateEvent("button_press_event", instance._OnButtonPress)

        figure.ActivateTightLayout(h_pad=0.05)

        return instance

    def _UpdateLinkedAnnotation(
        self,
        event: event_h,
        /,
    ) -> None:
        """"""
        raise NotImplementedError

    # def _OnButtonPress(
    #     self,
    #     event: event_h,
    #     /,
    # ) -> None:
    #     """"""
    #     if self.dbe.IsTargetOfEvent(self.t_viewer.axes, event):
    #         self._UpdateLinkedAnnotation(event)
    #     # elif self.dbe.IsTargetOfEvent(self.s_viewer.axes, event):
    #     #     pass
    #     elif self.dbe.IsVisible(self.annotation):
    #         self.dbe.SetVisibility(self.annotation, False)
    #         self.figure.Update()
