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

from numbers import Real as number_t
from typing import Callable, Dict, Optional, Sequence, Union

import numpy as nmpy
from logger_36 import LOGGER

from cell_tracking_BC.in_out.graphics.type.figure import figure_t


class rectangle_t(list):
    edge_color: tuple[float, float, float, float] = None
    face_color: tuple[float, float, float, float] = None

    @classmethod
    def NewFromDetails(
        cls, corner: tuple[int, float], width: float, height: float, /
    ) -> rectangle_t:
        """"""
        return cls((corner, width, height))

    @property
    def corner(self) -> tuple[int, float]:
        """"""
        return self[0]

    def Details(self) -> tuple:
        """
        corner, width, height, edge_color, face_color
        """
        return *tuple(self), self.edge_color, self.face_color

    def SetHeight(self, height: float, /) -> None:
        """"""
        self[2] = height


rectangle_info_h = tuple[int, float, float, bool, bool]
ValueTransform_h = Optional[Union[float, Callable[[float], float]]]


DIVISION_MARKER = "3"
DEATH_MARKER = "x"
DIVISION_MARKER_SIZE = 60
DEATH_MARKER_SIZE = 30

_RECTANGLE_TYPE_DIV = 0
_RECTANGLE_TYPE_DEA = 1
_RECTANGLE_TYPE_MIXED = 2


def ShowDivisionAndDeathEventResponses(
    cell_division_response: Dict[int, Optional[Sequence[float]]],
    cell_death_response: Dict[int, Optional[Sequence[float]]],
    cell_division_frame_idc: Dict[int, Optional[Sequence[int]]],
    cell_death_frame_idc: Dict[int, Optional[int]],
    sequence_length: int,
    /,
    *,
    ValueTransform: ValueTransform_h = None,
    zero_is_black: bool = True,
    show_as_barplot: bool = False,
    PlotAndShow: Callable[..., Optional[figure_t]],
    figure_name: str = "division-and-death-responses",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
) -> Optional[figure_t]:
    """
    Note: Does not respect pruning
    """
    max_label, div_values, dea_values, rectangles_w_details = _ValuesAndRectangles(
        cell_division_response,
        cell_death_response,
        cell_division_frame_idc,
        cell_death_frame_idc,
        show_as_barplot,
    )
    if rectangles_w_details.__len__() == 0:
        LOGGER.info("Empty division or death responses")
        return

    _SetRectanglesColorAndHeight(
        rectangles_w_details,
        div_values,
        dea_values,
        ValueTransform,
        zero_is_black,
        show_as_barplot,
    )
    events = _DivisionAndDeathEvents(rectangles_w_details)
    rectangles = tuple(_elm[0] for _elm in rectangles_w_details)

    if show_as_barplot:
        track_height = 2
    else:
        track_height = 1

    return PlotAndShow(
        events,
        rectangles,
        track_height,
        sequence_length,
        max_label,
        zero_is_black=zero_is_black,
        show_as_barplot=show_as_barplot,
        figure_name=figure_name,
        prepare_only=prepare_only,
        interactively=interactively,
        in_main_thread=in_main_thread,
    )


