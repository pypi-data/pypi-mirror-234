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

import tempfile as temp
import time
from pathlib import Path as path_t
from typing import Any, Dict, Sequence, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.measure as msre
import skimage.transform as trfm
import tifffile as tiff

from cell_tracking_BC.in_out.graphics.dbe.matplotlib.style import CellAnnotationStyle
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.base import AdjustedMapWithMargin
from cell_tracking_BC.type.compartment.cell import cell_t, state_e

array_t = nmpy.ndarray


def SaveSequenceAnnotations(
    path: Union[str, path_t],
    analysis: analysis_t,
    /,
    *,
    cell_margin: float = -50.0,
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.is_dir():
        path /= "sequence_annotations.tiff"

    if path.exists():
        print(f"{path}: File (or folder) already exists...")
        path = path_t(temp.mkdtemp()) / path.name
        print(f"Using {path} instead")

    track_labels = {_tpt: {} for _tpt in range(analysis.sequence.length)}
    for track in analysis.tracks:
        root_time_point = track.topologic_root_time_point
        for cells, label in track.LabeledThreadIterator(topologic_mode=True):
            for time_point, cell in enumerate(cells, start=root_time_point):
                if cell.state is state_e.discarded:
                    # Leave "-" at the end to allow numerical sorting
                    text = f"{label}-"
                elif cell.state is state_e.dead:
                    # Leave "x" at the end to allow numerical sorting
                    text = f"{label}x"
                elif cell.state is state_e.dividing:
                    # Leave "x" at the end to allow numerical sorting
                    text = f"{label}y"
                else:
                    text = str(label)
                if cell in track_labels[time_point]:
                    track_labels[time_point][cell][0].append(label)
                    track_labels[time_point][cell][1].append(text)
                else:
                    track_labels[time_point][cell] = ([label], [text], cell.centroid)

    backend = pypl.get_backend()
    pypl.switch_backend("Agg")
    figure, axes = pypl.subplots(facecolor="w")
    canvas = figure.canvas
    renderer = canvas.get_renderer()

    annotated = None
    frame_shape = analysis.sequence.shape
    for f_idx in range(analysis.sequence.length):
        if f_idx % 20 == 0:
            print(f"    Writing frame {f_idx} @ {time.ctime()}...")

        axes.clear()
        axes.set_xlim(left=0, right=frame_shape[1] - 1)
        axes.set_ylim(bottom=0, top=frame_shape[0] - 1)
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.set_facecolor("k")
        axes.set_position((0.0, 0.0, 1.0, 1.0))

        description = _CellDescriptions(
            analysis.segmentations[f_idx].cells,
            analysis.sequence.shape,
            margins=(0, cell_margin),
        )
        for contours in description["cell_contours"].values():
            for contour in contours:
                axes.plot(
                    contour[:, 1],
                    contour[:, 0],
                    linestyle=":",
                    color=(0.0, 0.8, 0.8, 0.3),
                )

        for labels, texts, position in track_labels[f_idx].values():
            if (n_labels := labels.__len__()) > 1:
                text = f"{min(labels)}\n(+{n_labels-1})"
            else:
                text = texts[0]
            style = CellAnnotationStyle(False, n_labels > 1)
            axes.annotate(
                text,
                nmpy.flipud(position),
                ha="center",
                va="center",
                **style,
            )
        canvas.draw()

        content = nmpy.array(renderer.buffer_rgba())[1:, 1:, :3]
        if annotated is None:
            annotated = nmpy.empty(
                (*content.shape, analysis.sequence.length), dtype=nmpy.uint8
            )
        annotated[..., f_idx] = content

    pypl.close(fig=figure)  # To prevent remaining caught in event loop
    pypl.switch_backend(backend)

    # row_slice, col_slice = BoundingBoxSlices(annotated)
    # annotated = annotated[row_slice, col_slice, :, :]
    annotated = trfm.resize(
        annotated,
        (*analysis.sequence.shape, 3, analysis.sequence.length),
        preserve_range=True,
    )
    annotated = annotated.astype(nmpy.uint8, copy=False)
    annotated = nmpy.moveaxis(annotated, (0, 1, 2, 3), (2, 3, 1, 0))
    annotated = annotated[:, nmpy.newaxis, :, :, :]

    tiff.imwrite(
        str(path),
        annotated,
        photometric="rgb",
        compression="deflate",
        planarconfig="separate",
        metadata={"axes": "XYZCT"},
    )


def _CellDescriptions(
    cells: Sequence[cell_t],
    shape: tuple[int, int],
    /,
    *,
    margins: Sequence[float] = None,
) -> Dict[str, Any]:
    """"""
    output = {"cell_labels": tuple((_cll.label, _cll.centroid) for _cll in cells)}

    contours = {}
    if margins is None:
        margins = (0.0,)
    for margin in margins:
        for_margin = []
        for cell in cells:
            if (margin is None) or (margin <= 0.0):
                bb_map = nmpy.pad(cell.BBMap().astype(nmpy.int8), 1)
                if (margin is not None) and (margin < 0.0):
                    bb_map = AdjustedMapWithMargin(bb_map, cell.area, margin)
                around_cell = _LargestContourOfMap(bb_map)
                around_cell += (
                    cell.bb_slices[0].start - 1,
                    cell.bb_slices[1].start - 1,
                )
            else:
                cell_map = cell.Map(shape, margin=margin)
                around_cell = _LargestContourOfMap(cell_map)
            for_margin.append(around_cell)
        contours[margin] = tuple(for_margin)
    output["cell_contours"] = contours

    return output


def _LargestContourOfMap(map_: array_t, /) -> array_t:
    """"""
    contours = msre.find_contours(map_, level=0.5)
    if (n_contours := contours.__len__()) > 1:
        lengths = tuple(_ctr.shape[0] for _ctr in contours)
        largest = lengths.index(max(lengths))

        return contours[largest]
    elif n_contours > 0:
        return contours[0]

    raise ValueError("Cell map has no 0.5-isocontour")
