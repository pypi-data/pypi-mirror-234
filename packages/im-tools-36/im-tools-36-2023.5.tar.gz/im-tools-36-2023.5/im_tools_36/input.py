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

import importlib as mprt
import itertools as ittl
import sys as sstm
from types import ModuleType as module_t
from typing import Sequence, Tuple

# See https://imageio.readthedocs.io/en/stable/reference/index.html#plugins-backend-libraries
import imageio as mgio
import numpy as nmpy
from im_tools_36.path import path_h, path_t


def _Module(name: str, /) -> module_t | None:
    """"""
    if name in sstm.modules:
        return sstm.modules[name]

    # https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported
    if (spec := mprt.util.find_spec(name)) is None:
        return None

    output = mprt.util.module_from_spec(spec)
    sstm.modules[name] = output
    spec.loader.exec_module(output)

    return output


# Using VTK seems too complicated. See
# https://stackoverflow.com/questions/25230541/how-to-convert-a-vtkimage-into-a-numpy-array
# for a 3-D example.
aics = _Module("aicsimageio")
pncv = _Module("cv2")
tkio = _Module("itk")
mrci = _Module("mrc")
nbbl = _Module("nibabel")
pllw = _Module("PIL")
skio = _Module("skimage.io")
tiff = _Module("tifffile")
MODULES = (aics, mgio, mrci, nbbl, pllw, pncv, skio, tiff, tkio)
MODULE_WITH_NAME = {
    "aicsimageio": aics,
    "imageio": mgio,
    "itk": tkio,
    "mrc": mrci,
    "nibabel": nbbl,
    "opencv": pncv,
    "pillow": pllw,
    "scikit-image": skio,
    "skimage": skio,
    "tifffile": tiff,
}


array_t = nmpy.ndarray


def _WithAICS(path: str, /) -> array_t:
    """
    Arrangement: TCZYX
    """
    return aics.AICSImage(path).data


def _WithMRC(path: str, /) -> array_t:
    """
    If output.ndim == 5, probably time x channel x Z x Y x X, while sequences are:
        time x channel   x (Z=1 x)             Y x X.
    So one gets:
        time x channel=1 x Z=actual channels x Y x X. Then, use: output[:, 0, :, :]
    numpy.array: Because the returned value seems to be a read-only memory map
    """
    return nmpy.array(mrci.imread(path))


def _WithNibabel(path: str, /) -> array_t:
    """"""
    image = nbbl.load(path)

    return image.get_fdata()


def _WithPillow(path: str, /) -> array_t:
    """"""
    image_t = getattr(pllw, "Image")
    with image_t.open(path) as image:
        image.load()

    return nmpy.asarray(image)


# /!\ Must be in the order corresponding to MODULES
FUNCTIONS = (
    _WithAICS if aics is not None else None,
    mgio.v3.imread if mgio is not None else None,
    _WithMRC if mrci is not None else None,
    _WithNibabel if nbbl is not None else None,
    _WithPillow if pllw is not None else None,
    pncv.imread if pncv is not None else None,
    skio.imread if skio is not None else None,
    tiff.imread if tiff is not None else None,
    tkio.imread if tkio is not None else None,
)
FUNCTION_OF_MODULE = {None: None}
for module_, function in zip(MODULES, FUNCTIONS):
    if module_ is not None:
        FUNCTION_OF_MODULE[module_] = function


