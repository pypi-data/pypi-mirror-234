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

from typing import Tuple

import numpy as nmpy
from im_tools_36.type.image import intensity_h, number_h
from scipy import ndimage as spim
from skimage import color as sicl


array_t = nmpy.ndarray


def ValueScaledVersion(
    img: array_t, /, scaling: Tuple[intensity_h, intensity_h] = (-1.0, 1.0)
) -> array_t:
    """
    Value-scaled: as opposed to geometrically scaled.
    Default scaling is between [-1,+1], where the number representation is the most detailed
    TODO: check skimage.exposure.rescale_intensity
    """
    min_value, max_value, *_ = spim.extrema(img)
    factor = (scaling[1] - scaling[0]) / (max_value - min_value)
    output = factor * (img.astype(nmpy.float64, copy=False) - min_value) + scaling[0]

    return output


def UInt8RGBVersion(img: array_t, /, *, normalization: bool = True) -> array_t:
    """"""
    if normalization:
        normalized_img = ValueScaledVersion(img, scaling=(0, 255))
    else:
        normalized_img = img
    rounded_img = nmpy.around(normalized_img).astype(nmpy.uint8)

    if rounded_img.ndim == 2:
        output = nmpy.repeat(rounded_img[:, :, nmpy.newaxis], 3, axis=2)
    elif rounded_img.ndim == 3:
        if rounded_img.shape[2] == 1:
            output = nmpy.repeat(rounded_img, 3, axis=2)
        elif rounded_img.shape[2] == 3:
            output = rounded_img
        else:
            raise ValueError(
                f"{rounded_img.shape[2]}: Invalid number of planes; Must be 1 or 3"
            )
    else:
        raise ValueError(f"{rounded_img.ndim}: Invalid dimension; Must be 2 or 3")

    return output


def GloballyRelightedVersion(
    img: array_t, /, amplitude: intensity_h | number_h, *, mode: str = "+"
) -> array_t:
    """
    img: must have a uint8 dtype
    amplitude: in [0, 100] in additive mode, and in [0, infinity[ for multiplicative mode
    """
    relighted = sicl.rgb2lab(img)
    lightness = relighted[:, :, 0]
    if mode == "+":
        lightness += amplitude
    elif mode == "*":
        lightness *= amplitude
    else:
        raise ValueError(f"{mode}: Invalid mode")
    lightness[lightness < 0.0] = 0.0
    lightness[lightness > 100.0] = 100.0

    output = sicl.lab2rgb(relighted)
    output = UInt8RGBVersion(output)

    return output
