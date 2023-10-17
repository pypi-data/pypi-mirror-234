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

from cell_tracking_BC.type.compartment.base import compartment_t

array_t = nmpy.ndarray


def IntensityEntropy(
    compartment: compartment_t,
    frame: array_t,
    /,
    *,
    min_intensity: float = 0.0,
    max_intensity: float = 255.0,
    n_bins: int = None,
    normalized_version: bool = True,
    margin: float = None,
) -> float:
    """
    normalized_version: It True, the entropy is normalized by 1/log(n_bins) so that the output belongs to [0,1]
    """
    map_ = compartment.Map(frame.shape, as_boolean=True, margin=margin)
    intensities = frame[map_]

    if n_bins is None:
        n_bins = max(3, int(round(nmpy.sqrt(intensities.size))))
    histogram, _ = nmpy.histogram(
        intensities, range=(min_intensity, max_intensity), bins=n_bins
    )
    normed = histogram / nmpy.sum(histogram)
    non_zero = normed[normed > 0.0]

    output = -nmpy.sum(non_zero * nmpy.log(non_zero))
    if normalized_version:
        output /= nmpy.log(n_bins)

    return output.item()
