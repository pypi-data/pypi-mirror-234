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

from typing import Dict

from xlsxwriter import Workbook as workbook_t
from xlsxwriter.format import Format as xlsx_format_t
from xlsxwriter.worksheet import Worksheet as worksheet_t

from cell_tracking_BC.in_out.file.table.cell import AddCellStateLegend
from cell_tracking_BC.in_out.file.table.column import AlphaColumnFromIndex
from cell_tracking_BC.type.track.multiple.structured import tracks_t

_DASH_TYPES = (
    "solid",
    "round_dot",
    "square_dot",
    "dash",
    "dash_dot",
    "long_dash",
    "long_dash_dot",
    "long_dash_dot_dot",
)
_N_DASH_TYPES = _DASH_TYPES.__len__()


def AddChart_Mainly(
    tracks: tracks_t,
    per_row_limits: Dict[int, tuple[int, int]],
    workbook: workbook_t,
    sheet_name: str,
    worksheet: worksheet_t,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    next_available_row = tracks.total_n_topologic_threads

    worksheet.write_string(next_available_row, 0, "END")
    next_available_row += 2  # With margin

    AddCellStateLegend(
        worksheet, next_available_row, pruned_format, division_format, death_format
    )
    next_available_row += 3  # With margin

    if per_row_limits.__len__() > 0:
        chart = workbook.add_chart({"type": "line"})
        for l_idx, (row, (min_col, max_col)) in enumerate(per_row_limits.items()):
            min_col = AlphaColumnFromIndex(min_col)
            max_col = AlphaColumnFromIndex(max_col)
            chart.add_series(
                {
                    "name": str(row),
                    "values": f"='{sheet_name}'!${min_col}${row}:${max_col}${row}",
                    "line": {
                        "width": 1.0,
                        "dash_type": _DASH_TYPES[l_idx % _N_DASH_TYPES],
                    },
                }
            )
        worksheet.insert_chart(f"A{next_available_row}", chart)
