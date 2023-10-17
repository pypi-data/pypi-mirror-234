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

import string as strg
from typing import Any

# Accented characters can be added with: + "".join(chr(_asc) for _asc in range(192, 256))
_GREEK_LOWERCASE = "αβγδεζηθικλμξπρςστφχψ"
_CIRCLED_DIGITS = "➊➋➌➍➎➏➐➑➒"
_SHAPES = "◀▲▶▼"
_EMOTICONS = "😀😐😦🙃"
_ASCII_OF = (
    strg.ascii_lowercase
    + strg.digits
    + strg.ascii_uppercase
    + _CIRCLED_DIGITS
    + _GREEK_LOWERCASE
    + _SHAPES
    + _EMOTICONS
)


def Identity(obj: Any, /) -> str:
    """"""
    hash_key = str(hash(obj))
    # hash can return negative values
    if hash_key[0] == "-":
        hash_key = "1" + hash_key[1:]
    else:
        hash_key = "0" + hash_key

    characters = (
        _ASCII_OF[int(hash_key[_idx : (_idx + 2)])]
        for _idx in range(0, hash_key.__len__(), 2)
    )
    uid = "".join(characters)

    return f"{obj.__class__.__name__}.{uid}"
