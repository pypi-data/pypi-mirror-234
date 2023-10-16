# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
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

from typing import Sequence

import numpy as nmpy
from skimage import transform as sitf


array_t = nmpy.ndarray


def Mosaic(imgs: Sequence[array_t], /, *, resize_factor: float = 1.0) -> array_t:
    #
    n_images = imgs.__len__()
    n_cols = int(nmpy.ceil(nmpy.sqrt(n_images)))
    n_rows, remaining = divmod(n_images, n_cols)
    if remaining > 0:
        n_rows += 1

    vignette_lengths = tuple(
        int(nmpy.around(resize_factor * length).item()) for length in imgs[0].shape
    )

    output = nmpy.empty(
        (n_rows * vignette_lengths[0], n_cols * vignette_lengths[1]), dtype=nmpy.uint64
    )

    row = 0
    col = 0
    row_slice = None
    for img in imgs:
        row_slice = slice(row * vignette_lengths[0], (row + 1) * vignette_lengths[0])
        col_slice = slice(col * vignette_lengths[1], (col + 1) * vignette_lengths[1])
        output[row_slice, col_slice] = sitf.resize(img, vignette_lengths)

        col += 1
        if col >= n_cols:
            col = 0
            row += 1
    col -= 1  # Unroll last unused col index

    if col < n_cols - 1:
        diagonal = nmpy.diag(vignette_lengths[0] * (1,)) > 0

        cross_value = nmpy.median(output)
        cross_img = nmpy.zeros(vignette_lengths)
        cross_img[diagonal] = cross_value
        cross_img[nmpy.rot90(diagonal)] = cross_value

        while col < n_cols - 1:
            col += 1
            col_slice = slice(
                col * vignette_lengths[1], (col + 1) * vignette_lengths[1]
            )
            output[row_slice, col_slice] = cross_img

    return output
