# Copyright CNRS/Inria/UNS
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

import textwrap as text
from typing import Sequence


def Flattened(string: str, /) -> str:
    """"""
    return text.dedent(string).replace("\n", "; ")


def AlignedOnSeparator(
    string: str | Sequence[str], separator: str, replacement: str, /
) -> str | tuple[str, ...] | list[str]:
    """"""
    if should_return_str := isinstance(string, str):
        lines = string.splitlines()
    else:
        lines = string
    indices = tuple(_lne.find(separator) for _lne in lines)
    longest = max(indices)

    output = (
        _lne.replace(separator, (longest - _lgt) * " " + replacement, 1)
        if _lgt > 0
        else _lne
        for _lne, _lgt in zip(lines, indices)
    )
    if should_return_str:
        return "\n".join(output)
    elif isinstance(string, tuple):
        return tuple(output)
    else:
        return list(output)