def _ValuesAndRectangles(
    cell_division_response: Dict[int, Optional[Sequence[float]]],
    cell_death_response: Dict[int, Optional[Sequence[float]]],
    cell_division_frame_idc: Dict[int, Optional[Sequence[int]]],
    cell_death_frame_idc: Dict[int, Optional[int]],
    show_as_barplot: bool,
    /,
) -> tuple[
    int,
    Sequence[float],
    Sequence[float],
    Sequence[tuple[rectangle_t, rectangle_info_h]],
]:
    """"""
    if (cell_division_response.__len__() == 0) or (cell_death_response.__len__() == 0):
        LOGGER.warning("Event Responses: No associated multiple.")
        return 0, (), (), ()

    max_label = max(max(cell_division_response.keys()), max(cell_death_response.keys()))
    div_values = []
    dea_values = []
    rectangles = []

    invalid_labels = set(range(1, max_label + 1))
    for label, division_response in cell_division_response.items():
        if label in cell_death_response:
            death_response = cell_death_response[label]
        else:
            death_response = None
        if label in cell_division_frame_idc:
            division_frame_idc = cell_division_frame_idc[label]
        else:
            division_frame_idc = None
        if label in cell_death_frame_idc:
            death_frame_idx = cell_death_frame_idc[label]
        else:
            death_frame_idx = None
        invalid_labels.remove(label)

        if (division_response is None) and (death_response is None):
            LOGGER.warning(f"Track {label}: No event responses")
            continue

        if division_response is None:
            LOGGER.warning(
                f"Track {label}: No division response (too short or fully pruned after death detection)"
            )
        if death_response is None:
            LOGGER.warning(
                f"Track {label}: No death response (too short or fully pruned after splitting invalidation)"
            )

        # Whether pattern-based or track-based
        death_occurred = death_frame_idx is not None
        if death_occurred:
            n_valids = abs(death_frame_idx) + 1
            if division_response is not None:
                division_response = division_response[:n_valids]
            # The death response can be None if death is topologic (negative death_frame_idx)
            if death_response is not None:
                death_response = death_response[:n_valids]

        if division_response is not None:
            div_values.extend(division_response)
        if death_response is not None:
            dea_values.extend(death_response)

        # Could be inside an "if not show_as_barplot", but the IDE might complain about potentially uninitialized object
        rtype = _RECTANGLE_TYPE_MIXED
        if division_response is None:
            if show_as_barplot:
                rtype = _RECTANGLE_TYPE_DEA
            for t_idx, dea_value in enumerate(death_response):
                if dea_value is None:
                    # The trajectory does not start at time point 0
                    continue

                # Note: division_frame_idc is None if no divisions (used to be (-1,))
                # Note: division is checked despite the track having no division response because the sibling track
                # might have a response (if long enough) higher enough.
                dividing = (division_frame_idc is not None) and (
                    t_idx in division_frame_idc
                )
                # Detected by pattern matching (track ending => negative death frame index)
                dying = death_occurred and (t_idx == death_frame_idx)

                rectangle = _EventRectangle(t_idx, label, show_as_barplot)
                details = (rtype, 0.0, dea_value, dividing, dying)
                rectangles.append((rectangle, details))

                if dying:
                    break
        elif death_response is None:
            if show_as_barplot:
                rtype = _RECTANGLE_TYPE_DIV
            for t_idx, div_value in enumerate(division_response):
                if div_value is None:
                    # The trajectory does not start at time point 0
                    continue

                # Note: division_frame_idc is None if no divisions (used to be (-1,))
                dividing = (division_frame_idc is not None) and (
                    t_idx in division_frame_idc
                )

                rectangle = _EventRectangle(t_idx, label, show_as_barplot)
                details = (rtype, div_value, 0.0, dividing, False)
                rectangles.append((rectangle, details))
        else:
            for t_idx, (div_value, dea_value) in enumerate(
                zip(division_response, death_response)
            ):
                if div_value is None:
                    # The trajectory does not start at time point 0
                    if dea_value is not None:
                        raise ValueError(
                            f"{label}: Trajectory has a valid death response at time point {t_idx} "
                            f"whereas the division response is invalid"
                        )
                    continue

                # Note: division_frame_idc is None if no divisions (used to be (-1,))
                dividing = (division_frame_idc is not None) and (
                    t_idx in division_frame_idc
                )
                # Detected by pattern matching (track ending => negative death frame index)
                dying = death_occurred and (t_idx == death_frame_idx)

                rectangle = _EventRectangle(t_idx, label, show_as_barplot)
                if show_as_barplot:
                    details = (_RECTANGLE_TYPE_DEA, 0.0, dea_value, False, dying)
                    rectangles.append((rectangle, details))

                    rectangle = _EventRectangle(t_idx, label, show_as_barplot)
                    details = (_RECTANGLE_TYPE_DIV, div_value, 0.0, dividing, False)
                else:
                    details = (
                        _RECTANGLE_TYPE_MIXED,
                        div_value,
                        dea_value,
                        dividing,
                        dying,
                    )
                rectangles.append((rectangle, details))

                if dying:
                    break

    LOGGER.warning(f"Invalid Tracks (no event responses): {invalid_labels}")

    return max_label, div_values, dea_values, rectangles


