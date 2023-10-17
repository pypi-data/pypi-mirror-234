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

"""
margin: percentage of the compartment area
"""

from typing import Any, Callable, Dict
from typing import NamedTuple as named_tuple_t
from typing import Sequence, Union

from numpy import ndarray as array_t

from cell_tracking_BC.type.compartment.base import compartment_id_t, compartment_t

geometrical_feature_computation_h = Callable[
    [compartment_t, Dict[str, Any]], Union[Any, Sequence[Any]]
]
radiometric_feature_computation_h = Callable[
    [compartment_t, Union[array_t, Sequence[array_t]], Dict[str, Any]],
    Union[Any, Sequence[Any]],
]
feature_computation_h = Union[
    geometrical_feature_computation_h, radiometric_feature_computation_h
]


class definition_t(named_tuple_t):
    name: Union[str, Sequence[str]]
    computation: feature_computation_h
    compartment: compartment_id_t = compartment_id_t.CELL
    channel: Union[str, Sequence[str]] = None
