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

import importlib.util as mprt
import inspect as nspt
import sys as sstm
from types import FunctionType as function_t
from types import ModuleType as module_t
from typing import Callable

from logger_36 import LOGGER

from cell_tracking_BC.standard.path import path_h, path_t


def Main(path: path_h, /, *, base_folder: path_h = None) -> Callable:
    """"""
    if isinstance(path, str):
        path = path_t(path)

    if base_folder is None:
        module_name = path.stem
    else:
        module_name = (
            str(path.relative_to(base_folder))
            .split(".py", maxsplit=1)[0]
            .replace("/", ".")
        )
    try:
        specification = mprt.spec_from_file_location(module_name, path)
    except Exception as exception:
        LOGGER.error(
            f"\n[bold red]{path}: Unloadable module specification\n{exception}[/]"
        )
        sstm.exit(1)

    try:
        module_: module_t = mprt.module_from_spec(specification)
    except Exception as exception:
        LOGGER.error(
            f"\n[bold red]{path}: Invalid module specification\n{exception}[/]"
        )
        sstm.exit(1)

    try:
        specification.loader.exec_module(module_)
    except Exception as exception:
        LOGGER.error(f"\n[bold red]{path}: Invalid module\n{exception}[/]")
        sstm.exit(1)

    functions = nspt.getmembers(
        module_, lambda _elm: isinstance(_elm, function_t) and (_elm.__name__[0] != "_")
    )
    if functions.__len__() == 1:
        return functions[0][1]

    LOGGER.error(
        f"\n[bold red]{path}.{functions}: No, or too many, top-level functions. Expected=1.[/]"
    )
    sstm.exit(1)
