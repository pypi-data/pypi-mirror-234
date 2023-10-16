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

import re as rgex
from typing import Any, Dict, Final, List, Sequence, Tuple, Union

import numpy as nmpy
from im_tools_36.type.image import intensity_h, pix_value_h, spectrum_h
from scipy import ndimage as spim


array_t = nmpy.ndarray


GRAYSCALE_MODE_MARKER: Final = "g"
VALUE_GUESSING_REGEX: Final = rgex.compile(
    r"([" + GRAYSCALE_MODE_MARKER + r"m]uess)([0-9]*)"
)


def AutoCropped(
    img: array_t,
    /,
    *,
    force_color: bool = False,
    axis: Union[int, Sequence[int]] = None,
    value: Union[pix_value_h, str] = 0,
    tolerance: float = 0.0,
    return_value: bool = False,
    return_offsets: bool = False,
) -> Union[
    array_t,
    Tuple[array_t, array_t],
    Tuple[array_t, Tuple[int, ...]],
    Tuple[array_t, array_t, Tuple[int, ...]],
]:
    """
    The image is considered to be grayscale (or scalar) if "force_color" is False and "value" is a number or a string of
    the format "guess[some_int]" (see below). If "force_color" is True, or "value" is a sequence of numbers or a string
    of the format "muess[some_int]" (see below), the image is treated as a multichannel image (or multi/hyperspectral,
    or vector-valued, or color (whatever the color space is)), the channel dimension being the last one. The length of
    "value" must therefore be equal to this dimension. Note that for a multichannel image, "value" can actually be a
    number, in which case it will be treated as a tuple of this number repeated as many times as the image length in its
    last dimension.
    If "value" is a string, it can be:
    - "guess[some_int]":
    - "muess[some_int]": ("guess" with "g"->"m" as if it meant "Grayscale"->"Multichannel")
    some_int: The border width used to look for the most frequent value (grayscale) or value sequence (multichannel). It
    is 1 by default.

    tolerance: Fraction of the full dynamic of the image, if grayscale, or the largest full dynamic among the channels
    if multichannel. The latter could be replaced with the full vectorial dynamic using the L2 norm for example.
    However, this would require computing the diameter of the vector point cloud. This might be implemented in the
    future.
    In theory, the tolerance should belong to [0,1] for both grayscale and multichannel. However, due to the full
    dynamic computation method for multichannel, the useful range goes beyond 1 in this case.

    return_value: If true, the function returns the value that has been cropped; Meaningful only if "value" is
    "guess[some_int]" or "muess[some_int]".

    return_offsets: If true, the function returns, after the value if also returned, a tuple of the per-dimension
    offsets of the cropped image.
    """
    if force_color:
        grayscale_mode = False
    elif isinstance(value, str):
        grayscale_mode = value[0] == GRAYSCALE_MODE_MARKER
    else:
        grayscale_mode = isinstance(value, int) or isinstance(value, float)

    if isinstance(value, str):
        method, border_width = _GuessingMethodAndBorderWidth(value)
        border_values = _BorderValues(img, method, border_width)
        if method == "guess":
            value = _ValueFromGrayscaleBorder(border_values)
        else:
            value = _ValueFromMultichannelBorder(border_values, img.shape[-1])
    elif grayscale_mode:
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError(f"{type(value)}: Invalid value type for grayscale")
    elif isinstance(value, int) or isinstance(value, float):
        value = img.shape[-1] * (value,)
    elif value.__len__() != img.shape[-1]:
        raise ValueError(
            f"{value.__len__()}: Invalid autocropping value length; Expected_{img.shape[-1]}"
        )

    if axis is None:
        if grayscale_mode:
            cropping_axes = tuple(range(img.ndim))
        else:
            cropping_axes = tuple(range(img.ndim - 1))
    elif isinstance(axis, int):
        cropping_axes = (axis,)
    else:
        cropping_axes = axis
    if grayscale_mode:
        kept_axes = set(range(img.ndim))
    else:
        kept_axes = set(range(img.ndim - 1))

    if tolerance == 0.0:
        vequ_bmap = _StrictValueEqualityBMap(img, value, grayscale_mode)
    elif grayscale_mode:
        vequ_bmap = _FuzzyGrayscaleValueEqualityBMap(img, value, tolerance)
    else:
        vequ_bmap = _FuzzyMultichannelValueEqualityBMap(img, value, tolerance)

    slices = img.ndim * [slice(None)]
    for cropping_axis in cropping_axes:
        kept_axes.remove(cropping_axis)
        #
        all_equal = nmpy.all(vequ_bmap, axis=tuple(kept_axes))
        padded_all_equal = nmpy.pad(all_equal, 1, constant_values=True)
        change_idc = nmpy.where(nmpy.diff(padded_all_equal) > 0)[0]
        #
        if change_idc.__len__() > 1:
            slices[cropping_axis] = slice(change_idc[0], change_idc[-1])
        else:
            slices[cropping_axis] = slice(0, 0)
        #
        kept_axes.add(cropping_axis)

    # Returned sliced image is copied to avoid modifying original image from cropped one
    output = [img[tuple(slices)].copy()]

    if return_value:
        if not isinstance(value, array_t):
            value = nmpy.array(value)
        output.append(value)

    if return_offsets:
        if grayscale_mode:
            slices_for_offsets = slices
        else:
            slices_for_offsets = slices[:-1]
        offsets = tuple(one_slice.start for one_slice in slices_for_offsets)
        output.append(offsets)

    if output.__len__() > 1:
        return tuple(output)
    else:
        return output[0]


