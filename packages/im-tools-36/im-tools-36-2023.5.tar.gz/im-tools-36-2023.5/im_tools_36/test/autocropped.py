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

from typing import Final, Sequence, Tuple, Union

import matplotlib as mplb
import matplotlib.pyplot as pypl
import mplb_tools_36.mplb_tools_36 as mp36
import numpy as nmpy
import skimage.color as sicl
import skimage.data as sidt
from im_tools_36.intensity import GloballyRelightedVersion
from im_tools_36.shape import AutoCropped, PaddedToCommonShape
from magicgui import event_loop, magicgui


# Because MagicGUI uses it, and only one backend can be sued at a time, I suppose
mplb.use("QtCairo")


GUESS_PREFIXES: Final = {2: "g", 3: "m"}


@magicgui(layout="vertical", call_button="Run")
def AutocropRocket(*, grayscale_mode: bool = False, border_width: int = 10) -> None:
    """"""
    img = sidt.rocket()
    cropping_tolerances_grayscale = nmpy.linspace(0.0, 0.95, num=8)
    cropping_tolerances_color = (0.0, 0.85, 0.95, 1.05, 1.35, 1.5, 1.8, 2.0)
    text_color = "c"

    if grayscale_mode:
        img = sicl.rgb2gray(img)
        cropping_tolerances = tuple(cropping_tolerances_grayscale)
    else:
        cropping_tolerances = tuple(cropping_tolerances_color)
    # Insert dummy tolerance for original image
    cropping_tolerances = (None,) + cropping_tolerances

    guess_mode = f"{GUESS_PREFIXES[img.ndim]}uess{border_width}"

    cropped_imgs = [img]
    cropping_values = [None]
    cropped_offsets = [None]
    for tolerance in cropping_tolerances[1:]:
        tolerance: float
        cropped, value, offsets = AutoCropped(
            img,
            value=guess_mode,
            tolerance=tolerance,
            return_value=True,
            return_offsets=True,
        )
        cropped_imgs.append(cropped)
        cropping_values.append(value.tolist())
        cropped_offsets.append(offsets)

    if grayscale_mode:
        background = 0.4 * img
    else:
        background = GloballyRelightedVersion(img, -25)
    p_cropped_imgs = PaddedToCommonShape(
        cropped_imgs, background=background, offsets=cropped_offsets
    )

    _, all_axes = mp36.SimpleDisplay(
        p_cropped_imgs, auto_grid=True, mode="make_only", return_axes=True
    )
    for a_idx, axes in enumerate(all_axes):
        if axes is None:
            continue

        cropping_value_as_str = _CroppingValueAsStr(cropping_values[a_idx])
        cropping_tolerance_as_str = _CroppingToleranceAsStr(cropping_tolerances[a_idx])
        lengths_as_str = _LengthsAsStr(cropped_imgs[a_idx].shape, img.shape[:2])

        mp36.RemoveColorbarFromAxes(axes)
        axes.set_axis_off()
        axes.annotate(
            f"{cropping_value_as_str}{cropping_tolerance_as_str}={lengths_as_str}",
            xy=(4, 8),
            color=text_color,
            verticalalignment="top",
            fontsize="x-small",
        )

    pypl.show()


def _CroppingValueAsStr(
    cropping_value: Union[Union[int, float], Sequence[Union[int, float]]], /
) -> str:
    """"""
    if cropping_value is None:
        output = "Original Image"
    else:
        if not isinstance(cropping_value, Sequence):
            cropping_value = (cropping_value,)

        elms_as_str = []
        for elm in cropping_value:
            if float(elm).is_integer():
                elms_as_str.append(int(elm).__str__())
            else:
                elms_as_str.append(f"{elm:.2f}")

        if elms_as_str.__len__() > 1:
            output = "(" + ",".join(elms_as_str) + ")"
        else:
            output = elms_as_str[0]

    return output


def _CroppingToleranceAsStr(cropping_tolerance: float | None, /) -> str:
    """"""
    if cropping_tolerance is None:
        output = ""
    else:
        output = f"+{cropping_tolerance:.2f}"

    return output


def _LengthsAsStr(lengths: Tuple[int, ...], ref_lengths: Tuple[int, ...], /) -> str:
    """"""
    height, width, *_ = lengths
    if (height, width) == ref_lengths:
        output = "Original Size"
    else:
        output = f"{width}x{height}"

    return output


if __name__ == "__main__":
    #
    with event_loop():
        _ = AutocropRocket.show()
