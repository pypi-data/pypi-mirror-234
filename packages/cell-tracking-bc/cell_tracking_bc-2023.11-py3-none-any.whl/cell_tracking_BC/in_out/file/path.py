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

import datetime as dttm
import sys as sstm
from typing import Union

from logger_36 import LOGGER

from cell_tracking_BC.standard.number import MAX_INT
from cell_tracking_BC.standard.path import path_h, path_t

# The following lists are meant to be safe enough, not to serve as references
PATH_ILLEGAL_CHARACTERS_LIN = r"/"
PATH_ILLEGAL_CHARACTERS_OSX = r":"
PATH_ILLEGAL_CHARACTERS_WIN = r'|/\<>:?*"'

REPLACEMENT_CHARACTER = "_"
VERSION_SEPARATOR = "-"

PATH_ILLEGAL_CHARACTERS = "".join(
    set(
        PATH_ILLEGAL_CHARACTERS_LIN
        + PATH_ILLEGAL_CHARACTERS_OSX
        + PATH_ILLEGAL_CHARACTERS_WIN
    )
)
if (REPLACEMENT_CHARACTER in PATH_ILLEGAL_CHARACTERS) or (
    VERSION_SEPARATOR in PATH_ILLEGAL_CHARACTERS
):
    raise ValueError(
        f'The character "{REPLACEMENT_CHARACTER}" or "{VERSION_SEPARATOR}" is an illegal path character'
    )


def StorageFolderForMain(
    base_folder: path_h,
    should_structure_folder: bool,
    sequence_name: str,
    first_frame: int,
    last_frame: int | None,
    /,
) -> path_t:
    """
    Call with main_py_module equal to __file__
    """
    if isinstance(base_folder, str):
        base_folder = path_t(base_folder)

    if should_structure_folder:
        output = ReplacePathIllegalCharacters(base_folder)
    else:
        output = base_folder
    if not output.exists():
        # exist_ok: added for thread safety (could use only mkdir then...)
        output.mkdir(exist_ok=True)
    elif not output.is_dir():
        LOGGER.error(f"{output}: Not a suitable storage folder")
        sstm.exit(-1)

    if not should_structure_folder:
        return output

    first_is_first = first_frame == 0
    last_is_last = (last_frame is None) or (last_frame == MAX_INT)
    if first_is_first and last_is_last:
        folder_name = sequence_name
    else:
        if first_is_first:
            from_frame = "FromStart"
        else:
            from_frame = f"From{first_frame}"
        if last_is_last:
            to_frame = "ToEnd"
        else:
            to_frame = f"To{last_frame}"
        folder_name = f"{sequence_name}-{from_frame}-{to_frame}"

    output /= ReplacePathIllegalCharacters(folder_name)
    if not output.exists():
        # exist_ok: added for thread safety (could use only mkdir then...)
        output.mkdir(exist_ok=True)
    elif not output.is_dir():
        LOGGER.error(f"{output}: Not a suitable storage folder")
        sstm.exit(-1)

    output /= TimeStamp()
    if output.exists():
        LOGGER.error(f"{output}: Existing date-based storage folder; Exiting")
        sstm.exit(-1)
    output.mkdir()

    return output


def TimeStamp() -> str:
    """"""
    return (
        dttm.datetime.now()
        .isoformat(timespec="milliseconds")
        .replace(".", "-")
        .replace(":", "-")
    )


def ReplacePathIllegalCharacters(
    path: Union[str, path_t], /, *, replacement: str = REPLACEMENT_CHARACTER
) -> Union[str, path_t]:
    """"""
    translations = str.maketrans(
        PATH_ILLEGAL_CHARACTERS, PATH_ILLEGAL_CHARACTERS.__len__() * replacement
    )
    if isinstance(path, str):
        as_path = path_t(path)
    else:
        as_path = path
    parts = as_path.parts
    if parts[0] == as_path.drive + as_path.root:
        output = [parts[0]]
        p_idx = 1
    else:
        output = []
        p_idx = 0
    for part in parts[p_idx:]:
        output.append(part.translate(translations))
    output = path_t(*output)

    if isinstance(path, str):
        return str(output)

    return output
