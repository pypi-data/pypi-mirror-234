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
from pathlib import Path as path_t
from typing import IO, Union

import xlsxwriter as xlsx
from logger_36 import LOGGER
from xlsxwriter.workbook import Workbook as workbook_t

from cell_tracking_BC.in_out.file.table.sheet import (
    SheetNameFromLongName,
    SortAndWriteCSVLines,
)
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t
from cell_tracking_BC.type.track.single.structured import structured_track_t

INVALID_TRACK_MARKER = "Invalid"
PRUNED_TRACK_MARKER = "Pruned"
VALID_TRACK_MARKER = "Valid"


def SaveTrackDetailsToXLSX(
    path: Union[str, path_t],
    analysis: analysis_t,
    /,
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.is_dir():
        path /= "tracks.xlsx"

    if path.exists():
        print(f"{path}: File (or folder) already exists...")
        path = path_t(temp.mkdtemp()) / path.name
        print(f"Using {path} instead")

    workbook = xlsx.Workbook(str(path))

    csv_path = path.with_suffix(".csv")
    csv_accessor = open(csv_path, mode="w")

    tracks = analysis.tracks
    if (tracks is None) or (tracks.__len__() == 0):
        LOGGER.warning("Sequence with no valid tracks.")
    else:
        _SaveSiblings(tracks, workbook, csv_accessor)
        _SaveTrackStatus(tracks, workbook, csv_accessor)

    workbook.close()
    csv_accessor.close()


def _SaveSiblings(
    tracks: tracks_t,
    workbook: workbook_t,
    csv_accessor: IO,
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName("siblings")
    worksheets = [workbook.add_worksheet(sheet_name)]
    sheet_name = SheetNameFromLongName("siblings_topological")
    worksheets.append(workbook.add_worksheet(sheet_name))

    csv_lines = [[], []]

    for track in tracks.all_structured_iterator:
        for s_idx, (labels, label_type) in enumerate(
            zip(
                (set(track.labels), set(track.topologic_labels)),
                ("", "Topologic "),
            )
        ):
            for label in labels:
                other_labels = str(sorted(labels.difference((label,))))[1:-1]
                if other_labels.__len__() > 0:
                    worksheets[s_idx].write_string(label - 1, 0, other_labels)
                    csv_lines[s_idx].append(
                        f"{label}, {label_type}Labels: {other_labels}"
                    )
                else:
                    if label_type.__len__() > 0:
                        message = f"Thread track in {label_type}mode"
                    else:
                        message = "Thread track"
                    worksheets[s_idx].write_string(label - 1, 0, message)
                    csv_lines[s_idx].append(f"{label}, {message}")

    for worksheet in worksheets:
        worksheet.write_string(tracks.total_n_topologic_threads, 0, "END")

    for s_idx, label_type in enumerate(("", " (Topologic)")):
        csv_accessor.write(f"--- Siblings{label_type}\n")
        SortAndWriteCSVLines(csv_lines[s_idx], csv_accessor)


def _SaveTrackStatus(
    tracks: tracks_t,
    workbook: workbook_t,
    csv_accessor: IO,
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName("status")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Status\n")

    csv_lines = []
    invalids = (
        _rcd[0] for _rcd in tracks.invalids if isinstance(_rcd[0], structured_track_t)
    )
    for tracks_per_status, status in zip(
        (tracks, tracks.fully_pruned, invalids),
        (VALID_TRACK_MARKER, PRUNED_TRACK_MARKER, INVALID_TRACK_MARKER),
    ):
        for track in tracks_per_status:
            for label in track.topologic_labels:
                if (label in track.labels) or (status != VALID_TRACK_MARKER):
                    thread_status = status
                else:
                    thread_status = PRUNED_TRACK_MARKER
                worksheet.write_string(label - 1, 0, thread_status)
                csv_lines.append(f"{label}, {thread_status}")

    worksheet.write_string(tracks.total_n_topologic_threads, 0, "END")
    SortAndWriteCSVLines(csv_lines, csv_accessor)