def _GuessingMethodAndBorderWidth(value: str) -> Tuple[str, int]:
    """"""
    match = VALUE_GUESSING_REGEX.match(value)
    if match:
        groups = match.groups()
        method = groups[0]
        if groups[1].__len__() > 1:
            border_width = int(groups[1])
            if border_width < 1:
                raise ValueError(f"{border_width}: Invalid border width; Expected_>0")
        else:
            border_width = 1
    else:
        raise ValueError(f"{value}: Invalid autocropping value")

    return method, border_width


def _BorderValues(img: array_t, method: str, border_width: int) -> List[intensity_h]:
    """
    Note that some border values are repeated in the list. This is not correct, but probably not too dramatic for the
    subsequent steps.
    """
    first_border = img.ndim * [slice(None)]
    last_border = img.ndim * [slice(None)]
    first_border[0] = slice(border_width)
    last_border[0] = slice(-border_width, None)

    output = []
    if method == "guess":
        n_rolls = img.ndim
    else:
        n_rolls = img.ndim - 1
    for _ in range(n_rolls):
        output.extend(img[tuple(first_border)].flatten())
        output.extend(img[tuple(last_border)].flatten())

        first_border = [first_border[-1]] + first_border[:-1]
        last_border = [last_border[-1]] + last_border[:-1]

    return output


def _ValueFromGrayscaleBorder(border_values: List[intensity_h]) -> intensity_h:
    """
    Since some border values are repeated in the list, the result is biased. However, this has a significant influence
    only for tiny images.
    """
    unique_values = nmpy.unique(border_values)
    bin_edges = nmpy.concatenate((unique_values, (unique_values[-1] + 1,)))
    n_occurrences, _ = nmpy.histogram(border_values, bins=bin_edges)
    most_frequent = nmpy.argmax(n_occurrences)
    if n_occurrences[most_frequent] == 1:
        output = nmpy.median(border_values)
    else:
        output = unique_values[most_frequent]

    return output


def _ValueFromMultichannelBorder(
    border_values: List[intensity_h], n_channels: int
) -> spectrum_h:
    """
    Since some border values are repeated in the list, the result is biased. However, this has a significant influence
    only for tiny images.
    """
    border_values = nmpy.reshape(border_values, (n_channels, -1))
    unique_values = nmpy.unique(border_values, axis=1).T
    channel_shape = (n_channels, 1)
    n_occurrences = (
        nmpy.count_nonzero(border_values == nmpy.reshape(value, channel_shape))
        for value in unique_values
    )
    n_occurrences = nmpy.fromiter(n_occurrences, nmpy.int64)
    most_frequent = nmpy.argmax(n_occurrences)
    if n_occurrences[most_frequent] == 1:
        output = nmpy.median(border_values, axis=1)
    else:
        output = unique_values[most_frequent, :]

    return output


def _StrictValueEqualityBMap(
    img: array_t, value: pix_value_h, grayscale_mode: bool
) -> array_t:
    """"""
    if grayscale_mode:
        output = img == value
    else:
        output = img[..., 0] == value[0]
        for idx in range(1, value.__len__()):
            nmpy.logical_and(output, img[..., idx] == value[idx], out=output)

    return output


