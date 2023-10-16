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

from __future__ import annotations

import inspect as nspt
import sys as sstm
from typing import Callable

from rich.text import Text as text_t
from str_to_obj.interface.console import NameValueTypeAsRichStr, TypeAsRichStr

from conf_ini_g.extension.path import any_path_h, path_t
from conf_ini_g.extension.string import AlignedOnSeparator
from conf_ini_g.phase.raw.config import ini_config_h
from conf_ini_g.phase.specification.parameter.type import type_t

_SECTION_PARAMETER_SEPARATOR = "__"


class config_t:
    path: path_t
    _types: dict[str, type_t]

    @classmethod
    def NewFromDictionary(
        cls, ini_config: ini_config_h, /, *, path: any_path_h = None
    ) -> config_t:
        """
        The dictionary values are already properly typed
        """
        output = cls()

        if (path is not None) and isinstance(path, str):
            path = path_t(path)

        output.path = path
        output._types = {
            _nme: type_t.NewFromTypeHint(_hnt)
            for _nme, _hnt in nspt.get_annotations(cls).items()
        }

        issues = []
        for s_name, section in ini_config.items():
            for p_name, value in section.items():
                issues.extend(output.Set(_FullName(s_name, p_name), value))

        if issues.__len__() > 0:
            issues = "\n".join(issues)
            print(f"{path}: Invalid configuration.\n{issues}")
            sstm.exit(1)

        return output

    def Set(self, name: str, value: str, /) -> list[str]:
        """"""
        expected_type = self._types[name]
        typed_value, issues = expected_type.InterpretedValueOf(value)

        if issues.__len__() > 0:
            return [
                f"{value}: "
                f'Invalid value of parameter "{name}": {", ".join(issues)}.'
            ]

        setattr(self, name, typed_value)
        return []

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [TypeAsRichStr(self)]

        AllButCallable = lambda _elm: not isinstance(_elm, Callable)
        for name, value in nspt.getmembers(self, AllButCallable):
            if name[0] != "_":
                name = name.replace(_SECTION_PARAMETER_SEPARATOR, ".", 1)
                output.append(
                    "    " + NameValueTypeAsRichStr(name, value, separator="@=@")
                )

        output = AlignedOnSeparator(output, "@=@", " = ")

        return "\n".join(output)


def _FullName(section: str, parameter: str, /) -> str:
    """"""
    return f"{section.strip().lower().replace(' ', '_')}{_SECTION_PARAMETER_SEPARATOR}{parameter.strip().lower()}"
