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
import scipy.interpolate as trpl
import skimage as skim

array_t = nmpy.ndarray


# _LOCAL_HISTOGRAM_FILTER_WIDTH = 3.0
# _RESCALING_FILTER_WIDTH = 9.0


def WithBackgroundSubtracted(
    image: array_t,
    segmentation: array_t,
    /,
    *,
    mode: str = None,
    dilation: int = 5,
) -> array_t:
    """
    mode: None (=mean), mean, median, interpolated
    Using the image and its segmentation.
    """
    missing_map = skim.morphology.binary_dilation(
        segmentation, footprint=skim.morphology.disk(dilation)
    )
    filled_map = nmpy.logical_not(missing_map)

    if (mode is None) or (mode == "mean"):
        output = image - nmpy.mean(image[filled_map])
    elif mode == "median":
        output = image - nmpy.median(image[filled_map])
    elif mode == "interpolated":
        output = image - PChipInterpolatedBackground(image, filled_map, missing_map)
    else:
        raise NotImplementedError(
            f"{mode}: Invalid or unimplemented background subtraction mode"
        )

    output[output < 0.0] = 0.0

    return output


def PChipInterpolatedBackground(
    incomplete: array_t, filled_map: array_t, missing_map: array_t, /
) -> array_t:
    """
    Uses pchip interpolation to avoid negative values.
    No smoothing is performed on the estimated background.
    """
    # Since pchip works in 1-D, interpolation has to be done in 2 steps
    # Step 1: row-wise interpolation
    row_wise = nmpy.array(incomplete, dtype=nmpy.float64)

    for col in range(row_wise.shape[1]):
        old_rows = nmpy.nonzero(filled_map[:, col])[0]
        new_rows = nmpy.nonzero(missing_map[:, col])[0]

        row_wise[new_rows, col] = trpl.pchip_interpolate(
            old_rows, incomplete[old_rows, col], new_rows
        )

    # Step 2: column-wise interpolation
    col_wise = nmpy.array(incomplete, dtype=nmpy.float64)

    for row in range(col_wise.shape[0]):
        old_cols = nmpy.nonzero(filled_map[row, :])[0]
        new_cols = nmpy.nonzero(missing_map[row, :])[0]

        col_wise[row, new_cols] = trpl.pchip_interpolate(
            old_cols, incomplete[row, old_cols], new_cols
        )

    output = nmpy.array(incomplete, dtype=nmpy.float64)
    output[missing_map] = 0.5 * (row_wise[missing_map] + col_wise[missing_map])

    return output
