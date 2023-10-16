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
from typing import Optional, Sequence

from xlsxwriter.format import Format as xlsx_format_t
from xlsxwriter.worksheet import Worksheet as worksheet_t

from cell_tracking_BC.type.compartment.cell import cell_t, state_e


def SetStateBasedCellFormat(
    worksheet: worksheet_t,
    row: int,
    root_time_point: int,
    cells: Sequence[cell_t],
    values: Sequence,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    for time_point, cell in enumerate(cells, start=root_time_point):
        if cell.state is state_e.discarded:
            cell_format = pruned_format
        elif cell.state is state_e.dividing:
            cell_format = division_format
        elif cell.state is state_e.dead:
            cell_format = death_format
        else:
            cell_format = None

        if cell_format is not None:
            value = values[time_point - root_time_point]
            if isinstance(value, nmbr.Number):
                worksheet.write_number(row, time_point, value, cell_format)
            else:
                worksheet.write_string(row, time_point, value, cell_format)


def AddCellStateLegend(
    worksheet: worksheet_t,
    row: int,
    pruned_format: Optional[xlsx_format_t],
    division_format: Optional[xlsx_format_t],
    death_format: Optional[xlsx_format_t],
    /,
) -> None:
    """"""
    for col, state, cell_format in zip(
        range(3),
        ("Dividing", "Dead", "Pruned"),
        (division_format, death_format, pruned_format),
    ):
        if cell_format is not None:
            worksheet.write_string(row, col, state, cell_format)
