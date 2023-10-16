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
import tempfile as temp
from math import nan as NaN
from pathlib import Path as path_t
from typing import IO, Any, Optional, Sequence, Union

import xlsxwriter as xlsx
from logger_36 import LOGGER
from xlsxwriter.format import Format as xlsx_format_t
from xlsxwriter.workbook import Workbook as workbook_t

from cell_tracking_BC.in_out.file.table.cell import SetStateBasedCellFormat
from cell_tracking_BC.in_out.file.table.chart import AddChart_Mainly
from cell_tracking_BC.in_out.file.table.sheet import (
    SheetNameFromLongName,
    SortAndWriteCSVLines,
)
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.base import compartment_id_t, compartment_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t


def SaveCompartmentsFeaturesToXLSX(
    base_path: Union[str, path_t],
    analysis: analysis_t,
    /,
) -> dict[(str, str), Sequence[Any]]:
    """"""
    if isinstance(base_path, str):
        base_path = path_t(base_path)
    if base_path.is_dir():
        base_path /= "features.xlsx"

    for compartment_id in tuple(compartment_id_t):
        path = (
            base_path.parent
            / f"{base_path.stem}-{str.lower(compartment_id.name)}{base_path.suffix}"
        )

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
            one_compartment = (
                analysis.segmentations[0].cells[0].compartments[compartment_id]
            )
            if not isinstance(one_compartment, compartment_t):
                one_compartment = one_compartment[0]
            for feature in one_compartment.available_features:
                _SaveFeature(
                    compartment_id,
                    feature,
                    tracks,
                    workbook,
                    csv_accessor,
                    feature_book,
                    pruned_format,
                    division_format,
                    death_format,
                )

        # jsoned, _ = jsny.JsonStringOf(feature_book)
        # compressed = gzip.compress(jsoned.encode())
        # json_path = path.with_suffix(".json")
        # with open(json_path, mode="wb") as json_accessor:
        #     json_accessor.write(compressed)

        workbook.close()
        csv_accessor.close()

        return feature_book


def _SaveFeature(
    compartment_id: compartment_id_t,
    feature: str,
    tracks: tracks_t,
    workbook: workbook_t,
    csv_accessor: IO,
    feature_book: dict[(str, str), Sequence[Any]],
    pruned_format: Optional[xlsx_format_t],
    division_format: Optional[xlsx_format_t],
    death_format: Optional[xlsx_format_t],
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName(feature)
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write(f"--- Feature {feature}\n")

    per_row_limits = {}
    csv_lines = []
    feature_is_number = False
    for track in tracks.all_structured_iterator:
        root_time_point = track.topologic_root_time_point
        for path, label in track.LabeledThreadIterator(topologic_mode=True):
            row = label - 1

            if feature not in path[0].features:
                message = f'Feature "{feature}" missing'
                worksheet.write_string(row, 0, message)
                csv_lines.append(f"{label}, {message}")
                continue

            raw_evolution = []
            for cell in path:
                compartment = cell.compartments[compartment_id]
                if isinstance(compartment, compartment_t):
                    raw_evolution.append(compartment.features[feature])
                else:
                    raw_evolution.append(
                        tuple(_cpt.features[feature] for _cpt in compartment)
                    )
            feature_is_number = isinstance(raw_evolution[0], nmbr.Number)
            evolution_as_str_list = list(map(_AsStrWithoutNewlines, raw_evolution))
            if isinstance(raw_evolution[0], (nmbr.Number, str)):
                evolution = raw_evolution
            else:
                evolution = evolution_as_str_list

            if root_time_point > 0:
                worksheet.write_row(row, 0, root_time_point * ("x",))
            if feature_is_number:
                worksheet.write_row(row, root_time_point, evolution)
            else:
                for time_point, value in enumerate(evolution, start=root_time_point):
                    worksheet.write_string(row, time_point, value)
            csv_lines.append(
                f"{label}, " + root_time_point * "," + ", ".join(evolution_as_str_list)
            )
            feature_book[(feature, label)] = root_time_point * (NaN,) + tuple(
                raw_evolution
            )

            SetStateBasedCellFormat(
                worksheet,
                row,
                root_time_point,
                path,
                evolution,
                pruned_format,
                division_format,
                death_format,
            )

            per_row_limits[row + 1] = (
                root_time_point,
                root_time_point + evolution.__len__() - 1,
            )

    worksheet.autofit()

    if feature_is_number:
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


def _AsStrWithoutNewlines(element: Any, /) -> str:
    """"""
    output = str(element)
    return output.replace("\n", " ")
