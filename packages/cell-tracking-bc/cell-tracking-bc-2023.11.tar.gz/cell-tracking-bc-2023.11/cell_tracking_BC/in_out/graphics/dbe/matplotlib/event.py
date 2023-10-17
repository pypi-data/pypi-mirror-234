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

from typing import Callable, Optional, Sequence, Union

import matplotlib.lines as lins
import matplotlib.pyplot as pypl
import numpy as nmpy
from matplotlib.collections import PatchCollection as patches_t
from matplotlib.legend_handler import HandlerTuple as tuple_handler_t
from matplotlib.patches import Rectangle as mpl_rectangle_t

from cell_tracking_BC.in_out.graphics.dbe.matplotlib.d_2 import figure_t
from cell_tracking_BC.in_out.graphics.event import rectangle_t

rectangle_info_h = tuple[int, float, float, bool, bool]
ValueTransform_h = Optional[Union[float, Callable[[float], float]]]


DIVISION_MARKER = "3"
DEATH_MARKER = "x"
DIVISION_MARKER_SIZE = 60
DEATH_MARKER_SIZE = 30
N_SCORE_LEGEND_SHADES = 8

_RECTANGLE_TYPE_DIV = 0
_RECTANGLE_TYPE_DEA = 1
_RECTANGLE_TYPE_MIXED = 2

_rectangle = mpl_rectangle_t((0.0, 0.0), 1.0, 1.0)
_rectangle.set_facecolor("None")
_NO_COLOR_MATPLOTLIB = _rectangle.get_facecolor()


def PlotDivisionAndDeathEventResponses(
    events: Sequence[tuple[str, int, Sequence[float]]],
    rectangles: Sequence[rectangle_t],
    track_height: int,
    sequence_length: int,
    max_label: int,
    zero_is_black: bool = True,
    show_as_barplot: bool = False,
    figure_name: str = "division-and-death-responses",
    prepare_only: bool = False,
    interactively: bool = True,
    in_main_thread: bool = True,
) -> Optional[figure_t]:
    """"""
    output = None

    mpl_rectangles = []
    for rectangle in rectangles:
        *geometry, edge_color, face_color = rectangle.Details()
        if face_color is None:
            face_color = _NO_COLOR_MATPLOTLIB

        mpl_rectangle = mpl_rectangle_t(*geometry)
        mpl_rectangle.set_edgecolor(edge_color)
        mpl_rectangle.set_facecolor(face_color)

        mpl_rectangles.append(mpl_rectangle)

    edge_colors = tuple(_rct.get_edgecolor() for _rct in mpl_rectangles)
    face_colors = tuple(_rct.get_facecolor() for _rct in mpl_rectangles)
    patches = patches_t(mpl_rectangles, edgecolors=edge_colors, facecolors=face_colors)

    figure, axes = figure_t.NewFigureAndAxes()

    axes.add_collection(patches)
    if show_as_barplot:
        color = "k"
    elif zero_is_black:
        color = "w"
    else:
        color = "k"
    for what, size, where in events:
        axes.scatter(*where, c=color, marker=what, s=size)
    _SetAxesProperties(axes, sequence_length, max_label, track_height)
    _AddLegend(axes, zero_is_black)

    figure.Archive(name=figure_name)
    if prepare_only:
        output = figure
    else:
        figure.Show(interactively=interactively, in_main_thread=in_main_thread)

    return output


def _SetAxesProperties(
    axes: pypl.Axes, sequence_length: int, max_label: int, track_height: int, /
) -> None:
    """"""
    axes.set_xlim(left=0, right=sequence_length)
    axes.set_ylim(bottom=0, top=track_height * max_label + 1)

    if track_height == 2:
        offset = -0.5
    else:
        offset = 0.0
    positions = range(1, max_label + 1, max(1, int(round(max_label / 10))))
    axes.yaxis.set_ticks(track_height * nmpy.array(positions) + offset)
    axes.yaxis.set_ticklabels(positions)


def _AddLegend(axes: pypl.Axes, zero_is_black: bool, /) -> None:
    """"""
    shades = nmpy.linspace(0.0, 1.0, num=N_SCORE_LEGEND_SHADES)

    if zero_is_black:
        DivisionColor = lambda _shd: (0.0, 0.0, _shd)
        DeathColor = lambda _shd: (_shd, 0.0, 0.0)
    else:
        DivisionColor = lambda _shd: (1.0 - _shd, 1.0 - _shd, 1.0)
        DeathColor = lambda _shd: (1.0, 1.0 - _shd, 1.0 - _shd)
    score_legends = [
        [
            mpl_rectangle_t(
                (0, 0),
                3.0,
                5.0,
                edgecolor=_NO_COLOR_MATPLOTLIB,
                facecolor=_Clr(_shd),
            )
            for _shd in shades
        ]
        for _Clr in (DivisionColor, DeathColor)
    ]

    event_legends = [
        lins.Line2D(
            (),
            (),
            color="k",
            marker=_mrk,
            markersize=_sze,
            linestyle="None",
        )
        for _mrk, _sze in (
            (DIVISION_MARKER, DIVISION_MARKER_SIZE // 5),
            (DEATH_MARKER, DEATH_MARKER_SIZE // 5),
        )
    ]

    axes.legend(
        handles=(*score_legends, *event_legends),
        labels=("Division Score", "Death Score", "Division", "Death (pattern)"),
        loc="right",
        bbox_to_anchor=(1.3, 0.5),
        handler_map={list: tuple_handler_t(ndivide=None, pad=0)},
    )
