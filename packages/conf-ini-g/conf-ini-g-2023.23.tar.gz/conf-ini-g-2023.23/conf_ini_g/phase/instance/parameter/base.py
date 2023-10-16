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

import dataclasses as dtcl
from abc import ABC as abstract_class_t
from abc import abstractmethod
from typing import Any

from rich.text import Text as text_t

from conf_ini_g.phase.instance.parameter.value import INVALID_VALUE, invalid_value_t
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class base_t(abstract_class_t):
    # str: From INI document or interfaces.
    # Any: For default values.
    # None: For empty text in interfaces.
    value: str | Any | None = None
    comment: str | None = None

    @abstractmethod
    def SetINIorInterfaceOrDefaultValue(
        self,
        value_w_unit_w_comment: str | Any,
        comment_marker: str,
        /,
        *,
        unit: str = None,
    ) -> None:
        """"""
        ...

    @abstractmethod
    def TypedValue(
        self,
        expected_type: type_t,
        /,
        *,
        units: dict[str, int | float | invalid_value_t] | None = None,
    ) -> tuple[Any, list[str]]:
        """"""
        ...

    @abstractmethod
    def Text(self) -> str:
        """"""
        ...

    def Issues(self) -> list[str]:
        """"""
        if self.value is INVALID_VALUE:
            return ["Invalid value"]

        return []

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        return self.Text()


def Pieces(
    combined: str, separator: str, /, *, from_left: bool = True
) -> tuple[str, str | None]:
    """"""
    if from_left:
        where_separator = combined.find(separator)
    else:
        where_separator = combined.rfind(separator)

    if where_separator != -1:
        left = combined[:where_separator].strip()
        right = combined[(where_separator + separator.__len__()) :].strip()
    else:
        left = combined
        right = None

    return left, right
