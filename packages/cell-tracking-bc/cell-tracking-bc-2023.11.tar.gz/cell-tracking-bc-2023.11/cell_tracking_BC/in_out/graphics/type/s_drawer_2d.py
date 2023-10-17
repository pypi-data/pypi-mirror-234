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
from typing import Optional, Sequence, Union

import numpy as nmpy

import cell_tracking_BC.in_out.graphics.generic.d_any as gphc
from cell_tracking_BC.in_out.graphics.type.annotation import annotation_h
from cell_tracking_BC.in_out.graphics.type.axes import axes_2d_t as axes_t
from cell_tracking_BC.in_out.graphics.type.context import context_t
from cell_tracking_BC.in_out.graphics.type.figure import figure_t
from cell_tracking_BC.in_out.graphics.type.signatures import signatures_p
from cell_tracking_BC.in_out.graphics.type.widget import slider_h
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.base import compartment_id_t
from cell_tracking_BC.type.compartment.cell import cell_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t

array_t = nmpy.ndarray


@dtcl.dataclass(repr=False, eq=False)
class s_drawer_2d_t:
    figure: figure_t
    axes: axes_t

    current_time_point: int = -1  # Used only when slider is None
    current_label: int = -1

    slider: slider_h = None

    # Only meaningful for NewForChannels
    cell_contours: Sequence[Sequence[array_t]] = None
    # Using frame labeling for array_t's, or cell_frames below for sequence_t
    with_cell_labels: bool = False
    main_frames: Sequence[array_t] = None
    all_cells: Sequence[Sequence[cell_t]] = None
    tracks: tracks_t = None
    annotations: Sequence[
        tuple[int, Union[annotation_h, Sequence[annotation_h]]]
    ] = None

    dbe: context_t = None

    @classmethod
    def NewForChannels(
        cls,
        analysis: analysis_t,
        dbe: context_t,
        /,
        *,
        channel: str = None,
        with_segmentation: bool = False,
        with_cell_labels: bool = False,
        with_track_labels: bool = False,
        in_axes: axes_t = None,
        with_ticks: bool = True,
        with_colorbar: bool = True,
    ) -> s_drawer_2d_t:
        """"""
        has_cells = (
            analysis.segmentations is not None
        ) and analysis.segmentations.has_cells
        with_cell_labels = with_cell_labels and has_cells
        if has_cells:
            main_frames = analysis.sequence[analysis.sequence.plot_channel]
            cells = tuple(analysis.segmentations.cells_iterator)
        else:
            main_frames = None
            cells = None

        if channel is None:
            channel = analysis.sequence.plot_channel
        instance = cls._NewForSequence(
            analysis,
            analysis.sequence[channel],
            dbe,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            main_frames=main_frames,
            all_cells=cells,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
        )
        if with_colorbar:
            instance.AddColorbarForImage()

        return instance

    @classmethod
    def NewForSegmentation(
        cls,
        analysis: analysis_t,
        dbe: context_t,
        /,
        *,
        with_cell_labels: bool = True,
        with_track_labels: bool = True,
        in_axes: axes_t = None,
        with_ticks: bool = True,
    ) -> s_drawer_2d_t:
        """"""
        has_cells = (
            analysis.segmentations is not None
        ) and analysis.segmentations.has_cells
        if has_cells:
            main_frames = analysis.sequence[analysis.sequence.plot_channel]
            cells = tuple(analysis.segmentations.cells_iterator)
        else:
            main_frames = None
            cells = None

        return cls._NewForSequence(
            analysis,
            analysis.segmentations.Compartments(compartment_id_t.CELL),
            dbe,
            with_cell_labels=with_cell_labels,
            main_frames=main_frames,
            all_cells=cells,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
        )

    @classmethod
    def NewForAllStreams(
        cls,
        analysis: analysis_t,
        dbe: context_t,
        /,
        *,
        with_segmentation: bool = False,
        with_cell_labels: bool = False,
        with_track_labels: bool = False,
        in_axes: axes_t = None,
        with_ticks: bool = True,
        with_colorbar: bool = True,
    ) -> s_drawer_2d_t:
        """"""
        has_cells = (
            analysis.segmentations is not None
        ) and analysis.segmentations.has_cells
        with_cell_labels = with_cell_labels and has_cells
        if has_cells:
            main_frames = analysis.sequence[analysis.sequence.plot_channel]
            cells = tuple(analysis.segmentations.cells_iterator)
        else:
            main_frames = None
            cells = None

        instance = cls._NewForSequence(
            analysis,
            analysis.sequence[analysis.sequence.plot_channel],
            dbe,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            main_frames=main_frames,
            all_cells=cells,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
        )
        if with_colorbar:
            instance.AddColorbarForImage()

        return instance

    @classmethod
    def _NewForSequence(
        cls,
        analysis: analysis_t,
        dbe: context_t,
        /,
        *,
        with_segmentation: bool = False,
        with_cell_labels: bool = True,
        main_frames: Sequence[array_t] = None,
        all_cells: Sequence[Sequence[cell_t]] = None,
        with_track_labels: bool = True,
        in_axes: axes_t = None,
        with_ticks: bool = True,
    ) -> s_drawer_2d_t:
        """"""
        if in_axes is None:
            figure, axes = dbe.figure_2d_t.NewFigureAndAxes()
        else:
            figure = in_axes.Figure()
            axes = in_axes
        if not with_ticks:
            axes.TurnTicksOff()

        cell_contours = gphc.CellContours(analysis, with_segmentation)
        tracks = gphc.CellTracks(analysis, with_track_labels)

        cell_annotations = _PlotFirstFrame(
            cell_contours,
            with_cell_labels,
            main_frames,
            all_cells,
            tracks,
            axes,
            dbe.CellAnnotationStyle,
        )

        instance = cls(
            figure=figure,
            axes=axes,
            current_time_point=0,
            cell_contours=cell_contours,
            with_cell_labels=with_cell_labels,
            tracks=tracks,
            main_frames=main_frames,
            all_cells=all_cells,
            annotations=cell_annotations,
            dbe=dbe,
        )

        return instance

    def AddColorbarForImage(self) -> None:
        """"""
        raise NotImplementedError

    def SelectTimePoint(
        self,
        /,
        *,
        time_point: Union[int, float] = None,
        highlighted: int = -1,
        should_draw_frame: bool = True,
        force_new_time_point: bool = False,
        should_update_limits: bool = False,
        should_update_figure: bool = True,
    ) -> None:
        """
        force_new_time_point: If the slider has been updated externally, the time point will not be considered new, and
        no update will be made. Hence, this parameter.
        """
        if self.slider is None:
            current_time_point = self.current_time_point
        else:
            current_time_point = self.slider.val
        if time_point is None:
            time_point = current_time_point
        else:
            time_point = int(time_point)

        # If not should_draw_frame, new version is enforced so that at time point 0, when current_time_point is also 0,
        # an image of zeros is plotted anyway. An alternative would be to call this method with force_new_time_point.
        # Actually, when this function is called to save an annotated sequence, it is curious that the first frame is
        # already plotted since one could assume that, in this case, the drawer would be blank. This should be
        # investigated.
        time_point_is_new = (time_point != current_time_point) or force_new_time_point

        if time_point_is_new:
            frame = None
            # interval, frames = self.all_versions[version]
            # frame = frames[time_point]
            # if should_draw_frame:
            #     self.axes.UpdateImage(
            #         frame, interval=interval, should_update_limits=should_update_limits
            #     )
            # else:
            #     self.axes.UpdateImage(numpy.zeros_like(frame))
        else:
            frame = None

        if self.annotations is not None:
            if time_point_is_new:
                if self.cell_contours is None:
                    contours = None
                else:
                    contours = self.cell_contours[time_point]
                if self.all_cells is None:
                    cells = None
                else:
                    cells = self.all_cells[time_point]

                self.annotations = self.axes.PlotCellsDetails(
                    frame,
                    contours,
                    self.with_cell_labels,
                    cells,
                    self.tracks,
                    self.dbe.CellAnnotationStyle,
                    highlighted=highlighted,
                )
                self.current_label = highlighted
            elif highlighted > 0:
                self.HighlightAnnotation(highlighted, should_draw=False)

        if time_point_is_new:
            if self.slider is None:
                self.current_time_point = time_point
            else:
                self.dbe.UpdateSlider(self.slider, time_point)

        if should_update_figure:
            self.figure.Update()

    def HighlightAnnotation(self, label: int, /, *, should_draw: bool = True) -> None:
        """
        If label is <= 0 or > max cell label in current frame, then un-highlights all annotations
        """
        raise NotImplementedError


