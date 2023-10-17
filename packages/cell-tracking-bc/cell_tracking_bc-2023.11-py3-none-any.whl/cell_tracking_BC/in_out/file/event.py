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
from math import nan as NaN
from pathlib import Path as path_t
from typing import IO, Any, Dict, Optional, Sequence, Union

import xlsxwriter as xlsx
from logger_36 import LOGGER
from xlsxwriter.format import Format as xlsx_format_t

from cell_tracking_BC.in_out.file.table.cell import SetStateBasedCellFormat
from cell_tracking_BC.in_out.file.table.chart import AddChart_Mainly
from cell_tracking_BC.in_out.file.table.sheet import (
    SheetNameFromLongName,
    SortAndWriteCSVLines,
)
from cell_tracking_BC.in_out.file.track import INVALID_TRACK_MARKER, PRUNED_TRACK_MARKER
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t
from cell_tracking_BC.type.track.single.thread import thread_track_t

division_times_h = Dict[int, Sequence[int]]
death_time_h = Dict[int, int]


def SaveCellEventsToXLSX(
    path: Union[str, path_t],
    analysis: analysis_t,
    /,
    *,
    division_response: str = None,
    death_response: str = None,
) -> dict[(str, str), Sequence[Any]]:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.is_dir():
        path /= "cell_events.xlsx"

    if path.exists():
        print(f"{path}: File (or folder) already exists...")
        path = path_t(temp.mkdtemp()) / path.name
        print(f"Using {path} instead")

    workbook = xlsx.Workbook(str(path))
    pruned_format = workbook.add_format({"bg_color": "gray"})
    division_format = workbook.add_format({"bg_color": "blue"})
    death_format = workbook.add_format({"bg_color": "red"})

    csv_path = path.with_suffix(".csv")
    csv_accessor = open(csv_path, mode="w")

    feature_book = {}

    tracks = analysis.tracks
    if (tracks is None) or (tracks.__len__() == 0):
        LOGGER.warning("Sequence with no valid tracks.")
    else:
        division_time_points = tracks.DivisionTimePoints()
        death_time_points = tracks.DeathTimePoints(
            analysis.sequence.length, with_living_leaves=True
        )
        for SaveEvents, time_point in zip(
            (_SaveDivisionEvents, _SaveDeathEvents),
            (division_time_points, death_time_points),
        ):
            SaveEvents(workbook, csv_accessor, feature_book, time_point, tracks)

        n_divisions = sum(_tck.n_dividing_cells for _tck in tracks)
        _SaveEventCounts(workbook, csv_accessor, n_divisions, death_time_points)

        for event, response in zip(
            ("division", "death"), (division_response, death_response)
        ):
            if response is not None:
                _SaveEventResponse(
                    event,
                    workbook,
                    csv_accessor,
                    feature_book,
                    response,
                    tracks,
                    pruned_format,
                    division_format,
                    death_format,
                )

    workbook.close()
    csv_accessor.close()

    return feature_book


def _SaveDivisionEvents(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    feature_book: dict[(str, str), Sequence[Any]],
    division_time_points: Optional[division_times_h],
    tracks: tracks_t,
    /,
) -> None:
    """"""
    if (division_time_points is None) or (division_time_points.__len__() == 0):
        LOGGER.warning("Division Events: No associated tracks.")
        return

    sheet_name = SheetNameFromLongName("division times")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Division Times\n")

    total_n_topologic_threads = tracks.total_n_topologic_threads
    for label in range(1, total_n_topologic_threads + 1):
        row = label - 1

        if label not in division_time_points:
            worksheet.write_string(
                row, 0, f"{INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}"
            )
            csv_accessor.write(
                f"{label}:, {INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}\n"
            )
            feature_book[(sheet_name, label)] = ()
            continue

        time_points = division_time_points[label]
        if (time_points is None) or (time_points.__len__() == 0):
            worksheet.write_string(row, 0, "No Divisions")
            csv_accessor.write(f"{label}:, No Divisions\n")
            feature_book[(sheet_name, label)] = ()
        else:
            worksheet.write_row(row, 0, time_points)
            csv_accessor.write(f"{label}:," + ", ".join(map(str, time_points)) + "\n")
            feature_book[(sheet_name, label)] = tuple(time_points)

    worksheet.write_string(total_n_topologic_threads, 0, "END")


