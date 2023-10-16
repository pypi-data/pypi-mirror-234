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

import sys as sstm
from pathlib import Path as path_t

import cell_tracking_BC.in_out.file.json_format as jsft


def Main():
    """"""
    arguments = sstm.argv[1:]
    file = path_t(arguments[0])
    shape = (int(arguments[2]), int(arguments[1]))
    time_point = int(arguments[3])
    pixel = (shape[0] - int(arguments[5]) - 1, int(arguments[4]))

    for track in jsft.Load(list, file.parent, name=file.name):
        for thread, label in track.LabeledThreadIterator():
            if thread.__len__() > time_point:
                map_ = thread[time_point].Map(shape, as_boolean=True)
                if map_[pixel]:
                    print(track)
                    if track.labels.__len__() > 1:
                        print(f"Thread track label: {label}")
                    sstm.exit(0)


if __name__ == "__main__":
    #
    Main()