def _PlotFirstFrame(
    cell_contours: Optional[Sequence[Sequence[array_t]]],
    with_cell_labels: bool,
    main_frames: Optional[Sequence[array_t]],
    cells: Optional[Sequence[Sequence[cell_t]]],
    tracks: Optional[tracks_t],
    axes: axes_t,
    CellAnnotationStyle: signatures_p.cell_annotation_style_h,
    /,
) -> Optional[Sequence[tuple[int, annotation_h]]]:
    """"""
    cell_annotations = None
    # interval, version = all_versions[current_version]
    # first_frame = version[0]
    #
    # axes.PlotImage(first_frame, interval=interval)
    #
    # if (cell_contours is not None) or with_cell_labels or (tracks is not None):
    #     if cell_contours is None:
    #         contours = None
    #     else:
    #         contours = cell_contours[0]
    #     if cells is None:
    #         first_cells = None
    #     else:
    #         first_cells = cells[0]
    #     cell_annotations = axes.PlotCellsDetails(
    #         first_frame,
    #         contours,
    #         with_cell_labels,
    #         first_cells,
    #         tracks,
    #         CellAnnotationStyle,
    #     )
    # else:
    #     cell_annotations = None

    # Once the first frame has been plot, disable axes autoscale to try to speed future plots up
    axes.Freeze()

    return cell_annotations
