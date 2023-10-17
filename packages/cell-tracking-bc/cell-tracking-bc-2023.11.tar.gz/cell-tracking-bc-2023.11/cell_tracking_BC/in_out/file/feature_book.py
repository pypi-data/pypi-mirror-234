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

from math import nan as NaN
from pathlib import Path as path_t
from typing import Any

import pandas as pnds
from json_any.task.storage import LoadFromJSON, StoreAsJSON


def SaveFeatureBookToJSON(
    feature_book: dict[(str, str), tuple[Any, ...]],
    base_path: str | path_t,
    /,
) -> None:
    """
    /!\ The feature book is modified to make all sequences the same length.
    """
    common_length = max(map(len, feature_book.values()))
    for key, value in feature_book.items():
        if (current_length := value.__len__()) < common_length:
            feature_book[key] = value + (common_length - current_length) * (NaN,)

    feature_book = pnds.DataFrame(data=feature_book)
    feature_book.columns.set_names(("Feature", "Track Label"), inplace=True)
    feature_book.index.set_names("Time Point", inplace=True)

    if isinstance(base_path, str):
        base_path = path_t(base_path)
    if base_path.is_dir():
        base_path /= "feature-book"

    StoreAsJSON(feature_book, base_path)


def NewFeatureBookFromJSON(path: str | path_t, /) -> pnds.DataFrame:
    """"""
    return LoadFromJSON(path)
