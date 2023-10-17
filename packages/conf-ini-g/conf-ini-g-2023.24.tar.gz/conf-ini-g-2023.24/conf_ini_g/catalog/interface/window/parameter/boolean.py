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

from babelwidget.main import backend_t, choices_dots_wgt_h, library_wgt_h

from conf_ini_g.catalog.specification.parameter.boolean import boolean_t
from conf_ini_g.interface.window.component.parameter.protocol import parameter_a
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class boolean_wgt_t(parameter_a):
    library_wgt: library_wgt_h
    true_btn: choices_dots_wgt_h = dtcl.field(init=False, default=None)

    @classmethod
    def NewWithDetails(
        cls,
        value: bool | None,
        value_type: type_t | boolean_t | None,
        backend: backend_t,
        _: parameter_t | None,
        /,
    ) -> boolean_wgt_t:
        """
        If value_type does not contain the necessary details, an exclamation point is added to the default values.
        """
        output = cls(library_wgt=backend.library_wgt_t())

        value = _ValidValue(value)

        if value_type is None:
            labels = None
        else:
            if isinstance(value_type, type_t):
                annotation = value_type.FirstAnnotationWithAttribute("mode")
            else:
                annotation = value_type
            if annotation is None:
                labels = None
            else:
                labels = getattr(annotation.mode, "value", None)
        if labels is None:
            labels = ("True!", "False!")

        true_btn = backend.dot_button_wgt_t(labels[0], parent=output.library_wgt)
        false_btn = backend.dot_button_wgt_t(labels[1], parent=output.library_wgt)
        true_btn.setChecked(value)
        false_btn.setChecked(not value)

        output.true_btn = true_btn

        layout = backend.hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(true_btn)
        layout.addWidget(false_btn)
        output.library_wgt.setLayout(layout)

        return output

    def Assign(self, value: bool | None, _: type_t | boolean_t | None, /) -> None:
        """"""
        self.true_btn.setChecked(_ValidValue(value))

    def Text(self) -> str:
        """"""
        return str(self.true_btn.isChecked())


def _ValidValue(value: bool | None, /) -> bool:
    """"""
    if value is None:
        return False
    else:
        return value
