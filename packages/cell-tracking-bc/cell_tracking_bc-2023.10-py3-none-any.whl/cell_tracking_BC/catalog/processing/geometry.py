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

import numpy as nmpy
import scipy.ndimage.morphology as scph
import skimage.morphology as mrph

array_t = nmpy.ndarray


def WithSmallHolesRemoved(frame: array_t, /, *, max_hole_area: int = None) -> array_t:
    """"""
    output = scph.binary_fill_holes(frame)
    if max_hole_area is None:
        return output

    holes = output.copy()
    holes[frame] = 0
    labeled, n_holes = mrph.label(holes, return_num=True, connectivity=1)
    for label in range(1, n_holes + 1):
        where_label = holes == label
        area = nmpy.count_nonzero(where_label)
        if area <= max_hole_area:
            output[where_label] = 0

    return output


def WithSmallObjectsAndHolesRemoved(
    frame: array_t, min_object_area: int, max_hole_area: int, /
) -> array_t:
    """"""
    big_objects = mrph.remove_small_objects(frame, min_size=min_object_area)
    output = WithSmallHolesRemoved(big_objects, max_hole_area=max_hole_area)

    return output
