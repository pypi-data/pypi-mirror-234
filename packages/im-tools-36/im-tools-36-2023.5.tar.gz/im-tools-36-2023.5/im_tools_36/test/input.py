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

import textwrap as txtw
from pathlib import Path as path_t
from typing import Tuple

from numpy import ndarray as array_t

from im_tools_36.input import AvailableModules, ImageVolumeOrSequence

PATH_JR = "/home/eric/Data/Videos/people/jeremie-roux"


modules_details = AvailableModules()

print("--- PYTHON MODULES")
for module in AvailableModules(as_modules=True):
    print(module)
print("--- MODULE DETAILS")
for c_name, p_name, version, function in modules_details:
    print(
        f"Casual name: {c_name}\n    Python name: {p_name}=={version}\n    {function}"
    )


def CheckImage(path: path_t, expected_shape: Tuple[int | None, ...], /) -> None:
    """"""
    print(f"--- {path}: {expected_shape}")

    for module_ in ((None,),) + modules_details:
        ivs = ImageVolumeOrSequence(
            path,
            expected_shape=expected_shape,
            with_module=module_[0],
            should_print_module=module_[0] is None,
        )
        if isinstance(ivs, array_t):
            print(f"{module_[0]}: Success w/ shape {ivs.shape}")
        else:
            print(f"!!! {module_[0]}: Failure")
            print(txtw.indent("\n".join(ivs), "    "))


channels = ("YFP", "mCherry", "POL")
CheckImage(
    path_t(PATH_JR) / "p53" / "treat01_10_R3D.dv", (None, None, channels.__len__(), 433)
)

channels = ("CFP", "YFP", "POL")
CheckImage(path_t(PATH_JR) / "TREAT02_13_R3D.dv", (None, None, channels.__len__(), 241))