def _EventRectangle(
    time_point: int,
    label: int,
    show_as_barplot: bool,
    /,
) -> rectangle_t:
    """"""
    if show_as_barplot:
        corner_y = 2.0 * label - 1.5
    else:
        corner_y = label - 0.5

    return rectangle_t.NewFromDetails((time_point, corner_y), 1.0, 1.0)


def _SetRectanglesColorAndHeight(
    rectangles: Sequence[tuple[rectangle_t, rectangle_info_h]],
    div_values: Sequence[float],
    dea_values: Sequence[float],
    ValueTransform: ValueTransform_h,
    zero_is_black: bool,
    show_as_barplot: bool,
    /,
) -> None:
    """
    ValueTransform: if a number, then value <= ValueTransform => value <- 0.0
    """
    if ValueTransform is None:
        ValueTransform = lambda _vle: _vle
    elif isinstance(ValueTransform, number_t):
        threshold = float(ValueTransform)

        def _ValueTransform(_vle: float, /) -> float:
            if _vle <= threshold:
                return 0.0
            else:
                return _vle

        ValueTransform = _ValueTransform

    min_div_value, div_scaling = _MinimumAndScaling(div_values)
    min_dea_value, dea_scaling = _MinimumAndScaling(dea_values)

    for rectangle, (rtype, div_value, dea_value, dividing, dying) in rectangles:
        div = ValueTransform(div_scaling * (div_value - min_div_value))
        dea = ValueTransform(dea_scaling * (dea_value - min_dea_value))

        if show_as_barplot:
            if rtype == _RECTANGLE_TYPE_DEA:
                if zero_is_black:
                    color = (dea, 0.0, 0.0)
                else:
                    color = (1.0, 1.0 - dea, 1.0 - dea)
                rectangle.SetHeight(1.5 * dea)
            else:
                if zero_is_black:
                    color = (0.0, 0.0, div)
                else:
                    color = (1.0 - div, 1.0 - div, 1.0)
                rectangle.SetHeight(1.5 * div)
                rectangle.face_color = color + (0.3,)
            rectangle.edge_color = color
        else:
            if zero_is_black:
                color = (dea, 0.0, div)
            else:
                div_color = (1.0 - div, 1.0 - div, 1.0)
                dea_color = (1.0, 1.0 - dea, 1.0 - dea)
                color = nmpy.minimum(div_color, dea_color)
            rectangle.edge_color = color
            rectangle.face_color = color


def _DivisionAndDeathEvents(
    rectangles: Sequence[tuple[rectangle_t, rectangle_info_h]],
    /,
) -> Sequence[tuple[str, int, Sequence[float]]]:
    """"""
    output = []

    for rectangle, (*_, dividing, dying) in rectangles:
        if dividing or dying:
            where = tuple(_crd + 0.5 for _crd in rectangle.corner)
            if dividing:
                output.append((DIVISION_MARKER, DIVISION_MARKER_SIZE, where))
            if dying:
                output.append((DEATH_MARKER, DEATH_MARKER_SIZE, where))

    return output


def _MinimumAndScaling(values: Sequence[float], /) -> tuple[float, float]:
    """"""
    if values.__len__() > 0:
        min_value = min(values)
        max_value = max(values)
        scaling = 1.0 / (max_value - min_value)
    else:
        min_value, scaling = 0.0, 1.0

    return min_value, scaling