def _FuzzyGrayscaleValueEqualityBMap(
    img: array_t, value: intensity_h, tolerance: float
) -> array_t:
    """"""
    min_value, max_value, *_ = spim.extrema(img)
    full_dynamic = max_value - min_value
    half_interval = 0.5 * tolerance * full_dynamic

    lower_threshold = value - half_interval
    upper_threshold = value + half_interval
    # It is not a problem to consider the following 2 cases as mutually exclusive, although they are not. The
    # shifts are done so that if value is too close to min_value or max_value, it still gets a full tolerance
    # instead of a "truncated" one.
    if lower_threshold < min_value:
        shift = min_value - lower_threshold
        lower_threshold = min_value
        upper_threshold += shift
    elif upper_threshold > max_value:
        shift = upper_threshold - max_value
        lower_threshold -= shift
        upper_threshold = max_value

    output = nmpy.logical_and(img >= lower_threshold, img <= upper_threshold)

    return output


def _FuzzyMultichannelValueEqualityBMap(
    img: array_t, value: spectrum_h, tolerance: float
) -> array_t:
    """"""
    min_value, max_value, full_dynamic = None, None, 0.0
    for c_idx in range(img.shape[-1]):
        min_current, max_current, *_ = spim.extrema(img[..., c_idx])
        current_dynamic = max_current - min_current
        if current_dynamic > full_dynamic:
            full_dynamic = current_dynamic
    half_interval = 0.5 * tolerance * full_dynamic

    # Unfortunately, the multichannel mode does not get the full tolerance management of the grayscale mode
    value = nmpy.reshape(value, (img.ndim - 1) * (1,) + (img.ndim,))
    color_centered = img.astype(nmpy.float64) - value
    color_sq_distances = nmpy.sum(color_centered**2, axis=-1)

    output = color_sq_distances <= half_interval**2

    return output


def PaddedToCommonShape(
    imgs: Sequence[array_t],
    /,
    *,
    padding_type: str = "constant",
    type_details: Dict[str, Any] = None,
    value_combination: str = None,
    background: array_t = None,
    offsets: Sequence[Sequence[int]] = None,
) -> Tuple[array_t, ...]:
    """
    All the images must have the same dimension, and there is no distinction between single- and multiple-channel images
    """
    if type_details is None:
        type_details = {}
    elif value_combination is not None:
        # A copy is necessary (to avoid a side effect) since the details will be updated
        type_details = type_details.copy()

    all_lengths = nmpy.array(tuple(img.shape for img in imgs), dtype=nmpy.int64)
    max_lengths = nmpy.amax(all_lengths, axis=0, keepdims=True)
    total_paddings = max_lengths - all_lengths
    paddings_before = nmpy.floor_divide(total_paddings, 2)
    paddings_after = total_paddings - paddings_before

    if background is None:
        if value_combination is not None:
            if value_combination == "min":
                CombinedValue = nmpy.amin
            elif value_combination == "max":
                CombinedValue = nmpy.amax
            elif value_combination == "mean":
                CombinedValue = nmpy.mean
            elif value_combination == "median":
                CombinedValue = nmpy.median
            else:
                raise ValueError(f"{value_combination}: Invalid value combination")
            if padding_type == "min":
                PaddingValue = nmpy.amin
            elif padding_type == "max":
                PaddingValue = nmpy.amax
            elif padding_type == "mean":
                PaddingValue = nmpy.mean
            elif padding_type == "median":
                PaddingValue = nmpy.median
            else:
                raise ValueError(
                    f"{padding_type}: Invalid padding type when combining values"
                )
            padding_type = "constant"
            padding_value = CombinedValue(tuple(PaddingValue(img) for img in imgs))
            type_details["constant_values"] = padding_value
    elif nmpy.any(max_lengths != background.shape):
        raise ValueError(
            f"{background.shape}: Invalid background lengths; Expected_{tuple(nmpy.squeeze(max_lengths))}"
        )

    output = []
    dimension_idc = tuple(range(imgs[0].ndim))
    for i_idx, img in enumerate(imgs):
        # Paddings after are equal to padding before + 0 or 1
        if nmpy.any(paddings_after[i_idx, :]):
            per_dim_paddings = tuple(
                (paddings_before[i_idx, d_idx], paddings_after[i_idx, d_idx])
                for d_idx in dimension_idc
            )
            if background is None:
                padded = nmpy.pad(
                    img, per_dim_paddings, mode=padding_type, **type_details
                )
            else:
                slices = img.ndim * [slice(None)]
                img_shape = img.shape
                if offsets is None:
                    for d_idx, paddings in enumerate(per_dim_paddings):
                        slices[d_idx] = slice(
                            paddings[0], (paddings[0] + img_shape[d_idx])
                        )
                else:
                    for d_idx, offset in enumerate(offsets[i_idx]):
                        slices[d_idx] = slice(offset, (offset + img_shape[d_idx]))
                padded = background.astype(img.dtype)
                padded[tuple(slices)] = img
            output.append(padded)
        else:
            output.append(img.copy())

    return tuple(output)