def _SaveDeathEvents(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    feature_book: dict[(str, str), Sequence[Any]],
    death_time_points: Optional[death_time_h],
    tracks: tracks_t,
    /,
) -> None:
    """"""
    if (death_time_points is None) or (death_time_points.__len__() == 0):
        LOGGER.warning("Death Events: No associated tracks.")
        return

    sheet_name = SheetNameFromLongName("death time")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Death Times\n")

    total_n_topologic_threads = tracks.total_n_topologic_threads
    for label in range(1, total_n_topologic_threads + 1):
        row = label - 1

        if label not in death_time_points:
            worksheet.write_string(
                row, 0, f"{INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}"
            )
            csv_accessor.write(
                f"{label}:, {INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}\n"
            )
            feature_book[(sheet_name, label)] = ()
            continue

        time_point = death_time_points[label]
        if time_point is None:
            worksheet.write_string(row, 0, "No Death")
            csv_accessor.write(f"{label}:, No Death\n")
            feature_book[(sheet_name, label)] = ()
        else:
            worksheet.write_number(row, 0, time_point)
            csv_accessor.write(f"{label}:, {time_point}\n")
            feature_book[(sheet_name, label)] = (time_point,)

    worksheet.write_string(total_n_topologic_threads, 0, "END")


def _SaveEventCounts(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    n_divisions: int,
    death_time_points: Optional[death_time_h],
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName("event counts")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Event Counts\n")

    n_deaths_pattern = 0
    n_deaths_track = 0
    if death_time_points is not None:
        for time_point in death_time_points.values():
            if time_point is not None:
                if time_point >= 0:
                    n_deaths_pattern += 1
                else:
                    n_deaths_track += 1

    for r_idx, (title, value) in enumerate(
        zip(
            ("divisions", "death (pattern)", "death (topologic)", "death"),
            (
                n_divisions,
                n_deaths_pattern,
                n_deaths_track,
                n_deaths_pattern + n_deaths_track,
            ),
        )
    ):
        worksheet.write_string(r_idx, 0, title)
        worksheet.write_number(r_idx, 1, value)
        csv_accessor.write(f"{title}, {value}\n")


def _SaveEventResponse(
    event: str,
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    feature_book: dict[(str, str), Sequence[Any]],
    name: str,
    tracks: tracks_t,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName(f"{event} response")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write(f"--- {event.title()} response\n")

    per_row_limits = {}
    csv_lines = []
    for track in tracks.all_structured_iterator:
        if name not in track.features:
            message = f'Track without "{name}" response'
            for label in track.topologic_labels:
                worksheet.write_string(label - 1, 0, message)
                csv_lines.append(f"{label}, {message}")
            continue

        root_time_point = track.topologic_root_time_point
        for label, response in track.features[name].items():
            row = label - 1
            if response is None:
                message = "Track too Short for Valid Response"
                worksheet.write_string(row, 0, message)
                csv_lines.append(f"{label}, {message}")
                feature_book[(sheet_name, label)] = ()
            else:
                worksheet.write_row(row, root_time_point, response)
                csv_lines.append(
                    f"{label}, " + root_time_point * "," + ", ".join(map(str, response))
                )
                feature_book[(sheet_name, label)] = root_time_point * (NaN,) + tuple(
                    response
                )

                if isinstance(track, thread_track_t):
                    cells = track
                else:
                    leaf_idx = track.topologic_labels.index(label)
                    leaf = track.topologic_leaves[leaf_idx]
                    cells = track.PathFromTo(track.topologic_root, leaf)
                SetStateBasedCellFormat(
                    worksheet,
                    row,
                    root_time_point,
                    cells,
                    response,
                    pruned_format,
                    division_format,
                    death_format,
                )

                per_row_limits[label] = (
                    root_time_point,
                    root_time_point + response.__len__() - 1,
                )

    AddChart_Mainly(
        tracks,
        per_row_limits,
        workbook,
        sheet_name,
        worksheet,
        pruned_format,
        division_format,
        death_format,
    )
    SortAndWriteCSVLines(csv_lines, csv_accessor)
