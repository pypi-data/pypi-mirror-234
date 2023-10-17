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

import dataclasses as dtcl
from typing import Any

from babelwidget.main import backend_t, choices_list_wgt_h

from conf_ini_g.catalog.specification.parameter.choices import choices_t
from conf_ini_g.interface.window.component.parameter.protocol import parameter_a
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.parameter.type import type_t

INDEX_FOR_NONE = 0


@dtcl.dataclass(slots=True, repr=False, eq=False)
class choices_wgt_t(parameter_a):
    library_wgt: choices_list_wgt_h

    @classmethod
    def NewWithDetails(
        cls,
        value: str | None,
        value_type: type_t | choices_t | None,
        backend: backend_t,
        _: parameter_t | None,
        /,
    ) -> choices_wgt_t:
        """
        If value_type does not contain the necessary details, the initial value (if valid) is the only choice, or a unique
        default choice ending with an exclamation point is added.
        """
        output = cls(library_wgt=backend.choice_menu_wgt_t())

        value_is_valid = isinstance(value, str)
        if value_is_valid:
            value = value.strip()

        if value_type is None:
            choices = _DefaultChoices(value, value_is_valid)
        else:
            if isinstance(value_type, type_t):
                annotation = value_type.FirstAnnotationWithAttribute("options")
            else:
                annotation = value_type
            if annotation is None:
                choices = _DefaultChoices(value, value_is_valid)
            else:
                choices = annotation.options

        for choice in choices:
            output.library_wgt.addItem(choice)
        if value_is_valid:
            output.library_wgt.setCurrentText(value)
        else:
            output.library_wgt.setCurrentIndex(INDEX_FOR_NONE)

        return output

    def Assign(self, value: str | None, _: type_t | choices_t | None, /) -> None:
        """"""
        if value is None:
            where = INDEX_FOR_NONE
        else:
            choices = tuple(map(self.itemText, range(self.count())))
            try:
                where = choices.index(value)
            except ValueError:
                choices = " or ".join(choices)
                raise ValueError(f"Invalid value. Actual={value}; Expected={choices}.")

        self.setCurrentIndex(where)

    def Text(self) -> str:
        """"""
        return self.library_wgt.currentText()

    def __getattr__(self, attribute: str, /) -> Any:
        """
        E.g., used for "SetFunction".
        """
        try:
            output = super(choices_wgt_t, self).__getattr__(attribute)
        except AttributeError:
            output = getattr(self.library_wgt, attribute)

        return output


def _DefaultChoices(value: str, value_is_valid: bool, /) -> tuple[str]:
    """"""
    if value_is_valid:
        return (value,)
    else:
        return ("Default!",)