def ImageVolumeOrSequence(
    path: path_h,
    /,
    *,
    should_squeeze: bool = True,
    expected_dim: int = None,
    expected_shape: Sequence[int | None] = None,
    with_module: str = None,
    should_print_module: bool = False,
) -> array_t | Tuple[str, ...]:
    """"""
    # Potential outputs
    image = None
    issues = []

    if isinstance(path, str):
        path_str = path
        path_lib = path_t(path)
    else:
        path_str = str(path)
        path_lib = path
    if (expected_dim is None) and (expected_shape is not None):
        expected_dim = expected_shape.__len__()

    if with_module is None:
        reading_functions = [
            FUNCTION_OF_MODULE[mgio],
            FUNCTION_OF_MODULE[tkio],
            FUNCTION_OF_MODULE[pllw],
            FUNCTION_OF_MODULE[pncv],
            FUNCTION_OF_MODULE[skio],
            FUNCTION_OF_MODULE[nbbl],
        ]

        img_format = path_lib.suffix[1:].lower()
        if img_format in ("tif", "tiff"):
            reading_functions.append(FUNCTION_OF_MODULE[aics])
            reading_functions.append(FUNCTION_OF_MODULE[tiff])
        elif img_format in ("dv", "mrc"):
            if img_format == "dv":
                reading_functions.append(FUNCTION_OF_MODULE[aics])
            reading_functions.append(FUNCTION_OF_MODULE[mrci])
        elif img_format in ("czi", "lif", "nd2"):
            reading_functions.append(FUNCTION_OF_MODULE[aics])
    elif with_module in MODULE_WITH_NAME:
        reading_functions = [FUNCTION_OF_MODULE[MODULE_WITH_NAME[with_module]]]
    else:
        return (
            f"{with_module}: Invalid module. "
            f"Expected={str(tuple(MODULE_WITH_NAME.keys()))[1:-1]}",
        )

    failure = True
    for Read in reversed(reading_functions):
        if Read is None:
            continue

        try:
            image = Read(path_str)
            # A module might return None, for example, in case of a failure instead of
            # raising an exception. Hence the test below.
            if isinstance(image, array_t):
                failure = False
                if should_print_module:
                    print(f'{path_str}: Read with function "{Read.__name__}".')
                break
        except Exception as exception:
            issues.append(
                f'Cannot open image with function "{Read.__module__}.{Read.__name__}". '
                f'Error:\n{exception}'
            )

    if failure:
        if issues.__len__() > 0:
            return tuple(issues)
        return ("Silent Exception",)

    if should_squeeze:
        image = nmpy.squeeze(image)

    if (expected_dim is not None) and (image.ndim != expected_dim):
        return (
            f"{image.ndim}: Invalid dimension (shape={image.shape}). "
            f"Expected={expected_dim}",
        )
    if expected_shape is None:
        return image

    shape = image.shape
    if _ShapeMatches(shape, expected_shape):
        return image

    shape_as_array = nmpy.array(shape)
    for order in ittl.permutations(range(image.ndim)):
        if _ShapeMatches(shape_as_array[nmpy.array(order)], expected_shape):
            return nmpy.moveaxis(image, order, range(image.ndim))

    return (
        f"{shape}: Invalid shape. "
        f"Expected={tuple(expected_shape)}, or a permutation of it.",
    )


def _ShapeMatches(
    actual: Tuple[int, ...] | array_t, expected: Sequence[int | None], /
) -> bool:
    """"""
    return all((_ctl == _xpt) or (_xpt is None) for _ctl, _xpt in zip(actual, expected))


def AvailableModules(
    *, as_modules: bool = False
) -> Tuple[module_t, ...] | Tuple[Tuple[str, str, str, str], ...]:
    """
    Tuple[str, str, str, str]:
        name for "with_module" parameter of ImageVolumeOrSequence,
        module Python name,
        module version,
        reading function name
    """
    if as_modules:
        return tuple(_mdl for _mdl in FUNCTION_OF_MODULE.keys() if _mdl is not None)

    output = []
    for c_name, module_ in MODULE_WITH_NAME.items():
        if module_ is None:
            continue

        p_name = getattr(module_, "__name__", "???")
        if "." in p_name:
            parent = p_name.split(sep=".", maxsplit=1)[0]
            version = getattr(sstm.modules[parent], "__version__", "???")
        else:
            version = getattr(module_, "__version__", "???")
        output.append((c_name, p_name, version, FUNCTION_OF_MODULE[module_].__name__))

    return tuple(output)
